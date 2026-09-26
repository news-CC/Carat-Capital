// Calendar arithmetic in the paper's timezone. Carat Capital goes to press at
// 06:00 New York time, so its days start at New York midnight, not UTC's.

const formats = new Map();

function format(tz) {
  let f = formats.get(tz);
  if (!f) {
    f = new Intl.DateTimeFormat('en-CA', {
      timeZone: tz, hourCycle: 'h23',
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit',
    });
    formats.set(tz, f);
  }
  return f;
}

/** Wall-clock parts of the instant `ms` (UTC milliseconds) in `tz`. */
export function wallClock(ms, tz) {
  const p = {};
  for (const { type, value } of format(tz).formatToParts(new Date(ms))) p[type] = value;
  return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour, mi: +p.minute, s: +p.second };
}

const pad = (n) => String(n).padStart(2, '0');

/** YYYY-MM-DD of the instant `ms` in `tz`. */
export function dayOf(ms, tz) {
  const p = wallClock(ms, tz);
  return `${p.y}-${pad(p.m)}-${pad(p.d)}`;
}

/** Local time minus UTC at the instant `ms`, in milliseconds. */
function offset(ms, tz) {
  const p = wallClock(ms, tz);
  return Date.UTC(p.y, p.m - 1, p.d, p.h, p.mi, p.s) - Math.floor(ms / 1000) * 1000;
}

/** UTC milliseconds at which local `day` begins in `tz`. */
export function startOfDay(day, tz) {
  const [y, m, d] = day.split('-').map(Number);
  const guess = Date.UTC(y, m - 1, d);
  const first = guess - offset(guess, tz);
  return guess - offset(first, tz); // the second pass settles daylight-saving edges
}

/** `day` moved by `n` calendar days. */
export function addDays(day, n) {
  const [y, m, d] = day.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, d + n)).toISOString().slice(0, 10);
}

/** [start, end) of local `day` in unix seconds. */
export function dayBounds(day, tz) {
  return [startOfDay(day, tz) / 1000, startOfDay(addDays(day, 1), tz) / 1000];
}

export const isDay = (s) => typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s);
