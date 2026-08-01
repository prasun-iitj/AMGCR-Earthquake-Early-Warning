"use client";

import { motion, useReducedMotion } from "framer-motion";
import type { DatasetRecord } from "@/lib/dataset/types";

type DatasetOverviewProps = {
  dataset: DatasetRecord;
};

export function DatasetOverview({ dataset }: DatasetOverviewProps) {
  const shouldReduceMotion = useReducedMotion();
  const stats = dataset.statistics;

  const items = [
    { label: "Region", value: dataset.region },
    { label: "Source", value: dataset.source },
    { label: "Acquisition", value: "ObsPy FDSN" },
    { label: "Events", value: stats.eventCount ?? "—" },
    { label: "Stations", value: stats.stationCount ?? "—" },
    { label: "Waveforms", value: stats.waveformCount ?? "—" },
    {
      label: "Time range",
      value:
        stats.timeRangeStart && stats.timeRangeEnd
          ? `${formatDate(stats.timeRangeStart)} → ${formatDate(stats.timeRangeEnd)}`
          : "—",
    },
    {
      label: "Sampling rate",
      value: stats.samplingRateHz ? `${stats.samplingRateHz} Hz` : "—",
    },
    {
      label: "Channels",
      value: stats.channels.length > 0 ? stats.channels.join(", ") : "—",
    },
    {
      label: "Magnitude",
      value:
        stats.magnitudeMin != null && stats.magnitudeMax != null
          ? `${stats.magnitudeMin} – ${stats.magnitudeMax}`
          : "—",
    },
    { label: "Features", value: stats.featureCount ?? "—" },
    { label: "Figures", value: stats.figureCount ?? "—" },
    { label: "Tables", value: stats.tableCount ?? "—" },
    { label: "Reports", value: stats.reportCount ?? "—" },
  ];

  return (
    <section className="border-b border-border bg-surface-elevated py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Dataset overview
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            {dataset.name}
          </h2>
          <p className="mt-3 text-text-muted">{dataset.summary}</p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {items.map((item, index) => (
            <motion.article
              key={item.label}
              initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.22, delay: index * 0.02 }}
              className="rounded-xl border border-border bg-surface px-4 py-4"
            >
              <p className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                {item.label}
              </p>
              <p className="mt-2 text-sm font-medium leading-relaxed text-text">
                {item.value}
              </p>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}

function formatDate(iso: string): string {
  try {
    return new Date(iso).toISOString().slice(0, 10);
  } catch {
    return iso;
  }
}
