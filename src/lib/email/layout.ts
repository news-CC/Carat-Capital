/**
 * Shared chrome for every email we send.
 *
 * Constraints these emails are built to survive (Gmail web/iOS/Android, Outlook 2016+, Apple Mail):
 * tables for layout, inline styles only, fixed 600px, no flexbox, no grid, no CSS custom properties,
 * no background images, no <style> block carrying layout. Light-only by design — `color-scheme`
 * is pinned so Gmail's dark mode does not invert the cream.
 */

/**
 * Palette mirrors the app's @theme tokens in src/app/globals.css. Literal hex only — email clients
 * have no variables — so the two have to be kept in step by hand: when a token there changes, change
 * it here. inkMute and sage carry 10-13px text on the cream card in both templates, so they are the
 * two that have to clear WCAG AA 4.5:1 (5.56:1 and 5.60:1 on cream at these values).
 */
export const PALETTE = {
  ink: '#17150F',
  inkSoft: '#57503F',
  inkMute: '#6B6353',
  cream: '#FAF7F1',
  shell: '#F1EBE1',
  brass: '#B0803C',
  brassDeep: '#8A6229',
  brassWash: '#F6EEE1',
  sage: '#506A4D',
  line: '#E4DCCF',
} as const;

export const SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";
export const SERIF = "Georgia,'Times New Roman',Times,serif";

/**
 * The single escape used by every template. A salon named `Bella & Co <3` must not break the markup,
 * and nothing that reaches these templates is trusted markup — it is transcript text and uploaded names.
 */
export function escapeHtml(value: unknown): string {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** A 1px hairline as its own table row. Outlook drops styled empty divs; a table cell always paints. */
export function emailRule(color: string = PALETTE.line): string {
  return `<tr><td style="padding:0 32px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
        <td height="1" style="height:1px;line-height:1px;font-size:0;background-color:${color};">&nbsp;</td>
      </tr></table>
    </td></tr>`;
}

/**
 * Wraps prebuilt table rows in the masthead/footer shell.
 * `preheader` and `title` are plain text and are escaped here; `body` must already be a sequence of
 * escaped `<tr>` rows belonging to the 600px card table.
 */
export function emailShell(a: { preheader: string; title: string; body: string; footer?: string }): string {
  const title = escapeHtml(a.title);
  const footer =
    a.footer ??
    'Calls go only to contacts marked as consenting, inside your local calling window, one attempt each. Opt-outs are honoured immediately and permanently.';

  return `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>${title}</title>
</head>
<body style="margin:0;padding:0;width:100%;background-color:${PALETTE.shell};-webkit-text-size-adjust:100%;">
<span style="display:none!important;visibility:hidden;opacity:0;color:transparent;height:0;width:0;max-height:0;max-width:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;">${escapeHtml(a.preheader)}</span>
<span style="display:none!important;visibility:hidden;opacity:0;color:transparent;height:0;width:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;">&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:${PALETTE.shell};"><tr>
<td align="center" style="padding:32px 12px;">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background-color:${PALETTE.cream};border:1px solid ${PALETTE.line};">
  <tr><td height="3" style="height:3px;line-height:3px;font-size:0;background-color:${PALETTE.brass};">&nbsp;</td></tr>
  <tr><td style="padding:26px 32px 14px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td align="left" style="font-family:${SANS};font-size:11px;line-height:14px;letter-spacing:.18em;text-transform:uppercase;font-weight:700;color:${PALETTE.ink};">Salon&nbsp;Malone</td>
      <td align="right" style="font-family:${SANS};font-size:11px;line-height:14px;letter-spacing:.14em;text-transform:uppercase;color:${PALETTE.inkMute};">${title}</td>
    </tr></table>
  </td></tr>
${emailRule()}
${a.body}
  <tr><td style="padding:0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td style="padding:22px 32px 26px 32px;background-color:${PALETTE.shell};border-top:1px solid ${PALETTE.line};font-family:${SANS};font-size:11px;line-height:18px;color:${PALETTE.inkMute};">
        ${escapeHtml(footer)}<br><br>
        Salon Malone is a virtual concierge. It says so on every call.
      </td>
    </tr></table>
  </td></tr>
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table>
</body></html>`;
}
