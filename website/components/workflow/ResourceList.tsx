import Link from "next/link";
import type { WorkflowLink } from "@/lib/workflow/loader";

type ResourceListProps = {
  title: string;
  items: WorkflowLink[];
  emptyMessage?: string;
};

export function ResourceList({
  title,
  items,
  emptyMessage = "None listed for this stage.",
}: ResourceListProps) {
  if (items.length === 0) {
    return (
      <section>
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
          {title}
        </h3>
        <p className="mt-2 text-sm text-text-muted">{emptyMessage}</p>
      </section>
    );
  }

  return (
    <section>
      <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
        {title}
      </h3>
      <ul className="mt-3 space-y-2">
        {items.map((item) => (
          <li key={`${title}-${item.path}`}>
            <ResourceLink item={item} />
          </li>
        ))}
      </ul>
    </section>
  );
}

function ResourceLink({ item }: { item: WorkflowLink }) {
  const className = [
    "group flex items-start justify-between gap-3 rounded-lg border border-border bg-surface px-3 py-2 text-sm transition-colors hover:border-primary/30 hover:bg-white",
    !item.exists ? "opacity-70" : "",
  ].join(" ");

  const content = (
    <>
      <span className="min-w-0 text-text group-hover:text-primary">
        {item.label}
      </span>
      <span className="shrink-0 font-mono text-[0.7rem] text-text-muted">
        {item.external ? "GitHub ↗" : "Site →"}
      </span>
    </>
  );

  if (item.external) {
    return (
      <a
        href={item.href}
        target="_blank"
        rel="noopener noreferrer"
        className={className}
      >
        {content}
      </a>
    );
  }

  return (
    <Link href={item.href} className={className}>
      {content}
    </Link>
  );
}
