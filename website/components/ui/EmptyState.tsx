import type { ReactNode } from "react";

type EmptyStateProps = {
  title: string;
  description: string;
  action?: ReactNode;
  icon?: ReactNode;
};

export function EmptyState({ title, description, action, icon }: EmptyStateProps) {
  return (
    <div
      role="status"
      className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-surface px-6 py-12 text-center"
    >
      {icon ? (
        <div className="mb-4 text-text-muted" aria-hidden="true">
          {icon}
        </div>
      ) : (
        <div
          aria-hidden="true"
          className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-surface-elevated text-text-muted"
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
            <path d="M4 7h16M4 12h10M4 17h16" strokeLinecap="round" />
          </svg>
        </div>
      )}
      <h3 className="font-serif text-lg font-semibold text-text">{title}</h3>
      <p className="mt-2 max-w-md text-sm leading-relaxed text-text-muted">{description}</p>
      {action ? <div className="mt-6">{action}</div> : null}
    </div>
  );
}
