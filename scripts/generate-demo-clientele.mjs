#!/usr/bin/env node
/**
 * Generates the demo clientele workbook used to show the scrub gates working.
 *
 * EVERY ROW IS SYNTHETIC. No real person, no real phone, no real email.
 * Phone numbers are all +1 (XXX) 555-01NN — the range reserved for fiction (NANP 555-0100..555-0199),
 * which is not routable. The area codes are real, the numbers are not dialable. Emails are @example.com,
 * which RFC 2606 reserves for documentation.
 *
 * Deterministic: seeded PRNG, no Math.random. Re-running produces byte-identical row data.
 *
 * Writes:
 *   demo/salon-malone-demo-clientele.xlsx   (sheet 'Clientele' + sheet 'READ ME')
 *   demo/salon-malone-demo-clientele.csv    (same rows, for CSV-path testing)
 *   demo/upload-template.csv                (empty-ish template with the headers the parser expects)
 *
 * Usage: node scripts/generate-demo-clientele.mjs
 */
import * as XLSX from 'xlsx';
import * as fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

XLSX.set_fs(fs);

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DEMO_DIR = join(ROOT, 'demo');

const TOTAL = 250;
const SEED = 0x5a10e;
/** Fixed "today" so last_visit dates never drift between runs. */
const BASE_DATE = new Date('2026-08-01T00:00:00Z');

/**
 * The demo workbook deliberately omits first_name so the upload exercises deriving it from `name`.
 * The blank template offers the full column set — it must stay equal to UPLOAD_TEMPLATE_HEADERS in
 * src/lib/parse-sheet.ts, which is what the app documents as a well-formed upload.
 */
const HEADERS = ['name', 'phone', 'email', 'consent', 'last_visit', 'lifetime_value'];
const TEMPLATE_HEADERS = ['name', 'first_name', 'phone', 'email', 'consent', 'last_visit', 'lifetime_value'];

// Exact row composition. These numbers ARE the expected scrub outcome printed at the end.
const COMPOSITION = { ok: 206, no_consent: 34, invalid_phone: 7, duplicate: 2, missing_phone: 1 };

// ── deterministic PRNG ────────────────────────────────────────────────────────
function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rnd = mulberry32(SEED);
const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
const int = (min, max) => min + Math.floor(rnd() * (max - min + 1));
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── pools ─────────────────────────────────────────────────────────────────────
const FIRST_NAMES = [
  'Dana', 'Priya', 'Marcus', 'Yolanda', 'Tessa', 'Omar', 'Bianca', 'Curtis', 'Noelle', 'Rashida',
  'Devon', 'Marisol', 'Hollis', 'Junie', 'Kwame', 'Simone', 'Arturo', 'Delphine', 'Reggie', 'Imani',
  'Sloane', 'Ezra', 'Camille', 'Bo', 'Lucinda', 'Trey', 'Anneke', 'Vaughn', 'Neveah', 'Isadora',
  'Roscoe', 'Paloma', 'Wendell', 'Cleo', 'Amara', 'Fitz', 'Nadia', 'Sterling', 'Odette', 'Rufus',
  'Thandiwe', 'Gil', 'Marguerite', 'Ozzie', 'Sunniva', 'Elias', 'Lark', 'Cyrus', 'Delia', 'Winston',
  'Zelda', 'Ignacio', 'Birdie', 'Malachi', 'Rosalind', 'Dex', 'Perpetua', 'Silas', 'Verity', 'Otis',
];
const LAST_NAMES = [
  'Ashgrove', 'Petrakis', 'Vandermeer', 'Okonjo', 'Lindqvist', 'Bellweather', 'Marchetti', 'Ferrante',
  'Whitlock', 'Adebayo', 'Cavanaugh', 'Rosenblum', 'Thibodeaux', 'Nakamura', 'Delacroix', 'Farrow',
  'Osei', 'Kowalczyk', 'Brightwater', 'Santamaria', 'Halloran', 'Ivanković', 'Prewitt', 'Achebe',
  'Fontaine', 'Sandoval', 'Quillen', 'Bergström', 'Mwangi', 'Castellano', 'Ravensworth', 'Dupree',
  'Yildirim', 'Colefax', 'Abernathy', 'Solano', 'Kirkbride', 'Nwachukwu', 'Larkspur', 'Beaumont',
  'Trevino', 'Haverford', 'Okafor', 'Winterbourne', 'Sarkissian', 'Mendelsohn', 'Grayling', 'Boateng',
  'Fairweather', 'Zamora',
];
const AREA_CODES = ['212', '213', '305', '312', '404', '415', '512', '617', '702', '786'];

/** Every one of these must map to true through parseConsent(). */
const CONSENT_TRUE = ['TRUE', 'TRUE', 'true', 'yes', 'yes', 'Yes', 'Y', 'y', '1', 't', 'granted', 'opted_in', 'opt_in', 'consented'];
/** Every one of these must map to false — including the empty string. */
const CONSENT_FALSE = ['FALSE', 'false', 'no', 'No', 'N', '0', '', '', 'pending', 'unknown'];

/**
 * Phones that must fail normalizePhone(). Chosen so none could be mistaken for a real line:
 * too short, area code or exchange starting 0/1, all-same digits, or not a number at all.
 */
const MALFORMED_PHONES = [
  '555-0142',
  '(015) 555-0133',
  '1155550117',
  '0000000000',
  'no phone on file',
  '415-555-01',
  '415) 5550',
];

// ── field builders ────────────────────────────────────────────────────────────
const usedPhones = new Set();
/** Reserved-for-fiction only: exchange is always 555, line is always 01NN. */
function freshFictionPhone() {
  for (;;) {
    const digits = `${pick(AREA_CODES)}55501${String(int(0, 99)).padStart(2, '0')}`;
    if (!usedPhones.has(digits)) {
      usedPhones.add(digits);
      return digits;
    }
  }
}
/** Presentation variants, so the parser's normalizer gets exercised. All normalize to +1 + digits. */
function formatPhoneRaw(digits) {
  const a = digits.slice(0, 3);
  const b = digits.slice(3, 6);
  const c = digits.slice(6);
  switch (int(0, 6)) {
    case 0: return `(${a}) ${b}-${c}`;
    case 1: return `${a}-${b}-${c}`;
    case 2: return `${a}.${b}.${c}`;
    case 3: return `+1 ${a} ${b} ${c}`;
    case 4: return digits;
    case 5: return `1-${a}-${b}-${c}`;
    default: return `  (${a}) ${b}-${c} `;
  }
}

function lastVisit() {
  // Lapsed clientele: 8 to 30 months since the last appointment.
  const d = new Date(BASE_DATE.getTime() - int(240, 900) * 86400000);
  const y = d.getUTCFullYear();
  const m = d.getUTCMonth();
  const day = d.getUTCDate();
  const p2 = (n) => String(n).padStart(2, '0');
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  switch (int(0, 6)) {
    case 0: return `${y}-${p2(m + 1)}-${p2(day)}`;
    case 1: return `${p2(m + 1)}/${p2(day)}/${y}`;
    case 2: return `${day} ${MON[m]} ${y}`;
    case 3: return `${y}/${p2(m + 1)}/${p2(day)}`;
    case 4: return `${MON[m]} ${day}, ${y}`;
    case 5: return `${p2(m + 1)}/${p2(day)}/${String(y).slice(2)}`;
    default: return '';
  }
}

function lifetimeValue() {
  const dollars = int(45, 4200);
  switch (int(0, 5)) {
    case 0: return `$${dollars.toLocaleString('en-US')}.${String(int(0, 99)).padStart(2, '0')}`;
    case 1: return `$${dollars.toLocaleString('en-US')}`;
    case 2: return `${dollars}.${String(int(0, 9))}`;
    case 3: return dollars.toLocaleString('en-US');
    case 4: return '';
    default: return '0';
  }
}

function person() {
  const first = pick(FIRST_NAMES);
  const last = pick(LAST_NAMES);
  return { name: `${first} ${last}`, first, last };
}
function emailFor(p) {
  if (int(0, 11) === 0) return ''; // a few blanks — email is not a gate
  const slug = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z]/g, '');
  const tail = int(0, 2) === 0 ? String(int(2, 99)) : '';
  return `${slug(p.first)}.${slug(p.last)}${tail}@example.com`;
}

// ── build the rows ────────────────────────────────────────────────────────────
const roles = shuffle([
  ...Array(COMPOSITION.ok).fill('ok'),
  ...Array(COMPOSITION.no_consent).fill('no_consent'),
  ...Array(COMPOSITION.invalid_phone).fill('invalid_phone'),
  ...Array(COMPOSITION.missing_phone).fill('missing_phone'),
  ...Array(COMPOSITION.duplicate).fill('duplicate'),
]);

const rows = [];
const keptDigits = []; // valid+consented phones, the pool the deliberate duplicates copy from
let malformedIdx = 0;

for (const role of roles) {
  const p = person();
  let phone;
  let consent;

  switch (role) {
    case 'ok': {
      const digits = freshFictionPhone();
      keptDigits.push(digits);
      phone = formatPhoneRaw(digits);
      consent = pick(CONSENT_TRUE);
      break;
    }
    case 'no_consent':
      // Consent is the first gate, so these are dropped regardless of how good the phone is.
      phone = formatPhoneRaw(freshFictionPhone());
      consent = pick(CONSENT_FALSE);
      break;
    case 'invalid_phone':
      phone = MALFORMED_PHONES[malformedIdx++ % MALFORMED_PHONES.length];
      consent = pick(CONSENT_TRUE);
      break;
    case 'missing_phone':
      phone = '';
      consent = pick(CONSENT_TRUE);
      break;
    case 'duplicate':
      phone = null; // resolved in a second pass, once keptDigits is fully populated
      consent = pick(CONSENT_TRUE);
      break;
    default:
      throw new Error(`unknown role ${role}`);
  }

  rows.push({ role, name: p.name, phone, email: emailFor(p), consent, last_visit: lastVisit(), lifetime_value: lifetimeValue() });
}

// Two duplicate phones, for the two reasons salon exports actually contain them: the same guest
// recorded once with a middle initial and once without, and a household sharing one number.
// Dedupe keeps whichever row comes first, so both spellings must be a usable name on their own.
const dupTargets = [keptDigits[17], keptDigits[131]];
let dupIdx = 0;
for (const row of rows) {
  if (row.role !== 'duplicate') continue;
  const digits = dupTargets[dupIdx];
  const original = rows.find((r) => r.role === 'ok' && r.phone.replace(/\D/g, '').endsWith(digits));
  const [firstName, lastName] = original.name.split(' ');
  row.phone = formatPhoneRaw(digits);
  row.name =
    dupIdx === 0
      ? `${firstName} ${pick(['A', 'J', 'M', 'R', 'T'])}. ${lastName}`
      : `${pick(FIRST_NAMES)} ${lastName}`;
  dupIdx += 1;
}

const aoa = [HEADERS, ...rows.map((r) => [r.name, r.phone, r.email, r.consent, r.last_visit, r.lifetime_value])];

// ── READ ME sheet ─────────────────────────────────────────────────────────────
const READ_ME = [
  ['SALON MALONE — DEMO CLIENTELE'],
  [''],
  ['This data is entirely synthetic. It was generated by a script.'],
  [''],
  ['There are no real people in this file. The names were assembled at random from two word'],
  ['lists. Any resemblance to a living person is coincidence, not a record.'],
  [''],
  ['None of the phone numbers can be dialled. Every one of them uses the 555-0100 to 555-0199'],
  ['range, which the North American Numbering Plan reserves for fiction — the range films and'],
  ['television use precisely so that nobody receives a call. The area codes are real; the'],
  ['numbers behind them are not assigned and never will be.'],
  [''],
  ['Every email address ends in @example.com, a domain RFC 2606 reserves for documentation.'],
  ['It cannot receive mail.'],
  [''],
  ['The file is deliberately messy. It contains rows with no consent, malformed phone numbers,'],
  ['a missing phone number, duplicate numbers, six different date formats and currency-'],
  ['formatted amounts. That is the point: uploading it demonstrates the scrub gates dropping'],
  ['the rows that must never be dialled, and shows you the count for each reason.'],
  [''],
  [`Rows: ${TOTAL}. Expected to survive the scrub: ${COMPOSITION.ok}. Expected to be dropped: ${TOTAL - COMPOSITION.ok}.`],
  [''],
  ['Do not replace these rows with a real client list to "test with real data". Upload a real'],
  ['list only when it carries real, documented consent.'],
];

// ── write ─────────────────────────────────────────────────────────────────────
fs.mkdirSync(DEMO_DIR, { recursive: true });

const sheet = XLSX.utils.aoa_to_sheet(aoa);
sheet['!cols'] = [{ wch: 26 }, { wch: 20 }, { wch: 34 }, { wch: 11 }, { wch: 14 }, { wch: 16 }];
sheet['!autofilter'] = { ref: XLSX.utils.encode_range({ s: { r: 0, c: 0 }, e: { r: TOTAL, c: HEADERS.length - 1 } }) };

const readme = XLSX.utils.aoa_to_sheet(READ_ME);
readme['!cols'] = [{ wch: 95 }];

const wb = XLSX.utils.book_new();
// Fixed doc properties keep the workbook from differing run to run purely by timestamp.
wb.Props = {
  Title: 'Salon Malone — demo clientele (synthetic)',
  Author: 'scripts/generate-demo-clientele.mjs',
  Comments: 'Entirely synthetic. Phone numbers are in the 555-01XX fiction range and are not dialable.',
  CreatedDate: BASE_DATE,
};
XLSX.utils.book_append_sheet(wb, sheet, 'Clientele');
XLSX.utils.book_append_sheet(wb, readme, 'READ ME');

const xlsxPath = join(DEMO_DIR, 'salon-malone-demo-clientele.xlsx');
const csvPath = join(DEMO_DIR, 'salon-malone-demo-clientele.csv');
const templatePath = join(DEMO_DIR, 'upload-template.csv');

XLSX.writeFile(wb, xlsxPath, { bookType: 'xlsx' });
fs.writeFileSync(csvPath, XLSX.utils.sheet_to_csv(sheet));

// Template example rows carry consent=FALSE on purpose: if somebody forgets to delete them, the scrub
// drops them instead of queueing two fictional people for a call.
fs.writeFileSync(
  templatePath,
  [
    TEMPLATE_HEADERS.join(','),
    'Example Row — delete me,Example,(415) 555-0100,example.row@example.com,FALSE,2025-03-14,$240',
    'Second Example — delete me,Second,(415) 555-0101,second.example@example.com,FALSE,03/14/2025,"$1,180.00"',
    '',
  ].join('\n'),
);

// ── report ────────────────────────────────────────────────────────────────────
const consentTrueCount = rows.filter((r) => r.role !== 'no_consent').length;
const pctDropped = (((TOTAL - COMPOSITION.ok) / TOTAL) * 100).toFixed(1);
const rel = (p) => p.replace(`${ROOT}/`, '');

console.log('');
console.log(`Wrote ${rel(xlsxPath)}         ${TOTAL} rows · sheets: Clientele, READ ME`);
console.log(`Wrote ${rel(csvPath)}          same rows, CSV`);
console.log(`Wrote ${rel(templatePath)}                     headers + 2 disposable example rows`);
console.log('');
console.log('All phone numbers are +1 (XXX) 555-01NN — reserved for fiction, not dialable.');
console.log('All emails are @example.com. No real person appears in this file.');
console.log('');
console.log('EXPECTED SCRUB OUTCOME (empty suppression table):');
console.log('');
console.log(`  total                    ${String(TOTAL).padStart(4)}`);
console.log(`  kept                     ${String(COMPOSITION.ok).padStart(4)}   queued as pending, consent = true`);
console.log(`  dropped_no_consent       ${String(COMPOSITION.no_consent).padStart(4)}   consent blank / no / false / 0 / pending / unknown`);
console.log(`  dropped_invalid_phone    ${String(COMPOSITION.invalid_phone).padStart(4)}   too short, leading 0/1, all zeroes, free text`);
console.log(`  dropped_missing_phone    ${String(COMPOSITION.missing_phone).padStart(4)}   phone cell empty`);
console.log(`  dropped_duplicate        ${String(COMPOSITION.duplicate).padStart(4)}   same number as an earlier row in the batch`);
console.log(`  dropped_suppressed          0   depends on your suppression table`);
console.log('');
console.log(`  ${TOTAL - COMPOSITION.ok} of ${TOTAL} rows dropped (${pctDropped}%). ${consentTrueCount} rows claim consent; ${COMPOSITION.ok} survive every gate.`);
console.log('');
console.log('If you add your own number as a consented row to receive the demo call, kept goes to');
console.log(`${COMPOSITION.ok + 1} and total to ${TOTAL + 1}. See demo/README.md.`);
console.log('');
