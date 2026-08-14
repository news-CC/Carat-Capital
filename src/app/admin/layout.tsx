import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { requireAdmin } from '@/lib/auth';
import { Nav } from '@/components/admin/Nav';

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: 'Operator · Salon Malone',
  robots: { index: false, follow: false },
};

export default async function AdminLayout({ children }: { children: ReactNode }) {
  // Gate: middleware only checks that a cookie exists — this verifies the signature.
  const { email } = await requireAdmin();

  return (
    <div className="min-h-screen bg-cream">
      <Nav email={email} />
      <main className="mx-auto w-full max-w-6xl px-6 py-10">{children}</main>
    </div>
  );
}
