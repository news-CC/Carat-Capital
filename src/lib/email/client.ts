import { Resend } from 'resend';
import { serverEnv } from '@/lib/env';
import { err, ok, type Result } from '@/lib/result';

/**
 * The Resend client is built on first send, not at module load: an email template imported into a
 * page must never make the build fail because RESEND_API_KEY is absent from the build environment.
 */
let cached: Resend | null = null;

function client(): Resend {
  if (!cached) cached = new Resend(serverEnv('RESEND_API_KEY'));
  return cached;
}

/**
 * Sends one email. Never throws — a failed Friday report must not take down a cron run, and a failed
 * booking alert must not stop the webhook from recording the booking.
 */
export async function sendEmail(a: {
  to: string | string[];
  subject: string;
  html: string;
  replyTo?: string;
}): Promise<Result<{ id: string }>> {
  const recipients = (Array.isArray(a.to) ? a.to : [a.to]).map((t) => t.trim()).filter(Boolean);
  if (recipients.length === 0) return err('no recipient');

  try {
    const from = serverEnv('EMAIL_FROM');
    const res = await client().emails.send({
      from,
      to: recipients,
      subject: a.subject,
      html: a.html,
      ...(a.replyTo ? { replyTo: a.replyTo } : {}),
    });

    if (res.error) {
      const detail = `${res.error.name}: ${res.error.message}`;
      console.error('[email] send failed', { to: recipients, subject: a.subject, detail });
      return err(detail);
    }
    if (!res.data?.id) {
      console.error('[email] send returned no id', { to: recipients, subject: a.subject });
      return err('resend returned no message id');
    }
    return ok({ id: res.data.id });
  } catch (e: unknown) {
    const detail = e instanceof Error ? e.message : String(e);
    console.error('[email] send threw', { to: recipients, subject: a.subject, detail });
    return err(detail);
  }
}
