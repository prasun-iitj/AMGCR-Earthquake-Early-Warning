import Link from "next/link";
import type { ReactNode } from "react";

export type BreadcrumbItem = {
  label: string;
  href?: string;
};

type BreadcrumbsProps = {
  items: BreadcrumbItem[];
  /** When true, prepends Home if not already first. */
  includeHome?: boolean;
};

export function Breadcrumbs({ items, includeHome = false }: BreadcrumbsProps) {
  const resolvedItems =
    includeHome && items[0]?.label !== "Home"
      ? [{ label: "Home", href: "/" }, ...items]
      : items;

  return (
    <nav aria-label="Breadcrumb" className="mb-8">
      <ol className="flex flex-wrap items-center gap-2 text-sm text-text-muted">
        {resolvedItems.map((item, index) => {
          const isLast = index === resolvedItems.length - 1;

          return (
            <li key={`${item.label}-${index}`} className="flex items-center gap-2">
              {index > 0 && (
                <span aria-hidden="true" className="text-border">
                  /
                </span>
              )}
              {item.href && !isLast ? (
                <Link
                  href={item.href}
                  className="transition-colors hover:text-primary"
                >
                  {item.label}
                </Link>
              ) : (
                <span
                  className={isLast ? "font-medium text-text" : undefined}
                  aria-current={isLast ? "page" : undefined}
                >
                  {item.label}
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

type DocPageShellProps = {
  breadcrumbs: BreadcrumbItem[];
  sourcePath: string;
  children: ReactNode;
  sidebar?: ReactNode;
};

export function DocPageShell({
  breadcrumbs,
  sourcePath,
  children,
  sidebar,
}: DocPageShellProps) {
  return (
    <div className="border-b border-border bg-surface-elevated">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <Breadcrumbs items={breadcrumbs} />
        <p className="mb-8 text-xs text-text-muted">
          Rendered from repository source:{" "}
          <code className="rounded bg-surface px-1.5 py-0.5 font-mono text-[0.8rem]">
            {sourcePath}
          </code>
        </p>
        <div className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_240px] xl:grid-cols-[minmax(0,1fr)_280px]">
          <div className="min-w-0">{children}</div>
          {sidebar ? (
            <aside className="hidden lg:block">
              <div className="sticky top-24">{sidebar}</div>
            </aside>
          ) : null}
        </div>
      </div>
    </div>
  );
}
