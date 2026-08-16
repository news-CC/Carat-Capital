import { NextResponse } from 'next/server';

import { unsubscribeByToken } from '@/lib/outreach';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/**
 * RFC 8058 one-click unsubscribe. Gmail and Outlook POST here directly from the
 * List-Unsubscribe-Post header without ever showing the recipient a page, so POST is the path
 * that matters most. GET is kept for clients that follow the header as a plain link.
 */
async function handle(req: Request): Promise<NextResponse> {
  const token = new URL(req.url).searchParams.get('token');
  const result = await unsubscribeByToken(token);

  if (!result.ok) {
    // A real failure to record the opt-out. Say so with a 5xx rather than a cheerful 200 — this is
    // the one case where the sender needs to know the request did not land.
    return NextResponse.json({ ok: false, error: result.error }, { status: 500 });
  }

  // 'invalid' and 'missing' still answer 200: a mail provider probing a stale token should not be
  // handed an error, and there is nothing the recipient can do about a bad link.
  return NextResponse.json({ ok: true, outcome: result.data });
}

export async function POST(req: Request) {
  return handle(req);
}

export async function GET(req: Request) {
  return handle(req);
}
