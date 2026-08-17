import type { Metadata } from 'next';
import Link from 'next/link';

import DemoCallForm from '@/components/admin/DemoCallForm';
import { requireAdmin } from '@/lib/auth';
import { localTimeInZone } from '@/lib/call-window';
import { callWindow } from '@/lib/env';
import { formatPhone } from '@/lib/phone';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const metadata: Metadata = { title: 'Demo call' };
export const dynamic = 'force-dynamic';

const DEMO_CLIENT_NAME = 'Salon Malone — live demos';

type DemoCall = {
  id: string;
  outcome: string;
  ended_reason: string | null;
  summary: string | null;
  duration_seconds: number | null;
  transcript_url: string | null;
  created_at: string;
  contacts: { phone: string | null; first_name: string | null; campaign: string } | null;
};

const TONE: Record<string, string> = {
  booked: 'badge-ok',
  answered: 'badge-ok',
  dialing: 'badge-warn',
  voicemail: 'badge-mute',
  no_answer: 'badge-mute',
  declined: 'badge-mute',
  busy: 'badge-mute',
  opted_out: 'badge-bad',
  failed: 'badge-bad',
};

export default async function DemoPage() {
  await requireAdmin();
  const db = supabaseAdmin();
  const window = callWindow();

  const client = (await db.from('clients').select('id').eq('name', DEMO_CLIENT_NAME).maybeSingle()).data;

  let recent: DemoCall[] = [];
  if (client) {
    const { data } = await db
      .from('calls')
      .select('id, outcome, ended_reason, summary, duration_seconds, transcript_url, created_at, contacts(phone, first_name, campaign)')
      .eq('client_id', client.id)
      .order('created_at', { ascending: false })
      .limit(12);
    recent = (data ?? []) as unknown as DemoCall[];
  }

  return (
    <div className="mx-auto w-full max-w-6xl px-6 py-10">
      <p className="eyebrow">Sales</p>
      <h1 className="h-display mt-3 text-[clamp(1.9rem,4vw,2.75rem)]">Put Malone on the phone</h1>
      <p className="prose-tight mt-4 max-w-2xl">
        For the salon owner who says &ldquo;let me hear it&rdquo;. Same assistant, same webhook, same
        booking and opt-out handling as a paying client&apos;s campaign — the only difference is that
        this one dials immediately instead of waiting for the queue.
      </p>
      <p className="help mt-3">
        Calling hours are {window.start}–{window.end} in their local time. It is currently{' '}
        {localTimeInZone('America/New_York')} in New York.
      </p>

      <div className="rule my-8" />

      <DemoCallForm defaultTimezone="America/New_York" />

      <div className="rule my-10" />

      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <h2 className="font-display text-xl">Recent demos</h2>
        <Link className="btn btn-ghost btn-sm" href="/admin/calls">
          All calls
        </Link>
      </div>

      {recent.length === 0 ? (
        <div className="card card-pad mt-4">
          <p className="help">No demo calls yet. The first one you place will show up here with its transcript.</p>
        </div>
      ) : (
        <div className="card mt-4 overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>When</th>
                <th>Number</th>
                <th>Outcome</th>
                <th className="text-right">Length</th>
                <th>What happened</th>
              </tr>
            </thead>
            <tbody>
              {recent.map((call) => (
                <tr key={call.id}>
                  <td className="whitespace-nowrap text-ink-mute">
                    {new Date(call.created_at).toLocaleString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      hour: 'numeric',
                      minute: '2-digit',
                    })}
                  </td>
                  <td className="whitespace-nowrap tabular-nums">
                    {call.contacts?.phone ? formatPhone(call.contacts.phone) : '—'}
                  </td>
                  <td>
                    <span className={`badge ${TONE[call.outcome] ?? 'badge-mute'}`}>{call.outcome}</span>
                  </td>
                  <td className="text-right tabular-nums text-ink-mute">
                    {call.duration_seconds != null ? `${call.duration_seconds}s` : '—'}
                  </td>
                  <td className="max-w-md text-ink-soft">
                    {call.summary ?? call.ended_reason ?? '—'}
                    {call.transcript_url && (
                      <>
                        {' '}
                        <a className="underline" href={call.transcript_url} target="_blank" rel="noreferrer">
                          transcript
                        </a>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
