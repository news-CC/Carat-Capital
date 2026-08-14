/**
 * Client-safe sheet reader for the upload wizard.
 *
 * SheetJS only: no server imports, no node builtins, so the browser and the server action can
 * share it. The file the operator picks never leaves the browser — only the mapped rows do.
 */
import * as XLSX from 'xlsx';

export type ParsedSheet = {
  headers: string[];
  rows: Record<string, unknown>[];
  fileName: string;
  sheetName: string;
};

/** The columns the template ships with — also the canonical keys `applyMapping` emits. */
export const UPLOAD_TEMPLATE_HEADERS: string[] = [
  'name',
  'first_name',
  'phone',
  'email',
  'consent',
  'last_visit',
  'lifetime_value',
];

/** One upload, one server action call. `upload/actions.ts` rejects anything past this. */
export const MAX_UPLOAD_ROWS = 20_000;

/** Key holding the 1-based row number from the original sheet, so drops can be cited by row. */
export const SHEET_ROW_INDEX = '__row';

export type SheetField =
  | 'phone'
  | 'consent'
  | 'first_name'
  | 'name'
  | 'email'
  | 'last_visit'
  | 'lifetime_value';

export type FieldSpec = {
  field: SheetField;
  label: string;
  required: boolean;
  hint: string;
  aliases: string[];
};

/** Display order: the two that decide whether a call happens come first. */
export const SHEET_FIELDS: FieldSpec[] = [
  {
    field: 'phone',
    label: 'Phone',
    required: true,
    hint: 'The number Malone dials. US and Canada.',
    aliases: ['phone', 'phone_number', 'mobile', 'cell', 'telephone', 'tel'],
  },
  {
    field: 'consent',
    label: 'Consent',
    required: true,
    hint: 'Must read as a yes. No yes, no call.',
    aliases: ['consent', 'sms_consent', 'opt_in', 'marketing_consent', 'permission'],
  },
  {
    field: 'first_name',
    label: 'First name',
    required: false,
    hint: 'What Malone says out loud.',
    aliases: ['first_name', 'first', 'fname'],
  },
  {
    field: 'name',
    label: 'Full name',
    required: false,
    hint: 'A first name is taken from this when there is no first-name column.',
    aliases: ['name', 'full_name', 'client_name', 'customer'],
  },
  {
    field: 'email',
    label: 'Email',
    required: false,
    hint: 'Stored with the contact. Nothing is emailed to them.',
    aliases: ['email', 'e-mail', 'email_address'],
  },
  {
    field: 'last_visit',
    label: 'Last visit',
    required: false,
    hint: 'Any recognizable date.',
    aliases: ['last_visit', 'last_appointment', 'last_seen', 'last_visit_date'],
  },
  {
    field: 'lifetime_value',
    label: 'Lifetime value',
    required: false,
    hint: 'Dollars. $1,234.50 is fine.',
    aliases: ['lifetime_value', 'ltv', 'total_spend', 'lifetime_spend'],
  },
];

/**
 * Order for the loose second detection pass, most specific first: `first_name` must get a shot at
 * "Client First Name" before `name` can claim it, and `consent` before `phone` so a column called
 * "Phone Consent" lands on consent.
 */
const LOOSE_RANK: Record<SheetField, number> = {
  consent: 0,
  first_name: 1,
  last_visit: 2,
  lifetime_value: 3,
  phone: 4,
  email: 5,
  name: 6,
};

export type ColumnMapping = Record<SheetField, string | null>;

const READABLE_EXTENSIONS = ['csv', 'xls', 'xlsx'];
const MAX_FILE_BYTES = 25 * 1024 * 1024;
const DATE_FORMAT = 'yyyy-mm-dd';

export async function parseSheetFile(file: File): Promise<ParsedSheet> {
  const extension = file.name.split('.').pop()?.toLowerCase() ?? '';
  if (!READABLE_EXTENSIONS.includes(extension)) {
    throw new Error(
      `Salon Malone reads .csv, .xls and .xlsx files${extension ? `, not .${extension}` : ''}. Export the list again and pick one of those.`,
    );
  }
  if (file.size === 0) throw new Error(`${file.name} is empty — 0 bytes.`);
  if (file.size > MAX_FILE_BYTES) {
    throw new Error(
      `${file.name} is ${Math.round(file.size / 1_048_576)} MB. Export just the client-list columns, or split the file.`,
    );
  }

  const bytes = new Uint8Array(await file.arrayBuffer());
  let book: XLSX.WorkBook;
  try {
    // cellDates + dateNF so a last-visit column arrives as 'YYYY-MM-DD' instead of a serial number.
    book = XLSX.read(bytes, { type: 'array', cellDates: true, dateNF: DATE_FORMAT });
  } catch {
    throw new Error(`${file.name} could not be opened as a spreadsheet. It may be corrupt or password protected.`);
  }

  const sheetName = book.SheetNames[0];
  const sheet = sheetName ? book.Sheets[sheetName] : undefined;
  if (!sheetName || !sheet) throw new Error(`${file.name} has no sheets in it.`);

  // raw: false gives formatted text, so "$1,234.50" and "(415) 555-0142" survive as written.
  const grid = XLSX.utils.sheet_to_json<unknown[]>(sheet, {
    header: 1,
    raw: false,
    defval: null,
    blankrows: true,
    dateNF: DATE_FORMAT,
  });

  const headerIndex = grid.findIndex(isPopulated);
  if (headerIndex === -1) throw new Error(`Sheet "${sheetName}" is empty — no header row, no data.`);

  const headers = labelHeaders(grid[headerIndex]);
  const rows: Record<string, unknown>[] = [];
  for (let i = headerIndex + 1; i < grid.length; i++) {
    const cells = grid[i];
    if (!isPopulated(cells)) continue;
    const row: Record<string, unknown> = { [SHEET_ROW_INDEX]: i + 1 };
    headers.forEach((header, column) => {
      row[header] = normalizeCell(cells[column]);
    });
    rows.push(row);
  }
  if (rows.length === 0) {
    throw new Error(`Sheet "${sheetName}" has a header row but nothing under it.`);
  }

  return { headers, rows, fileName: file.name, sheetName };
}

export function detectMapping(headers: string[]): ColumnMapping {
  const mapping = emptyMapping();
  const claimed = new Set<string>();
  const candidates = headers.map((header) => ({ header, key: canonical(header) }));

  // Pass 1: exact header names, case/space/underscore-insensitive.
  for (const spec of SHEET_FIELDS) {
    const aliases = new Set(spec.aliases.map(canonical));
    const hit = candidates.find((c) => !claimed.has(c.header) && aliases.has(c.key));
    if (hit) {
      mapping[spec.field] = hit.header;
      claimed.add(hit.header);
    }
  }

  // Pass 2: real salon exports say "Client Mobile Phone", not "phone".
  const loose = [...SHEET_FIELDS].sort((a, b) => LOOSE_RANK[a.field] - LOOSE_RANK[b.field]);
  for (const spec of loose) {
    if (mapping[spec.field]) continue;
    const aliases = spec.aliases.map(canonical).sort((a, b) => b.length - a.length);
    const hit = candidates.find((c) => !claimed.has(c.header) && aliases.some((a) => c.key.includes(a)));
    if (hit) {
      mapping[spec.field] = hit.header;
      claimed.add(hit.header);
    }
  }

  return mapping;
}

/**
 * Rewrite each row under the canonical field names. Unmapped columns are dropped here, which is
 * also why the payload the operator confirms contains only the columns they chose.
 */
export function applyMapping(
  rows: Record<string, unknown>[],
  mapping: ColumnMapping,
): Record<string, unknown>[] {
  const pairs: [SheetField, string][] = [];
  for (const spec of SHEET_FIELDS) {
    const header = mapping[spec.field];
    if (header) pairs.push([spec.field, header]);
  }
  return rows.map((row) => {
    const mapped: Record<string, unknown> = { [SHEET_ROW_INDEX]: sheetRowOf(row) };
    for (const [field, header] of pairs) {
      const value = row[header];
      mapped[field] = value === undefined ? null : value;
    }
    return mapped;
  });
}

export function missingRequiredFields(mapping: ColumnMapping): SheetField[] {
  return SHEET_FIELDS.filter((spec) => spec.required && !mapping[spec.field]).map((spec) => spec.field);
}

export function labelFor(field: SheetField): string {
  const spec = SHEET_FIELDS.find((s) => s.field === field);
  return spec ? spec.label : field;
}

export function sheetRowOf(row: Record<string, unknown>): number | null {
  const value = row[SHEET_ROW_INDEX];
  return typeof value === 'number' ? value : null;
}

/** First non-empty value in a column, with the sheet row it came from — the mapping sanity check. */
export function firstValue(
  rows: Record<string, unknown>[],
  header: string | null,
): { value: string; row: number | null } | null {
  if (!header) return null;
  for (const row of rows) {
    const value = row[header];
    if (value === null || value === undefined || value === '') continue;
    return { value: String(value), row: sheetRowOf(row) };
  }
  return null;
}

function emptyMapping(): ColumnMapping {
  return {
    phone: null,
    consent: null,
    first_name: null,
    name: null,
    email: null,
    last_visit: null,
    lifetime_value: null,
  };
}

function canonical(header: string): string {
  return header.toLowerCase().replace(/[^a-z0-9]+/g, '');
}

function isPopulated(cells: unknown): boolean {
  return (
    Array.isArray(cells) &&
    cells.some((cell) => cell !== null && cell !== undefined && String(cell).trim() !== '')
  );
}

function labelHeaders(cells: unknown[]): string[] {
  const used = new Set<string>();
  return cells.map((cell, index) => {
    const raw = cell === null || cell === undefined ? '' : String(cell).trim();
    let label = raw || `column_${index + 1}`;
    let suffix = 2;
    while (used.has(label)) label = `${raw || `column_${index + 1}`}__${suffix++}`;
    used.add(label);
    return label;
  });
}

function normalizeCell(cell: unknown): unknown {
  if (cell === null || cell === undefined) return null;
  if (cell instanceof Date) return cell.toISOString().slice(0, 10);
  if (typeof cell === 'string') {
    const trimmed = cell.trim();
    return trimmed === '' ? null : trimmed;
  }
  return cell;
}
