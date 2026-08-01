"use client";

import type { MapDatasetOption, MapFilterBounds, MapFilterState } from "@/lib/map/types";

type MapFiltersProps = {
  filters: MapFilterState;
  bounds: MapFilterBounds;
  datasetOptions: MapDatasetOption[];
  visibleCount: number;
  totalCount: number;
  onChange: (filters: MapFilterState) => void;
  onReset: () => void;
};

export function MapFilters({
  filters,
  bounds,
  datasetOptions,
  visibleCount,
  totalCount,
  onChange,
  onReset,
}: MapFiltersProps) {
  return (
    <div className="rounded-xl border border-border bg-surface-elevated p-4 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Filters
          </p>
          <p className="mt-1 text-sm text-text-muted">
            Showing {visibleCount} of {totalCount} events · static client-side filtering
          </p>
        </div>
        <button
          type="button"
          onClick={onReset}
          className="rounded-full border border-border px-3 py-1.5 text-sm font-medium text-text-muted transition-colors hover:border-primary/30 hover:text-text"
        >
          Reset filters
        </button>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <label className="block text-sm">
          <span className="mb-2 block font-medium text-text">Dataset</span>
          <select
            value={filters.dataset}
            onChange={(event) =>
              onChange({ ...filters, dataset: event.target.value as MapFilterState["dataset"] })
            }
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-text"
          >
            {datasetOptions.map((option) => (
              <option
                key={option.id}
                value={option.id}
                disabled={option.status === "planned" && option.eventCount === 0}
              >
                {option.label}
                {option.eventCount > 0
                  ? ` (${option.eventCount})`
                  : option.status === "planned"
                    ? " — planned"
                    : ""}
              </option>
            ))}
          </select>
        </label>

        <label className="block text-sm">
          <span className="mb-2 block font-medium text-text">
            Magnitude min ({bounds.magnitudeMin} – {bounds.magnitudeMax})
          </span>
          <input
            type="range"
            min={bounds.magnitudeMin}
            max={bounds.magnitudeMax}
            step={0.1}
            value={filters.magnitudeMin}
            onChange={(event) =>
              onChange({
                ...filters,
                magnitudeMin: Math.min(
                  Number.parseFloat(event.target.value),
                  filters.magnitudeMax,
                ),
              })
            }
            className="w-full accent-primary"
          />
          <span className="mt-1 block text-xs text-text-muted">
            Minimum: M{filters.magnitudeMin.toFixed(1)}
          </span>
        </label>

        <label className="block text-sm">
          <span className="mb-2 block font-medium text-text">Magnitude max</span>
          <input
            type="range"
            min={bounds.magnitudeMin}
            max={bounds.magnitudeMax}
            step={0.1}
            value={filters.magnitudeMax}
            onChange={(event) =>
              onChange({
                ...filters,
                magnitudeMax: Math.max(
                  Number.parseFloat(event.target.value),
                  filters.magnitudeMin,
                ),
              })
            }
            className="w-full accent-primary"
          />
          <span className="mt-1 block text-xs text-text-muted">
            Maximum: M{filters.magnitudeMax.toFixed(1)}
          </span>
        </label>

        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
          <label className="block text-sm">
            <span className="mb-2 block font-medium text-text">Time from</span>
            <input
              type="date"
              value={filters.timeStart}
              min={bounds.timeStart}
              max={filters.timeEnd}
              onChange={(event) =>
                onChange({ ...filters, timeStart: event.target.value })
              }
              className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-text"
            />
          </label>
          <label className="block text-sm">
            <span className="mb-2 block font-medium text-text">Time to</span>
            <input
              type="date"
              value={filters.timeEnd}
              min={bounds.timeStart}
              max={bounds.timeEnd}
              onChange={(event) =>
                onChange({ ...filters, timeEnd: event.target.value })
              }
              className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-text"
            />
          </label>
        </div>
      </div>
    </div>
  );
}
