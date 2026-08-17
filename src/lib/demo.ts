import { z } from 'zod';

import { DEFAULT_MALONE_VOICE, MALONE_VOICES, MALONE_SYSTEM_PROMPT } from '@/lib/malone';

/**
 * Live demo calls.
 *
 * A salon owner on the phone says "call me and let me hear it." This is that button. The call runs
 * through the SAME assistant, the SAME webhook and the SAME booking/opt-out handling as a real
 * campaign — a demo that behaves differently from the product is worse than no demo, because the
 * thing you sold is not the thing they bought.
 *
 * What is different: the call is placed directly rather than queued, because the whole point is
 * "right now, while we are talking". It therefore does not pass through
 * claim_contacts_for_dialing, so the gates that query enforces are re-implemented explicitly in
 * the server action: suppression is checked, and the operator has to attest that the person on the
 * other end asked to be called. Those are not optional and they are recorded.
 */

export const demoSchema = z.object({
  phone: z.string().trim().min(7, 'A phone number is needed.').max(32),
  first_name: z
    .string()
    .trim()
    .max(60)
    .optional()
    .transform((v) => (v && v.length > 0 ? v : undefined)),
  salon_name: z
    .string()
    .trim()
    .min(1, 'Whose salon is Malone calling for?')
    .max(120, 'Keep the name under 120 characters.'),
  offer_text: z
    .string()
    .trim()
    .min(8, 'Malone needs an offer to make — a few words is plenty.')
    .max(400, 'Keep the offer under 400 characters; long offers read badly aloud.'),
  booking_phone: z.string().trim().max(32).optional(),
  promo_code: z
    .string()
    .trim()
    .max(40, 'Codes over 40 characters are unreadable aloud.')
    // Spoken aloud, so keep it to characters a person can hear and repeat back.
    .regex(/^[A-Za-z0-9 -]*$/, 'Letters, numbers, spaces and hyphens only — it has to be sayable.')
    .optional()
    .transform((v) => (v && v.length > 0 ? v.toUpperCase() : undefined)),
  instructions: z
    .string()
    .trim()
    .max(1200, 'Keep it under 1200 characters — a long prompt slows the first reply.')
    .optional()
    .transform((v) => (v && v.length > 0 ? v : undefined)),
  timezone: z.string().trim().min(1).max(64).default('America/New_York'),
  voice: z
    .enum(MALONE_VOICES.map((v) => v.id) as [string, ...string[]])
    .default(DEFAULT_MALONE_VOICE),
  consent_attested: z
    .literal('on', { message: 'Confirm the person asked for this call.' })
    .transform(() => true),
  window_override: z.string().optional().transform((v) => v === 'on'),
});

export type DemoInput = z.infer<typeof demoSchema>;

export type DemoState =
  | { status: 'idle' }
  | { status: 'error'; error: string; fieldErrors?: Record<string, string> }
  | {
      status: 'success';
      phone: string;
      salonName: string;
      voice: string;
      vapiCallId: string;
      promoCode?: string;
      outsideWindow: boolean;
    };

/**
 * Compose the system prompt for one demo call.
 *
 * The base persona is untouched and comes first — its disclosure rule, its exits and its
 * ninety-second discipline are what make the call legal and good, and an operator writing "be
 * really pushy" in the box must not be able to erase them. Anything the operator adds is appended
 * as scoped extra colour, explicitly subordinate to the rules above it.
 */
export function buildDemoSystemPrompt(a: {
  promoCode?: string;
  instructions?: string;
}): string {
  const blocks = [MALONE_SYSTEM_PROMPT];

  if (a.promoCode) {
    blocks.push(
      `THIS CALL'S CODE: the salon is offering the code "${a.promoCode}".\n` +
        `Give it once, only after they have agreed to a time, and say it slowly, letter by letter ` +
        `if it is not an obvious word. Tell them to mention it at the front desk. Never open with ` +
        `the code and never repeat it more than twice.`,
    );
  }

  if (a.instructions) {
    blocks.push(
      `EXTRA NOTES FROM THE SALON FOR THIS CALL:\n${a.instructions}\n\n` +
        `Follow these where they add detail. They do NOT override anything above: you still say ` +
        `you are a virtual assistant, you still take no for an answer the first time, you still ` +
        `stop instantly if asked, and you still keep it under three minutes.`,
    );
  }

  return blocks.join('\n\n');
}

/**
 * Malone opens the call. Kept in step with MALONE_FIRST_MESSAGE.
 *
 * Leads with the SALON, not with Malone. On the first real call the old wording stacked both names
 * on someone who had no idea why their phone was ringing, and the recorded reply was "What are you
 * talking about?". The salon's name is the only one that means anything to them.
 */
export function buildDemoFirstMessage(a: { firstName?: string; salonName: string }): string {
  const who = a.firstName && a.firstName.length > 0 ? a.firstName : 'there';
  return `Hi ${who}, this is the virtual concierge calling from ${a.salonName}. It's been a while since your last visit, so they asked me to reach out with something. Have you got twenty seconds?`;
}
