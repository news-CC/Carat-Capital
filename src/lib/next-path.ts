/**
 * Open-redirect gate for the `?next=` value the login flow carries, in one place.
 *
 * Prefix-matching is not enough, which is why this is a shared function rather than a check copied
 * into each file: browsers treat `\` as `/` in an http(s) URL, so `/\evil.com` (and `/\/evil.com`)
 * starts with a single slash yet resolves to another origin — and the no-JS / pre-hydration form post
 * turns `redirect()` into a raw `Location:` header the browser parses exactly that way. So parse the
 * value the way the browser will, against a base that can never be a real host, and keep it only if
 * it stayed there. Returning the PARSED path rather than the raw string also drops anything the
 * parser normalised away.
 *
 * Both the page that seeds the hidden field and the server action that acts on it call this, so the
 * two gates cannot drift apart.
 */

/** Reserved TLD (RFC 6761): `.invalid` is guaranteed never to resolve, so nothing can spoof it. */
const NEXT_BASE = 'https://salon-malone.invalid';

/** Where an absent or rejected `next` lands. */
export const DEFAULT_NEXT = '/admin';

export function safeNextPath(raw: unknown): string {
  const value = typeof raw === 'string' ? raw.trim() : '';
  if (!value.startsWith('/')) return DEFAULT_NEXT;

  let url: URL;
  try {
    url = new URL(value, NEXT_BASE);
  } catch {
    return DEFAULT_NEXT;
  }
  if (url.origin !== NEXT_BASE) return DEFAULT_NEXT;
  return url.pathname + url.search;
}
