'use server';

import { revalidatePath } from 'next/cache';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { requireAdmin } from '@/lib/auth';
import { publicEnv, serverEnv } from '@/lib/env';
import { normalizePhone } from '@/lib/phone';
import { err, ok, type Result } from '@/lib/result';
import { supabaseAdmin } from '@/lib/supabase/admin';

/** Only types and async functions may leave a `'use server'` module. */
export type ClientFormState = {
  ok: boolean;
  message?: string;
  error?: string;
  fieldErrors?: Record<string, string>;
  /** React 19 resets an uncontrolled form after the action, so echo values back on failure. */
  values?: Record<string, string>;
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/;

function isValidTimeZone(tz: string): boolean {
  try {
    new Intl.DateTimeFormat('en-US', { timeZone: tz });
    return true;
  } catch {
    return false;
  }
}

const ClientSchema = z.object({
  name: z.string().min(2, 'Use the salon’s real name — Malone says it out loud.').max(120),
  contact_name: z.string().max(120),
  contact_email: z.string().regex(EMAIL_RE, 'A working email — booking alerts and the Friday report go here.'),
  contact_phone: z.string().max(40),
  booking_phone: z.string().max(40),
  offer_text: z
    .string()
    .min(10, 'Write the offer the way it should be spoken, not the way it looks on a flyer.')
    .max(400),
  timezone: z.string().refine(isValidTimeZone, 'Choose a timezone from the list.'),
  vertical: z.enum(['salon', 'medspa']),
  avg_ticket_dollars: z
    .number()
    .int('Whole dollars.')
    .min(1, 'Average ticket drives every revenue number in the product.')
    .max(5000, 'That is higher than any real ticket — check the figure.'),
});

type ClientWritable = {
  name: string;
  contact_name: string | null;
  contact_email: string;
  contact_phone: string | null;
  booking_phone: string | null;
  offer_text: string;
  timezone: string;
  vertical: 'salon' | 'medspa';
  avg_ticket_cents: number;
};

function field(formData: FormData, key: string): string {
  const value = formData.get(key);
  return typeof value === 'string' ? value.trim() : '';
}

const FORM_FIELDS = [
  'name',
  'contact_name',
  'contact_email',
  'contact_phone',
  'booking_phone',
  'offer_text',
  'timezone',
  'vertical',
  'avg_ticket_dollars',
] as const;

function rawValues(formData: FormData): Record<string, string> {
  const values: Record<string, string> = {};
  for (const key of FORM_FIELDS) values[key] = field(formData, key);
  return values;
}

function parseClient(formData: FormData): { ok: true; row: ClientWritable } | { ok: false; state: ClientFormState } {
  const values = rawValues(formData);

  const dollars = Number(values.avg_ticket_dollars);
  const parsed = ClientSchema.safeParse({
    ...values,
    contact_email: values.contact_email.toLowerCase(),
    avg_ticket_dollars: Number.isFinite(dollars) ? dollars : 0,
  });

  if (!parsed.success) {
    const fieldErrors: Record<string, string> = {};
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? 'form');
      if (!(key in fieldErrors)) fieldErrors[key] = issue.message;
    }
    return { ok: false, state: { ok: false, error: 'Fix the highlighted fields.', fieldErrors, values } };
  }

  const input = parsed.data;
  const contactPhone = input.contact_phone ? normalizePhone(input.contact_phone) : null;
  const bookingPhone = input.booking_phone ? normalizePhone(input.booking_phone) : null;

  if (input.contact_phone && !contactPhone) {
    return { ok: false, state: { ok: false, values, fieldErrors: { contact_phone: 'That number is not dialable.' } } };
  }
  // Malone reads this number out on voicemail, so a wrong one is worse than none.
  if (input.booking_phone && !bookingPhone) {
    return { ok: false, state: { ok: false, values, fieldErrors: { booking_phone: 'That number is not dialable.' } } };
  }

  return {
    ok: true,
    row: {
      name: input.name,
      contact_name: input.contact_name || null,
      contact_email: input.contact_email,
      contact_phone: contactPhone,
      booking_phone: bookingPhone,
      offer_text: input.offer_text,
      timezone: input.timezone,
      vertical: input.vertical,
      avg_ticket_cents: input.avg_ticket_dollars * 100,
    },
  };
}

export async function createClientAction(
  _prev: ClientFormState,
  formData: FormData,
): Promise<ClientFormState> {
  await requireAdmin(); // gate: server actions are public endpoints, not just page code
  const parsed = parseClient(formData);
  if (!parsed.ok) return parsed.state;

  const { data, error } = await supabaseAdmin()
    .from('clients')
    .insert(parsed.row)
    .select('id')
    .single();

  if (error || !data) {
    return { ok: false, error: error?.message ?? 'Could not save the client.', values: rawValues(formData) };
  }

  revalidatePath('/admin');
  revalidatePath('/admin/clients');
  redirect(`/admin/clients/${data.id}`);
}

export async function updateClientAction(
  _prev: ClientFormState,
  formData: FormData,
): Promise<ClientFormState> {
  await requireAdmin();
  const id = field(formData, 'id');
  if (!id) return { ok: false, error: 'Missing client id.' };

  const parsed = parseClient(formData);
  if (!parsed.ok) return parsed.state;

  const { error } = await supabaseAdmin().from('clients').update(parsed.row).eq('id', id);
  if (error) return { ok: false, error: error.message, values: rawValues(formData) };

  revalidatePath('/admin');
  revalidatePath('/admin/clients');
  revalidatePath(`/admin/clients/${id}`);
  return { ok: true, message: 'Saved. New calls use the new offer immediately.' };
}

/** Hit our own running instance, not NEXT_PUBLIC_APP_URL (which points at production). */
async function selfOrigin(): Promise<string> {
  const h = await headers();
  const host = h.get('x-forwarded-host') ?? h.get('host');
  if (!host) return publicEnv.appUrl;
  const proto = h.get('x-forwarded-proto') ?? (host.startsWith('localhost') ? 'http' : 'https');
  return `${proto}://${host}`;
}

/** What /api/cron/report answers with. It returns HTTP 200 for "nothing was sent" as well. */
type ReportRunResult = { salonName: string; sent: boolean; reason?: string };
type ReportRunBody = { ok?: boolean; error?: string; results?: ReportRunResult[] };

/** Enough names to be useful, few enough to fit in a redirect URL. */
const NAME_LIMIT = 3;

export async function sendWeeklyReportNowAction(formData: FormData): Promise<void> {
  await requireAdmin();
  const id = field(formData, 'id');
  const url = new URL('/api/cron/report', await selfOrigin());
  if (id) url.searchParams.set('client_id', id);

  const run = await runReportJob(url);

  // Same ?notice / ?error convention the campaign actions use.
  const query = new URLSearchParams(
    run.ok ? { notice: run.data } : { error: run.error },
  ).toString();
  redirect(id ? `/admin/clients/${id}?${query}` : `/admin/clients?${query}`);
}

/**
 * Same door the Friday cron uses, so a manual send exercises the real code path — which means the
 * verdict has to come out of the body, not the status code. A quiet week, a client the billing gate
 * excludes and a dead Resend key all answer HTTP 200, and a green "job ran" notice for an email
 * that never left is how the operator finds out a week late.
 */
async function runReportJob(url: URL): Promise<Result<string>> {
  let res: Response;
  try {
    res = await fetch(url, {
      headers: { Authorization: `Bearer ${serverEnv('CRON_SECRET')}` },
      cache: 'no-store',
    });
  } catch (e) {
    const detail = e instanceof Error ? e.message : 'no response';
    return err(`The report job did not run (${detail}). Check the logs.`);
  }

  const body = await readReportBody(res);
  if (!res.ok || body === null || body.ok === false) {
    return err(
      `The report job failed (HTTP ${res.status}: ${body?.error ?? 'unreadable response'}). Check the logs.`,
    );
  }

  const results = body.results ?? [];
  const sent = results.filter((r) => r.sent);
  const skipped = results.filter((r) => !r.sent);

  if (sent.length === 0) {
    return err(
      results.length === 0
        ? 'No report was sent: the job matched no client. Check the client still exists.'
        : `No report was sent — ${skipSummary(skipped)}.`,
    );
  }

  const names =
    sent.length <= NAME_LIMIT ? sent.map((r) => r.salonName).join(', ') : `${sent.length} clients`;
  return ok(
    skipped.length === 0
      ? `Report emailed to ${names}.`
      : `Report emailed to ${names}. Skipped — ${skipSummary(skipped)}.`,
  );
}

async function readReportBody(res: Response): Promise<ReportRunBody | null> {
  try {
    return (await res.json()) as ReportRunBody;
  } catch {
    // Null is a distinct outcome, not a swallowed error: the caller reports it with the status.
    return null;
  }
}

function skipSummary(skipped: ReportRunResult[]): string {
  if (skipped.length > NAME_LIMIT) return `${skipped.length} clients skipped, reasons in the logs`;
  return skipped.map((r) => `${r.salonName}: ${skipPhrase(r.reason)}`).join('; ');
}

/** Plain English for the route's reasons, which are a bare token or `<token>: <detail>`. */
function skipPhrase(reason: string | undefined): string {
  if (!reason) return 'skipped, no reason given';
  if (reason === 'no_activity') return 'no calls in the last 7 days';
  if (reason.startsWith('not_reportable: ')) return reason.slice('not_reportable: '.length);
  // One of the five count queries behind the email (four on calls, one on bookings) errored.
  if (reason.startsWith('counts_query_failed: ')) {
    return `the week's numbers could not be counted — ${reason.slice('counts_query_failed: '.length)}`;
  }
  return reason; // A Resend failure comes back as its own message, already readable.
}
