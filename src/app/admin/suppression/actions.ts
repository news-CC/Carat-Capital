'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { requireAdmin } from '@/lib/auth';
import { normalizePhone } from '@/lib/phone';
import { supabaseAdmin } from '@/lib/supabase/admin';

const REASONS = ['opt_out', 'dnc', 'complaint', 'invalid', 'manual'] as const;

export async function addSuppressionAction(formData: FormData): Promise<void> {
  await requireAdmin(); // gate
  const phone = normalizePhone(formData.get('phone'));
  const reason = REASONS.find((r) => r === formData.get('reason')) ?? 'manual';

  // Store E.164 only: the dial query joins on an exact phone match, so an unparseable
  // number would silently protect nobody.
  if (!phone) redirect('/admin/suppression?error=phone');

  const db = supabaseAdmin();
  const { error } = await db
    .from('suppression')
    .upsert({ phone, reason }, { onConflict: 'phone', ignoreDuplicates: true });

  if (error) redirect('/admin/suppression?error=save');

  // Gate: suppression is global and instant — take the number out of any queue now
  // rather than relying on the claim query to skip it later.
  await db
    .from('contacts')
    .update({ status: 'suppressed', scrub_reason: `suppression:${reason}` })
    .eq('phone', phone)
    .eq('status', 'pending');

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
