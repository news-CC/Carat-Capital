import type { ReactNode } from "react";

type Props = {
  label: string;
  value: ReactNode;
  hint?: ReactNode;
};

export function Stat({ label, value, hint }: Props) {
  return (
    <div className="stat">
      <span className="stat-num">{value}</span>
      <span className="stat-label">{label}</span>
      {hint ? <span className="help">{hint}</span> : null}
    </div>
  );
}
