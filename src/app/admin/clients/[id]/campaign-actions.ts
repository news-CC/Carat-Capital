'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

import { requireAdmin } from '@/lib/auth';
import { err, ok, type Result } from '@/lib/result';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { asSuppressionReason, loadSuppressionPhones, suppressPhoneGlobally } from '@/lib/suppression';
import type { ContactStatus } from '@/lib/types';

/**
 * Gate counts recomputed from the database, mirroring `claim_contacts_for_dialing` so the number on
 * screen is the number the dialer will actually find. Call-window and billing state are time- and
 * client-level facts, so they are reported alongside the counts rather than folded into them.
 */
export type CampaignScrubReport = {
  client_id: string;
  campaign: string | null;
  generated_at: string;
  total: number;
  dialable_now: number;
  blocked_no_consent: number;
  blocked_missing_phone: number;
  blocked_suppressed: number;
  already_attempted: number;
  by_status: Record<ContactStatus, number>;
  suppression_list_size: number;
  client_active: boolean;
  stripe_status: string;
  /** True when this client has more contacts than one report can scan. */
  truncated: boolean;
};

const CONTACT_STATUSES: ContactStatus[] = [
  'pending',
  'calling',
  'called',
  'booked',
  'declined',
  'opted_out',
  'suppressed',
  'invalid',
  'no_answer',
  'failed',
];

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const CONTACT_PAGE = 1_000;
const CONTACT_SCAN_CAP = 60_000;

type Sb = ReturnType<typeof supabaseAdmin>;
type ClientRow = { id: string; name: string; active: boolean; stripe_status: string };

export async function scrubReport(
  clientId: string,
  campaign?: string | null,
): Promise<Result<CampaignScrubReport>> {
  await requireAdmin(); // GATE: admin session, or redirect to /login.
  if (!UUID_RE.test(clientId)) return err('That client link is malformed.');

  const sb = supabaseAdmin();
  const loaded = await loadClient(sb, clientId);
  if (!loaded.ok) return loaded;
  if (!loaded.data) return err('That client no longer exists.');

  return computeReport(sb, loaded.data, campaign ?? null);
}

export async function startCampaign(input: string | FormData): Promise<void> {
  await requireAdmin();
  const clientId = requiredId(input, 'clientId');
  const sb = supabaseAdmin();

  const loaded = await loadClient(sb, clientId);
  if (!loaded.ok) redirect(clientPath(clientId, { error: loaded.error }));
  if (!loaded.data) redirect(clientsPath({ error: 'That client no longer exists.' }));
  const client = loaded.data;

  // GATE: the claim query only takes active|trialing clients, so starting here would be a lie.
  if (client.stripe_status !== 'active' && client.stripe_status !== 'trialing') {
    redirect(
      clientPath(clientId, {
        error: `Billing is ${client.stripe_status}. Dialing stays off until that clears.`,
      }),
    );
  }

  const counted = await computeReport(sb, client, null);
  if (!counted.ok) redirect(clientPath(clientId, { error: `Nothing changed: ${counted.error}` }));
  const report = counted.data;

  if (report.dialable_now === 0) {
    redirect(
      clientPath(clientId, {
        error: `Nothing to dial. Of ${report.total} contacts: ${report.blocked_no_consent} without consent, ${report.blocked_missing_phone} without a usable number, ${report.blocked_suppressed} on the do-not-contact list, ${report.already_attempted} already attempted.`,
      }),
    );
  }

  const { error } = await sb.from('clients').update({ active: true }).eq('id', clientId);
  if (error) redirect(clientPath(clientId, { error: `Could not start the campaign: ${error.message}` }));

  revalidatePath(`/admin/clients/${clientId}`);
  revalidatePath('/admin');
  redirect(
    clientPath(clientId, {
      notice: `Campaign live. ${report.dialable_now} contacts are dialable — the next cron run inside the call window picks them up.`,
    }),
  );
}

export async function pauseCampaign(input: string | FormData): Promise<void> {
  await requireAdmin();
  const clientId = requiredId(input, 'clientId');
  const sb = supabaseAdmin();

  // GATE: clients.active = false is what the claim query reads. Nothing new gets claimed.
  const { error } = await sb.from('clients').update({ active: false }).eq('id', clientId);
  if (error) redirect(clientPath(clientId, { error: `Could not pause the campaign: ${error.message}` }));

  revalidatePath(`/admin/clients/${clientId}`);
  revalidatePath('/admin');
  redirect(
    clientPath(clientId, {
      notice: 'Campaign paused. No new calls will start; a call already in progress finishes.',
    }),
  );
}

/**
 * Clears the untouched part of a campaign. Contacts with an attempt on them are left alone — they
 * are the audit trail for calls that were actually placed.
 */
export async function deletePendingContacts(input: string | FormData): Promise<void> {
  await requireAdmin();
  const clientId = requiredId(input, 'clientId');
  const campaign = formField(input, 'campaign');
  const sb = supabaseAdmin();

  let query = sb
    .from('contacts')
    .delete()
    .eq('client_id', clientId)
    .eq('status', 'pending')
    .eq('attempts', 0);
  if (campaign) query = query.eq('campaign', campaign);

  const { data, error } = await query.select('id');
  if (error) redirect(clientPath(clientId, { error: `Could not clear the queue: ${error.message}` }));

  revalidatePath(`/admin/clients/${clientId}`);
  revalidatePath('/admin');
  redirect(
    clientPath(clientId, {
      notice: `Removed ${(data?.length ?? 0).toLocaleString('en-US')} never-called contacts from ${
        campaign ? `campaign "${campaign}"` : 'this client'
      }. Contacts that were already dialed were kept.`,
    }),
  );
}

/**
 * Suppresses one contact by id. No redirect: this button belongs on several pages, so it revalidates
 * and leaves the operator where they were.
 */
export async function suppressContact(input: string | FormData): Promise<void> {
  await requireAdmin();
  const contactId = formField(input, 'contactId') ?? bareString(input);
  if (!contactId || !UUID_RE.test(contactId)) return;

  const reason = asSuppressionReason(formField(input, 'reason'));

  const sb = supabaseAdmin();
  const { data: contact, error: loadError } = await sb
    .from('contacts')
    .select('id, client_id, phone')
    .eq('id', contactId)
    .maybeSingle();
  if (loadError || !contact) {
    if (loadError) console.error('suppressContact: load failed', loadError.message);
    return;
  }

  if (contact.phone) {
    // GATE: suppression is global. One row stops every client's campaign from dialing this number,
    // and the shared helper is what the opt-out webhook and the suppression form use too, so all
    // three write the same row and the same fan-out (src/lib/suppression.ts).
    const suppressed = await suppressPhoneGlobally(sb, {
      phone: contact.phone,
      reason,
      sourceContactId: contact.id,
      tag: '[suppress-contact]',
    });
    if (suppressed.error) return;
  }

  // The fan-out above only moves rows still 'pending'; this contact may be any status, and it is
  // the one the operator clicked, so it is marked explicitly.
  const { error: markError } = await sb
    .from('contacts')
    .update({ status: 'suppressed', scrub_reason: `suppression:${reason}` })
    .eq('id', contact.id);
  if (markError) console.error('suppressContact: mark failed', markError.message);

  revalidatePath(`/admin/clients/${contact.client_id}`);
  revalidatePath('/admin/suppression');
  revalidatePath('/admin');
}

async function computeReport(
  sb: Sb,
  client: ClientRow,
  campaign: string | null,
): Promise<Result<CampaignScrubReport>> {
  // The same read the upload path and the dialer use — one implementation, one paging rule.
  const suppression = await loadSuppressionPhones(sb);
  if (!suppression.ok) return suppression;
  const suppressed = suppression.data;

  const byStatus = {} as Record<ContactStatus, number>;
  for (const status of CONTACT_STATUSES) byStatus[status] = 0;

  const report: CampaignScrubReport = {
    client_id: client.id,
    campaign,
    generated_at: new Date().toISOString(),
    total: 0,
    dialable_now: 0,
    blocked_no_consent: 0,
    blocked_missing_phone: 0,
    blocked_suppressed: 0,
    already_attempted: 0,
    by_status: byStatus,
    suppression_list_size: suppressed.size,
    client_active: client.active,
    stripe_status: client.stripe_status,
    truncated: false,
  };

  for (let from = 0; from < CONTACT_SCAN_CAP; from += CONTACT_PAGE) {
    let query = sb
      .from('contacts')
      .select('phone, consent, status, attempts')
      .eq('client_id', client.id)
      .order('created_at')
      .range(from, from + CONTACT_PAGE - 1);
    if (campaign) query = query.eq('campaign', campaign);

    const { data, error } = await query;
    if (error) return err(error.message);
    if (!data || data.length === 0) return ok(report);

    for (const row of data) {
      report.total += 1;
      if (isContactStatus(row.status)) report.by_status[row.status] += 1;
      if (row.attempts > 0) report.already_attempted += 1;

      if (!row.consent) report.blocked_no_consent += 1;
      else if (!row.phone) report.blocked_missing_phone += 1;
      else if (suppressed.has(row.phone)) report.blocked_suppressed += 1;
      else if (row.status === 'pending' && row.attempts === 0) report.dialable_now += 1;
    }

    if (data.length < CONTACT_PAGE) return ok(report);
  }

  report.truncated = true;
  return ok(report);
}

async function loadClient(sb: Sb, clientId: string): Promise<Result<ClientRow | null>> {
  const { data, error } = await sb
    .from('clients')
    .select('id, name, active, stripe_status')
    .eq('id', clientId)
    .maybeSingle();
  if (error) return err(`Could not load that client: ${error.message}`);
  return ok(data ?? null);
}

function isContactStatus(value: unknown): value is ContactStatus {
  return typeof value === 'string' && (CONTACT_STATUSES as string[]).includes(value);
}

/** Accepts a bare id (called from a client component) or a submitted form (`<form action={…}>`). */
function requiredId(input: string | FormData, key: string): string {
  const value = formField(input, key) ?? bareString(input);
  if (!value || !UUID_RE.test(value)) redirect(clientsPath({ error: 'That link is malformed.' }));
  return value;
}

function bareString(input: string | FormData): string | null {
  return typeof input === 'string' && input.trim() !== '' ? input.trim() : null;
}

function formField(input: string | FormData, key: string): string | null {
  if (typeof input === 'string') return null;
  const value = input.get(key);
  return typeof value === 'string' && value.trim() !== '' ? value.trim() : null;
}

function clientPath(clientId: string, params: Record<string, string>): string {
  return `/admin/clients/${clientId}?${new URLSearchParams(params).toString()}`;
}

function clientsPath(params: Record<string, string>): string {
  return `/admin/clients?${new URLSearchParams(params).toString()}`;
}
