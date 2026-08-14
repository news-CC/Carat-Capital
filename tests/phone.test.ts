import { describe, expect, it } from 'vitest';
import { formatPhone, isFictionalPhone, normalizePhone } from '@/lib/phone';

describe('normalizePhone', () => {
  it('normalizes the shapes a salon export actually contains', () => {
    expect(normalizePhone('4155550142')).toBe('+14155550142');
    expect(normalizePhone('(415) 555-0142')).toBe('+14155550142');
    expect(normalizePhone('415.555.0142')).toBe('+14155550142');
    expect(normalizePhone('415 555 0142')).toBe('+14155550142');
    expect(normalizePhone('14155550142')).toBe('+14155550142');
    expect(normalizePhone('1-415-555-0142')).toBe('+14155550142');
    expect(normalizePhone('+1 (415) 555-0142')).toBe('+14155550142');
    expect(normalizePhone('  +14155550142  ')).toBe('+14155550142');
  });

  it('accepts a numeric cell from a spreadsheet', () => {
    expect(normalizePhone(4155550142)).toBe('+14155550142');
  });

  it('drops an extension instead of folding it into the number', () => {
    expect(normalizePhone('415-555-0142 x12')).toBe('+14155550142');
    expect(normalizePhone('(415) 555-0142 ext. 908')).toBe('+14155550142');
    expect(normalizePhone('4155550142 extension 4')).toBe('+14155550142');
  });

  it('keeps a genuine international number', () => {
    expect(normalizePhone('+44 20 7183 8750')).toBe('+442071838750');
    expect(normalizePhone('0044 20 7183 8750')).toBe('+442071838750');
  });

  it('rejects wrong lengths', () => {
    expect(normalizePhone('415555014')).toBeNull(); // 9
    expect(normalizePhone('555-0142')).toBeNull(); // 7
    expect(normalizePhone('+1234567890123456')).toBeNull(); // 16
    expect(normalizePhone('415555014222')).toBeNull(); // 12, no country code written
  });

  it('rejects unassignable NANP area codes and exchanges', () => {
    expect(normalizePhone('015-555-0142')).toBeNull();
    expect(normalizePhone('115-555-0142')).toBeNull();
    expect(normalizePhone('415-055-0142')).toBeNull();
    expect(normalizePhone('415-155-0142')).toBeNull();
    expect(normalizePhone('+1 015 555 0142')).toBeNull();
  });

  it('rejects placeholder junk', () => {
    expect(normalizePhone('0000000000')).toBeNull();
    expect(normalizePhone('5555555555')).toBeNull();
    expect(normalizePhone('1111111111')).toBeNull();
    expect(normalizePhone('9999999999999')).toBeNull();
  });

  it('rejects a bare 12-15 digit number claiming country code 1', () => {
    expect(normalizePhone('+141555501422')).toBeNull();
  });

  it('rejects non-phone input without throwing', () => {
    expect(normalizePhone(null)).toBeNull();
    expect(normalizePhone(undefined)).toBeNull();
    expect(normalizePhone('')).toBeNull();
    expect(normalizePhone('   ')).toBeNull();
    expect(normalizePhone('n/a')).toBeNull();
    expect(normalizePhone('call the salon')).toBeNull();
    expect(normalizePhone({})).toBeNull();
    expect(normalizePhone([])).toBeNull();
    expect(normalizePhone(['4155550142'])).toBeNull();
    expect(normalizePhone(Number.NaN)).toBeNull();
    expect(normalizePhone(true)).toBeNull();
  });

  it('is idempotent — normalizing its own output changes nothing', () => {
    const once = normalizePhone('(415) 555-0142');
    expect(once).not.toBeNull();
    expect(normalizePhone(once)).toBe(once);
    expect(normalizePhone(normalizePhone('+442071838750'))).toBe('+442071838750');
  });
});

describe('formatPhone', () => {
  it('formats US numbers for humans and leaves others alone', () => {
    expect(formatPhone('+14155550142')).toBe('(415) 555-0142');
    expect(formatPhone('+442071838750')).toBe('+442071838750');
    expect(formatPhone('')).toBe('');
  });
});

describe('isFictionalPhone', () => {
  it('recognises the 555-01XX reserved-for-fiction range', () => {
    expect(isFictionalPhone('+14155550100')).toBe(true);
    expect(isFictionalPhone('+14155550142')).toBe(true);
    expect(isFictionalPhone('+14155550199')).toBe(true);
  });

  it('does not claim real-looking numbers are fictional', () => {
    expect(isFictionalPhone('+14155551234')).toBe(false);
    expect(isFictionalPhone('+14155550200')).toBe(false);
    expect(isFictionalPhone('+14155540142')).toBe(false);
    expect(isFictionalPhone('+442071838750')).toBe(false);
  });
});

describe('a written country code is never reinterpreted as NANP', () => {
  // Regression: normalizePhone used to take the 10-digit NANP branch without consulting the
  // leading '+', turning a Norwegian mobile into a real Arkansas number and dialing a stranger.
  it.each([
    ['+47 941 23 456', 'Norway'],
    ['+4794123456', 'Norway, unspaced'],
    ['+45 26 45 67 89', 'Denmark'],
    ['+65 8234 5678', 'Singapore'],
  ])('drops %s (%s) rather than inventing a +1 number', (input) => {
    const out = normalizePhone(input);
    expect(out).toBeNull();
    // The specific catastrophe: silently becoming a dialable NANP number.
    expect(out === null || !out.startsWith('+1')).toBe(true);
  });

  it('still normalizes the same numbers correctly in 00 trunk form', () => {
    expect(normalizePhone('0047 94123456')).toBe('+4794123456');
    expect(normalizePhone('0045 26456789')).toBe('+4526456789');
  });

  it('does not regress plain NANP or +1 NANP', () => {
    expect(normalizePhone('(415) 555-0142')).toBe('+14155550142');
    expect(normalizePhone('415-555-0142')).toBe('+14155550142');
    expect(normalizePhone('+1 (415) 555-0142')).toBe('+14155550142');
    expect(normalizePhone('+14155550142')).toBe('+14155550142');
    expect(normalizePhone('1-415-555-0142')).toBe('+14155550142');
  });

  it('still accepts genuine longer international numbers', () => {
    expect(normalizePhone('+44 20 7183 8750')).toBe('+442071838750');
    expect(normalizePhone('+33 6 12 34 56 78')).toBe('+33612345678');
    expect(normalizePhone('+61 2 9374 4000')).toBe('+61293744000');
  });
});
