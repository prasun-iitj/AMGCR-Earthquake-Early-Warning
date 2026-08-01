"use client";

import type { WaveformDatasetGroup } from "@/lib/waveforms/types";

type WaveformListProps = {
  groups: WaveformDatasetGroup[];
  selectedId: string;
  onSelect: (id: string) => void;
  seriesAvailableCount: number;
  totalWaveforms: number;
};

function formatOriginTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toISOString().replace("T", " ").slice(0, 19);
}

export function WaveformList({
  groups,
  selectedId,
  onSelect,
  seriesAvailableCount,
  totalWaveforms,
}: WaveformListProps) {
  return (
    <section className="border-t border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Waveform catalogue
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            Events grouped by dataset
          </h2>
          <p className="mt-3 text-text-muted">
            {totalWaveforms} pilot waveforms · {seriesAvailableCount} with
            interactive series preview from preprocessing NPZ exports.
          </p>
        </div>

        <div className="space-y-10">
          {groups.map((group) => (
            <div key={group.datasetId}>
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h3 className="font-serif text-2xl font-semibold text-text">
                    {group.datasetName}
                  </h3>
                  <p className="mt-1 text-sm text-text-muted">
                    {group.status === "active"
                      ? `${group.waveformCount} waveforms available`
                      : "Planned — catalogue slot reserved for future acquisition"}
                  </p>
                </div>
                <span
                  className={[
                    "rounded-full px-3 py-1 text-xs font-semibold uppercase",
                    group.status === "active"
                      ? "bg-success/15 text-success"
                      : "bg-warning/15 text-warning",
                  ].join(" ")}
                >
                  {group.status}
                </span>
              </div>

              {group.waveforms.length === 0 ? (
                <div className="rounded-xl border border-dashed border-border bg-surface-elevated p-6 text-sm text-text-muted">
                  Waveforms will appear here once this dataset is acquired using
                  the same manifest-and-report pattern as the California pilot.
                </div>
              ) : (
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                  {group.waveforms.map((waveform) => {
                    const isSelected = waveform.id === selectedId;

                    return (
                      <button
                        key={waveform.id}
                        type="button"
                        onClick={() => onSelect(waveform.id)}
                        aria-pressed={isSelected}
                        className={[
                          "rounded-xl border p-4 text-left transition-colors",
                          isSelected
                            ? "border-primary bg-primary text-white shadow-sm"
                            : "border-border bg-surface-elevated hover:border-primary/30",
                        ].join(" ")}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <p
                            className={[
                              "font-mono text-xs uppercase tracking-wide",
                              isSelected ? "text-white/80" : "text-text-muted",
                            ].join(" ")}
                          >
                            {waveform.id}
                          </p>
                          {waveform.seriesAvailable ? (
                            <span
                              className={[
                                "rounded-full px-2 py-0.5 text-[0.65rem] font-semibold uppercase",
                                isSelected
                                  ? "bg-white/15 text-white"
                                  : "bg-success/15 text-success",
                              ].join(" ")}
                            >
                              series
                            </span>
                          ) : null}
                        </div>
                        <p className="mt-2 font-serif text-lg font-semibold">
                          M{waveform.magnitude.toFixed(2)} · {waveform.stationId.split(".")[1] ?? waveform.stationId}
                        </p>
                        <p
                          className={[
                            "mt-2 text-sm",
                            isSelected ? "text-white/85" : "text-text-muted",
                          ].join(" ")}
                        >
                          {formatOriginTime(waveform.originTimeUtc)} UTC
                        </p>
                        <p
                          className={[
                            "mt-2 text-xs",
                            isSelected ? "text-white/70" : "text-text-muted",
                          ].join(" ")}
                        >
                          {waveform.samplingRateHz} Hz · {waveform.durationS}s ·{" "}
                          {waveform.channel}
                        </p>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
