import { formatPhone } from '@/lib/phone';
import { usd } from '@/lib/money';
import type { Result } from '@/lib/result';
import { sendEmail } from './client';
import { emailRule, emailShell, escapeHtml, PALETTE, SANS, SERIF } from './layout';

type BookingAlert = {
  salonName: string;
  firstName: string;
  phone: string;
  slotText: string;
  summary: string | null;
  transcriptUrl: string | null;
  estimatedValueCents: number | null;
};

/** Subject lines are plain text, never HTML — escaping here would leak `&amp;` into the inbox. */
function clip(s: string, max: number): string {
  const flat = s.replace(/\s+/g, ' ').trim();
  if (flat.length <= max) return flat;
  const cut = flat.slice(0, max);
  const lastSpace = cut.lastIndexOf(' ');
  return `${(lastSpace > max * 0.6 ? cut.slice(0, lastSpace) : cut).trimEnd()}…`;
}

/** Gate: hrefs come from webhook payloads, so only http(s) is ever rendered as a link. */
function safeUrl(url: string | null): string | null {
  if (!url) return null;
  return /^https?:\/\//i.test(url.trim()) ? url.trim() : null;
}

function detailRow(label: string, value: string): string {
  return `<tr>
      <td width="150" style="padding:9px 0;font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.12em;text-transform:uppercase;color:${PALETTE.inkMute};vertical-align:top;">${escapeHtml(label)}</td>
      <td style="padding:9px 0;font-family:${SANS};font-size:15px;line-height:22px;color:${PALETTE.ink};vertical-align:top;">${value}</td>
    </tr>`;
}

export function bookingAlertEmail(a: BookingAlert): { subject: string; html: string } {
  const who = a.firstName.trim() || 'A lapsed client';
  const slot = a.slotText.trim();
  const value = typeof a.estimatedValueCents === 'number' && a.estimatedValueCents > 0 ? a.estimatedValueCents : null;
  const transcript = safeUrl(a.transcriptUrl);
  const dial = a.phone.replace(/[^\d+]/g, '');

  const subject = slot ? `New booking: ${who} — ${clip(slot, 38)}` : `New booking: ${who}`;
  const preheader = value
    ? `${slot || 'Slot in the call notes'} · about ${usd(value)} · ${formatPhone(a.phone)}`
    : `${slot || 'Slot in the call notes'} · ${formatPhone(a.phone)}`;

  const body = `
  <tr><td style="padding:30px 32px 0 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.16em;text-transform:uppercase;color:${PALETTE.brassDeep};">${escapeHtml(a.salonName)} · just booked</div>
    <div style="font-family:${SERIF};font-size:38px;line-height:44px;color:${PALETTE.ink};padding-top:8px;">${escapeHtml(who)}</div>
  </td></tr>
  ${
    slot
      ? `<tr><td style="padding:20px 32px 0 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      <td style="padding:16px 20px;background-color:${PALETTE.brassWash};border-left:3px solid ${PALETTE.brass};font-family:${SERIF};font-size:20px;line-height:28px;font-style:italic;color:${PALETTE.ink};">&ldquo;${escapeHtml(slot)}&rdquo;</td>
    </tr></table>
    <div style="font-family:${SANS};font-size:11px;line-height:16px;color:${PALETTE.inkMute};padding-top:7px;">Her words, as Malone heard them. Put it in your book the way it reads.</div>
  </td></tr>`
      : ''
  }
  <tr><td style="padding:24px 32px 4px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      ${detailRow(
        'Call her back',
        `<a href="tel:${escapeHtml(dial)}" style="color:${PALETTE.brassDeep};text-decoration:none;font-weight:600;">${escapeHtml(formatPhone(a.phone))}</a>`,
      )}
      ${value ? detailRow('Estimated value', escapeHtml(usd(value))) : ''}
      ${a.summary && a.summary.trim() ? detailRow('What happened', escapeHtml(a.summary.trim())) : ''}
    </table>
  </td></tr>
  <tr><td style="padding:22px 32px 26px 32px;">
    ${
      transcript
        ? `<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
        <td align="center" bgcolor="${PALETTE.brass}" style="background-color:${PALETTE.brass};">
          <a href="${escapeHtml(transcript)}" style="display:inline-block;padding:13px 26px;font-family:${SANS};font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;">Listen to the call</a>
        </td>
      </tr></table>`
        : `<div style="font-family:${SANS};font-size:13px;line-height:20px;color:${PALETTE.inkSoft};">The recording and transcript land in your dashboard a minute or two after the call ends.</div>`
    }
  </td></tr>
${emailRule()}
  <tr><td style="padding:16px 32px 28px 32px;font-family:${SANS};font-size:13px;line-height:20px;color:${PALETTE.inkSoft};">
    Malone told her the chair was hers and that someone from ${escapeHtml(a.salonName)} would confirm. One quick text or call closes it.
  </td></tr>`;

  return { subject, html: emailShell({ preheader, title: 'New booking', body }) };
}

export async function sendBookingAlert(a: { to: string } & BookingAlert): Promise<Result<{ id: string }>> {
  const { to, ...alert } = a;
  const { subject, html } = bookingAlertEmail(alert);
  return sendEmail({ to, subject, html });
}
