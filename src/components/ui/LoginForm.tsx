"use client";

import { useActionState } from "react";
import { login, type LoginState } from "@/app/login/actions";
import { Field } from "./Field";

const INITIAL: LoginState = { error: null };

export function LoginForm({ next }: { next: string }) {
  const [state, formAction, pending] = useActionState(login, INITIAL);

  return (
    <form action={formAction} className="grid gap-5" noValidate>
      <input type="hidden" name="next" value={next} />

      <Field label="Email" htmlFor="email">
        <input
          id="email"
          name="email"
          type="email"
          className="input"
          autoComplete="username"
          autoFocus
          required
        />
      </Field>

      <Field label="Password" htmlFor="password">
        <input
          id="password"
          name="password"
          type="password"
          className="input"
          autoComplete="current-password"
          required
        />
      </Field>

      {state.error ? (
        <p className="error-text" role="alert">
          {state.error}
        </p>
      ) : null}

      <button type="submit" className="btn btn-primary mt-1 w-full" disabled={pending}>
        {pending ? "Checking…" : "Sign in"}
      </button>
    </form>
  );
}
