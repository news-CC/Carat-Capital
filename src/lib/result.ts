/**
 * The only error-handling shape in the codebase: fallible operations return a
 * Result instead of throwing, so route handlers can never 500 on one bad row.
 */
export type Ok<T> = { ok: true; data: T };
export type Err = { ok: false; error: string };
export type Result<T> = Ok<T> | Err;

export const ok = <T,>(data: T): Ok<T> => ({ ok: true, data });
export const err = (error: string): Err => ({ ok: false, error });
