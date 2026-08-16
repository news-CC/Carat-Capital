import { afterEach, describe, expect, it } from 'vitest';
import {
  BUSINESS_TYPES,
  LIST_SIZES,
  SMALLEST_LIST_SIZE,
  StartSchema,
  TIMEZONE_GROUPS,
  firstNameOf,
  isSupportedTimeZone,
  planById,
  recommendPlan,
  recommendationReason,
  verticalFor,
  type BusinessType,
  type ListSize,
} from '@/lib/onboarding';
import { PLANS, bookingCallUrl } from '@/lib/site';

const OFFERED_ZONES = TIMEZONE_GROUPS.flatMap((g) => g.zones.map(([zone]) => zone));

/**
 * The recommendation is what a prospect sees at the moment they are asked for money, so the
 * rules are pinned here rather than left to whoever edits the copy next.
 */
describe('recommendPlan', () => {
  it('sends every vertical to the one-time pilot when the list is the smallest range', () => {
    for (const businessType of BUSINESS_TYPES) {
      expect(recommendPlan({ businessType, listSize: SMALLEST_LIST_SIZE })).toBe('pilot');
    }
  });

  it('matches the vertical once the list is big enough for a subscription', () => {
    const bigEnough: ListSize[] = ['250_1000', '1000_5000', '5000_plus'];
    for (const listSize of bigEnough) {
      expect(recommendPlan({ businessType: 'salon', listSize })).toBe('salon');
      expect(recommendPlan({ businessType: 'medspa', listSize })).toBe('medspa');
      expect(recommendPlan({ businessType: 'multi-location', listSize })).toBe('group');
    }
  });

  it('never recommends a plan that does not exist', () => {
    const ids = new Set(PLANS.map((p) => p.id));
    for (const businessType of BUSINESS_TYPES) {
      for (const listSize of LIST_SIZES) {
        expect(ids.has(recommendPlan({ businessType, listSize }))).toBe(true);
      }
    }
  });

  it('is total: every business type × list size pair produces a recommendation', () => {
    for (const businessType of BUSINESS_TYPES) {
      for (const listSize of LIST_SIZES) {
        expect(typeof recommendPlan({ businessType, listSize })).toBe('string');
      }
    }
  });
});

describe('recommendationReason', () => {
  it('gives a non-empty reason for every combination', () => {
    for (const businessType of BUSINESS_TYPES) {
      for (const listSize of LIST_SIZES) {
        expect(recommendationReason({ businessType, listSize }).length).toBeGreaterThan(20);
      }
    }
  });

  it('explains the pilot, not the vertical, when the smallest list wins', () => {
    // A med spa with a tiny list is recommended the pilot; the reason must talk about the pilot
    // rather than about med spa recall, or the screen contradicts itself.
    const reason = recommendationReason({
      businessType: 'medspa',
      listSize: SMALLEST_LIST_SIZE,
    });
    expect(reason).toMatch(/pilot/i);
  });
});

describe('planById', () => {
  it('resolves each recommendation to a real, priced plan', () => {
    for (const businessType of BUSINESS_TYPES) {
      for (const listSize of LIST_SIZES) {
        const plan = planById(recommendPlan({ businessType, listSize }));
        expect(plan.priceLabel).toMatch(/^\$[\d,]+$/);
        expect(plan.features.length).toBeGreaterThan(0);
      }
    }
  });
});

/**
 * The database has exactly two verticals. A multi-location group must not widen that column by
 * accident — the operator email carries the real answer instead.
 */
describe('verticalFor', () => {
  it('maps the three business types onto the two the schema has', () => {
    expect(verticalFor('salon')).toBe('salon');
    expect(verticalFor('medspa')).toBe('medspa');
    expect(verticalFor('multi-location')).toBe('salon');
  });

  it('only ever returns a value the clients.vertical check constraint accepts', () => {
    const allowed = new Set(['salon', 'medspa']);
    for (const businessType of BUSINESS_TYPES) {
      expect(allowed.has(verticalFor(businessType))).toBe(true);
    }
  });
});

describe('isSupportedTimeZone', () => {
  it('accepts every zone offered in the form', () => {
    for (const zone of OFFERED_ZONES) {
      expect(isSupportedTimeZone(zone)).toBe(true);
    }
  });

  it('rejects a made-up zone rather than throwing', () => {
    expect(isSupportedTimeZone('Mars/Olympus_Mons')).toBe(false);
    expect(isSupportedTimeZone('')).toBe(false);
    expect(isSupportedTimeZone('EST5EDT_TYPO')).toBe(false);
  });
});

describe('firstNameOf', () => {
  it('takes the first word', () => {
    expect(firstNameOf('Renée Alvarez')).toBe('Renée');
    expect(firstNameOf('  Dana  Okonkwo ')).toBe('Dana');
    expect(firstNameOf('Cher')).toBe('Cher');
  });

  it('falls back to a neutral greeting rather than an empty one', () => {
    expect(firstNameOf('')).toBe('there');
    expect(firstNameOf('   ')).toBe('there');
  });
});

/** The public endpoint's only gate. Every field is capped and every rejection is a message. */
describe('StartSchema', () => {
  const valid = {
    salon_name: 'Ridgeline Hair',
    contact_name: 'Renée Alvarez',
    contact_email: 'renee@ridgeline.example',
    contact_phone: '(415) 555-0142',
    business_type: 'salon' as BusinessType,
    timezone: 'America/Los_Angeles',
    list_size: '250_1000' as ListSize,
    avg_ticket_dollars: 120,
    offer_text: 'A complimentary gloss with your next cut.',
  };

  it('accepts a complete, ordinary submission', () => {
    expect(StartSchema.safeParse(valid).success).toBe(true);
  });

  it('rejects a timezone the dialer could not evaluate', () => {
    // A zone the dialer cannot read fails closed and never dials, so it must never be stored.
    const result = StartSchema.safeParse({ ...valid, timezone: 'Pacific/Atlantis' });
    expect(result.success).toBe(false);
  });

  it('rejects a business type outside the three offered', () => {
    expect(StartSchema.safeParse({ ...valid, business_type: 'barbershop' }).success).toBe(false);
  });

  it('rejects a list size outside the four ranges', () => {
    expect(StartSchema.safeParse({ ...valid, list_size: 'loads' }).success).toBe(false);
  });

  it('rejects a ticket that is not whole dollars in range', () => {
    expect(StartSchema.safeParse({ ...valid, avg_ticket_dollars: 120.5 }).success).toBe(false);
    expect(StartSchema.safeParse({ ...valid, avg_ticket_dollars: 0 }).success).toBe(false);
    expect(StartSchema.safeParse({ ...valid, avg_ticket_dollars: 9_000 }).success).toBe(false);
    expect(StartSchema.safeParse({ ...valid, avg_ticket_dollars: Number.NaN }).success).toBe(false);
  });

  it('rejects malformed email addresses', () => {
    for (const contact_email of ['renee', 'renee@', '@ridgeline.example', 'renee@ridgeline']) {
      expect(StartSchema.safeParse({ ...valid, contact_email }).success).toBe(false);
    }
  });

  it('caps every free-text field so nothing unbounded reaches the database', () => {
    expect(StartSchema.safeParse({ ...valid, salon_name: 'x'.repeat(121) }).success).toBe(false);
    expect(StartSchema.safeParse({ ...valid, contact_name: 'x'.repeat(121) }).success).toBe(false);
    expect(StartSchema.safeParse({ ...valid, offer_text: 'x'.repeat(401) }).success).toBe(false);
    expect(StartSchema.safeParse({ ...valid, contact_phone: '1'.repeat(41) }).success).toBe(false);
  });

  it('rejects an offer too short to be worth saying out loud', () => {
    expect(StartSchema.safeParse({ ...valid, offer_text: '20% off' }).success).toBe(false);
  });

  it('reports the offending field so the form can highlight it', () => {
    const result = StartSchema.safeParse({ ...valid, salon_name: 'R' });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].path[0]).toBe('salon_name');
      expect(result.error.issues[0].message.length).toBeGreaterThan(0);
    }
  });
});

/**
 * Every "book a call" on the site, in the funnel and in the confirmation email resolves through
 * this one function. It was pointed at cal.com/startup25/salon-malone — an event type that does
 * not exist — so every booking CTA on a live, paid site landed on a 404. These pin the repair.
 */
describe('bookingCallUrl', () => {
  const CANONICAL = 'https://cal.com/startup25';
  const original = process.env.NEXT_PUBLIC_BOOKING_CALL_URL;

  afterEach(() => {
    if (original === undefined) delete process.env.NEXT_PUBLIC_BOOKING_CALL_URL;
    else process.env.NEXT_PUBLIC_BOOKING_CALL_URL = original;
  });

  const set = (value: string | undefined) => {
    if (value === undefined) delete process.env.NEXT_PUBLIC_BOOKING_CALL_URL;
    else process.env.NEXT_PUBLIC_BOOKING_CALL_URL = value;
  };

  it('is the canonical calendar when nothing is configured', () => {
    set(undefined);
    expect(bookingCallUrl()).toBe(CANONICAL);
    set('   ');
    expect(bookingCallUrl()).toBe(CANONICAL);
  });

  it('collapses the dead sub-path back to the calendar, however it is written', () => {
    for (const dead of [
      'https://cal.com/startup25/salon-malone',
      'https://www.cal.com/startup25/salon-malone',
      'https://cal.com/startup25/15min',
      'https://cal.com/startup25/anything/deeper',
      'https://CAL.COM/startup25/Salon-Malone',
    ]) {
      set(dead);
      expect(bookingCallUrl()).toBe(CANONICAL);
    }
  });

  it('accepts the canonical URL unchanged', () => {
    set(CANONICAL);
    expect(bookingCallUrl()).toBe(CANONICAL);
  });

  it('still lets the environment point at a different scheduler entirely', () => {
    set('https://calendly.com/easecase/15min');
    expect(bookingCallUrl()).toBe('https://calendly.com/easecase/15min');
    // A different cal.com handle is somebody else's calendar, not our dead sub-path.
    set('https://cal.com/someone-else/intro');
    expect(bookingCallUrl()).toBe('https://cal.com/someone-else/intro');
  });

  it('refuses anything that is not an https URL', () => {
    for (const bad of ['http://cal.com/startup25', 'cal.com/startup25', 'javascript:alert(1)', 'not a url']) {
      set(bad);
      expect(bookingCallUrl()).toBe(CANONICAL);
    }
  });

  it('never returns a URL containing the dead event-type slug', () => {
    for (const value of [undefined, 'https://cal.com/startup25/salon-malone', CANONICAL]) {
      set(value);
      expect(bookingCallUrl()).not.toContain('salon-malone');
    }
  });
});
