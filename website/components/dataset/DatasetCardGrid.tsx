"use client";

import type { DatasetRegistryEntry } from "@/lib/dataset/types";

type DatasetCardGridProps = {
  registry: DatasetRegistryEntry[];
  selectedId: string;
  onSelect: (id: string) => void;
};

export function DatasetCardGrid({
  registry,
  selectedId,
  onSelect,
}: DatasetCardGridProps) {
  return (
    <section className="border-t border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Datasets
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            Pilot and planned catalogues
          </h2>
          <p className="mt-3 text-text-muted">
            Select a dataset to view details. Future regions plug into the same
            card and detail components.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          {registry.map((entry) => {
            const isSelected = entry.id === selectedId;
            const isPlanned = entry.status === "planned";

            return (
              <button
                key={entry.id}
                type="button"
                onClick={() => onSelect(entry.id)}
                className={[
                  "rounded-xl border p-6 text-left transition-colors",
                  isSelected
                    ? "border-primary bg-primary text-white shadow-sm"
                    : "border-border bg-surface-elevated hover:border-primary/30",
                  isPlanned && !isSelected ? "opacity-80" : "",
                ].join(" ")}
                aria-pressed={isSelected}
              >
                <div className="flex items-center justify-between gap-2">
                  <p
                    className={[
                      "text-xs font-semibold uppercase tracking-wider",
                      isSelected ? "text-white/80" : "text-text-muted",
                    ].join(" ")}
                  >
                    {entry.region}
                  </p>
                  <span
                    className={[
                      "rounded-full px-2 py-0.5 text-[0.65rem] font-semibold uppercase",
                      isSelected
                        ? "bg-white/15 text-white"
                        : entry.status === "active"
                          ? "bg-success/15 text-success"
                          : "bg-warning/15 text-warning",
                    ].join(" ")}
                  >
                    {entry.status}
                  </span>
                </div>
                <h3 className="mt-3 font-serif text-xl font-semibold">
                  {entry.name}
                </h3>
                <p
                  className={[
                    "mt-3 text-sm leading-relaxed",
                    isSelected ? "text-white/85" : "text-text-muted",
                  ].join(" ")}
                >
                  {entry.teaser}
                </p>
                {isPlanned && (
                  <p
                    className={[
                      "mt-4 text-xs",
                      isSelected ? "text-white/70" : "text-text-muted",
                    ].join(" ")}
                  >
                    Planned — metadata shell ready for future acquisition.
                  </p>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
