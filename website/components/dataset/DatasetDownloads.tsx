import Link from "next/link";
import type { DatasetRecord } from "@/lib/dataset/types";

type DatasetDownloadsProps = {
  dataset: DatasetRecord;
};

export function DatasetDownloads({ dataset }: DatasetDownloadsProps) {
  if (dataset.downloads.length === 0) {
    return null;
  }

  return (
    <section id="downloads" className="border-t border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Downloads
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            Repository assets
          </h2>
          <p className="mt-3 text-text-muted">
            Direct links to manifests, tables, and reports from the{" "}
            {dataset.name}. Files are synced from the repository at build time
            where available.
          </p>
        </div>

        <ul className="grid gap-4 md:grid-cols-2">
          {dataset.downloads.map((item) => (
            <li
              key={`${item.path}-${item.label}`}
              className="flex items-center justify-between gap-4 rounded-xl border border-border bg-surface-elevated px-5 py-4"
            >
              <div className="min-w-0">
                <p className="font-medium text-text">{item.label}</p>
                <p className="mt-1 truncate font-mono text-xs text-text-muted">
                  {item.path}
                </p>
              </div>
              {item.external ? (
                <a
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="shrink-0 rounded-lg border border-border px-3 py-2 text-sm font-medium text-primary transition-colors hover:border-primary/30"
                >
                  Open ↗
                </a>
              ) : item.href.startsWith("/") && item.path.endsWith(".csv") ? (
                <a
                  href={item.href}
                  download
                  className="shrink-0 rounded-lg bg-primary px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-light"
                >
                  Download
                </a>
              ) : (
                <Link
                  href={item.href}
                  className="shrink-0 rounded-lg border border-border px-3 py-2 text-sm font-medium text-primary transition-colors hover:border-primary/30"
                >
                  Open →
                </Link>
              )}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
