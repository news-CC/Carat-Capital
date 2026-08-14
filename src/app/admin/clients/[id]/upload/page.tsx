import Link from 'next/link';
import { notFound } from 'next/navigation';

import { UploadWizard } from '@/components/admin/UploadWizard';
import { requireAdmin } from '@/lib/auth';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const metadata = { title: 'Upload a list' };

export default async function UploadPage({ params }: { params: Promise<{ id: string }> }) {
  await requireAdmin(); // GATE: admin session, or redirect to /login.
  const { id } = await params;

  const sb = supabaseAdmin();
  const { data: client } = await sb
    .from('clients')
    .select('id, name, offer_text, timezone, booking_phone')
    .eq('id', id)
    .maybeSingle();
  if (!client) notFound();

  const [contacts, suppression] = await Promise.all([
    sb.from('contacts').select('id', { count: 'exact', head: true }).eq('client_id', client.id),
    sb.from('suppression').select('id', { count: 'exact', head: true }),
  ]);

  return (
    <div className="space-y-8">
      <header className="space-y-3">
        <Link href={`/admin/clients/${client.id}`} className="eyebrow">
          ← {client.name}
        </Link>
        <h1 className="h-display text-3xl">Upload a client list</h1>
        <p className="prose-tight max-w-2xl text-ink-soft">
          Three steps: pick the file, confirm which column is which, then read the dry run before a
          single row is written. Malone calls the survivors with {client.name}&rsquo;s offer —{' '}
          <span className="text-ink">{client.offer_text}</span>
        </p>
      </header>

      <UploadWizard
        clientId={client.id}
        clientName={client.name}
        offerText={client.offer_text}
        existingContacts={contacts.count ?? 0}
        suppressionListSize={suppression.count ?? 0}
      />

      <section className="card card-pad space-y-3">
        <h2 className="eyebrow">What happens to these rows</h2>
        <ul className="prose-tight space-y-2 text-sm text-ink-soft">
          <li>
            <span className="text-ink">Consent is required.</span> A row whose consent column does not
            read as a yes is dropped and never stored as dialable.
          </li>
          <li>
            <span className="text-ink">The do-not-contact list wins.</span> Every number is checked
            against it on the server, on upload and again at dial time.
          </li>
          <li>
            <span className="text-ink">One attempt per contact, ever.</span> No retries, no second
            campaign quietly calling the same number.
          </li>
          <li>
            <span className="text-ink">Calls only inside the window,</span> in {client.timezone} — the
            time zone {client.name} keeps, not ours.
          </li>
          <li>
            <span className="text-ink">Malone says what he is</span> in the first sentence, and leaves{' '}
            {client.booking_phone ? client.booking_phone : `${client.name}'s own number`} on voicemail.
          </li>
        </ul>
      </section>
    </div>
  );
}
