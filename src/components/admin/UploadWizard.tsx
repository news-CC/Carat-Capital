'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState, useTransition } from 'react';

import {
  uploadContacts,
  uploadPolicy,
  type UploadOutcome,
} from '@/app/admin/clients/[id]/upload/actions';
import {
  applyMapping,
  detectMapping,
  firstValue,
  labelFor,
  MAX_UPLOAD_ROWS,
  missingRequiredFields,
  parseSheetFile,
  SHEET_FIELDS,
  SHEET_ROW_INDEX,
  sheetRowOf,
  UPLOAD_TEMPLATE_HEADERS,
  type ColumnMapping,
  type ParsedSheet,
} from '@/lib/parse-sheet';
import { formatPhone } from '@/lib/phone';
import { scrubRows, type DroppedRow, type ScrubResult, type ScrubStats } from '@/lib/scrub';

type Props = {
  clientId: string;
  clientName: string;
  offerText: string;
  existingContacts: number;
  suppressionListSize: number;
};

type Step = 1 | 2 | 3 | 4;

const STEP_LABELS = ['Choose the file', 'Confirm the columns', 'Dry run', 'Written'];

/**
 * Next caps a server action body at 1 MB by default; we stop short of it with a real message. Bytes
 * are the limit that actually binds a real export — well before MAX_UPLOAD_ROWS — so step 1 measures
 * them there and then, where splitting the file is still the only work lost.
 */
const MAX_PAYLOAD_BYTES = 900_000;

const DROP_LINES: {
  key: keyof ScrubStats;
  label: string;
  why: string;
  /** The browser has no access to the suppression table, so it can never count this one. */
  serverOnly?: boolean;
}[] = [
  {
    key: 'dropped_no_consent',
    label: 'No recorded consent',
    why: 'Nothing in the consent column read as a yes.',
  },
  { key: 'dropped_missing_phone', label: 'No phone number', why: 'The phone cell was empty.' },
  {
    key: 'dropped_invalid_phone',
    label: 'Unusable phone number',
    why: 'Not a dialable US or Canadian number.',
  },
  {
    key: 'dropped_suppressed',
    label: 'On the do-not-contact list',
    why: 'Opted out, complained, or was suppressed by hand — for any client, ever.',
    serverOnly: true,
  },
  {
    key: 'dropped_duplicate',
    label: 'Duplicate inside this file',
    why: 'The same number appeared in an earlier row.',
  },
];

const REASON_LABEL: Record<DroppedRow['reason'], string> = {
  no_consent: 'No consent',
  missing_phone: 'No number',
  invalid_phone: 'Bad number',
  suppressed: 'Do-not-contact',
  duplicate: 'Duplicate',
};

const REASON_BADGE: Record<DroppedRow['reason'], string> = {
  no_consent: 'badge badge-warn',
  missing_phone: 'badge badge-mute',
  invalid_phone: 'badge badge-warn',
  suppressed: 'badge badge-bad',
  duplicate: 'badge badge-mute',
};

export function UploadWizard({
  clientId,
  clientName,
  offerText,
  existingContacts,
  suppressionListSize,
}: Props) {
  const [step, setStep] = useState<Step>(1);
  const [sheet, setSheet] = useState<ParsedSheet | null>(null);
  const [autoMapping, setAutoMapping] = useState<ColumnMapping | null>(null);
  const [mapping, setMapping] = useState<ColumnMapping | null>(null);
  const [dragging, setDragging] = useState(false);
  const [parsing, setParsing] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [campaign, setCampaign] = useState('default');
  const [serverError, setServerError] = useState<string | null>(null);
  const [confirmed, setConfirmed] = useState<ScrubStats | null>(null);
  const [outcome, setOutcome] = useState<UploadOutcome | null>(null);
  const [consentRequired, setConsentRequired] = useState<boolean | null>(null);
  const [policyError, setPolicyError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  /**
   * REQUIRE_CONSENT_FLAG lives on the server, so the wizard asks for it rather than assuming: a dry
   * run that applied a gate the server does not would show a count that is not the one written. Until
   * the answer arrives there is no preview at all — guessing the stricter value would still be a
   * guess, and this is the screen the operator reads before real phones get dialed.
   */
  useEffect(() => {
    let live = true;
    void uploadPolicy().then(
      (policy) => {
        if (live) setConsentRequired(policy.consent_required);
      },
      () => {
        if (live) {
          setPolicyError('Could not read this environment’s consent setting. Reload the page.');
        }
      },
    );
    return () => {
      live = false;
    };
  }, []);

  /**
   * Advisory dry run. The browser passes an empty suppression list because it has none — that gate is
   * the server's alone. Consent is scrubbed exactly as the server will scrub it.
   */
  const preview = useMemo<ScrubResult | null>(() => {
    if (!sheet || !mapping || consentRequired === null || step < 3) return null;
    return scrubRows(applyMapping(sheet.rows, mapping), [], { requireConsent: consentRequired });
  }, [sheet, mapping, consentRequired, step]);

  const missing = mapping ? missingRequiredFields(mapping) : [];

  function reset() {
    setStep(1);
    setSheet(null);
    setAutoMapping(null);
    setMapping(null);
    setFileError(null);
    setServerError(null);
    setConfirmed(null);
    setOutcome(null);
  }

  async function readFile(file: File | null | undefined) {
    if (!file) return;
    setParsing(true);
    setFileError(null);
    setServerError(null);
    setOutcome(null);
    try {
      const parsed = await parseSheetFile(file);
      const detected = detectMapping(parsed.headers);
      // Measured on the columns we just detected, so the size limit lands here instead of after the
      // operator has mapped columns and read a dry run. They can map more at step 2, so submit()
      // measures the real payload again before it sends.
      const bytes = payloadBytes(applyMapping(parsed.rows, detected).map(toPayloadRow));
      if (bytes > MAX_PAYLOAD_BYTES) {
        throw new Error(tooLargeMessage(parsed.fileName, parsed.rows.length, bytes));
      }
      if (parsed.rows.length > MAX_UPLOAD_ROWS) {
        throw new Error(
          `${parsed.fileName} has ${count(parsed.rows.length)} rows. One upload takes ${count(MAX_UPLOAD_ROWS)} — split the file and do it in parts.`,
        );
      }
      setSheet(parsed);
      setAutoMapping(detected);
      setMapping(detected);
      setStep(2);
    } catch (cause) {
      setSheet(null);
      setMapping(null);
      setFileError(cause instanceof Error ? cause.message : 'That file could not be read.');
    } finally {
      setParsing(false);
    }
  }

  function submit() {
    if (!sheet || !mapping || !preview) return;
    // Every mapped row goes up, including the ones this preview would drop: the server has to reach
    // its own verdict on the full list rather than trust a filtered one.
    const rows = applyMapping(sheet.rows, mapping).map(toPayloadRow);
    const bytes = payloadBytes(rows);
    if (bytes > MAX_PAYLOAD_BYTES) {
      setServerError(tooLargeMessage(sheet.fileName, rows.length, bytes));
      return;
    }
    setServerError(null);
    setConfirmed(preview.stats);
    startTransition(async () => {
      const result = await uploadContacts({ clientId, campaign: campaign.trim() || 'default', rows });
      if (result.ok) {
        setOutcome(result.data);
        setStep(4);
      } else {
        setServerError(result.error);
      }
    });
  }

  return (
    <div className="space-y-6">
      <ol className="flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px] font-medium uppercase tracking-[0.16em]">
        {STEP_LABELS.map((label, index) => {
          const position = index + 1;
          const tone =
            position === step
              ? 'bg-ink text-cream'
              : position < step
                ? 'bg-brass text-cream'
                : 'bg-shell text-ink-mute';
          return (
            <li key={label} className="flex items-center gap-2">
              <span className={`flex h-5 w-5 items-center justify-center rounded-full text-[10px] ${tone}`}>
                {position}
              </span>
              <span className={position > step ? 'text-ink-mute' : 'text-ink'}>{label}</span>
            </li>
          );
        })}
      </ol>

      {sheet && (
        <div className="card card-pad flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <p className="text-sm font-medium text-ink">{sheet.fileName}</p>
            <p className="text-xs text-ink-soft">
              Sheet “{sheet.sheetName}” · {count(sheet.rows.length)} data rows ·{' '}
              {count(sheet.headers.length)} columns
            </p>
          </div>
          <button type="button" className="btn btn-ghost btn-sm" onClick={reset} disabled={pending}>
            Start over with another file
          </button>
        </div>
      )}

      {step === 1 && (
        <div className="card card-pad space-y-4">
          <div className="space-y-1">
            <h2 className="h-display text-xl">Point us at the list</h2>
            <p className="text-sm text-ink-soft">
              CSV, XLS or XLSX. The file is read here in your browser — it is never uploaded. Only the
              columns you map get sent, and only after you have seen the dry run.
            </p>
          </div>

          <label
            onDragOver={(event) => {
              event.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={(event) => {
              event.preventDefault();
              setDragging(false);
              void readFile(event.dataTransfer.files?.[0]);
            }}
            className={`relative flex cursor-pointer flex-col items-center justify-center gap-2 rounded-[14px] border border-dashed px-6 py-14 text-center transition-opacity duration-150 focus-within:border-brass focus-within:ring-2 focus-within:ring-brass ${
              dragging ? 'border-brass bg-brass-wash' : 'border-line bg-cream hover:opacity-90'
            }`}
          >
            {/*
              sr-only, not hidden: display:none takes the input out of the tab order, and picking the
              file is the only way into the app. Clipped to a pixel it still takes focus and still
              opens the picker on Enter, and focus-within puts the ring on the drop zone.
            */}
            <input
              type="file"
              accept=".csv,.xls,.xlsx"
              className="sr-only"
              onChange={(event) => void readFile(event.target.files?.[0])}
            />
            <span className="font-display text-lg text-ink">
              {parsing ? 'Reading the file…' : 'Drop the client list here'}
            </span>
            <span className="text-sm text-ink-mute">or click to choose it</span>
          </label>

          <p className="help">
            Expected columns: {UPLOAD_TEMPLATE_HEADERS.join(' · ')}. Close enough names — “Mobile
            Phone”, “Opt In”, “Last Appointment” — are matched for you on the next screen.
          </p>
          <p className="text-xs text-ink-mute">
            {clientName} already has {count(existingContacts)}{' '}
            {existingContacts === 1 ? 'contact' : 'contacts'}. An upload adds to that list; nothing is
            replaced or overwritten.
          </p>
          {fileError && <p className="error-text">{fileError}</p>}
        </div>
      )}

      {step === 2 && sheet && mapping && (
        <div className="card card-pad space-y-5">
          <div className="space-y-1">
            <h2 className="h-display text-xl">Confirm the columns</h2>
            <p className="text-sm text-ink-soft">
              Phone and consent are the two that decide whether a call ever happens. Check them
              against the sample values, then move on.
            </p>
          </div>

          {missing.length > 0 && (
            <p className="rounded-[14px] border border-rose/30 bg-rose/5 px-4 py-3 text-sm text-ink">
              {missing.map((field) => labelFor(field)).join(' and ')}{' '}
              {missing.length === 1 ? 'is' : 'are'} not mapped yet.{' '}
              {missing.includes('phone') && 'Without a phone column there is nothing to dial. '}
              {missing.includes('consent') &&
                'Without a consent column every row is dropped — we do not dial a number that never said yes.'}
            </p>
          )}

          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Field</th>
                  <th>Column in your file</th>
                  <th>First value we see</th>
                </tr>
              </thead>
              <tbody>
                {SHEET_FIELDS.map((spec) => {
                  const chosen = mapping[spec.field];
                  const sample = firstValue(sheet.rows, chosen);
                  const auto = autoMapping?.[spec.field] ?? null;
                  return (
                    <tr key={spec.field}>
                      <td>
                        <span className="text-sm font-medium text-ink">{spec.label}</span>
                        {spec.required && <span className="ml-2 badge badge-warn">required</span>}
                        <p className="mt-1 text-xs text-ink-mute">{spec.hint}</p>
                      </td>
                      <td>
                        <select
                          className="select"
                          value={chosen ?? ''}
                          aria-label={`Column for ${spec.label}`}
                          onChange={(event) =>
                            setMapping({ ...mapping, [spec.field]: event.target.value || null })
                          }
                        >
                          <option value="">— not mapped —</option>
                          {sheet.headers.map((header) => (
                            <option key={header} value={header}>
                              {header}
                            </option>
                          ))}
                        </select>
                        {chosen && auto === chosen && (
                          <p className="mt-1 text-xs text-ink-mute">matched automatically</p>
                        )}
                        {chosen && auto !== chosen && (
                          <p className="mt-1 text-xs text-brass-deep">you set this</p>
                        )}
                      </td>
                      <td>
                        {sample ? (
                          <span className="text-sm text-ink">
                            {truncate(sample.value)}
                            {sample.row !== null && (
                              <span className="text-ink-mute"> · row {sample.row}</span>
                            )}
                          </span>
                        ) : (
                          <span className="text-sm text-ink-mute">
                            {chosen ? 'every cell is empty' : '—'}
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {policyError && <p className="error-text">{policyError}</p>}

          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="help">
              Columns you leave unmapped are ignored — they are not sent and not stored.
            </p>
            <button
              type="button"
              className="btn btn-primary"
              disabled={missing.length > 0 || consentRequired === null}
              onClick={() => setStep(3)}
            >
              {consentRequired === null
                ? 'Checking the server’s consent setting…'
                : `Dry run ${count(sheet.rows.length)} rows`}
            </button>
          </div>
        </div>
      )}

      {step === 3 && preview && sheet && (
        <div className="space-y-6">
          <div className="card card-pad space-y-5">
            <div className="space-y-1">
              <h2 className="h-display text-xl">Dry run — nothing has been written yet</h2>
              <p className="text-sm text-ink-soft">
                This is what {clientName}’s list looks like after the gates. Read the drops before you
                confirm.
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              <Tile value={count(preview.stats.total)} label="Rows in the file" />
              <Tile value={count(preview.stats.kept)} label="Would be added" />
              <Tile value={count(preview.dropped.length)} label="Would be dropped" />
            </div>

            <div className="divide-y divide-line overflow-hidden rounded-[14px] border border-line">
              {DROP_LINES.map((line) => (
                <div key={line.key} className="flex items-baseline justify-between gap-4 px-4 py-3">
                  <div>
                    <p className="text-sm font-medium text-ink">{line.label}</p>
                    <p className="text-xs text-ink-soft">{line.why}</p>
                  </div>
                  {line.serverOnly ? (
                    <p className="shrink-0 text-right text-xs text-ink-mute">
                      checked on the server
                      <br />
                      against {count(suppressionListSize)} numbers
                    </p>
                  ) : (
                    <p
                      className={`font-display text-lg ${
                        preview.stats[line.key] > 0 ? 'text-ink' : 'text-ink-mute'
                      }`}
                    >
                      {count(preview.stats[line.key])}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>

          {preview.kept.length > 0 && (
            <div className="card card-pad space-y-3">
              <h3 className="font-display text-lg text-ink">
                The first numbers Malone would dial
              </h3>
              <div className="overflow-x-auto">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Number</th>
                      <th>Last visit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {preview.kept.slice(0, 5).map((row) => (
                      <tr key={row.phone}>
                        <td>{row.first_name ?? row.name ?? '—'}</td>
                        <td className="whitespace-nowrap">{formatPhone(row.phone)}</td>
                        <td>{row.last_visit ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="help">Offer on the call: {offerText}</p>
            </div>
          )}

          <div className="card card-pad space-y-3">
            <h3 className="font-display text-lg text-ink">
              {preview.dropped.length > 0
                ? `Dropped rows — showing ${Math.min(10, preview.dropped.length)} of ${count(preview.dropped.length)}`
                : 'Dropped rows'}
            </h3>
            {preview.dropped.length === 0 ? (
              <p className="text-sm text-ink-soft">
                Every row passed the browser checks. The server still re-runs them against the
                do-not-contact list.
              </p>
            ) : (
              <div className="overflow-x-auto">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Row</th>
                      <th>Reason</th>
                      <th>Name</th>
                      <th>Phone as written</th>
                      <th>Consent as written</th>
                    </tr>
                  </thead>
                  <tbody>
                    {preview.dropped.slice(0, 10).map((drop, index) => (
                      <tr key={`${sheetRowOf(drop.row) ?? index}-${drop.reason}`}>
                        <td className="whitespace-nowrap text-ink-mute">
                          {sheetRowOf(drop.row) ?? '—'}
                        </td>
                        <td className="whitespace-nowrap">
                          <span className={REASON_BADGE[drop.reason]}>{REASON_LABEL[drop.reason]}</span>
                        </td>
                        <td>{cellText(drop.row.name ?? drop.row.first_name)}</td>
                        <td>{cellText(drop.row.phone)}</td>
                        <td>{cellText(drop.row.consent)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <div className="card card-pad space-y-4">
            <div className="field">
              <label className="label" htmlFor="campaign">
                Campaign name
              </label>
              <input
                id="campaign"
                className="input"
                value={campaign}
                maxLength={60}
                onChange={(event) => setCampaign(event.target.value)}
              />
              <p className="help">
                One attempt per contact per campaign, ever. Reuse a name and the numbers already in it
                are skipped rather than called twice.
              </p>
            </div>

            <div className="rule" />

            <p className="prose-tight text-sm text-ink-soft">
              This dry run ran in your browser against consent, phone format and in-file duplicates
              only. Your browser cannot see the do-not-contact list. When you confirm, the server runs
              the same scrub again — this time against the live list of {count(suppressionListSize)}{' '}
              suppressed numbers — and writes only the rows that survive it.{' '}
              <strong className="text-ink">The server’s numbers are the ones that count.</strong>
            </p>

            {consentRequired === false && (
              <p className="rounded-[14px] border border-amber/40 bg-brass-wash px-4 py-3 text-sm text-ink">
                REQUIRE_CONSENT_FLAG is off in this environment, so “No recorded consent” above counts
                only the rows whose consent cell says no out loud — those are dropped whatever the flag
                says. Rows with a blank consent cell are kept instead of dropped, and stored with
                consent = no: they land on {clientName}’s list and Malone can never dial them. Turn the
                flag back on and they are dropped rather than stored.
              </p>
            )}

            {preview.stats.kept === 0 && (
              <p className="rounded-[14px] border border-rose/30 bg-rose/5 px-4 py-3 text-sm text-ink">
                Not one row in this file passes the gates, so there is nothing to write. Check the
                consent and phone columns on the previous screen — a consent column pointed at the
                wrong field drops the whole list.
              </p>
            )}

            {serverError && <p className="error-text">{serverError}</p>}

            <div className="flex flex-wrap items-center gap-3">
              <button
                type="button"
                className="btn btn-primary"
                disabled={pending || preview.stats.kept === 0}
                onClick={submit}
              >
                {pending
                  ? 'Scrubbing on the server…'
                  : `Add ${count(preview.stats.kept)} contacts to ${clientName}`}
              </button>
              <button
                type="button"
                className="btn btn-ghost"
                disabled={pending}
                onClick={() => setStep(2)}
              >
                Back to columns
              </button>
            </div>
          </div>
        </div>
      )}

      {step === 4 && outcome && (
        <div className="space-y-6">
          <div className="card card-pad space-y-5">
            <div className="space-y-1">
              <h2 className="h-display text-xl">
                {count(outcome.inserted)} {outcome.inserted === 1 ? 'contact is' : 'contacts are'}{' '}
                queued for {clientName}
              </h2>
              <p className="text-sm text-ink-soft">
                Campaign “{outcome.campaign}” · scrubbed against {count(outcome.suppression_list_size)}{' '}
                suppressed numbers · written {new Date().toLocaleTimeString('en-US')}
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              <Tile value={count(outcome.inserted)} label="Added as pending" />
              <Tile value={count(outcome.stats.total - outcome.stats.kept)} label="Dropped by the server" />
              <Tile value={count(outcome.already_on_campaign)} label="Already on this campaign" />
            </div>

            {!outcome.consent_required && (
              <p className="rounded-[14px] border border-amber/40 bg-brass-wash px-4 py-3 text-sm text-ink">
                REQUIRE_CONSENT_FLAG is off in this environment, so{' '}
                {count(outcome.stored_without_consent)}{' '}
                {outcome.stored_without_consent === 1 ? 'row' : 'rows'} with a blank consent cell{' '}
                {outcome.stored_without_consent === 1 ? 'was' : 'were'} kept and stored with consent =
                no. They will never be dialed — consent = yes is the dialer’s hard gate — and turning
                the flag back on does not change what was already written. Turn it back on.
              </p>
            )}

            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr>
                    <th>Outcome</th>
                    <th>Your dry run</th>
                    <th>Server</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="text-sm font-medium text-ink">Passed every gate</td>
                    <td className="text-ink-mute">{confirmed ? count(confirmed.kept) : '—'}</td>
                    <td className="font-display text-ink">{count(outcome.stats.kept)}</td>
                  </tr>
                  {DROP_LINES.map((line) => (
                    <tr key={line.key}>
                      <td>
                        <span className="text-sm text-ink">{line.label}</span>
                      </td>
                      <td className="text-ink-mute">
                        {line.serverOnly ? 'not visible' : confirmed ? count(confirmed[line.key]) : '—'}
                      </td>
                      <td className="font-display text-ink">{count(outcome.stats[line.key])}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <p className="prose-tight text-sm text-ink-soft">
              {outcome.stats.dropped_suppressed > 0
                ? `${count(outcome.stats.dropped_suppressed)} ${
                    outcome.stats.dropped_suppressed === 1 ? 'number' : 'numbers'
                  } in this file ${outcome.stats.dropped_suppressed === 1 ? 'is' : 'are'} on the do-not-contact list. Your browser could not see ${
                    outcome.stats.dropped_suppressed === 1 ? 'it' : 'them'
                  }; the server dropped ${outcome.stats.dropped_suppressed === 1 ? 'it' : 'them'} and nothing was written for ${
                    outcome.stats.dropped_suppressed === 1 ? 'it' : 'them'
                  }.`
                : 'No number in this file was on the do-not-contact list.'}
              {outcome.already_on_campaign > 0 &&
                ` ${count(outcome.already_on_campaign)} passed the gates but were already on campaign “${outcome.campaign}”, so they were left exactly as they were — nobody gets called twice.`}
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <Link className="btn btn-primary" href={`/admin/clients/${clientId}`}>
                Back to {clientName}
              </Link>
              <button type="button" className="btn btn-ghost" onClick={reset}>
                Upload another list
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Tile({ value, label }: { value: string; label: string }) {
  return (
    <div className="stat">
      <div className="stat-num">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

/**
 * The server re-scrubs from scratch, so it only needs the mapped values: the sheet row number and
 * empty cells are dropped to keep the request small.
 */
function toPayloadRow(row: Record<string, unknown>): Record<string, unknown> {
  const payload: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(row)) {
    if (key === SHEET_ROW_INDEX || value === null || value === '') continue;
    payload[key] = value;
  }
  return payload;
}

/** Next measures the request body in bytes, so we do too — an accented name is more than one. */
function payloadBytes(rows: Record<string, unknown>[]): number {
  return new TextEncoder().encode(JSON.stringify(rows)).length;
}

/** Says how many parts, and how big, so the operator never has to find the limit by trial. */
function tooLargeMessage(fileName: string, rows: number, bytes: number): string {
  const parts = Math.ceil(bytes / MAX_PAYLOAD_BYTES);
  return `${fileName} has ${count(rows)} rows, which is ${megabytes(bytes)} MB to send — one upload takes ${megabytes(MAX_PAYLOAD_BYTES)} MB. Split it into ${count(parts)} files of about ${count(Math.ceil(rows / parts))} rows and upload them one after another.`;
}

function megabytes(bytes: number): string {
  return (bytes / 1_000_000).toFixed(1);
}

function count(value: number): string {
  return value.toLocaleString('en-US');
}

function truncate(value: string): string {
  return value.length > 48 ? `${value.slice(0, 48)}…` : value;
}

function cellText(value: unknown): string {
  if (value === null || value === undefined || value === '') return '—';
  if (typeof value === 'string') return truncate(value);
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return '—';
}
