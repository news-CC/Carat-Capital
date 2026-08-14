import { describe, expect, it } from 'vitest';

import { callerSpeech, containsOptOutRequest, normalizeSpeech } from '@/lib/opt-out';

/**
 * The opt-out backstop is a compliance gate: a match writes a row to the global suppression list and
 * that number is never dialed again, by any client. Two failure directions, both real:
 *   MISSED  — we keep calling someone who asked us to stop. The expensive one.
 *   FALSE   — a happy customer is globally suppressed and (before the booking/outcome split) lost
 *             their appointment too.
 * Both directions are asserted here.
 */

/** Builds a Vapi-shaped speaker-prefixed transcript. */
const turns = (...lines: [speaker: string, text: string][]): string =>
  lines.map(([speaker, text]) => `${speaker}: ${text}`).join('\n');

const fromCaller = (text: string): string =>
  turns(
    ['AI', "Hey Jane — Salon Malone here, Ruby Room's virtual concierge."],
    ['User', text],
  );

describe('containsOptOutRequest — phrasings that MUST be honoured', () => {
  const optOuts = [
    // The plain imperatives.
    'Stop calling me.',
    'Stop calling.',
    'Quit calling me.',
    'Please stop contacting me.',
    'Cease calling this number.',
    'No more calls, please.',
    'No more phone calls.',
    // Contractions, with and without the apostrophe.
    "Please don't call again.",
    "Don't ever call me again.",
    'dont call again',
    'Do not call me again.',
    "Don't call me anymore.",
    "Don't call me any more.",
    'Never call me again.',
    'Never contact me.',
    // Removal requests.
    'Take my number off your list.',
    'Take me off your list.',
    'Get my name off your calling list.',
    'Remove me from your list.',
    'Delete my number.',
    'Erase my information.',
    'Lose my number.',
    'Forget my number.',
    'Unsubscribe me.',
    'Opt me out.',
    'I want to opt out of these calls.',
    'I want off your call list.',
    'Put me on your do not call list.',
    // The bare directive, with no redirect qualifier after it.
    "Don't call me.",
    "Don't call me at all.",
    'Do not call this number.',
  ];

  for (const phrase of optOuts) {
    it(`honours ${JSON.stringify(phrase)}`, () => {
      expect(containsOptOutRequest(fromCaller(phrase))).toBe(true);
    });
  }

  it('is not defeated by a smart-quote apostrophe', () => {
    // U+2019, U+02BC, U+2032 and a backtick all reach us from different STT vendors.
    expect(containsOptOutRequest(fromCaller('Don’t call me again.'))).toBe(true);
    expect(containsOptOutRequest(fromCaller('Donʼt call me again.'))).toBe(true);
    expect(containsOptOutRequest(fromCaller('Don′t call me again.'))).toBe(true);
    expect(containsOptOutRequest(fromCaller('Don`t call me again.'))).toBe(true);
  });

  it('is not defeated by casing or by a line wrapped mid-sentence', () => {
    expect(containsOptOutRequest(fromCaller('STOP CALLING ME'))).toBe(true);
    expect(containsOptOutRequest('User: take my number\noff your list please')).toBe(true);
  });

  it('reads a transcript with no speaker prefixes whole — fail closed', () => {
    // The flat message.transcript fallback carries no "User:" markers. Missing a real opt-out is
    // the dangerous direction, so the entire text is scanned.
    expect(containsOptOutRequest('yeah no thanks, take me off your list')).toBe(true);
  });
});

describe('containsOptOutRequest — speaker scoping', () => {
  it('ignores Malone confirming an opt-out, so the agent cannot suppress anybody', () => {
    // Malone's scripted line for a real opt-out. If this matched, every call where Malone read the
    // wrong line — or any call at all, on a transcript we mis-split — would suppress the customer.
    const transcript = turns(
      ['AI', "Done — you're off the list. Be good."],
      ['User', 'Thanks, appreciate it.'],
    );
    expect(containsOptOutRequest(transcript)).toBe(false);
  });

  it('ignores Malone offering to stop calling', () => {
    const transcript = turns(
      ['AI', 'Want me to take you off the list and never call again?'],
      ['User', 'No, Thursday is great.'],
    );
    expect(containsOptOutRequest(transcript)).toBe(false);
  });

  it('still honours the caller when Malone speaks in the same transcript', () => {
    const transcript = turns(
      ['AI', 'We have Thursday at two or Friday at five.'],
      ['User', 'Neither. Take me off your list.'],
      ['AI', "Done — you're off the list."],
    );
    expect(containsOptOutRequest(transcript)).toBe(true);
  });

  it('never matches a pattern spanning two turns', () => {
    // "stop" ends the caller's turn and "calling" opens the next one. Joined naively this would
    // read as "stop calling" and suppress a customer who said neither.
    const transcript = turns(
      ['User', 'Please stop'],
      ['AI', 'Calling you at this hour was my fault.'],
      ['User', 'It is fine.'],
    );
    expect(containsOptOutRequest(transcript)).toBe(false);
  });

  it('recognises every speaker label Vapi uses for the human', () => {
    for (const speaker of ['User', 'Customer', 'Caller', 'Human', 'user', 'CUSTOMER']) {
      expect(containsOptOutRequest(`${speaker}: take me off your list`)).toBe(true);
    }
  });
});

describe('containsOptOutRequest — a redirect is not an opt-out', () => {
  const redirects = [
    "Don't call me at work, use my cell.",
    "Don't call me on this line, try the other one.",
    "Don't call me before nine.",
    "Don't call me after six.",
    "Don't call me during my shift.",
    "Don't call me until next week.",
    "Don't call me on the weekend.",
    "Don't call me in the morning.",
    "Don't call me unless something opens up.",
    "Don't call me when I'm at the salon.",
  ];

  for (const phrase of redirects) {
    it(`does not suppress on ${JSON.stringify(phrase)}`, () => {
      expect(containsOptOutRequest(fromCaller(phrase))).toBe(false);
    });
  }

  it('does not suppress a booked call that contains a redirect aside', () => {
    const transcript = turns(
      ['AI', 'Thursday at two, or Friday at five?'],
      ['User', "Thursday at two works. Don't call me at work though, use my cell."],
      ['AI', 'Locked in for Thursday at two.'],
    );
    expect(containsOptOutRequest(transcript)).toBe(false);
  });

  it('still suppresses when the caller means it, in the same shape of sentence', () => {
    const transcript = turns(
      ['AI', 'Thursday at two, or Friday at five?'],
      ['User', 'Actually, take me off your list.'],
    );
    expect(containsOptOutRequest(transcript)).toBe(true);
  });
});

describe('containsOptOutRequest — an ordinary call is never an opt-out', () => {
  const benign = [
    'Thursday at two works for me.',
    'I stopped going because my stylist left.',
    'I quit my job last month, so mornings are open now.',
    'Can you call the salon and check?',
    'My number is the same one you called.',
    'I never got a call about the sale.',
    'How much is the list price?',
    'No thanks, I am all set.',
    '',
  ];

  for (const phrase of benign) {
    it(`leaves ${JSON.stringify(phrase)} alone`, () => {
      expect(containsOptOutRequest(fromCaller(phrase))).toBe(false);
    });
  }

  it('does not fire on a warm no — a decline is not a do-not-contact request', () => {
    const transcript = turns(
      ['AI', 'Thursday at two, or Friday at five?'],
      ['User', 'Not right now, thanks.'],
      ['AI', "All love — the chair's here when you're ready."],
    );
    expect(containsOptOutRequest(transcript)).toBe(false);
  });
});

describe('callerSpeech / normalizeSpeech', () => {
  it('keeps only the caller turns, joined with a sentence break', () => {
    const transcript = turns(
      ['AI', 'Hey Jane.'],
      ['User', 'Hi'],
      ['AI', 'Ninety seconds, I promise.'],
      ['User', 'Go ahead'],
    );
    expect(callerSpeech(transcript)).toBe('hi. go ahead');
  });

  it('keeps a wrapped continuation line with the turn it belongs to', () => {
    expect(callerSpeech('User: I am busy\nall week actually\nAI: Understood.')).toBe(
      'i am busy all week actually',
    );
  });

  it('returns the whole text when nothing is speaker-prefixed', () => {
    expect(callerSpeech('just some flat transcript text')).toBe('just some flat transcript text');
  });

  it('lowercases, folds smart quotes to ASCII and collapses whitespace', () => {
    expect(normalizeSpeech('  DON’T   CALL\n\nME  ')).toBe(" don't call me ");
  });
});
