/** Currency formatting. Pure — safe in the browser. Cents in, string out. */

function toDollars(cents: number | null | undefined): number {
  if (typeof cents !== 'number' || !Number.isFinite(cents)) return 0;
  return cents / 100;
}

/** '$1,234' when whole, '$1,234.50' when not. The number you show on a tile. */
export function usd(cents: number | null | undefined): string {
  const dollars = toDollars(cents);
  const fraction = Number.isInteger(dollars) ? 0 : 2;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: fraction,
    maximumFractionDigits: fraction,
  }).format(dollars);
}

/** Always two decimals. The number you show on an invoice line. */
export function usdExact(cents: number | null | undefined): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(toDollars(cents));
}
