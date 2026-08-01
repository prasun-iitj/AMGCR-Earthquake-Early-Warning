import { Section } from "@/components/ui/Section";
import type { DatasetMetrics } from "@/lib/dashboard/types";

type DatasetMetricsSectionProps = {
  metrics: DatasetMetrics;
};

function formatDate(value: string | null): string {
  if (!value) {
    return "—";
  }
  return value.slice(0, 10);
}

export function DatasetMetricsSection({ metrics }: DatasetMetricsSectionProps) {
  const items = [
    { label: "Events", value: metrics.eventCount ?? "—" },
    { label: "Stations", value: metrics.stationCount ?? "—" },
    { label: "Waveforms", value: metrics.waveformCount ?? "—" },
    {
      label: "Time range",
      value:
        metrics.timeRangeStart && metrics.timeRangeEnd
          ? `${formatDate(metrics.timeRangeStart)} → ${formatDate(metrics.timeRangeEnd)}`
          : "—",
    },
    {
      label: "Magnitude range",
      value:
        metrics.magnitudeMin != null && metrics.magnitudeMax != null
          ? `M${metrics.magnitudeMin} – M${metrics.magnitudeMax}`
          : "—",
    },
    {
      label: "Sampling rate",
      value: metrics.samplingRateHz
        ? `${metrics.samplingRateHz} Hz · ${metrics.channels.join(", ") || "BHZ"}`
        : "—",
    },
  ];

  return (
    <Section
      id="dataset-metrics"
      eyebrow="California pilot"
      title="Dataset metrics"
      subtitle="Counts and coverage from reports/eda/dataset_summary.json and feature summaries — not hardcoded."
    >
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <article
            key={item.label}
            className="rounded-xl border border-border bg-surface px-6 py-5"
          >
            <p className="text-sm font-medium text-text-muted">{item.label}</p>
            <p className="mt-2 font-serif text-xl font-semibold text-text">
              {item.value}
            </p>
          </article>
        ))}
      </div>
      {metrics.featureMatrixShape ? (
        <p className="mt-6 text-sm text-text-muted">
          Feature matrix shape: {metrics.featureMatrixShape} (events × features)
        </p>
      ) : null}
    </Section>
  );
}
