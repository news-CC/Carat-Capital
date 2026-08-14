import { describe, expect, it } from 'vitest';
import { firstNameOf, parseConsent, scrubRows, type RawRow, type ScrubResult } from '@/lib/scrub';

/** A row that passes every gate, so each test can break exactly one thing. */
function goodRow(overrides: RawRow = {}): RawRow {
  return {
    Name: 'Jane Doe',
    'Phone Number': '(415) 555-0142',
    Email: 'jane@example.com',
    'SMS Consent': 'yes',
    'Last Appointment': '2025-03-04',
    LTV: '$1,234.50',
    ...overrides,
  };
}

/** The invariant that makes the audit numbers trustworthy. */
function expectStatsBalance(result: ScrubResult): void {
  const s = result.stats;
  const droppedSum =
    s.dropped_no_consent +
    s.dropped_suppressed +
    s.dropped_invalid_phone +
    s.dropped_missing_phone +
    s.dropped_duplicate;
  expect(s.kept + droppedSum).toBe(s.total);
  expect(result.kept.length).toBe(s.kept);
  expect(result.dropped.length).toBe(droppedSum);
}

describe('parseConsent', () => {
  it('accepts the affirmative values a salon export uses', () => {
    for (const value of [
      true,
      1,
      '1',
      'true',
      'TRUE',
      ' True ',
      'yes',
      'YES',
      'Y',
      't',
      'granted',
      'Granted',
      'opted_in',
      'Opted In',
      'opt-in',
      'opt_in',
      'consented',
    ]) {
      expect(parseConsent(value), `expected ${String(value)} to be consent`).toBe(true);
    }
  });

  it('rejects everything else, including near-misses', () => {
    for (const value of [
      false,
      0,
      2,
      -1,
      '0',
      'no',
      'N',
      'false',
      'FALSE',
      'f',
      '',
      '   ',
      'maybe',
      'pending',
      'unsubscribed',
      'yes please',
      'opted out',
      null,
      undefined,
      {},
      [],
      ['yes'],
      Number.NaN,
    ]) {
      expect(parseConsent(value), `expected ${String(value)} to be refused`).toBe(false);
    }
  });
});

describe('firstNameOf', () => {
  it('takes the given name out of the shapes exports produce', () => {
    expect(firstNameOf('Jane Doe')).toBe('Jane');
    expect(firstNameOf('  Jane   Q. Doe ')).toBe('Jane');
    expect(firstNameOf('Jane')).toBe('Jane');
    expect(firstNameOf('DOE, JANE')).toBe('Jane');
    expect(firstNameOf('Doe, Jane Q.')).toBe('Jane');
    expect(firstNameOf('Mary-Jane Watson')).toBe('Mary-Jane');
    expect(firstNameOf("O'Brien Sean")).toBe("O'Brien");
  });

  it('title-cases shouting but leaves real casing alone', () => {
    expect(firstNameOf('JANE DOE')).toBe('Jane');
    expect(firstNameOf('McKenna Smith')).toBe('McKenna');
  });

  it('returns null when there is no name', () => {
    expect(firstNameOf(null)).toBeNull();
    expect(firstNameOf(undefined)).toBeNull();
    expect(firstNameOf('')).toBeNull();
    expect(firstNameOf('   ')).toBeNull();
    expect(firstNameOf('123')).toBeNull();
  });
});

describe('scrubRows — GATE 1: consent', () => {
  it('drops rows without consent', () => {
    const result = scrubRows(
      [
        goodRow({ 'SMS Consent': 'no' }),
        goodRow({ 'Phone Number': '415-555-0143', 'SMS Consent': '' }),
        goodRow({ 'Phone Number': '415-555-0144', 'SMS Consent': 'maybe later' }),
      ],
      [],
    );
    expect(result.kept).toHaveLength(0);
    expect(result.stats.dropped_no_consent).toBe(3);
    expect(result.dropped.every((d) => d.reason === 'no_consent')).toBe(true);
    expectStatsBalance(result);
  });

  it('drops a row with no consent column at all', () => {
    const result = scrubRows([{ Name: 'Jane', Phone: '4155550142' }], []);
    expect(result.stats.dropped_no_consent).toBe(1);
  });

  it('keeps consented rows and marks them consent: true', () => {
    const result = scrubRows([goodRow()], []);
    expect(result.kept).toHaveLength(1);
    expect(result.kept[0].consent).toBe(true);
  });

  it('honours requireConsent: false without loosening any other gate', () => {
    const rows = [
      goodRow({ 'SMS Consent': 'no' }),
      goodRow({ 'Phone Number': 'nope', 'SMS Consent': 'no' }),
      goodRow({ 'Phone Number': '415-555-0143', 'SMS Consent': 'no' }),
    ];
    const result = scrubRows(rows, ['+14155550143'], { requireConsent: false });
    expect(result.stats.dropped_no_consent).toBe(0);
    expect(result.stats.dropped_invalid_phone).toBe(1);
    expect(result.stats.dropped_suppressed).toBe(1);
    expect(result.kept).toHaveLength(1);
    expect(result.kept[0].consent).toBe(true);
    expectStatsBalance(result);
  });
});

describe('scrubRows — GATES 2 & 3: phone present and dialable', () => {
  it('separates a missing phone from an unusable one', () => {
    const result = scrubRows(
      [
        goodRow({ 'Phone Number': '' }),
        goodRow({ 'Phone Number': '   ' }),
        goodRow({ 'Phone Number': null }),
        goodRow({ 'Phone Number': '555-0142' }),
        goodRow({ 'Phone Number': '0000000000' }),
        goodRow({ 'Phone Number': 'ask at front desk' }),
        goodRow({ 'Phone Number': '115-555-0142' }),
      ],
      [],
    );
    expect(result.stats.dropped_missing_phone).toBe(3);
    expect(result.stats.dropped_invalid_phone).toBe(4);
    expect(result.kept).toHaveLength(0);
    expectStatsBalance(result);
  });

  it('records the offending value so the operator can fix the sheet', () => {
    const result = scrubRows([goodRow({ 'Phone Number': 'call salon' })], []);
    expect(result.dropped[0]).toMatchObject({ reason: 'invalid_phone', detail: 'call salon' });
  });

  it('stores E.164 in phone and the original string in phone_raw', () => {
    const result = scrubRows([goodRow({ 'Phone Number': ' (415) 555-0142 ' })], []);
    expect(result.kept[0].phone).toBe('+14155550142');
    expect(result.kept[0].phone_raw).toBe('(415) 555-0142');
  });

  it('keeps 555-01XX fiction numbers — the demo list has to dial', () => {
    const result = scrubRows([goodRow({ 'Phone Number': '+14155550100' })], []);
    expect(result.kept).toHaveLength(1);
  });
});

describe('scrubRows — GATE 4: suppression', () => {
  it('drops a suppressed number however it was typed', () => {
    const result = scrubRows(
      [
        goodRow({ 'Phone Number': '(415) 555-0142' }),
        goodRow({ 'Phone Number': '4155550143' }),
        goodRow({ 'Phone Number': '+1 415 555 0144' }),
      ],
      ['+14155550142', '(415) 555-0143', '1-415-555-0144'],
    );
    expect(result.stats.dropped_suppressed).toBe(3);
    expect(result.kept).toHaveLength(0);
    expectStatsBalance(result);
  });

  it('reports the E.164 form as the drop detail', () => {
    const result = scrubRows([goodRow()], ['4155550142']);
    expect(result.dropped[0]).toMatchObject({ reason: 'suppressed', detail: '+14155550142' });
  });

  it('ignores junk entries in the suppression list without dropping good rows', () => {
    const result = scrubRows([goodRow()], ['', '   ', 'not a phone']);
    expect(result.kept).toHaveLength(1);
  });

  it('accepts a Set as the suppression source', () => {
    const result = scrubRows([goodRow()], new Set(['+14155550142']));
    expect(result.stats.dropped_suppressed).toBe(1);
  });
});

describe('scrubRows — GATE 5: dedupe', () => {
  it('dedupes on E.164, not on the string in the cell', () => {
    const result = scrubRows(
      [
        goodRow({ 'Phone Number': '(415) 555-0142' }),
        goodRow({ 'Phone Number': '4155550142' }),
        goodRow({ 'Phone Number': '+1-415-555-0142' }),
        goodRow({ 'Phone Number': '415.555.0142 x99' }),
        goodRow({ 'Phone Number': '415-555-0143' }),
      ],
      [],
    );
    expect(result.kept).toHaveLength(2);
    expect(result.stats.dropped_duplicate).toBe(3);
    expect(result.kept.map((r) => r.phone)).toEqual(['+14155550142', '+14155550143']);
    expectStatsBalance(result);
  });

  it('keeps the first occurrence', () => {
    const result = scrubRows(
      [goodRow({ Name: 'First Winner' }), goodRow({ Name: 'Second Loser' })],
      [],
    );
    expect(result.kept[0].name).toBe('First Winner');
  });
});

describe('scrubRows — gate ordering is fixed', () => {
  it('reports the first failing gate, not the worst one', () => {
    // No consent AND an unusable phone -> no_consent, because consent is gate 1.
    const noConsent = scrubRows([goodRow({ 'SMS Consent': 'no', 'Phone Number': 'junk' })], []);
    expect(noConsent.stats.dropped_no_consent).toBe(1);
    expect(noConsent.stats.dropped_invalid_phone).toBe(0);

    // Suppressed AND duplicated -> suppressed, because suppression is gate 4.
    const suppressedDupe = scrubRows([goodRow(), goodRow()], ['+14155550142']);
    expect(suppressedDupe.stats.dropped_suppressed).toBe(2);
    expect(suppressedDupe.stats.dropped_duplicate).toBe(0);
  });

  it('never counts one row twice', () => {
    const result = scrubRows(
      [
        goodRow(),
        goodRow(),
        goodRow({ 'SMS Consent': 'no' }),
        goodRow({ 'Phone Number': '' }),
        goodRow({ 'Phone Number': 'junk' }),
        goodRow({ 'Phone Number': '415-555-0143' }),
      ],
      ['+14155550143'],
    );
    expect(result.stats).toEqual({
      total: 6,
      kept: 1,
      dropped_no_consent: 1,
      dropped_suppressed: 1,
      dropped_invalid_phone: 1,
      dropped_missing_phone: 1,
      dropped_duplicate: 1,
    });
    expectStatsBalance(result);
  });
});

describe('scrubRows — header tolerance', () => {
  it('reads the header spellings real exports use', () => {
    const result = scrubRows(
      [
        {
          '  Full Name  ': 'jane doe',
          MOBILE: '415-555-0142',
          'E-Mail': ' JANE@EXAMPLE.COM ',
          Opt_In: 'Y',
          'last seen': '3/4/2025',
          'Total Spend': '1,234.50',
        },
      ],
      [],
    );
    expect(result.kept[0]).toEqual({
      name: 'jane doe',
      first_name: 'jane',
      phone: '+14155550142',
      phone_raw: '415-555-0142',
      email: 'jane@example.com',
      consent: true,
      last_visit: '2025-03-04',
      lifetime_value_cents: 123450,
    });
  });

  it('falls through to the next phone alias when the first column is blank', () => {
    const result = scrubRows(
      [{ Phone: '', Cell: '415-555-0142', Consent: 'true' }],
      [],
    );
    expect(result.kept[0].phone).toBe('+14155550142');
  });

  it('prefers an explicit first_name column over splitting the full name', () => {
    const result = scrubRows(
      [goodRow({ Name: 'Doe, Jane', 'First Name': 'Janie' })],
      [],
    );
    expect(result.kept[0].first_name).toBe('Janie');
    expect(result.kept[0].name).toBe('Doe, Jane');
  });

  it('derives first_name when the sheet has only a full name', () => {
    const result = scrubRows([goodRow({ Name: 'DOE, JANE' })], []);
    expect(result.kept[0].first_name).toBe('Jane');
  });
});

describe('scrubRows — field parsing', () => {
  it('normalizes last_visit to ISO or null', () => {
    const cases: [unknown, string | null][] = [
      ['2025-03-04', '2025-03-04'],
      ['2025-03-04T18:30:00.000Z', '2025-03-04'],
      ['3/4/2025', '2025-03-04'],
      ['03/04/2025', '2025-03-04'],
      ['3-4-25', '2025-03-04'],
      [new Date('2025-03-04T12:00:00Z'), '2025-03-04'],
      [45720, '2025-03-04'], // Excel serial
      ['02/31/2025', null], // not a real day
      ['someday', null],
      ['', null],
      [null, null],
      [5, null], // a stray count, not a date
      [{}, null],
    ];
    for (const [input, expected] of cases) {
      const result = scrubRows([goodRow({ 'Last Appointment': input })], []);
      expect(result.kept[0].last_visit, `input ${String(input)}`).toBe(expected);
    }
  });

  it('converts lifetime value to integer cents', () => {
    const cases: [unknown, number | null][] = [
      ['$1,234.50', 123450],
      ['1234.5', 123450],
      [1234.5, 123450],
      ['$0', 0],
      [0, 0],
      ['840', 84000],
      ['$12.345', 1235], // rounds to the cent
      ['n/a', null],
      ['', null],
      [null, null],
      ['-50', null],
      ['(50.00)', null],
      ['1.2.3', null],
    ];
    for (const [input, expected] of cases) {
      const result = scrubRows([goodRow({ LTV: input })], []);
      expect(result.kept[0].lifetime_value_cents, `input ${String(input)}`).toBe(expected);
    }
  });

  it('keeps only plausible emails and lowercases them', () => {
    const cases: [unknown, string | null][] = [
      ['Jane@Example.COM', 'jane@example.com'],
      [' jane+tag@mail.co.uk ', 'jane+tag@mail.co.uk'],
      ['jane@example', null],
      ['jane at example.com', null],
      ['jane@example.com, bob@example.com', null],
      ['', null],
      [null, null],
    ];
    for (const [input, expected] of cases) {
      const result = scrubRows([goodRow({ Email: input })], []);
      expect(result.kept[0].email, `input ${String(input)}`).toBe(expected);
    }
  });
});

describe('scrubRows — degenerate input', () => {
  it('returns zeroed stats for an empty list', () => {
    const result = scrubRows([], []);
    expect(result.stats).toEqual({
      total: 0,
      kept: 0,
      dropped_no_consent: 0,
      dropped_suppressed: 0,
      dropped_invalid_phone: 0,
      dropped_missing_phone: 0,
      dropped_duplicate: 0,
    });
  });

  it('survives empty objects and unexpected value types', () => {
    const result = scrubRows(
      [{}, { Consent: true }, { Consent: true, Phone: {} }, { Consent: true, Phone: 4155550142 }],
      [],
    );
    expect(result.kept).toHaveLength(1);
    expect(result.kept[0].phone).toBe('+14155550142');
    expect(result.kept[0].name).toBeNull();
    expectStatsBalance(result);
  });

  it('does not mutate the caller’s rows', () => {
    const row = goodRow();
    const snapshot = JSON.stringify(row);
    scrubRows([row], ['+14155550142']);
    expect(JSON.stringify(row)).toBe(snapshot);
    expect(scrubRows([row], []).dropped).toHaveLength(0);
  });

  it('hands the original row back on a drop so the UI can show it', () => {
    const row = goodRow({ 'SMS Consent': 'no' });
    const result = scrubRows([row], []);
    expect(result.dropped[0].row).toBe(row);
  });
});
