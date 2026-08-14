/**
 * Phone normalization. Pure, no I/O — safe in the browser.
 * Everything we store or dial is E.164. A number we cannot normalize is never
 * dialled: contacts.phone stays NULL and the row is dropped by the scrub.
 */

/** "x123", "ext 4", "extension 12" — digits we must not fold into the number. */
const EXTENSION_RE = /\s*(?:,|;|#|x|ext\.?|extension)\s*\d+\s*$/i;

const NANP_RE = /^([2-9]\d{2})([2-9]\d{2})(\d{4})$/;

export function normalizePhone(raw: unknown): string | null {
  if (raw === null || raw === undefined) return null;
  if (typeof raw !== 'string' && typeof raw !== 'number' && typeof raw !== 'bigint') return null;
  if (typeof raw === 'number' && !Number.isFinite(raw)) return null;

  const text = String(raw).trim().replace(EXTENSION_RE, '');
  if (text === '') return null;

  const hadPlus = text.startsWith('+') || text.startsWith('00');
  const digits = text.replace(/\D/g, '');
  if (digits.length < 10 || digits.length > 15) return null;
  if (/^(\d)\1+$/.test(digits)) return null; // 0000000000, 5555555555 — placeholder junk

  if (digits.length === 10) return nanp(digits);
  if (digits.length === 11 && digits.startsWith('1')) return nanp(digits.slice(1));

  // International: only trust it when the caller actually wrote a country code.
  if (!hadPlus) return null;
  const intl = digits.startsWith('00') ? digits.slice(2) : digits;
  if (intl.length < 8 || intl.length > 15 || intl.startsWith('0')) return null;
  if (intl.startsWith('1')) return null; // country code 1 is NANP: it is 11 digits or it is wrong
  return `+${intl}`;
}

/** Rejects area codes and exchanges starting 0 or 1 — not assignable in NANP. */
function nanp(ten: string): string | null {
  return NANP_RE.test(ten) ? `+1${ten}` : null;
}

export function formatPhone(e164: string): string {
  const m = /^\+1(\d{3})(\d{3})(\d{4})$/.exec(e164);
  return m ? `(${m[1]}) ${m[2]}-${m[3]}` : e164;
}

/**
 * 555-0100 through 555-0199 is reserved for fiction. All demo and seed data
 * lives here so a stray campaign can never reach a real person.
 */
export function isFictionalPhone(e164: string): boolean {
  return /^\+1\d{3}55501\d{2}$/.test(e164);
}
