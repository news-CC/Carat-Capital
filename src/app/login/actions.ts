"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { SESSION_COOKIE, sessionCookieOptions, signSession, verifyAdminCredentials } from "@/lib/auth";

// Only async functions may be exported from a "use server" module — types are erased, so this is fine.
export type LoginState = { error: string | null };

/** Never leak which half was wrong. */
const GENERIC_ERROR = "Those credentials did not work.";
const FAILURE_DELAY_MS = 400;

export async function login(_prev: LoginState, formData: FormData): Promise<LoginState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const next = safeNext(formData.get("next"));

  if (!email || !password || !credentialsOk(email, password)) {
    // Crude brake on password guessing: every failure costs the caller 400ms.
    await delay(FAILURE_DELAY_MS);
    return { error: GENERIC_ERROR };
  }

  const store = await cookies();
  store.set(SESSION_COOKIE, signSession(email), sessionCookieOptions);

  redirect(next);
}

function credentialsOk(email: string, password: string): boolean {
  try {
    return verifyAdminCredentials(email, password);
  } catch {
    // Missing ADMIN_EMAIL / ADMIN_PASSWORD_HASH must read as a failed login, not a 500.
    return false;
  }
}

/** Open-redirect gate: only same-origin absolute paths survive. */
function safeNext(raw: unknown): string {
  const value = typeof raw === "string" ? raw.trim() : "";
  if (!value.startsWith("/") || value.startsWith("//")) return "/admin";
  return value;
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
