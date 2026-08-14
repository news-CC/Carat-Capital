import { describe, expect, it } from 'vitest';

import { DEFAULT_NEXT, safeNextPath } from '@/lib/next-path';

/**
 * Open-redirect gate. The `?next=` value reaches this from a URL an attacker can send to the
 * operator, and the result becomes a `Location:` header, so anything that escapes same-origin is a
 * phishing hand-off: the operator logs in for real and lands on someone else's page.
 */
describe('safeNextPath — values that must be rejected', () => {
  const hostile = [
    // Browsers treat a backslash as a slash in an http(s) URL, so these leave the origin while
    // still starting with a single '/'. A startsWith('//') check does not catch them.
    '/\\evil.com',
    '/\\/evil.com',
    '\\/evil.com',
    '\\\\evil.com',
    '//evil.com',
    '///evil.com',
    '/\t/evil.com',
    '/\n/evil.com',
    ' /\\evil.com ',
    // Absolute URLs and non-http schemes.
    'https://evil.com',
    'http://evil.com/admin',
    '//evil.com/admin',
    'evil.com',
    'javascript:alert(1)',
    'data:text/html,<script>alert(1)</script>',
    // Not a path at all.
    '',
    '   ',
    'admin',
  ];

  for (const value of hostile) {
    it(`sends ${JSON.stringify(value)} to ${DEFAULT_NEXT}`, () => {
      expect(safeNextPath(value)).toBe(DEFAULT_NEXT);
    });
  }

  it('rejects anything that is not a string, without throwing', () => {
    for (const value of [undefined, null, 42, {}, [], true, new URL('https://evil.com')]) {
      expect(safeNextPath(value)).toBe(DEFAULT_NEXT);
    }
  });
});

describe('safeNextPath — values that must survive', () => {
  it('keeps a plain admin path', () => {
    expect(safeNextPath('/admin')).toBe('/admin');
    expect(safeNextPath('/admin/bookings')).toBe('/admin/bookings');
  });

  it('keeps the query string, so a filtered view survives the login round trip', () => {
    expect(safeNextPath('/admin/clients/abc?tab=calls')).toBe('/admin/clients/abc?tab=calls');
    expect(safeNextPath('/admin/bookings?client=123')).toBe('/admin/bookings?client=123');
  });

  it('keeps a same-origin path that merely looks like a URL', () => {
    // '/https://evil.com' is a path on our own host, not a redirect off it.
    expect(safeNextPath('/https://evil.com')).toBe('/https://evil.com');
    // %5C is a literal backslash in a path segment — encoded, so it stays same-origin.
    expect(safeNextPath('/%5Cevil.com')).toBe('/%5Cevil.com');
  });

  it('drops the fragment, which never reaches the server anyway', () => {
    expect(safeNextPath('/admin#section')).toBe('/admin');
  });

  it('returns the parsed path, so traversal is normalised away rather than passed through', () => {
    expect(safeNextPath('/admin/../admin/calls')).toBe('/admin/calls');
    expect(safeNextPath('/../../etc/passwd')).toBe('/etc/passwd');
  });

  it('is idempotent — re-validating its own output changes nothing', () => {
    for (const value of ['/admin', '/admin/clients?x=1', '/\\evil.com', 'https://evil.com']) {
      expect(safeNextPath(safeNextPath(value))).toBe(safeNextPath(value));
    }
  });
});
