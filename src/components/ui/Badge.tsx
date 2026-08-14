import type { ReactNode } from "react";

export type BadgeTone = "ok" | "warn" | "bad" | "mute" | "plain";

const TONE: Record<BadgeTone, string> = {
  ok: "badge-ok",
  warn: "badge-warn",
  bad: "badge-bad",
  mute: "badge-mute",
  plain: "",
};

export function Badge({
  tone = "plain",
  children,
  className = "",
}: {
  tone?: BadgeTone;
  children: ReactNode;
  className?: string;
}) {
  const classes = ["badge", TONE[tone], className].filter(Boolean).join(" ");
  return <span className={classes}>{children}</span>;
}
