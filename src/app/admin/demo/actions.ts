'use server';

import { revalidatePath } from 'next/cache';

import { requireAdmin } from '@/lib/auth';
import { isInsideCallWindow, localTimeInZone } from '@/lib/call-window';
import { buildDemoFirstMessage, buildDemoSystemPrompt, demoSchema, type DemoState } from '@/lib/demo';
import { callWindow, serverEnv } from '@/lib/env';
import { maloneVariables } from '@/lib/malone';
import { isFictionalPhone, normalizePhone } from '@/lib/phone';
import { supabaseAdmin } from '@/lib/supabase/admin';

/** One client row holds every demo, so the operator console does not fill up with fake salons. */
const DEMO_CLIENT_NAME = 'Salon Malone — live demos';

export async function placeDemoCall(_prev: DemoState, formData: FormData): Promise<DemoState> {
  await requireAdmin();

  const parsed = demoSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    const fieldErrors: Record<string, string> = {};
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? '_');
      fieldErrors[key] ??= issue.message;
    }
    return { status: 'error', error: 'Have a look at the highlighted fields.', fieldErrors };
  }
  const input = parsed.data;

  const phone = normalizePhone(input.phone);
  if (!phone) {
    return {
      status: 'error',
      error: 'That number is not one we can dial.',
      fieldErrors: { phone: 'Use a US or Canada number, e.g. (510) 375-5890.' },
    };
  }

  // The 555-01XX range is reserved for fiction and routes nowhere. Dialing it burns a Vapi call
  // and looks like a product failure, so say what happened instead.
  if (isFictionalPhone(phone)) {
    return {
      status: 'error',
      error: 'That is a fiction-range number (555-01XX) and will not connect.',
      fieldErrors: { phone: 'Use a real number for a demo.' },
    };
  }

  const db = supabaseAdmin();

  // GATE: global suppression. A demo bypasses claim_contacts_for_dialing, so this check has to
  // exist here or the one promise the product makes — "stop calling means stop calling" — has a
  // hole in it that the operator can walk through by accident.
  const suppressed = await db.from('suppression').select('phone, reason').eq('phone', phone).maybeSingle();
  if (suppressed.error) {
    console.error('[demo] suppression lookup failed', { detail: suppressed.error.message });
    return { status: 'error', error: 'Could not check the do-not-call list, so nothing was dialed.' };
  }
  if (suppressed.data) {
    return {
      status: 'error',
      error: `${phone} is on the global do-not-call list (${suppressed.data.reason}). Not dialing.`,
      fieldErrors: { phone: 'This number asked never to be called again.' },
    };
  }

  // GATE: calling hours. Overridable, because the whole premise of a demo is that the person is
  // asking for it right now — but the override is deliberate, ticked by hand, and recorded.
  const window = callWindow();
  const inside = isInsideCallWindow(input.timezone, window.start, window.end);
  if (!inside && !input.window_override) {
    const local = localTimeInZone(input.timezone);
    return {
      status: 'error',
      error: `It is ${local} in ${input.timezone} — outside the ${window.start}-${window.end} calling window. Tick the override if they asked you to call now.`,
      fieldErrors: { window_override: 'Required outside calling hours.' },
    };
  }

  let assistantId: string;
  let phoneNumberId: string;
  try {
    assistantId = serverEnv('VAPI_ASSISTANT_ID');
    phoneNumberId = serverEnv('VAPI_PHONE_NUMBER_ID');
  } catch {
    return { status: 'error', error: 'Vapi is not configured — VAPI_ASSISTANT_ID or VAPI_PHONE_NUMBER_ID is missing.' };
  }

  // Reuse one demo client so /admin/clients stays a list of real prospects.
  let client = (await db.from('clients').select('*').eq('name', DEMO_CLIENT_NAME).maybeSingle()).data;
  if (!client) {
    const created = await db
      .from('clients')
      .insert({
        name: DEMO_CLIENT_NAME,
        contact_name: 'Operator',
        contact_email: serverEnv('ADMIN_EMAIL'),
        offer_text: 'Demo calls placed from the operator console.',
        timezone: input.timezone,
        vertical: 'salon',
        avg_ticket_cents: 12000,
        stripe_status: 'trialing',
        // Never claimable by the dialing cron. Demos are placed directly and on purpose; this row
        // existing must not cause a single automated call.
        active: false,
      })
      .select()
      .single();
    if (created.error || !created.data) {
      console.error('[demo] could not create the demo client', { detail: created.error?.message });
      return { status: 'error', error: 'Could not set up the demo client row.' };
    }
    client = created.data;
  }

  // A fresh campaign per demo. One attempt per contact is enforced by `attempts = 0` in the claim
  // query and by the unique key on (client_id, campaign, phone) — so demoing the same number twice
  // needs a new campaign rather than a reset row, which would quietly undo that guarantee.
  const campaign = `demo-${Date.now().toString(36)}`;
  const contact = await db
    .from('contacts')
    .insert({
      client_id: client.id,
      campaign,
      name: input.first_name ?? 'Demo listener',
      first_name: input.first_name ?? null,
      phone,
      phone_raw: input.phone,
      consent: true, // attested by the operator above; the checkbox is required to get here
      status: 'calling',
      attempts: 1,
      scrub_reason: input.window_override && !inside ? 'demo:window_override' : 'demo',
    })
    .select()
    .single();
  if (contact.error || !contact.data) {
    console.error('[demo] could not create the contact', { detail: contact.error?.message });
    return { status: 'error', error: 'Could not record the demo contact, so nothing was dialed.' };
  }

  const { startOutboundCall } = await import('@/lib/vapi');
  const started = await startOutboundCall({
    phone,
    assistantId,
    phoneNumberId,
    variables: {
      ...maloneVariables({
        first_name: input.first_name ?? '',
        salon_name: input.salon_name,
        offer_text: input.offer_text,
        booking_phone: input.booking_phone ?? '',
      }),
      ...(input.promo_code ? { promo_code: input.promo_code } : {}),
    },
    metadata: {
      contact_id: contact.data.id,
      client_id: client.id,
      campaign,
      demo: 'true',
    },
    systemPrompt: buildDemoSystemPrompt({ promoCode: input.promo_code, instructions: input.instructions }),
    firstMessage: buildDemoFirstMessage({ firstName: input.first_name, salonName: input.salon_name }),
  });

  // Every dial attempt writes a calls row, demo or not. The webhook then attaches the transcript,
  // the outcome, any booking and any opt-out to this row exactly as it would for a real campaign.
  const callRow = {
    contact_id: contact.data.id,
    client_id: client.id,
    started_at: new Date().toISOString(),
  };

  if (!started.ok) {
    const logged = await db.from('calls').insert({
      ...callRow,
      outcome: 'failed' as const,
      ended_reason: started.error.slice(0, 500),
      ended_at: new Date().toISOString(),
    });
    if (logged.error) console.error('[demo] FAILED CALL NOT LOGGED', { detail: logged.error.message });
    await db.from('contacts').update({ status: 'failed' }).eq('id', contact.data.id);
    revalidatePath('/admin/demo');
    return { status: 'error', error: started.error.slice(0, 300) };
  }

  const logged = await db
    .from('calls')
    .insert({ ...callRow, vapi_call_id: started.data.vapiCallId, outcome: 'dialing' as const });
  if (logged.error) console.error('[demo] DIAL NOT LOGGED', { detail: logged.error.message });

  revalidatePath('/admin/demo');
  revalidatePath('/admin/calls');

  return {
    status: 'success',
    phone,
    salonName: input.salon_name,
    vapiCallId: started.data.vapiCallId,
    promoCode: input.promo_code,
    outsideWindow: !inside,
  };
}
