import Link from "next/link";
import type { ResultTable } from "@/lib/results/loader";

type TablesSectionProps = {
  tables: ResultTable[];
};

export function TablesSection({ tables }: TablesSectionProps) {
  return (
    <section className="border-t border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Tables
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            CSV outputs
          </h2>
          <p className="mt-3 text-text-muted">
            Preview the first rows of each table. Download the full CSV or open
            the related phase report for interpretation.
          </p>
        </div>

        <div className="space-y-8">
          {tables.map((table) => (
            <article
              key={table.filename}
              className="overflow-hidden rounded-xl border border-border bg-surface-elevated shadow-sm"
            >
              <div className="flex flex-col gap-4 border-b border-border px-5 py-4 md:flex-row md:items-start md:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-accent">
                    {table.phaseLabel}
                  </p>
                  <h3 className="mt-1 font-serif text-xl font-semibold text-text">
                    {table.title}
                  </h3>
                  <p className="mt-2 max-w-3xl text-sm text-text-muted">
                    {table.description}
                  </p>
                </div>
                <div className="flex flex-wrap gap-3">
                  {table.available ? (
                    <a
                      href={table.downloadUrl}
                      download
                      className="inline-flex rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-light"
                    >
                      Download CSV
                    </a>
                  ) : (
                    <span className="inline-flex rounded-lg border border-border px-4 py-2 text-sm text-text-muted">
                      CSV unavailable
                    </span>
                  )}
                  {table.reportExternal ? (
                    <a
                      href={table.reportHref}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex rounded-lg border border-border px-4 py-2 text-sm font-medium text-text transition-colors hover:border-primary/30"
                    >
                      Related report ↗
                    </a>
                  ) : (
                    <Link
                      href={table.reportHref}
                      className="inline-flex rounded-lg border border-border px-4 py-2 text-sm font-medium text-text transition-colors hover:border-primary/30"
                    >
                      Related report
                    </Link>
                  )}
                </div>
              </div>

              {table.available && table.headers.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-left text-sm">
                    <thead className="bg-surface text-text-muted">
                      <tr>
                        {table.headers.map((header) => (
                          <th
                            key={header}
                            scope="col"
                            className="whitespace-nowrap px-4 py-3 font-medium"
                          >
                            {header}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {table.previewRows.map((row, rowIndex) => (
                        <tr
                          key={`${table.filename}-row-${rowIndex}`}
                          className="border-t border-border"
                        >
                          {row.map((cell, cellIndex) => (
                            <td
                              key={`${table.filename}-${rowIndex}-${cellIndex}`}
                              className="max-w-[16rem] truncate whitespace-nowrap px-4 py-3 text-text-muted"
                              title={cell}
                            >
                              {cell}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="px-5 py-6 text-sm text-text-muted">
                  Table preview unavailable. Regenerate outputs via analysis
                  scripts.
                </div>
              )}

              {table.available && (
                <div className="border-t border-border px-5 py-3 text-xs text-text-muted">
                  Showing {table.previewRows.length} of {table.rowCount} rows ·{" "}
                  <code className="font-mono">{table.filename}</code>
                </div>
              )}
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
