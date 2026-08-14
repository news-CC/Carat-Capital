/**
 * COMPLIANCE GATE: "stop calling me", in the caller's own words.
 *
 * Pure, zero I/O, zero env — like scrub.ts, and for the same reason: this decides whether a person
 * is added to the global do-not-contact list, so it has to be readable and testable on its own
 * (tests/opt-out.test.ts) rather than only reachable through a webhook payload.
 *
 * The webhook's primary signal is Vapi's own end-of-call extractor, which read the whole
 * conversation. This is the backstop for when the analysis plan times out or is skipped: either
 * signal alone is enough, because a caller who asked in plain words to be removed is removed even
 * when the extractor says otherwise.
 */

/** One match is an opt-out. Matched against normalised CALLER speech only — see callerSpeech. */
const OPT_OUT_RE: readonly RegExp[] = [
  /\b(stop|quit|cease)\s+(the\s+)?(call|calls|calling|contact|contacting|phoning)\b/,
  /\bno more\s+(calls?|calling|contact|phone calls)\b/,
  /\b(do not|don'?t)\s+ever\s+(call|contact|phone|ring)\b/,
  /\bnever\s+(call|contact|phone|ring)\b/,
  /\b(do not|don'?t)\s+(call|contact|phone|ring)\b[^.!?]{0,40}\b(again|any ?more)\b/,
  /\b(do not|don'?t)\s+(call|contact|phone|ring)\s+(me|us|this number)\s+at all\b/,
  // Bare "don't call me" counts, but NOT "don't call me at work" / "on my cell" / "before nine":
  // a caller pointing us at a better number or time is redirecting us, not asking to be removed.
  // Treating that as an opt-out would nuke a real booking and globally suppress a happy customer.
  /\b(do not|don'?t)\s+(call|contact|phone|ring)\s+(me|us|this number)\b(?!\s*(at|on|before|after|during|until|between|unless|when|in the|on the)\b)/,
  /\b(take|get)\s+(me|my (name|number|phone number))\s+off\b/,
  /\b(remove|delete|erase)\s+(me|my (name|number|phone number|info|information))\b/,
  /\b(lose|forget)\s+my number\b/,
  /\b(unsubscribe|opt me out|opt out of)\b/,
  /\b(off|not on)\s+(your|the|this)\s+(call(ing)?\s+)?list\b/,
  /\bdo.?not.?call list\b/,
];

/** Vapi's artifact.transcript is speaker-prefixed: "AI: …" / "User: …", one turn per line. */
const CALLER_TURN_RE = /^\s*(user|customer|caller|human)\s*:\s*(.*)$/i;
const AGENT_TURN_RE = /^\s*(ai|assistant|bot|agent|malone|system)\s*:\s*(.*)$/i;

/**
 * The caller's words, normalised. The backstop must read those only: an aside in the middle of a
 * booked call ("don't call me at work, use my cell") must not suppress a happy customer globally,
 * and Malone's own "you're off the list" must not suppress anyone at all.
 *
 * A transcript with no speaker prefixes (the flat message.transcript fallback) is used whole —
 * missing a real opt-out is the dangerous direction, so that case fails closed.
 */
export function callerSpeech(transcript: string): string {
  const turns: string[] = [];
  let current: string[] | null = null;
  let prefixed = false;

  const endTurn = (): void => {
    if (!current) return;
    const text = current.join(' ').trim();
    if (text !== '') turns.push(text);
    current = null;
  };

  for (const line of transcript.split(/\r?\n/)) {
    const asCaller = CALLER_TURN_RE.exec(line);
    if (asCaller) {
      prefixed = true;
      endTurn();
      current = [asCaller[2]];
      continue;
    }
    if (AGENT_TURN_RE.test(line)) {
      prefixed = true;
      endTurn();
      continue;
    }
    // A wrapped continuation belongs to the turn it is part of, joined with a plain SPACE: a
    // directive broken across a line ("take my number\noff your list") has to keep matching, since
    // missing a real opt-out is the dangerous direction.
    if (current) current.push(line);
  }
  endTurn();

  // Separate TURNS are joined with a sentence break, so no pattern can match across two of them —
  // the caller saying "please stop" and Malone saying "calling you now" must never read as
  // "stop calling".
  return normalizeSpeech(prefixed ? turns.join('. ') : transcript);
}

/** Casing, smart quotes and line wrapping must never decide a compliance outcome. */
export function normalizeSpeech(text: string): string {
  return text
    .toLowerCase()
    .replace(/[‘’ʼ′´`]/g, "'")
    .replace(/\s+/g, ' ');
}

/**
 * Whether the CALLER asked, in this transcript, never to be called again.
 * Takes the raw transcript and does its own speaker scoping and normalisation, so no call site can
 * forget either step.
 */
export function containsOptOutRequest(transcript: string): boolean {
  const speech = callerSpeech(transcript);
  return OPT_OUT_RE.some((re) => re.test(speech));
}
