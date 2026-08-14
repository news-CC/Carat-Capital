import { usd } from '@/lib/money';
import { reachRate } from '@/lib/revenue';
import type { Result } from '@/lib/result';
import { sendEmail } from './client';
import { emailRule, emailShell, escapeHtml, PALETTE, SANS, SERIF } from './layout';

export type WeeklyStats = {
  salonName: string;
  periodLabel: string;
  dialed: number;
  reached: number;
  booked: number;
  declined: number;
  optedOut: number;
  estimatedRecoveredCents: number;
  avgTicketCents: number;
  topBookings: { firstName: string; slotText: string }[];
};

function statCell(value: number, label: string): string {
  return `<td width="20%" align="center" style="padding:0 4px;">
      <div style="font-family:${SERIF};font-size:27px;line-height:32px;color:${PALETTE.ink};">${value.toLocaleString('en-US')}</div>
      <div style="font-family:${SANS};font-size:10px;line-height:14px;letter-spacing:.1em;text-transform:uppercase;color:${PALETTE.inkMute};padding-top:5px;">${escapeHtml(label)}</div>
    </td>`;
}

function bookingLine(b: { firstName: string; slotText: string }, isLast: boolean): string {
  const name = b.firstName.trim() || 'Client';
  const slot = b.slotText.trim();
  return `<tr>
      <td style="padding:12px 0;${isLast ? '' : `border-bottom:1px solid ${PALETTE.line};`}">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="34" valign="top" style="padding-top:6px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
              <td width="7" height="7" style="width:7px;height:7px;font-size:0;line-height:0;background-color:${PALETTE.brass};">&nbsp;</td>
            </tr></table>
          </td>
          <td valign="top" style="font-family:${SANS};font-size:15px;line-height:22px;font-weight:600;color:${PALETTE.ink};">${escapeHtml(name)}<br>
            <span style="font-family:${SERIF};font-size:15px;line-height:22px;font-style:italic;font-weight:400;color:${PALETTE.inkSoft};">${escapeHtml(slot || 'slot noted on the call')}</span>
          </td>
        </tr></table>
      </td>
    </tr>`;
}

export function weeklyReportEmail(s: WeeklyStats): { subject: string; html: string } {
  const recovered = usd(s.estimatedRecoveredCents);
  const pct = Math.round(reachRate(s.reached, s.dialed) * 100);
  const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? '' : 's'}`;

  const subject =
    s.booked > 0
      ? `Friday report — ${s.salonName}: ${recovered} recovered, ${plural(s.booked, 'booking')}`
      : `Friday report — ${s.salonName}: ${plural(s.dialed, 'call')} out, nothing booked yet`;

  const preheader = `${s.periodLabel} · ${s.reached} answered · ${s.booked} booked · ${s.optedOut} opted out`;

  // Spacing lives in each row's own padding — an empty spacer <td> collapses to nothing in Outlook.
  const headline = `
  <tr><td style="padding:32px 32px 28px 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.16em;text-transform:uppercase;color:${PALETTE.brassDeep};">${escapeHtml(s.salonName)} · ${escapeHtml(s.periodLabel)}</div>
    <div style="font-family:${SERIF};font-size:54px;line-height:60px;color:${PALETTE.brassDeep};padding-top:14px;">${escapeHtml(recovered)}</div>
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:${PALETTE.inkMute};padding-top:8px;">Estimated recovered revenue</div>
    <div style="font-family:${SANS};font-size:15px;line-height:23px;color:${PALETTE.inkSoft};padding-top:16px;">${
      s.booked > 0
        ? `${plural(s.booked, 'booking')} back on the books at your ${escapeHtml(usd(s.avgTicketCents))} average ticket, from ${plural(s.dialed, 'call')} to clients who had gone quiet.`
        : `${plural(s.dialed, 'call')} went out to clients who had gone quiet. Nothing booked yet — the two levers are the offer wording and who is on the list.`
    }</div>
  </td></tr>`;

  const band = `
  <tr><td style="padding:22px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
      ${statCell(s.dialed, 'Called')}
      ${statCell(s.reached, 'Answered')}
      ${statCell(s.booked, 'Booked')}
      ${statCell(s.declined, 'Declined')}
      ${statCell(s.optedOut, 'Opted out')}
    </tr></table>
    <div style="font-family:${SANS};font-size:13px;line-height:20px;color:${PALETTE.inkMute};padding-top:18px;text-align:center;">${
      s.dialed > 0
        ? `${s.reached} of ${s.dialed} picked up — a ${pct}% reach rate.`
        : 'No calls placed this week.'
    }</div>
  </td></tr>`;

  const bookings =
    s.topBookings.length > 0
      ? `
  <tr><td style="padding:26px 32px 24px 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:${PALETTE.inkMute};">Who came back</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
      ${s.topBookings.map((b, i) => bookingLine(b, i === s.topBookings.length - 1)).join('\n')}
    </table>
  </td></tr>`
      : `
  <tr><td style="padding:26px 32px 26px 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:${PALETTE.inkMute};">Who came back</div>
    <div style="font-family:${SERIF};font-size:17px;line-height:26px;font-style:italic;color:${PALETTE.inkSoft};padding-top:10px;">Nobody, this week.</div>
    <div style="font-family:${SANS};font-size:14px;line-height:22px;color:${PALETTE.inkSoft};padding-top:8px;">A quiet week is data. Reply to this email with the offer you would rather Malone lead with and we will run it next.</div>
  </td></tr>`;

  const method = `
  <tr><td style="padding:20px 32px 30px 32px;">
    <div style="font-family:${SANS};font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:${PALETTE.inkMute};">How the number is figured</div>
    <div style="font-family:${SANS};font-size:13px;line-height:21px;color:${PALETTE.inkSoft};padding-top:8px;">Booked slots &times; your ${escapeHtml(usd(s.avgTicketCents))} average ticket. It is an estimate of booked value, not money collected &mdash; a no-show is still counted here, so trust your own book for the final figure.</div>
  </td></tr>`;

  const body = `${headline}${emailRule()}${band}${emailRule()}${bookings}${emailRule()}${method}`;

  return { subject, html: emailShell({ preheader, title: 'Weekly report', body }) };
}

export async function sendWeeklyReport(a: { to: string } & WeeklyStats): Promise<Result<{ id: string }>> {
  const { to, ...stats } = a;
  const { subject, html } = weeklyReportEmail(stats);
  return sendEmail({ to, subject, html });
}
