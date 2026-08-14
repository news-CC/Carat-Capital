#!/usr/bin/env node
/**
 * Creates the four Salon Malone products, their prices and their payment links.
 *
 * Idempotent. Every object is looked up by its `sm_sku` metadata key before anything is created, so
 * re-running this never duplicates a product, a price or a link. Safe to run on every deploy.
 *
 * Usage:
 *   npm run setup:stripe                 # node --env-file=.env.local scripts/setup-stripe.mjs
 *   npm run setup:stripe -- --dry-run    # report what would change, write nothing
 *
 * Reads STRIPE_SECRET_KEY from the environment. The key is never printed.
 */
import Stripe from 'stripe';

const DRY_RUN = process.argv.includes('--dry-run');

const CATALOG = [
  {
    sku: 'sm_salon_399',
    envKey: 'STRIPE_LINK_SALON_399',
    name: 'Salon Malone — Salon',
    description:
      'Win-back calling for one salon. Malone calls your lapsed, consented clients, books them into real slots, and emails you the moment one lands. Friday report every week.',
    amount: 39900,
    interval: 'month',
  },
  {
    sku: 'sm_medspa_999',
    envKey: 'STRIPE_LINK_MEDSPA_999',
    name: 'Salon Malone — Med Spa',
    description:
      'Win-back calling for one med spa. Higher ticket, longer list, same machinery: consent-gated calls, spoken bookings, instant alerts, weekly recovered-revenue report.',
    amount: 99900,
    interval: 'month',
  },
  {
    sku: 'sm_group_2499',
    envKey: 'STRIPE_LINK_GROUP_2499',
    name: 'Salon Malone — Group',
    description:
      'Win-back calling across a group of locations. Every location gets its own offer, timezone, calling window and Friday report.',
    amount: 249900,
    interval: 'month',
  },
  {
    sku: 'sm_pilot_299',
    envKey: 'STRIPE_LINK_PILOT_299',
    name: 'Salon Malone — Pilot',
    description:
      'One paid pilot campaign against one list. You see the calls, the bookings and the recovered revenue before committing to a month.',
    amount: 29900,
    interval: null, // one-time
  },
];

const secretKey = process.env.STRIPE_SECRET_KEY;
if (!secretKey) {
  console.error('STRIPE_SECRET_KEY is not set.');
  console.error('Run through npm so the env file is loaded:  npm run setup:stripe');
  process.exit(1);
}
const LIVE = !/^(sk|rk)_test_/.test(secretKey);
const stripe = new Stripe(secretKey);

const money = (cents) => `$${(cents / 100).toLocaleString('en-US')}`;
const label = (item) => `${money(item.amount)}${item.interval ? `/${item.interval}` : ' one-time'}`;

/**
 * Lookup by metadata. Search is indexed but lags writes by up to a minute, so a bounded scan of
 * recent products backs it up — otherwise two runs in quick succession would duplicate everything.
 */
async function findProduct(sku) {
  try {
    const found = await stripe.products.search({ query: `metadata['sm_sku']:'${sku}'`, limit: 1 });
    if (found.data.length > 0) return found.data[0];
  } catch {
    // Search unavailable on this account; the scan below is authoritative anyway.
  }
  let checked = 0;
  for await (const product of stripe.products.list({ limit: 100 })) {
    if (product.metadata?.sm_sku === sku) return product;
    if (++checked >= 300) break;
  }
  return null;
}

async function findPrice(productId, amount, interval) {
  for await (const price of stripe.prices.list({ product: productId, active: true, limit: 100 })) {
    if (price.unit_amount !== amount || price.currency !== 'usd') continue;
    if (interval) {
      if (price.recurring?.interval === interval && price.recurring?.interval_count === 1) return price;
    } else if (!price.recurring) {
      return price;
    }
  }
  return null;
}

async function findPaymentLink(sku) {
  for await (const link of stripe.paymentLinks.list({ limit: 100 })) {
    if (link.metadata?.sm_sku === sku) return link;
  }
  return null;
}

/**
 * Whether an existing link already sells exactly this price at quantity 1.
 * The link's own line items are the authority, not its metadata — links created by earlier tooling
 * carry no `sm_price`, and trusting metadata alone would retire perfectly good live URLs on every run.
 */
async function linkSellsPrice(link, priceId) {
  if (link.metadata?.sm_price === priceId) return true;
  const items = await stripe.paymentLinks.listLineItems(link.id, { limit: 2 });
  return items.data.length === 1 && items.data[0].price?.id === priceId && items.data[0].quantity === 1;
}

function paymentLinkParams(item, priceId) {
  const recurring = Boolean(item.interval);
  return {
    // Quantity is locked: one salon, one subscription. Nobody buys "3 of these" by accident.
    line_items: [{ price: priceId, quantity: 1, adjustable_quantity: { enabled: false } }],
    metadata: { sm_sku: item.sku, sm_price: priceId },
    allow_promotion_codes: true,
    billing_address_collection: 'auto',
    // Checkout always collects the buyer's email. The business name is what we cannot get for free,
    // and it is how the Stripe webhook matches a payment to a row in `clients`.
    custom_fields: [
      {
        key: 'businessname',
        label: { type: 'custom', custom: 'Salon or med spa name' },
        type: 'text',
        optional: false,
      },
    ],
    after_completion: {
      type: 'hosted_confirmation',
      hosted_confirmation: {
        custom_message:
          "You're in. We'll email you within one business day to collect your offer wording and your client list.",
      },
    },
    ...(recurring
      ? { subscription_data: { metadata: { sm_sku: item.sku } } }
      : // One-time payments do not create a customer unless asked, and without a customer id the
        // webhook has nothing durable to match on.
        { customer_creation: 'always' }),
  };
}

async function provision(item) {
  const notes = [];

  let product = await findProduct(item.sku);
  if (product) {
    notes.push(`product exists ${product.id}`);
    if (!DRY_RUN && (product.name !== item.name || product.description !== item.description)) {
      product = await stripe.products.update(product.id, {
        name: item.name,
        description: item.description,
        metadata: { ...product.metadata, sm_sku: item.sku },
      });
      notes.push('product copy updated');
    }
  } else if (DRY_RUN) {
    notes.push('would CREATE product');
    return { item, notes, url: null };
  } else {
    product = await stripe.products.create({
      name: item.name,
      description: item.description,
      metadata: { sm_sku: item.sku },
    });
    notes.push(`product CREATED ${product.id}`);
  }

  let price = await findPrice(product.id, item.amount, item.interval);
  if (price) {
    notes.push(`price exists ${price.id}`);
  } else if (DRY_RUN) {
    notes.push(`would CREATE price ${label(item)}`);
    return { item, notes, url: null };
  } else {
    price = await stripe.prices.create({
      product: product.id,
      currency: 'usd',
      unit_amount: item.amount,
      ...(item.interval ? { recurring: { interval: item.interval } } : {}),
      metadata: { sm_sku: item.sku },
    });
    await stripe.products.update(product.id, { default_price: price.id });
    notes.push(`price CREATED ${price.id} (${label(item)})`);
  }

  let link = await findPaymentLink(item.sku);
  if (link && link.active && (await linkSellsPrice(link, price.id))) {
    notes.push(`link exists ${link.id}`);
    if (!DRY_RUN && link.metadata?.sm_price !== price.id) {
      // Backfill so the next run takes the fast path instead of re-reading line items.
      await stripe.paymentLinks.update(link.id, { metadata: { ...link.metadata, sm_sku: item.sku, sm_price: price.id } });
      notes.push('metadata backfilled');
    }
    return { item, notes, url: link.url };
  }

  if (DRY_RUN) {
    notes.push(link ? 'would REPLACE payment link (price changed)' : 'would CREATE payment link');
    return { item, notes, url: link?.url ?? null };
  }

  if (link) {
    // A payment link's price is immutable, so a price change means a new link. Retire the old one
    // rather than leaving a live URL that charges the wrong amount.
    await stripe.paymentLinks.update(link.id, { active: false });
    notes.push(`old link ${link.id} DEACTIVATED`);
  }
  link = await stripe.paymentLinks.create(paymentLinkParams(item, price.id));
  notes.push(`link CREATED ${link.id}`);
  return { item, notes, url: link.url };
}

async function main() {
  console.log('');
  console.log(`SALON MALONE — Stripe setup   [${LIVE ? 'LIVE MODE' : 'TEST MODE'}]${DRY_RUN ? '   (dry run — nothing will be written)' : ''}`);
  if (LIVE && !DRY_RUN) console.log('This is a live-mode key. Real payment links, real charges.');
  console.log('');

  const results = [];
  let failed = 0;

  for (const item of CATALOG) {
    process.stdout.write(`${item.sku.padEnd(16)} ${label(item).padEnd(14)} `);
    try {
      const result = await provision(item);
      results.push(result);
      console.log(result.notes.join(' · '));
    } catch (e) {
      failed += 1;
      console.log(`FAILED — ${e instanceof Error ? e.message : e}`);
    }
  }

  const urls = results.filter((r) => r.url);
  console.log('');

  if (urls.length > 0) {
    console.log('─'.repeat(78));
    console.log('Paste into .env.local, and into Vercel → Settings → Environment Variables.');
    console.log('Both forms are needed: the server copy for reference, the NEXT_PUBLIC_ copy because');
    console.log('the pricing buttons on the marketing page are rendered in the browser.');
    console.log('─'.repeat(78));
    console.log('');
    for (const { item, url } of urls) {
      console.log(`${item.envKey}=${url}`);
      console.log(`NEXT_PUBLIC_${item.envKey}=${url}`);
    }
    console.log('');
  }

  if (!DRY_RUN) {
    console.log('Next: point the Stripe webhook at the deployed app.');
    console.log('  Stripe dashboard → Developers → Webhooks → Add endpoint');
    console.log('  URL     https://<your-domain>/api/stripe/webhook');
    console.log('  Events  checkout.session.completed, customer.subscription.updated,');
    console.log('          customer.subscription.deleted, invoice.payment_failed');
    console.log('  Copy the signing secret into STRIPE_WEBHOOK_SECRET.');
    console.log('');
  }

  if (failed > 0) {
    console.error(`${failed} of ${CATALOG.length} products failed. Fix the errors above and re-run — the ones that succeeded will be reused, not duplicated.`);
    process.exit(1);
  }
}

main().catch((e) => {
  console.error('setup:stripe failed:', e instanceof Error ? e.message : e);
  process.exit(1);
});
