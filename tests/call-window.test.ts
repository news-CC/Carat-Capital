import { describe, expect, it } from 'vitest';
import {
  isInsideCallWindow,
  localTimeInZone,
  localTimeLabel,
  nextWindowOpenLabel,
} from '@/lib/call-window';

// 18:30 UTC on a summer Saturday: 14:30 in New York (EDT), 00:00 in Kolkata.
const SUMMER = new Date('2026-08-15T18:30:00Z');
const WINTER = new Date('2026-01-15T18:30:00Z');
// 23:30 UTC — after a 09:00-19:00 UTC window has closed for the day.
const EVENING = new Date('2026-08-15T23:30:00Z');

describe('localTimeInZone', () => {
  it('reads wall-clock time in the given zone', () => {
    expect(localTimeInZone('UTC', SUMMER)).toBe('18:30');
    expect(localTimeInZone('America/New_York', SUMMER)).toBe('14:30');
    expect(localTimeInZone('America/Los_Angeles', SUMMER)).toBe('11:30');
  });

  it('follows DST rather than a fixed offset', () => {
    expect(localTimeInZone('America/New_York', WINTER)).toBe('13:30');
  });

  it('renders midnight as 00:00, never 24:00', () => {
    expect(localTimeInZone('Asia/Kolkata', SUMMER)).toBe('00:00');
  });

  it('throws on a timezone that does not exist', () => {
    expect(() => localTimeInZone('Mars/Phobos', SUMMER)).toThrow(RangeError);
  });
});

describe('localTimeLabel', () => {
  it('reads the same clock as localTimeInZone for a real zone', () => {
    expect(localTimeLabel('America/New_York', SUMMER)).toBe('14:30');
  });

  // clients.timezone is free text in the database. One junk row must not 500 an admin page,
  // which is the whole reason this wrapper exists.
  it('never throws on a junk timezone', () => {
    expect(localTimeLabel('Mars/Phobos', SUMMER)).toBe('--:--');
    expect(localTimeLabel('', SUMMER)).toBe('--:--');
    expect(localTimeLabel('Eastern Standard Time', SUMMER)).toBe('--:--');
  });

  it('does not make a junk timezone look dialable', () => {
    // The label degrades; the gate stays shut.
    expect(localTimeLabel('Mars/Phobos', SUMMER)).toBe('--:--');
    expect(isInsideCallWindow('Mars/Phobos', '00:00', '23:59', SUMMER)).toBe(false);
  });
});

describe('isInsideCallWindow', () => {
  it('is true inside the window', () => {
    expect(isInsideCallWindow('America/New_York', '09:00', '19:00', SUMMER)).toBe(true);
  });

  it('is false before it opens and after it closes', () => {
    // 11:30 in Los Angeles: too early for a 13:00 open.
    expect(isInsideCallWindow('America/Los_Angeles', '13:00', '19:00', SUMMER)).toBe(false);
    // 03:30 the next morning in Tokyo: the window is not open at 3am either.
    expect(isInsideCallWindow('Asia/Tokyo', '09:00', '19:00', SUMMER)).toBe(false);
    expect(isInsideCallWindow('UTC', '09:00', '19:00', EVENING)).toBe(false);
  });

  it('is inclusive at both boundaries, matching the SQL between', () => {
    expect(isInsideCallWindow('UTC', '18:30', '19:00', SUMMER)).toBe(true);
    expect(isInsideCallWindow('UTC', '09:00', '18:30', SUMMER)).toBe(true);
    expect(isInsideCallWindow('UTC', '18:31', '19:00', SUMMER)).toBe(false);
    expect(isInsideCallWindow('UTC', '09:00', '18:29', SUMMER)).toBe(false);
  });

  it('fails closed on an invalid timezone — never dial on a bad tz', () => {
    expect(isInsideCallWindow('Mars/Phobos', '00:00', '23:59', SUMMER)).toBe(false);
    expect(isInsideCallWindow('', '00:00', '23:59', SUMMER)).toBe(false);
    expect(isInsideCallWindow('Eastern Standard Time', '00:00', '23:59', SUMMER)).toBe(false);
  });

  it('fails closed on an unparseable or impossible window', () => {
    expect(isInsideCallWindow('UTC', '9am', '7pm', SUMMER)).toBe(false);
    expect(isInsideCallWindow('UTC', '', '', SUMMER)).toBe(false);
    expect(isInsideCallWindow('UTC', '25:00', '26:00', SUMMER)).toBe(false);
    expect(isInsideCallWindow('UTC', '09:60', '19:00', SUMMER)).toBe(false);
    expect(isInsideCallWindow('UTC', '09:00', '19:0', SUMMER)).toBe(false);
  });

  it('handles a window that wraps midnight', () => {
    // 22:00 -> 02:00 with local time 18:30 is outside; 00:00 in Kolkata is inside.
    expect(isInsideCallWindow('UTC', '22:00', '02:00', SUMMER)).toBe(false);
    expect(isInsideCallWindow('Asia/Kolkata', '22:00', '02:00', SUMMER)).toBe(true);
  });

  it('accepts a single-minute window', () => {
    expect(isInsideCallWindow('UTC', '18:30', '18:30', SUMMER)).toBe(true);
    expect(isInsideCallWindow('UTC', '18:29', '18:29', SUMMER)).toBe(false);
  });
});

describe('nextWindowOpenLabel', () => {
  it('says how long is left while open', () => {
    expect(nextWindowOpenLabel('America/New_York', '09:00', '19:00', SUMMER)).toBe(
      'Open until 7:00 PM',
    );
  });

  it('says when it opens today', () => {
    expect(nextWindowOpenLabel('America/Los_Angeles', '13:00', '19:00', SUMMER)).toBe(
      'Opens today 1:00 PM',
    );
  });

  it('says when it opens tomorrow', () => {
    expect(nextWindowOpenLabel('UTC', '09:00', '19:00', EVENING)).toBe('Opens tomorrow 9:00 AM');
  });

  it('treats the small hours as later today, not tomorrow', () => {
    // 03:30 local in Tokyo: the window opens in five and a half hours.
    expect(nextWindowOpenLabel('Asia/Tokyo', '09:00', '19:00', SUMMER)).toBe('Opens today 9:00 AM');
  });

  it('labels midnight and noon without ambiguity', () => {
    expect(nextWindowOpenLabel('UTC', '00:00', '00:30', SUMMER)).toBe('Opens tomorrow 12:00 AM');
    expect(nextWindowOpenLabel('UTC', '12:00', '18:30', SUMMER)).toBe('Open until 6:30 PM');
  });

  it('reports bad configuration instead of guessing', () => {
    expect(nextWindowOpenLabel('Mars/Phobos', '09:00', '19:00', SUMMER)).toBe('Timezone invalid');
    expect(nextWindowOpenLabel('UTC', 'nine', 'seven', SUMMER)).toBe('Window invalid');
  });
});
