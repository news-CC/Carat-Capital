import type { ReactNode } from "react";

type Props = {
  label: string;
  htmlFor: string;
  children: ReactNode;
  help?: ReactNode;
  error?: string | null;
};

export function Field({ label, htmlFor, children, help, error }: Props) {
  return (
    <div className="field">
      <label className="label" htmlFor={htmlFor}>
        {label}
      </label>
      {children}
      {help && !error ? <p className="help">{help}</p> : null}
      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}
