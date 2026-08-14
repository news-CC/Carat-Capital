import type { ReactNode } from "react";

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center gap-3 px-6 py-14 text-center">
      <hr className="rule w-10" />
      <h3 className="font-display text-lg text-ink">{title}</h3>
      {description ? <p className="help max-w-sm">{description}</p> : null}
      {action}
    </div>
  );
}
