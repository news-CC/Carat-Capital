import { afterEach, describe, expect, it, vi } from 'vitest';

/**
 * Regression guard for a live failure: a demo call sent only `assistantOverrides.model.messages`
 * and Vapi rejected the WHOLE call with "assistantOverrides.model.provider must be one of the
 * following values: ...". It surfaced mid-demo. These assert the payload shape and the fallback.
 */

const ENV = {
  VAPI_API_KEY: 'test-key',
  ADMIN_PASSWORD_HASH: 'plain$x',
};

function args(extra: Record<string, unknown> = {}) {
  return {
    phone: '+12125551234',
    assistantId: 'a-1',
    phoneNumberId: 'p-1',
    variables: { first_name: 'Dana' },
    metadata: { demo: 'true' },
    ...extra,
  } as never;
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.resetModules();
});

function stubFetch(responses: { status: number; body: string }[]) {
  const calls: Record<string, unknown>[] = [];
  let i = 0;
  vi.stubGlobal(
    'fetch',
    vi.fn(async (_url: string, init: { body: string }) => {
      calls.push(JSON.parse(init.body));
      const r = responses[Math.min(i++, responses.length - 1)];
      return { status: r.status, text: async () => r.body } as Response;
    }),
  );
  return calls;
}

describe('assistantOverrides.model', () => {
  it('sends a COMPLETE model block, never just messages', async () => {
    Object.assign(process.env, ENV);
    const calls = stubFetch([{ status: 200, body: JSON.stringify({ id: 'call-1' }) }]);
    const { startOutboundCall } = await import('@/lib/vapi');

    const res = await startOutboundCall(args({ systemPrompt: 'you are a concierge' }));
    expect(res.ok).toBe(true);

    const model = (calls[0].assistantOverrides as Record<string, Record<string, unknown>>).model;
    // The exact fields Vapi rejected the call for omitting.
    expect(model.provider).toBe('openai');
    expect(model.model).toBe('gpt-4o-mini');
    expect(Array.isArray(model.messages)).toBe(true);
  });

  it('keeps provider/model in step with the assistant definition', async () => {
    const { MALONE_MODEL, maloneAssistantPayload } = await import('@/lib/malone');
    const payload = maloneAssistantPayload('https://x/y', 's') as {
      model: { provider: string; model: string };
    };
    expect(payload.model.provider).toBe(MALONE_MODEL.provider);
    expect(payload.model.model).toBe(MALONE_MODEL.model);
  });

  it('omits the model block entirely when no prompt override is given', async () => {
    Object.assign(process.env, ENV);
    const calls = stubFetch([{ status: 200, body: JSON.stringify({ id: 'call-2' }) }]);
    const { startOutboundCall } = await import('@/lib/vapi');
    await startOutboundCall(args());
    const overrides = calls[0].assistantOverrides as Record<string, unknown>;
    // Campaign dials must not override the model — it costs Vapi's warm prompt cache.
    expect(overrides.model).toBeUndefined();
    expect(overrides.variableValues).toEqual({ first_name: 'Dana' });
  });

  it('passes the chosen voice through as a complete provider+voiceId pair', async () => {
    Object.assign(process.env, ENV);
    const calls = stubFetch([{ status: 200, body: JSON.stringify({ id: 'call-3' }) }]);
    const { startOutboundCall } = await import('@/lib/vapi');
    await startOutboundCall(args({ voiceId: 'Rohan' }));
    expect((calls[0].assistantOverrides as Record<string, unknown>).voice).toEqual({
      provider: 'vapi',
      voiceId: 'Rohan',
    });
  });
});

describe('a rejected customisation must not kill the call', () => {
  it('retries without overrides on a 400 so the demo still happens', async () => {
    Object.assign(process.env, ENV);
    const calls = stubFetch([
      { status: 400, body: JSON.stringify({ message: ['assistantOverrides.model.provider must be...'] }) },
      { status: 200, body: JSON.stringify({ id: 'call-fallback' }) },
    ]);
    const { startOutboundCall } = await import('@/lib/vapi');

    const res = await startOutboundCall(args({ systemPrompt: 'x', voiceId: 'Rohan', firstMessage: 'hi' }));

    // The operator's phone still rings — with the standard script rather than nothing at all.
    expect(res.ok).toBe(true);
    if (res.ok) expect(res.data.vapiCallId).toBe('call-fallback');
    expect(calls).toHaveLength(2);
    const retry = calls[1].assistantOverrides as Record<string, unknown>;
    expect(retry.model).toBeUndefined();
    expect(retry.voice).toBeUndefined();
    expect(retry.variableValues).toEqual({ first_name: 'Dana' });
  });

  it('does NOT retry a 400 on a plain campaign dial — nothing to degrade to', async () => {
    Object.assign(process.env, ENV);
    const calls = stubFetch([{ status: 400, body: JSON.stringify({ message: 'bad number' }) }]);
    const { startOutboundCall } = await import('@/lib/vapi');
    const res = await startOutboundCall(args());
    expect(res.ok).toBe(false);
    expect(calls).toHaveLength(1);
  });

  it('does not retry a non-400 failure', async () => {
    Object.assign(process.env, ENV);
    const calls = stubFetch([{ status: 500, body: 'upstream boom' }]);
    const { startOutboundCall } = await import('@/lib/vapi');
    const res = await startOutboundCall(args({ systemPrompt: 'x' }));
    expect(res.ok).toBe(false);
    expect(calls).toHaveLength(1);
  });
});
