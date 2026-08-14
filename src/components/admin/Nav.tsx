'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const LINKS = [
  { href: '/admin', label: 'Dashboard' },
  { href: '/admin/clients', label: 'Clients' },
  { href: '/admin/calls', label: 'Calls' },
  { href: '/admin/bookings', label: 'Bookings' },
  { href: '/admin/suppression', label: 'Suppression' },
] as const;

function isCurrent(pathname: string, href: string): boolean {
  return href === '/admin' ? pathname === '/admin' : pathname.startsWith(href);
}

export function Nav({ email }: { email: string }) {
  const pathname = usePathname();

  return (
    <header className="border-b border-line bg-paper">
      <div className="mx-auto flex w-full max-w-6xl flex-wrap items-center gap-x-8 gap-y-3 px-6 py-4">
        <Link href="/admin" className="shrink-0">
          <span className="eyebrow block">Operator</span>
          <span className="font-display text-lg leading-none text-ink">Salon Malone</span>
        </Link>

        <nav className="flex flex-1 flex-wrap items-center gap-x-6 gap-y-2 text-sm">
          {LINKS.map((link) => {
            const current = isCurrent(pathname, link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                aria-current={current ? 'page' : undefined}
                className={
                  current
                    ? 'border-b border-brass pb-0.5 text-ink'
                    : 'border-b border-transparent pb-0.5 text-ink-soft transition-opacity duration-150 hover:opacity-70'
                }
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <span className="hidden text-xs text-ink-mute sm:block">{email}</span>
      </div>
    </header>
  );
}
