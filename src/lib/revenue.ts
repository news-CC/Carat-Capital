/**
 * The one number the client cares about. Deliberately conservative: bookings
 * times average ticket, no multipliers, no lifetime-value projections. If we
 * cannot defend the arithmetic in one sentence, we do not print it.
 */

function safeCount(n: number): number {
  return Number.isFinite(n) && n > 0 ? Math.floor(n) : 0;
}

export function estimatedRecoveredCents(bookingCount: number, avgTicketCents: number): number {
  const ticket = Number.isFinite(avgTicketCents) && avgTicketCents > 0 ? avgTicketCents : 0;
  return Math.round(safeCount(bookingCount) * ticket);
}

/** 0..1. Zero dialed is 0, not NaN — this feeds a percentage in an email. */
export function reachRate(reached: number, dialed: number): number {
  const total = safeCount(dialed);
  if (total === 0) return 0;
  return Math.min(1, safeCount(reached) / total);
}
