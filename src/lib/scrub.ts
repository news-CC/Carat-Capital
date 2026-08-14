import { normalizePhone } from '@/lib/phone';

/**
 * THE HARD GATE. Pure, zero I/O, zero env, zero database. Runs in the browser
 * for the upload preview and again on the server against the live suppression
 * table — the server run is the one that decides what gets inserted.
 *
 * Gate order per row is fixed and load-bearing (the audit numbers a client sees
 * depend on it): consent -> phone present -> phone valid -> suppression -> dedupe.
 */

export type RawRow = Record<string, unknown>;

export type DropReason =
  | 'no_consent'
  | 'suppressed'
  | 'invalid_phone'
  | 'missing_phone'
  | 'duplicate'
  // Never a drop: 555-01XX fiction numbers are kept on purpose so the demo list
  // is dialable end to end. Excluded from DroppedRow for exactly that reason.
  | 'fictional_ok';

export type ScrubbedRow = {
  name: string | null;
  first_name: string | null;
  phone: string;
  phone_raw: string | null;
  email: string | null;
  /**
   * What the sheet actually justified — never a claim the source did not make. False only when
   * requireConsent is off and the consent cell was blank, and such a row can never dial: the SQL
   * gate is `c2.consent = true`.
   */
  consent: boolean;
  last_visit: string | null;
  lifetime_value_cents: number | null;
};

export type DroppedRow = {
  row: RawRow;
  reason: Exclude<DropReason, 'fictional_ok'>;
  detail?: string;
};

export type ScrubStats = {
  total: number;
  kept: number;
  dropped_no_consent: number;
  dropped_suppressed: number;
  dropped_invalid_phone: number;
  dropped_missing_phone: number;
  dropped_duplicate: number;
};

export type ScrubResult = { kept: ScrubbedRow[]; dropped: DroppedRow[]; stats: ScrubStats };

/** 'Phone Number', 'phone_number', 'PHONE-NUMBER' all collapse to 'phone_number'. */
function normalizeKey(key: string): string {
  return key
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

/** Priority order matters: the first alias that carries a value wins. */
const FIELD_ALIASES = {
  phone: [
    'phone',
    'phone_number',
    'mobile',
    'mobile_phone',
    'mobile_number',
    'cell',
    'cell_phone',
    'telephone',
    'tel',
    'primary_phone',
    'phone_1',
  ],
  email: ['email', 'e_mail', 'email_address'],
  name: ['name', 'full_name', 'client_name', 'customer', 'customer_name'],
  first_name: ['first_name', 'first', 'fname', 'given_name'],
  consent: ['consent', 'sms_consent', 'opt_in', 'marketing_consent', 'permission'],
  last_visit: ['last_visit', 'last_appointment', 'last_seen', 'last_visit_date'],
  lifetime_value: ['lifetime_value', 'ltv', 'total_spend', 'lifetime_spend'],
} as const satisfies Record<string, readonly string[]>;

type FieldName = keyof typeof FIELD_ALIASES;

function indexRow(row: RawRow): Map<string, unknown> {
  const index = new Map<string, unknown>();
  for (const [key, value] of Object.entries(row)) {
    const normalized = normalizeKey(key);
    // First column wins on duplicate headers ("Phone" twice) — matches Excel's
    // left-to-right reading order.
    if (normalized !== '' && !index.has(normalized)) index.set(normalized, value);
  }
  return index;
}

function pick(index: Map<string, unknown>, field: FieldName): unknown {
  let firstPresent: unknown;
  let seen = false;
  for (const alias of FIELD_ALIASES[field]) {
    if (!index.has(alias)) continue;
    const value = index.get(alias);
    if (!seen) {
      firstPresent = value;
      seen = true;
    }
    if (!isBlank(value)) return value;
  }
  return firstPresent;
}

function isBlank(value: unknown): boolean {
  return value === null || value === undefined || (typeof value === 'string' && value.trim() === '');
}

function asText(value: unknown): string | null {
  if (isBlank(value)) return null;
  if (typeof value === 'string') return value.trim();
  if (typeof value === 'number' || typeof value === 'bigint' || typeof value === 'boolean') {
    return String(value);
  }
  return null;
}

const TRUTHY_CONSENT = new Set([
  '1',
  'true',
  'yes',
  'y',
  't',
  'granted',
  'opted_in',
  'opt_in',
  'consented',
]);

export function parseConsent(v: unknown): boolean {
  if (typeof v === 'boolean') return v;
  if (typeof v === 'number') return v === 1;
  if (typeof v !== 'string') return false;
  // 'Opted In', 'opt-in', ' YES ' all land on a canonical token.
  return TRUTHY_CONSENT.has(normalizeKey(v));
}

/**
 * A written refusal, as opposed to a blank cell. 'f' mirrors the truthy 't' and 'dnc' is
 * unambiguous; both are refusals by any reading of the cell.
 */
const REFUSED_CONSENT = new Set([
  '0',
  'false',
  'f',
  'no',
  'n',
  'opted_out',
  'opt_out',
  'unsubscribed',
  'revoked',
  'stop',
  'do_not_call',
  'dnc',
]);

/**
 * Whether the consent cell says no out loud. Distinct from `!parseConsent(v)`, which is also true
 * for a blank cell or a value nobody can read — a refusal is the only one the operator flag may
 * never override.
 */
export function isConsentRefused(v: unknown): boolean {
  if (typeof v === 'boolean') return !v;
  if (typeof v === 'number') return v === 0;
  if (typeof v !== 'string') return false;
  // 'Opted Out', 'opt-out', 'DO NOT CALL' all land on a canonical token.
  return REFUSED_CONSENT.has(normalizeKey(v));
}

export function firstNameOf(full: string | null | undefined): string | null {
  if (!full) return null;
  let text = full.trim();
  if (text === '') return null;

  // Salon exports love "SMITH, JANE" — the given name is after the comma.
  const comma = text.indexOf(',');
  if (comma > 0) text = text.slice(comma + 1).trim();

  const token = text.split(/\s+/)[0]?.replace(/[^\p{L}\p{M}'’-]/gu, '') ?? '';
  if (token === '') return null;

  // Shouty exports ("JANE") get title-cased; anything already mixed is left alone
  // so "McKenna" survives.
  return token === token.toUpperCase() && token.length > 1
    ? token.charAt(0) + token.slice(1).toLowerCase()
    : token;
}

function parseEmail(value: unknown): string | null {
  const text = asText(value)?.toLowerCase();
  if (!text) return null;
  return /^[^\s@,;]+@[^\s@,;]+\.[a-z]{2,}$/.test(text) ? text : null;
}

/** ISO 'YYYY-MM-DD' or null. Accepts Date, Excel serial, ISO, and M/D/YYYY. */
function parseDate(value: unknown): string | null {
  if (isBlank(value)) return null;

  if (value instanceof Date) return isoOrNull(value);

  if (typeof value === 'number') {
    // Excel serial day count, epoch 1899-12-30. Bounded to 1930..2060 so a
    // stray "5" in a date column does not become a date.
    if (value < 11000 || value > 60000) return null;
    return isoOrNull(new Date(Math.round((value - 25569) * 86400000)));
  }

  const text = asText(value);
  if (!text) return null;

  const iso = /^(\d{4})-(\d{2})-(\d{2})(?:[T\s].*)?$/.exec(text);
  if (iso) return checkedIso(Number(iso[1]), Number(iso[2]), Number(iso[3]));

  const slashed = /^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2}|\d{4})$/.exec(text);
  if (slashed) {
    const year = Number(slashed[3]);
    return checkedIso(
      year < 100 ? (year > 69 ? 1900 + year : 2000 + year) : year,
      Number(slashed[1]), // US ordering: salon software is US software
      Number(slashed[2]),
    );
  }

  const parsed = Date.parse(text);
  return Number.isNaN(parsed) ? null : isoOrNull(new Date(parsed));
}

function checkedIso(year: number, month: number, day: number): string | null {
  if (month < 1 || month > 12 || day < 1 || day > 31 || year < 1900 || year > 2100) return null;
  const date = new Date(Date.UTC(year, month - 1, day));
  if (date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) return null; // 02/31
  return isoOrNull(date);
}

function isoOrNull(date: Date): string | null {
  const time = date.getTime();
  if (Number.isNaN(time)) return null;
  return date.toISOString().slice(0, 10);
}

/**
 * contacts.lifetime_value_cents is int4. A cell past that is a mis-mapped column (an account or
 * loyalty number), not money, so it drops one optional field instead of failing an insert chunk
 * whose earlier siblings have already committed.
 */
const MAX_MONEY_CENTS = 2_147_483_647;

/** '$1,234.50' -> 123450. Dollars in, cents out, or null. */
function parseMoneyCents(value: unknown): number | null {
  if (isBlank(value)) return null;
  if (typeof value === 'number') {
    return Number.isFinite(value) && value >= 0 ? boundedCents(value) : null;
  }
  const text = asText(value);
  if (!text) return null;
  if (/^[(-]/.test(text.trim())) return null; // negative or accounting-negative

  // Currency symbols, letters and thin/normal spaces go; both separators stay, because which one is
  // the decimal point is the whole question. Spaces are only ever grouping ('1 234,50').
  const cleaned = text.replace(/[^0-9.,]/g, '');
  if (cleaned === '') return null;

  const dollars = parseDollars(cleaned);
  return dollars === null ? null : boundedCents(dollars);
}

/**
 * Reads a cleaned number under either convention: the LAST separator present is the decimal point
 * ('1,234.50' and '1.234,50' both mean 1234.50), and a separator that repeats can only be grouping.
 * A single '.' stays the decimal point on the US reading — '12.345' is $12.35, not $12,345 — and so
 * does a single ',' unless it groups three digits, where the US reading wins ('1,234' -> 1234).
 * Anything whose grouping does not hold up returns null: a wrong lifetime value is worse than none,
 * because it is what a client sees in the contacts table.
 */
function parseDollars(cleaned: string): number | null {
  const lastComma = cleaned.lastIndexOf(',');
  const lastDot = cleaned.lastIndexOf('.');
  const commas = (cleaned.match(/,/g) ?? []).length;
  const dots = (cleaned.match(/\./g) ?? []).length;

  let decimal: ',' | '.' | null = null;
  if (lastComma >= 0 && lastDot >= 0) decimal = lastComma > lastDot ? ',' : '.';
  else if (lastComma >= 0) decimal = commas === 1 && !/,\d{3}$/.test(cleaned) ? ',' : null;
  else if (lastDot >= 0) decimal = dots === 1 ? '.' : null;

  const cut = decimal === null ? cleaned.length : cleaned.lastIndexOf(decimal);
  const whole = cleaned.slice(0, cut);
  const fraction = cleaned.slice(cut + 1);
  if (fraction.includes(',') || fraction.includes('.')) return null;
  if (!isGrouped(whole)) return null;

  const digits = whole.replace(/[.,]/g, '');
  if (digits === '' && fraction === '') return null;
  const dollars = Number(`${digits === '' ? '0' : digits}.${fraction === '' ? '0' : fraction}`);
  return Number.isFinite(dollars) ? dollars : null;
}

/** '1234', '1,234', '1.234.567' yes; '1,23', '1.2.3', '12,34,567' no. */
function isGrouped(whole: string): boolean {
  if (!/[.,]/.test(whole)) return /^\d*$/.test(whole);
  const separator = whole.includes(',') ? ',' : '.';
  if (whole.includes(separator === ',' ? '.' : ',')) return false; // two grouping characters
  const groups = whole.split(separator);
  return /^\d{1,3}$/.test(groups[0]) && groups.slice(1).every((group) => /^\d{3}$/.test(group));
}

function boundedCents(dollars: number): number | null {
  const cents = Math.round(dollars * 100);
  return cents >= 0 && cents <= MAX_MONEY_CENTS ? cents : null;
}

/** Suppression list may arrive in any format; we compare on E.164. */
function suppressionSet(phones: Iterable<string>): Set<string> {
  const set = new Set<string>();
  for (const phone of phones) {
    if (typeof phone !== 'string') continue;
    const e164 = normalizePhone(phone);
    if (e164) set.add(e164);
    const trimmed = phone.trim();
    if (trimmed !== '') set.add(trimmed);
  }
  return set;
}

export function scrubRows(
  rows: RawRow[],
  suppressedPhones: Iterable<string>,
  opts?: { requireConsent?: boolean },
): ScrubResult {
  const consentRequired = opts?.requireConsent ?? true;
  const suppressed = suppressionSet(suppressedPhones);
  const seen = new Set<string>();

  const kept: ScrubbedRow[] = [];
  const dropped: DroppedRow[] = [];
  const stats: ScrubStats = {
    total: rows.length,
    kept: 0,
    dropped_no_consent: 0,
    dropped_suppressed: 0,
    dropped_invalid_phone: 0,
    dropped_missing_phone: 0,
    dropped_duplicate: 0,
  };

  const drop = (row: RawRow, reason: DroppedRow['reason'], detail?: string): void => {
    dropped.push(detail === undefined ? { row, reason } : { row, reason, detail });
    if (reason === 'no_consent') stats.dropped_no_consent += 1;
    else if (reason === 'suppressed') stats.dropped_suppressed += 1;
    else if (reason === 'invalid_phone') stats.dropped_invalid_phone += 1;
    else if (reason === 'missing_phone') stats.dropped_missing_phone += 1;
    else stats.dropped_duplicate += 1;
  };

  for (const row of rows) {
    const index = indexRow(row);
    const rawPhone = pick(index, 'phone');

    // GATE 1 — consent. TCPA: no consent, no dial, no exceptions. The flag only exists for lists
    // where consent is evidenced outside the spreadsheet, so it may cover a BLANK or absent cell and
    // nothing else: a cell that says no is a written refusal and no operator setting overrides it.
    const consentCell = pick(index, 'consent');
    const consented = parseConsent(consentCell);
    if (!consented && (consentRequired || isConsentRefused(consentCell))) {
      drop(row, 'no_consent');
      continue;
    }

    // GATE 2 — a phone number has to actually be there.
    if (isBlank(rawPhone)) {
      drop(row, 'missing_phone');
      continue;
    }

    // GATE 3 — it has to be dialable. Unnormalizable means we never store it.
    const phoneRaw = asText(rawPhone) ?? String(rawPhone);
    const phone = normalizePhone(rawPhone);
    if (!phone) {
      drop(row, 'invalid_phone', phoneRaw);
      continue;
    }

    // GATE 4 — global do-not-contact. Checked here and again in SQL at claim time.
    if (suppressed.has(phone) || suppressed.has(phoneRaw)) {
      drop(row, 'suppressed', phone);
      continue;
    }

    // GATE 5 — one row per number per batch, so nobody gets called twice.
    if (seen.has(phone)) {
      drop(row, 'duplicate', phone);
      continue;
    }
    seen.add(phone);

    const name = asText(pick(index, 'name'));
    kept.push({
      name,
      first_name: asText(pick(index, 'first_name')) ?? firstNameOf(name),
      phone,
      phone_raw: phoneRaw,
      email: parseEmail(pick(index, 'email')),
      // The sheet's own answer, stored as given. A row kept on the operator's flag with a blank cell
      // is stored as false rather than relabelled true: the compliance record has to say what the
      // source said, and `c2.consent = true` at claim time keeps such a row from ever dialing.
      consent: consented,
      last_visit: parseDate(pick(index, 'last_visit')),
      lifetime_value_cents: parseMoneyCents(pick(index, 'lifetime_value')),
    });
  }

  stats.kept = kept.length;
  return { kept, dropped, stats };
}
