'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { requireAdmin } from '@/lib/auth';
import { normalizePhone } from '@/lib/phone';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { asSuppressionReason, suppressPhoneGlobally } from '@/lib/suppression';

export async function addSuppressionAction(formData: FormData): Promise<void> {
  await requireAdmin(); // gate
  const phone = normalizePhone(formData.get('phone'));
  const reason = asSuppressionReason(formData.get('reason'));

  // Store E.164 only: the dial query joins on an exact phone match, so an unparseable
  // number would silently protect nobody.
  if (!phone) redirect('/admin/suppression?error=phone');

  // Gate: suppression is global and instant — the shared helper writes the durable row and takes
  // the number out of every client's queue in one step (src/lib/suppression.ts).
  const db = supabaseAdmin();
  const suppressed = await suppressPhoneGlobally(db, {
    phone,
    reason,
    tag: '[suppression-form]',
  });
  if (suppressed.error) redirect('/admin/suppression?error=save');

  revalidatePath('/admin/suppression');
  revalidatePath('/admin');
  redirect(`/admin/suppression?q=${encodeURIComponent(phone)}`);
}

export async function removeSuppressionAction(formData: FormData): Promise<void> {
  await requireAdmin();
  const id = formData.get('id');
  if (typeof id !== 'string' || !id) return;

  await supabaseAdmin().from('suppression').delete().eq('id', id);

  revalidatePath('/admin/suppression');
  revalidatePath('/admin');
}
