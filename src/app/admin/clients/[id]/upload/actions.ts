'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

import { requireAdmin } from '@/lib/auth';
import { requireConsent } from '@/lib/env';
import { MAX_UPLOAD_ROWS } from '@/lib/parse-sheet';
import { err, ok, type Result } from '@/lib/result';
import { scrubRows, type RawRow, type ScrubStats } from '@/lib/scrub';
import { supabaseAdmin } from '@/lib/supabase/admin';

/** What the wizard shows on the receipt screen. The server's numbers are the real ones. */
export type UploadOutcome = {
  campaign: string;
  stats: ScrubStats;
  inserted: number;
  already_on_campaign: number;
  suppression_list_size: number;
  consent_required: boolean;
};

const CHUNK_SIZE = 500;
const SUPPRESSION_PAGE = 1_000;
const SUPPRESSION_CAP = 200_000;

const UploadSchema = z.object({
  clientId: z.uuid('That client link is malformed.'),
  campaign: z
    .string()
    .trim()
    .min(1, 'Give the campaign a name.')
    .max(60, 'Campaign names stop at 60 characters.')
    .regex(/^[A-Za-z0-9][A-Za-z0-9 _-]*$/, 'Campaign names take letters, numbers, spaces, dashes and underscores.'),
  rows: z.array(z.record(z.string(), z.unknown())).min(1, 'There were no rows to add.'),
});

export type UploadInput = z.input<typeof UploadSchema>;

export async function uploadContacts(input: UploadInput): Promise<Result<UploadOutcome>> {
  await requireAdmin(); // GATE: admin session, or redirect to /login.

  // Checked before schema validation so an oversized list gets a message that says what to do.
  const rowCount = Array.isArray(input?.rows) ? input.rows.length : 0;
  if (rowCount > MAX_UPLOAD_ROWS) {
    return err(
      `That list has ${rowCount.toLocaleString('en-US')} rows. One upload takes ${MAX_UPLOAD_ROWS.toLocaleString('en-US')} — split the file and upload it in parts.`,
    );
  }

  const parsed = UploadSchema.safeParse(input);
  if (!parsed.success) {
    return err(parsed.error.issues[0]?.message ?? 'That upload did not look right.');
  }
  const { clientId, campaign, rows } = parsed.data;

  const sb = supabaseAdmin();
  const { data: client, error: clientError } = await sb
    .from('clients')
    .select('id, name')
    .eq('id', clientId)
    .maybeSingle();
  if (clientError) return err(`Could not load that client: ${clientError.message}`);
  if (!client) return err('That client no longer exists.');

  // GATE: the live do-not-contact list. If we cannot read it we fail closed and write nothing —
  // an upload that skipped the suppression check would be worse than a failed upload.
  let suppressed: Set<string>;
  try {
    suppressed = await loadSuppressionPhones(sb);
  } catch (cause) {
    const detail = cause instanceof Error ? cause.message : 'unknown error';
    return err(`Nothing was written: the do-not-contact list could not be read (${detail}).`);
  }

  // GATE: consent, phone validity, suppression and in-file duplicates, re-run server-side. The
  // browser preview the operator just looked at is advisory only; this run is the authority.
  const scrub = scrubRows(rows as RawRow[], suppressed, { requireConsent: requireConsent() });

  let inserted = 0;
  for (let i = 0; i < scrub.kept.length; i += CHUNK_SIZE) {
    const chunk = scrub.kept.slice(i, i + CHUNK_SIZE).map((row) => ({
      client_id: clientId,
      campaign,
      name: row.name,
      first_name: row.first_name,
      phone: row.phone,
      phone_raw: row.phone_raw,
      email: row.email,
      consent: true,
      last_visit: row.last_visit,
      lifetime_value_cents: row.lifetime_value_cents,
      status: 'pending' as const,
    }));
    const { data, error } = await sb
      .from('contacts')
      .upsert(chunk, { onConflict: 'client_id,campaign,phone', ignoreDuplicates: true })
      .select('id');
    if (error) {
      return err(
        `Added ${inserted.toLocaleString('en-US')} contacts, then the database refused the next batch: ${error.message}`,
      );
    }
    inserted += data?.length ?? 0;
  }

  revalidatePath(`/admin/clients/${clientId}`);
  revalidatePath('/admin');

  return ok({
    campaign,
    stats: scrub.stats,
    inserted,
    // Rows that passed every gate but were already on this campaign — the unique index caught them.
    already_on_campaign: scrub.stats.kept - inserted,
    suppression_list_size: suppressed.size,
    consent_required: requireConsent(),
  });
}

/**
 * The whole suppression list, paged because PostgREST caps a response at 1000 rows. Small table by
 * design: one row per person who ever said no.
 */
async function loadSuppressionPhones(sb: ReturnType<typeof supabaseAdmin>): Promise<Set<string>> {
  const phones = new Set<string>();
  for (let from = 0; from < SUPPRESSION_CAP; from += SUPPRESSION_PAGE) {
    const { data, error } = await sb
      .from('suppression')
      .select('phone')
      .order('phone')
      .range(from, from + SUPPRESSION_PAGE - 1);
    if (error) throw new Error(error.message);
    if (!data || data.length === 0) break;
    for (const row of data) if (row.phone) phones.add(row.phone);
    if (data.length < SUPPRESSION_PAGE) break;
  }
  return phones;
}
