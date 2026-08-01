import Link from "next/link";
import type { TocHeading } from "@/lib/content/loader";

type TableOfContentsProps = {
  headings: TocHeading[];
};

export function TableOfContents({ headings }: TableOfContentsProps) {
  if (headings.length === 0) {
    return null;
  }

  return (
    <nav aria-label="Table of contents">
      <p className="mb-3 text-sm font-semibold uppercase tracking-wider text-text-muted">
        On this page
      </p>
      <ul className="space-y-2 text-sm">
        {headings.map((heading) => (
          <li
            key={`${heading.slug}-${heading.level}`}
            style={{ paddingLeft: `${(heading.level - 2) * 0.75}rem` }}
          >
            <a
              href={`#${heading.slug}`}
              className="block leading-snug text-text-muted transition-colors hover:text-primary"
            >
              {heading.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

type DocNavigationProps = {
  previous: { title: string; href: string } | null;
  next: { title: string; href: string } | null;
};

export function DocNavigation({ previous, next }: DocNavigationProps) {
  if (!previous && !next) {
    return null;
  }

  return (
    <nav
      aria-label="Document navigation"
      className="mt-12 grid gap-4 border-t border-border pt-8 sm:grid-cols-2"
    >
      {previous ? (
        <Link
          href={previous.href}
          className="group rounded-xl border border-border bg-surface p-5 transition-colors hover:border-primary/30 hover:bg-surface-elevated"
        >
          <p className="text-xs font-semibold uppercase tracking-wider text-text-muted">
            Previous
          </p>
          <p className="mt-2 font-medium text-text group-hover:text-primary">
            ← {previous.title}
          </p>
        </Link>
      ) : (
        <div />
      )}
      {next ? (
        <Link
          href={next.href}
          className="group rounded-xl border border-border bg-surface p-5 text-right transition-colors hover:border-primary/30 hover:bg-surface-elevated sm:col-start-2"
        >
          <p className="text-xs font-semibold uppercase tracking-wider text-text-muted">
            Next
          </p>
          <p className="mt-2 font-medium text-text group-hover:text-primary">
            {next.title} →
          </p>
        </Link>
      ) : null}
    </nav>
  );
}
