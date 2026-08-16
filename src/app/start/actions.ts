'use server';

/**
 * The self-serve signup. This is a PUBLIC server action writing to the production database, so it
 * is written like an endpoint, not like a page helper: every string is capped, the phone is
 * normalized by the one implementation we have, a honeypot swallows bots without telling them,
 * a duplicate submit updates rather than inserts, and no database error string ever reaches the
 * browser.
 *
 * The row it writes is `active = false`. That is load-bearing — see the insert below.
 */

import { sendEmail } from '@/lib/email/client';
import { emailRule, emailShell, escapeHtml, PALETTE, SANS, SERIF } from '@/lib/email/layout';
import { optionalEnv } from '@/lib/env';
import {
  BUSINESS_TYPE_LABELS,
  HONEYPOT_FIELD,
  LIST_SIZE_LABELS,
  NEXT_STEPS,
  OPERATOR,
  OUTBOUND_NUMBER,
  START_FIELDS,
  SUPPORT_EMAIL,
  StartSchema,
  bookingCallUrl,
  firstNameOf,
  planById,
  recommendPlan,
  recommendationReason,
  verticalFor,
  type PlanId,
  type StartField,
  type StartInput,
  type StartState,
} from '@/lib/onboarding';
import { formatPhone, normalizePhone } from '@/lib/phone';
import { planLink } from '@/lib/site';
import { supabaseAdmin } from '@/lib/supabase/admin';

/**
 * A double-click, a flaky connection retried, or someone who wanted to fix a typo. Any of those
 * inside this window updates the row they already made.
 *
 * This is not cosmetic. `clients.contact_email` has no unique constraint, and the Stripe webhook
 * (src/app/api/stripe/webhook/route.ts) refuses to write anything when an email matches more than
 * one client — it logs "not guessing" and returns `ambiguous`. Two rows from one signup would mean
 * that salon's payment never marks anybody paid, forever.
 */
const DUPLICATE_WINDOW_MINUTES = 20;

type Outcome = {
  clientId: string | null;
  mode: 'created' | 'updated' | 'not_saved';
  dbError?: string;
  /**
   * Set when a client row with this email already existed from before the de-dupe window — an
   * established client filling the public form in again. We still take the signup, but the operator
   * has to merge the two rows or the Stripe webhook will refuse to match either of them.
   */
  duplicateOfClientId?: string;
};

/* ------------------------------------------------------------------ the action */

export async function startAction(_prev: StartState, formData: FormData): Promise<StartState> {
  const values = rawValues(formData);

  // Honeypot first, before validation: a bot that filled it gets the same success screen a human
  // gets, and nothing is written or sent. Giving it a validation error would tell it what to fix.
  if (field(formData, HONEYPOT_FIELD) !== '') {
    console.warn('[start] honeypot tripped, discarding submission');
    return discardedSuccess(values);
  }

  const ticket = Number(values.avg_ticket_dollars);
  const parsed = StartSchema.safeParse({
    ...values,
    contact_email: values.contact_email.toLowerCase(),
    avg_ticket_dollars: Number.isFinite(ticket) ? ticket : Number.NaN,
  });

  if (!parsed.success) {
    const fieldErrors: Partial<Record<StartField, string>> = {};
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? '') as StartField;
      if (key && !(key in fieldErrors)) fieldErrors[key] = issue.message;
    }
    return { status: 'error', error: 'Have a look at the highlighted fields.', fieldErrors, values };
  }

  const input = parsed.data;

  // One implementation of what a dialable number is, shared with the scrub and the dialer.
  const phone = normalizePhone(input.contact_phone);
  if (!phone) {
    return {
      status: 'error',
      values,
      fieldErrors: { contact_phone: 'We could not read that as a number we can dial. Include the area code.' },
    };
  }

  const planId = recommendPlan({ businessType: input.business_type, listSize: input.list_size });
  const outcome = await saveClient(input, phone);

  // Emails are best effort in both directions: a lead is worth more than a confirmation. sendEmail
  // never throws and already logs its own failures, and neither result can fail the signup.
  const [ops, confirmed] = await Promise.all([
    notifyOperator(input, phone, planId, outcome),
    confirmToProspect(input, planId),
  ]);

  // The only genuine failure: the row did not save AND the operator was not told. Then, and only
  // then, the lead really is lost and saying "you're in" would be a lie.
  if (outcome.mode === 'not_saved' && !ops) {
    return {
      status: 'error',
      values,
      error: `Something broke on our end and we could not record that. Email ${SUPPORT_EMAIL} and we will set you up by hand — nothing you typed was your fault.`,
    };
  }

  const plan = planById(planId);
  const link = planLink(plan);

  return {
    status: 'success',
    success: {
      greeting: firstNameOf(input.contact_name),
      salonName: input.salon_name,
      contactEmail: input.contact_email,
      recommendedPlanId: planId,
      recommendationReason: recommendationReason({
        businessType: input.business_type,
        listSize: input.list_size,
      }),
      checkoutUrl: link === '#' ? null : link,
      confirmationEmailed: confirmed,
    },
  };
}

/* ------------------------------------------------------------------ form reading */

function field(formData: FormData, key: string): string {
  const value = formData.get(key);
  return typeof value === 'string' ? value.trim() : '';
}

function rawValues(formData: FormData): Record<StartField, string> {
  // Cast once: the loop below assigns every key in START_FIELDS, which is the union itself.
  const values = {} as Record<StartField, string>;
  for (const key of START_FIELDS) {
    // Hard cap before anything else touches it: a 5MB "salon name" is not going into a log line.
    values[key] = field(formData, key).slice(0, 500);
  }
  return values;
}

/** What a bot sees. Indistinguishable from the real thing, and nothing happened. */
function discardedSuccess(values: Record<StartField, string>): StartState {
  const plan = planById('pilot');
  const link = planLink(plan);
  return {
    status: 'success',
    success: {
      greeting: firstNameOf(values.contact_name),
      salonName: values.salon_name,
      contactEmail: values.contact_email,
      recommendedPlanId: 'pilot',
      recommendationReason: recommendationReason({ businessType: 'salon', listSize: 'under_250' }),
      checkoutUrl: link === '#' ? null : link,
      confirmationEmailed: true,
    },
  };
}

/* ------------------------------------------------------------------ the write */

/**
 * Never throws. A thrown server action reaches the browser as an opaque runtime error, the form
 * loses everything the prospect typed, and no operator email goes out — so every failure in here
 * becomes `not_saved`, which the caller turns into an email the lead survives in.
 */
async function saveClient(input: StartInput, phone: string): Promise<Outcome> {
  try {
    return await writeClient(input, phone);
  } catch (e) {
    const detail = e instanceof Error ? e.message : String(e);
    console.error('[start] client write threw', { email: input.contact_email, detail });
    return { clientId: null, mode: 'not_saved', dbError: detail };
  }
}

async function writeClient(input: StartInput, phone: string): Promise<Outcome> {
  const db = supabaseAdmin();

  const writable = {
    name: input.salon_name,
    contact_name: input.contact_name,
    contact_email: input.contact_email,
    contact_phone: phone,
    // One number was asked for, so it fills both roles: the line we reach the owner on and the
    // line Malone reads out on voicemail. The operator confirms it during review and can split
    // the two in /admin before anything dials.
    booking_phone: phone,
    offer_text: input.offer_text,
    timezone: input.timezone,
    vertical: verticalFor(input.business_type),
    avg_ticket_cents: input.avg_ticket_dollars * 100,
  };

  const match = await clientsWithEmail(db, input.contact_email);

  if (match.recentId) {
    // Deliberately not touching `stripe_status` or `active`. A resubmit must never un-pay someone
    // who clicked the payment link between the two submits, and must never flip the dialing switch
    // in either direction — that switch belongs to the operator alone.
    const { error } = await db.from('clients').update(writable).eq('id', match.recentId);
    if (error) {
      console.error('[start] client update failed', { id: match.recentId, detail: error.message });
      return { clientId: match.recentId, mode: 'not_saved', dbError: error.message };
    }
    return { clientId: match.recentId, mode: 'updated' };
  }

  const { data, error } = await db
    .from('clients')
    .insert({
      ...writable,
      stripe_status: 'trialing',
      // LOAD-BEARING, DO NOT "FIX" THIS TO true.
      // `claim_contacts_for_dialing` (supabase/migrations/0001_init.sql) only ever claims contacts
      // whose client has `cl.active = true`. Writing false here means a signup that arrives at
      // 3am from a form on the open internet cannot dial one single person before a human has
      // looked at who they are and what is in their list. The operator flips it in /admin.
      active: false,
    })
    .select('id')
    .single();

  if (error || !data) {
    const detail = error?.message ?? 'insert returned no row';
    console.error('[start] client insert failed', { email: input.contact_email, detail });
    return { clientId: null, mode: 'not_saved', dbError: detail };
  }

  if (match.olderId) {
    console.warn('[start] second client row for one email', {
      email: input.contact_email,
      existing: match.olderId,
      created: data.id,
    });
  }

  return { clientId: data.id, mode: 'created', duplicateOfClientId: match.olderId ?? undefined };
}

/**
 * Splits the rows carrying this email into "just made one, they are correcting it" and "this email
 * already belonged to a client before today". The first is updated in place. The second is only
 * ever reported: silently overwriting a client row that an operator has already edited — offer_text
 * is what Malone says out loud — would let anyone who knows a salon's email rewrite its script.
 */
async function clientsWithEmail(
  db: ReturnType<typeof supabaseAdmin>,
  email: string,
): Promise<{ recentId: string | null; olderId: string | null }> {
  const since = Date.now() - DUPLICATE_WINDOW_MINUTES * 60_000;

  const { data, error } = await db
    .from('clients')
    .select('id, created_at')
    .eq('contact_email', email)
    .order('created_at', { ascending: false })
    .limit(5);

  if (error) {
    // Fail open, towards keeping the lead. If this select is broken the insert probably is too,
    // and the worst case is a duplicate row the operator merges by hand — better than dropping a
    // signup on the floor because a read failed.
    console.error('[start] duplicate lookup failed', { detail: error.message });
    return { recentId: null, olderId: null };
  }

  const rows = data ?? [];
  const recent = rows.find((r) => Date.parse(r.created_at) >= since);
  const older = rows.find((r) => Date.parse(r.created_at) < since);
  return { recentId: recent?.id ?? null, olderId: older?.id ?? null };
}

/* ------------------------------------------------------------------ emails */

/** ADMIN_EMAIL is the operator's inbox. The support address is the backstop, never nothing. */
function opsRecipient(): string {
  return optionalEnv('ADMIN_EMAIL') ?? SUPPORT_EMAIL;
}

/** Returns true when the operator was actually told. */
async function notifyOperator(
  input: StartInput,
  phone: string,
  planId: PlanId,
  outcome: Outcome,
): Promise<boolean> {
  const plan = planById(planId);
  const { subject, html } = operatorEmail(input, phone, plan.name, outcome);

  const res = await sendEmail({
    to: opsRecipient(),
    subject,
    html,
    // Hitting reply reaches the salon owner directly. That is the whole point of this email.
    replyTo: input.contact_email,
  });

  if (!res.ok) console.error('[start] operator notification failed', { detail: res.error });
  return res.ok;
}

/**
 * Returns whether the confirmation actually left. The failure is never surfaced as an error — a
 * prospect whose signup worked must not be shown something that looks broken — but the confirmation
 * screen uses this to avoid promising an inbox copy that is not on its way.
 */
async function confirmToProspect(input: StartInput, planId: PlanId): Promise<boolean> {
  const { subject, html } = prospectEmail(input, planById(planId).name);
  const res = await sendEmail({ to: input.contact_email, subject, html, replyTo: SUPPORT_EMAIL });
  if (!res.ok) console.error('[start] confirmation email failed', { detail: res.error });
  return res.ok;
}

function detailRow(label: string, value: string): string {
  return `<tr>
      <td width="150" style="padding:8px 0;font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.12em;text-transform:uppercase;color:${PALETTE.inkMute};vertical-align:top;">${escapeHtml(label)}</td>
      <td style="padding:8px 0;font-family:${SANS};font-size:15px;line-height:22px;color:${PALETTE.ink};vertical-align:top;">${value}</td>
    </tr>`;
}

/**
 * Every field they typed, so the lead survives even when the database write did not. This is the
 * copy of record until the operator opens /admin.
 */
function operatorEmail(
  input: StartInput,
  phone: string,
  planName: string,
  outcome: Outcome,
): { subject: string; html: string } {
  const failed = outcome.mode === 'not_saved';
  const subject = failed
    ? `SIGNUP NOT SAVED — ${input.salon_name} (details below)`
    : outcome.duplicateOfClientId
      ? `New signup: ${input.salon_name} — duplicate email, needs merging`
      : `New signup: ${input.salon_name} — ${BUSINESS_TYPE_LABELS[input.business_type]}`;

  const notice = (color: string, wash: string, html: string) =>
    `<tr><td style="padding:20px 32px 0 32px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td style="padding:14px 18px;background-color:${wash};border-left:3px solid ${color};font-family:${SANS};font-size:13px;line-height:20px;color:${color};">${html}</td>
        </tr></table>
      </td></tr>`;

  const banner = failed
    ? notice(
        '#A8474A',
        '#FBEDED',
        `<strong>The database write failed.</strong> There is no client row for this signup. Create it by hand in /admin from the details below — this email is the only copy.<br>${escapeHtml(outcome.dbError ?? 'no detail')}`,
      )
    : outcome.duplicateOfClientId
      ? notice(
          PALETTE.brassDeep,
          PALETTE.brassWash,
          `<strong>This email already belonged to client ${escapeHtml(outcome.duplicateOfClientId)}.</strong> A second row was created rather than overwriting theirs. Merge them: the Stripe webhook refuses to match a payment when one email maps to two clients, so billing status will stop updating for both until you do.`,
        )
      : '';

  const stateLine =
    outcome.mode === 'updated'
      ? 'Updated an existing client row (they submitted again within the de-dupe window).'
      : outcome.mode === 'created'
        ? 'New client row created, active = false. It cannot dial anyone until you switch it on.'
        : 'No client row exists yet.';

  const body = `
  ${banner}
  <tr><td style="padding:${banner ? '20px' : '30px'} 32px 0 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.16em;text-transform:uppercase;color:${PALETTE.brassDeep};">Self-serve signup · /start</div>
    <div style="font-family:${SERIF};font-size:34px;line-height:40px;color:${PALETTE.ink};padding-top:8px;">${escapeHtml(input.salon_name)}</div>
    <div style="font-family:${SANS};font-size:13px;line-height:20px;color:${PALETTE.inkSoft};padding-top:8px;">${escapeHtml(stateLine)}</div>
  </td></tr>
  <tr><td style="padding:18px 32px 4px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      ${detailRow('Contact', escapeHtml(input.contact_name))}
      ${detailRow(
        'Email',
        `<a href="mailto:${escapeHtml(input.contact_email)}" style="color:${PALETTE.brassDeep};text-decoration:none;font-weight:600;">${escapeHtml(input.contact_email)}</a>`,
      )}
      ${detailRow(
        'Phone',
        `<a href="tel:${escapeHtml(phone)}" style="color:${PALETTE.brassDeep};text-decoration:none;font-weight:600;">${escapeHtml(formatPhone(phone))}</a> <span style="color:${PALETTE.inkMute};font-size:12px;">(${escapeHtml(input.contact_phone)})</span>`,
      )}
      ${detailRow('Business type', escapeHtml(BUSINESS_TYPE_LABELS[input.business_type]))}
      ${detailRow('Stored vertical', escapeHtml(verticalFor(input.business_type)))}
      ${detailRow('Timezone', escapeHtml(input.timezone))}
      ${detailRow('Lapsed list size', escapeHtml(LIST_SIZE_LABELS[input.list_size]))}
      ${detailRow('Average ticket', `$${escapeHtml(String(input.avg_ticket_dollars))}`)}
      ${detailRow('Recommended plan', escapeHtml(planName))}
      ${detailRow('Client id', escapeHtml(outcome.clientId ?? '— not saved —'))}
    </table>
  </td></tr>
  <tr><td style="padding:16px 32px 0 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.12em;text-transform:uppercase;color:${PALETTE.inkMute};">Offer they want Malone to make</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td style="padding:14px 18px;background-color:${PALETTE.brassWash};border-left:3px solid ${PALETTE.brass};font-family:${SERIF};font-size:18px;line-height:26px;font-style:italic;color:${PALETTE.ink};">&ldquo;${escapeHtml(input.offer_text)}&rdquo;</td>
    </tr></table>
  </td></tr>
${emailRule()}
  <tr><td style="padding:16px 32px 28px 32px;font-family:${SANS};font-size:13px;line-height:20px;color:${PALETTE.inkSoft};">
    Reply to this email and it goes straight to ${escapeHtml(input.contact_name)}.
  </td></tr>`;

  return {
    subject,
    html: emailShell({
      preheader: `${input.salon_name} · ${BUSINESS_TYPE_LABELS[input.business_type]} · ${LIST_SIZE_LABELS[input.list_size]} · ${planName}`,
      title: 'New signup',
      body,
      footer:
        'Operator notification from the /start funnel. A new client row is written with active = false and cannot be claimed for dialing until you switch it on in /admin.',
    }),
  };
}

/** Short, warm, and specific about what happens next. No urgency, no countdown, no upsell. */
function prospectEmail(input: StartInput, planName: string): { subject: string; html: string } {
  const first = firstNameOf(input.contact_name);

  const steps = NEXT_STEPS.map(
    (s) => `<tr>
      <td width="42" style="padding:10px 0;font-family:${SERIF};font-size:20px;line-height:26px;color:${PALETTE.brass};vertical-align:top;">${escapeHtml(s.n)}</td>
      <td style="padding:10px 0;font-family:${SANS};font-size:14px;line-height:21px;color:${PALETTE.inkSoft};vertical-align:top;">
        <strong style="color:${PALETTE.ink};">${escapeHtml(s.title)}</strong><br>${escapeHtml(s.body)}
      </td>
    </tr>`,
  ).join('');

  const body = `
  <tr><td style="padding:30px 32px 0 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.16em;text-transform:uppercase;color:${PALETTE.brassDeep};">${escapeHtml(input.salon_name)}</div>
    <div style="font-family:${SERIF};font-size:34px;line-height:40px;color:${PALETTE.ink};padding-top:8px;">Thanks, ${escapeHtml(first)}.</div>
    <div style="font-family:${SANS};font-size:15px;line-height:23px;color:${PALETTE.inkSoft};padding-top:12px;">
      We have your details and your offer. Nothing is dialled yet, and nothing can be until we have been through your answers and your list with you.
    </div>
  </td></tr>
  <tr><td style="padding:14px 32px 0 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">${steps}</table>
  </td></tr>
${emailRule()}
  <tr><td style="padding:18px 32px 6px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      ${detailRow('Suggested plan', escapeHtml(planName))}
      ${detailRow(
        'Rather talk first',
        `<a href="${bookingCallUrl()}" style="color:${PALETTE.brassDeep};text-decoration:none;font-weight:600;">Book 15 minutes</a>`,
      )}
      ${detailRow(
        'Questions',
        `<a href="mailto:${SUPPORT_EMAIL}" style="color:${PALETTE.brassDeep};text-decoration:none;font-weight:600;">${SUPPORT_EMAIL}</a>`,
      )}
    </table>
  </td></tr>
  <tr><td style="padding:12px 32px 28px 32px;font-family:${SANS};font-size:13px;line-height:20px;color:${PALETTE.inkSoft};">
    When calling starts, Malone dials from ${escapeHtml(OUTBOUND_NUMBER)} — worth knowing if it turns up in your own call log.
  </td></tr>`;

  return {
    subject: `You're in — next steps for ${input.salon_name}`,
    html: emailShell({
      preheader: 'Your details are with us. Nothing dials until we have been through your list together.',
      title: 'Welcome',
      body,
      footer: `Salon Malone is operated by ${OPERATOR.legalName}, ${OPERATOR.address}. Questions: ${SUPPORT_EMAIL}. Calls go only to contacts marked as consenting, inside your local calling window, one attempt each. Opt-outs are honoured immediately and permanently.`,
    }),
  };
}
