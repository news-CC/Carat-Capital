'use server';

import { revalidatePath } from 'next/cache';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { requireAdmin } from '@/lib/auth';
import { publicEnv, serverEnv } from '@/lib/env';
import { normalizePhone } from '@/lib/phone';
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

export async function sendWeeklyReportNowAction(formData: FormData): Promise<void> {
  await requireAdmin();
  const id = field(formData, 'id');
  const url = new URL('/api/cron/report', await selfOrigin());
  if (id) url.searchParams.set('client_id', id);

  // Same door the Friday cron uses, so a manual send exercises the real code path.
  let status = 0;
  try {
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${serverEnv('CRON_SECRET')}` },
      cache: 'no-store',
    });
    status = res.status;
  } catch {
    status = 0;
  }

  // Same ?notice / ?error convention the campaign actions use.
  const params: Record<string, string> =
    status >= 200 && status < 300
      ? { notice: 'Report job ran. Clients with no dials this week are skipped.' }
      : { error: `The report job did not run (HTTP ${status || 'no response'}). Check the logs.` };

  const query = new URLSearchParams(params).toString();
  redirect(id ? `/admin/clients/${id}?${query}` : `/admin/clients?${query}`);
}
