import { NextResponse } from 'next/server';
import Stripe from 'stripe';

import { serverEnv } from '@/lib/env';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

type BillingStatus = 'trialing' | 'active' | 'past_due' | 'canceled';

type Change = { status: BillingStatus; customerId: string | null; email: string | null };

export async function POST(req: Request) {
  const signature = req.headers.get('stripe-signature');
  if (!signature) {
    return NextResponse.json({ received: false, error: 'missing stripe-signature' }, { status: 400 });
  }

  // Raw body, and a lazily constructed client so a missing key can never break the build.
  let stripe: Stripe;
  let event: Stripe.Event;
  try {
    stripe = new Stripe(serverEnv('STRIPE_SECRET_KEY'));
    event = stripe.webhooks.constructEvent(
      await req.text(),
      signature,
      serverEnv('STRIPE_WEBHOOK_SECRET'),
    );
  } catch (e) {
    return NextResponse.json(
      { received: false, error: e instanceof Error ? e.message : 'bad signature' },
      { status: 400 },
    );
  }

  const change = await resolveChange(stripe, event);
  if (!change) return NextResponse.json({ received: true, ignored: event.type });

  try {
    const matched = await applyStatus(change);
    if (matched === 'none') {
      // Payment links can be paid before the client row exists. Log it, don't make Stripe retry.
      console.warn('[stripe-webhook] no client matched', event.type, change.customerId, change.email);
    }
    return NextResponse.json({ received: true, type: event.type, status: change.status, matched });
  } catch (e) {
    return NextResponse.json(
      { received: false, error: e instanceof Error ? e.message : 'update failed' },
      { status: 500 },
    );
  }
}

async function resolveChange(stripe: Stripe, event: Stripe.Event): Promise<Change | null> {
  switch (event.type) {
    case 'checkout.session.completed': {
      const s = event.data.object;
      return {
        status: 'active',
        customerId: idOf(s.customer),
        email: s.customer_details?.email ?? s.customer_email ?? null,
      };
    }
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted': {
      const sub = event.data.object;
      const status =
        event.type === 'customer.subscription.deleted'
          ? 'canceled'
          : mapSubscriptionStatus(sub.status);
      const customerId = idOf(sub.customer);
      return { status, customerId, email: await customerEmail(stripe, customerId) };
    }
    case 'invoice.payment_failed': {
      const inv = event.data.object;
      return {
        status: 'past_due',
        customerId: idOf(inv.customer),
        email: inv.customer_email ?? null,
      };
    }
    default:
      return null;
  }
}

/** Match on stripe_customer_id first, then fall back to the contact email. */
async function applyStatus(change: Change): Promise<'customer_id' | 'email' | 'none'> {
  const db = supabaseAdmin();

  if (change.customerId) {
    const { data, error } = await db
      .from('clients')
      .update({ stripe_status: change.status })
      .eq('stripe_customer_id', change.customerId)
      .select('id');
    if (error) throw new Error(error.message);
    if ((data ?? []).length > 0) return 'customer_id';
  }

  if (change.email) {
    // Backfill the customer id so every later event matches on the fast path.
    const { data, error } = await db
      .from('clients')
      .update({
        stripe_status: change.status,
        ...(change.customerId ? { stripe_customer_id: change.customerId } : {}),
      })
      .ilike('contact_email', change.email)
      .select('id');
    if (error) throw new Error(error.message);
    if ((data ?? []).length > 0) return 'email';
  }

  return 'none';
}

function mapSubscriptionStatus(status: Stripe.Subscription.Status): BillingStatus {
  switch (status) {
    case 'active':
      return 'active';
    case 'trialing':
    case 'incomplete':
      return 'trialing';
    case 'past_due':
    case 'unpaid':
      return 'past_due';
    default:
      return 'canceled';
  }
}

async function customerEmail(stripe: Stripe, customerId: string | null): Promise<string | null> {
  if (!customerId) return null;
  try {
    const customer = await stripe.customers.retrieve(customerId);
    return 'email' in customer ? (customer.email ?? null) : null;
  } catch {
    return null;
  }
}

function idOf(v: string | { id: string } | null | undefined): string | null {
  if (typeof v === 'string') return v;
  return v?.id ?? null;
}
