/**
 * Calling hours in the CLIENT's timezone. Compliance gate: we never dial outside
 * the window, and an unparseable timezone or window fails closed (returns false)
 * rather than defaulting to UTC and calling someone at 4am.
 */

/** @throws RangeError when timeZone is not a valid IANA zone. */
export function localTimeInZone(timeZone: string, at: Date = new Date()): string {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone,
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
  }).formatToParts(at);

  const hour = parts.find((p) => p.type === 'hour')?.value ?? '';
  const minute = parts.find((p) => p.type === 'minute')?.value ?? '';
  if (hour === '' || minute === '') throw new RangeError(`Cannot read local time for ${timeZone}`);

  // Some ICU builds render midnight as "24" under hour12:false.
  return `${hour === '24' ? '00' : hour.padStart(2, '0')}:${minute.padStart(2, '0')}`;
}

function toMinutes(clock: string): number | null {
  const m = /^(\d{1,2}):(\d{2})$/.exec(clock.trim());
  if (!m) return null;
  const hour = Number(m[1]);
  const minute = Number(m[2]);
  if (hour > 23 || minute > 59) return null;
  return hour * 60 + minute;
}

function localMinutes(timeZone: string, at: Date): number | null {
  try {
    return toMinutes(localTimeInZone(timeZone, at));
  } catch {
    return null; // bad timezone -> fail closed
  }
}

export function isInsideCallWindow(
  timeZone: string,
  start: string,
  end: string,
  at: Date = new Date(),
): boolean {
  const from = toMinutes(start);
  const to = toMinutes(end);
  const now = localMinutes(timeZone, at);
  if (from === null || to === null || now === null) return false;

  // Inclusive on both ends, matching the SQL `between` in the claim query.
  return from <= to ? now >= from && now <= to : now >= from || now <= to;
}

/** Short pill copy for the admin UI: 'Open until 7:00 PM', 'Opens tomorrow 9:00 AM'. */
export function nextWindowOpenLabel(
  timeZone: string,
  start: string,
  end: string,
  at: Date = new Date(),
): string {
  const from = toMinutes(start);
  const to = toMinutes(end);
  const now = localMinutes(timeZone, at);
  if (from === null || to === null) return 'Window invalid';
  if (now === null) return 'Timezone invalid';

  if (isInsideCallWindow(timeZone, start, end, at)) return `Open until ${label(to)}`;
  return now < from ? `Opens today ${label(from)}` : `Opens tomorrow ${label(from)}`;
}

function label(minutes: number): string {
  const hour24 = Math.floor(minutes / 60);
  const minute = minutes % 60;
  const suffix = hour24 < 12 ? 'AM' : 'PM';
  const hour12 = hour24 % 12 === 0 ? 12 : hour24 % 12;
  return `${hour12}:${String(minute).padStart(2, '0')} ${suffix}`;
}
