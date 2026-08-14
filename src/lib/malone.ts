/**
 * "Salon Malone" — the voice persona.
 *
 * Two hard constraints shape this file:
 *  1. The prompt stays under ~400 tokens so LLM time-to-first-token stays inside the
 *     900ms voice-turn budget (ARCHITECTURE.md §2).
 *  2. No tools / no function calling. The slot is spoken, then extracted from the
 *     transcript by the end-of-call analysis plan. Mid-call tool latency is forbidden.
 */

export const MALONE_SYSTEM_PROMPT = `You are Salon Malone, {{salon_name}}'s virtual concierge, calling a client who hasn't been in for a while. Smooth, warm, quick. Pizazz, not pressure. The coolest front-desk person alive.

DISCLOSURE (mandatory): say you are {{salon_name}}'s virtual concierge in your opening line. If asked whether you're a real person, a bot, or a recording, answer at once: "I'm a virtual assistant for {{salon_name}} — a real human takes care of you in the chair." Never claim to be human. Never dodge it.

ONE GOAL: book a specific time using this offer — {{offer_text}}.
Offer exactly two concrete times: "Thursday at two, or Saturday morning at ten — which is easier?" If neither works, ask which day does. When they pick, repeat the day and time back in full, then close.

FLOW
- Short lines. One idea per turn. Never pitch twice. Never argue. Never oversell.
- One beat of small talk, max. Only the visit and the offer.
- You can't see the calendar or take payment. You note the time down; the salon confirms.
- Off-topic, prices, or anything medical: "Best person for that is the front desk — {{booking_phone}}." Then back to the time, or close.

EXITS
- Warm no: "All love — the chair's here when you're ready." End the call.
- Stop calling / take me off the list / do not call: "Done — you're off the list. Be good." End the call at once. Never pitch again.
- Wrong person, wrong number, or an upset caller: apologise once, end the call.

PACE: 90 seconds is the target, 3 minutes the hard ceiling. Near it, close or exit.`;

export const MALONE_FIRST_MESSAGE =
  "Hey {{first_name}} — Salon Malone here, {{salon_name}}'s virtual concierge. Ninety seconds, I promise. We miss you.";

/** ~15 seconds read aloud. Offer plus the salon's real number, nothing else. */
export const MALONE_VOICEMAIL_MESSAGE =
  "Hey {{first_name}}, Salon Malone here — {{salon_name}}'s virtual concierge. We miss you, and we saved you something: {{offer_text}}. Call {{booking_phone}} and we'll get you back in the chair. Take care.";

const STRUCTURED_DATA_INSTRUCTIONS = `You are reading a transcript of an outbound win-back call made by a salon's virtual concierge. Extract only what was actually said.
- outcome: "booked" only if the client agreed to a specific day/time. "declined" if they said no or not now. "opted_out" if they asked not to be called again. "voicemail" if only a machine was reached. "no_answer" if nobody spoke. Otherwise "answered".
- slot_text: the agreed day and time in the client's own words, e.g. "Thursday at 2pm". Empty string if nothing was agreed.
- opt_out: true only if the client asked to be removed, to stop calls, or said do not call.
- notes: one short sentence a salon owner would care about. No speculation.`;

export const MALONE_ANALYSIS_PLAN = {
  minMessagesThreshold: 1,
  summaryPlan: {
    enabled: true,
    timeoutSeconds: 20,
    messages: [
      {
        role: 'system',
        content:
          'Summarise this win-back call for the salon owner in two sentences: what the client said, and what happens next. Plain language, no preamble.',
      },
      { role: 'user', content: 'Transcript:\n\n{{transcript}}' },
    ],
  },
  structuredDataPlan: {
    enabled: true,
    timeoutSeconds: 20,
    messages: [
      { role: 'system', content: STRUCTURED_DATA_INSTRUCTIONS },
      { role: 'user', content: 'Transcript:\n\n{{transcript}}' },
    ],
    schema: {
      type: 'object',
      properties: {
        outcome: {
          type: 'string',
          enum: ['booked', 'declined', 'opted_out', 'voicemail', 'no_answer', 'answered'],
          description: 'How the call resolved.',
        },
        slot_text: {
          type: 'string',
          description: 'Agreed day and time in the client\'s words, or an empty string.',
        },
        opt_out: {
          type: 'boolean',
          description: 'True only if the client asked never to be called again.',
        },
        notes: { type: 'string', description: 'One short sentence for the salon owner.' },
      },
      required: ['outcome', 'opt_out'],
    },
  },
  successEvaluationPlan: { enabled: false },
} as const;

export function maloneVariables(args: {
  first_name: string;
  salon_name: string;
  offer_text: string;
  booking_phone: string;
}): Record<string, string> {
  return {
    first_name: clean(args.first_name) ?? 'there',
    salon_name: clean(args.salon_name) ?? 'the salon',
    offer_text: clean(args.offer_text) ?? 'a little something to welcome you back',
    // Spoken aloud on voicemail — never leave a blank where a phone number should be.
    booking_phone: clean(args.booking_phone) ?? 'the number on our website',
  };
}

/** Complete Vapi assistant create body. Consumed by scripts/setup-vapi.mjs (LANE F). */
export function maloneAssistantPayload(serverUrl: string, serverSecret: string): object {
  return {
    name: 'Salon Malone',
    firstMessage: MALONE_FIRST_MESSAGE,
    firstMessageMode: 'assistant-speaks-first',
    // Small fast model, short replies: the whole latency strategy in one object. No `tools`.
    model: {
      provider: 'openai',
      model: 'gpt-4o-mini',
      temperature: 0.4,
      maxTokens: 120,
      messages: [{ role: 'system', content: MALONE_SYSTEM_PROMPT }],
    },
    transcriber: {
      provider: 'deepgram',
      model: 'nova-2-phonecall',
      language: 'en',
      smartFormat: true,
    },
    // Streaming turbo voice tuned for latency, not for showing off.
    voice: {
      provider: '11labs',
      voiceId: 'rachel',
      model: 'eleven_turbo_v2_5',
      optimizeStreamingLatency: 3,
      stability: 0.5,
      similarityBoost: 0.75,
      useSpeakerBoost: true,
    },
    backchannelingEnabled: true,
    fillerInjectionEnabled: true,
    backgroundDenoisingEnabled: true,
    startSpeakingPlan: { waitSeconds: 0.4, smartEndpointingEnabled: true },
    stopSpeakingPlan: { numWords: 2, voiceSeconds: 0.2, backoffSeconds: 1 },
    endCallFunctionEnabled: true,
    endCallMessage: "All love — the chair's here when you're ready. Take care.",
    endCallPhrases: ['goodbye', 'good bye', 'be good', 'see you then'],
    silenceTimeoutSeconds: 20,
    maxDurationSeconds: 180, // 3 minute hard ceiling from the brief
    voicemailDetection: { provider: 'vapi' },
    voicemailMessage: MALONE_VOICEMAIL_MESSAGE,
    serverUrl,
    serverUrlSecret: serverSecret,
    serverMessages: ['status-update', 'end-of-call-report'],
    artifactPlan: { recordingEnabled: true, transcriptPlan: { enabled: true } },
    analysisPlan: MALONE_ANALYSIS_PLAN,
    metadata: { app: 'salon-malone' },
  };
}

function clean(v: string | null | undefined): string | null {
  const trimmed = (v ?? '').trim();
  return trimmed.length > 0 ? trimmed : null;
}
