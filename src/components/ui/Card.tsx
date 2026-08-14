import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  /** Set false when the card holds a full-bleed table and pads its own sections. */
  padded?: boolean;
  className?: string;
};

export function Card({ children, padded = true, className = "" }: Props) {
  const classes = ["card", padded ? "card-pad" : "", className].filter(Boolean).join(" ");
  return <div className={classes}>{children}</div>;
}

export function CardHeader({ title, action }: { title: ReactNode; action?: ReactNode }) {
  return (
    <div className="flex items-baseline justify-between gap-4 border-b border-line px-6 py-4">
      <h2 className="font-display text-lg">{title}</h2>
      {action}
    </div>
  );
}
