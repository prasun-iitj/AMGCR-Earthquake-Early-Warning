"use client";

import Link from "next/link";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { DatasetRecord } from "@/lib/dataset/types";

type DatasetDetailsPanelProps = {
  dataset: DatasetRecord;
};

export function DatasetDetailsPanel({ dataset }: DatasetDetailsPanelProps) {
  const shouldReduceMotion = useReducedMotion();
  const stats = dataset.statistics;

  if (dataset.status === "planned") {
    return (
      <AnimatePresence mode="wait">
        <motion.section
          key={dataset.id}
          initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
          transition={{ duration: 0.22 }}
          className="border-t border-border bg-surface-elevated py-12 md:py-16"
        >
          <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
            <h2 className="font-serif text-2xl font-semibold text-text">
              {dataset.name}
            </h2>
            <p className="mt-4 text-text-muted">{dataset.summary}</p>
            <p className="mt-6 text-sm text-text-muted">
              This dataset slot is reserved for future integration. The same
              detail panel will populate automatically once acquisition completes.
            </p>
          </div>
        </motion.section>
      </AnimatePresence>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.section
        key={dataset.id}
        initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
        transition={{ duration: 0.22 }}
        className="border-t border-border bg-surface-elevated py-12 md:py-16"
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <p className="text-sm font-semibold uppercase tracking-wider text-accent">
              Dataset details
            </p>
            <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
              {dataset.name}
            </h2>
          </div>

          <div className="grid gap-8 lg:grid-cols-2">
            <DetailGroup
              title="Acquisition"
              items={[
                ["Source", dataset.source],
                ["Region", dataset.region],
                ["Method", dataset.acquisitionMethod],
                [
                  "Providers",
                  dataset.providers.length > 0
                    ? dataset.providers.join(" · ")
                    : "—",
                ],
                ["Events", String(stats.eventCount ?? "—")],
                ["Stations", String(stats.stationCount ?? "—")],
                [
                  "Magnitude range",
                  stats.magnitudeMin != null && stats.magnitudeMax != null
                    ? `${stats.magnitudeMin} – ${stats.magnitudeMax}`
                    : "—",
                ],
                [
                  "Time period",
                  stats.timeRangeStart && stats.timeRangeEnd
                    ? `${stats.timeRangeStart.slice(0, 10)} → ${stats.timeRangeEnd.slice(0, 10)}`
                    : "—",
                ],
                [
                  "Sampling",
                  stats.samplingRateHz
                    ? `${stats.samplingRateHz} Hz · ${stats.channels.join(", ") || "BHZ"}`
                    : "—",
                ],
              ]}
            />

            <DetailGroup
              title="Generated outputs"
              items={[
                ["Reports", String(stats.reportCount ?? "—")],
                ["Figures", String(stats.figureCount ?? "—")],
                ["Tables", String(stats.tableCount ?? "—")],
                ["Features", String(stats.featureCount ?? "—")],
                ["Manifest", dataset.manifestPath ?? "—"],
                ["Raw waveforms", dataset.rawDataPath ?? "—"],
              ]}
            />
          </div>

          <div className="mt-10 grid gap-8 lg:grid-cols-3">
            <LinkGroup title="Reports" links={dataset.reports} />
            <LinkGroup title="Documentation" links={dataset.documentation} />
            <div>
              <LinkGroup title="Figures & tables" links={[...dataset.tables]} />
              {stats.figureCount && stats.figureCount > 0 ? (
                <Link
                  href="/results"
                  className="mt-3 inline-flex text-sm font-medium text-primary hover:text-primary-light"
                >
                  View all {stats.figureCount} figures in Results Explorer →
                </Link>
              ) : null}
            </div>
          </div>

          <div className="mt-8 rounded-xl border border-dashed border-border bg-surface p-4 text-xs text-text-muted">
            <p className="font-semibold uppercase tracking-wider">
              Future integration slots
            </p>
            <ul className="mt-2 space-y-1">
              <li>
                Waveform explorer:{" "}
                {dataset.capabilities.waveforms ? (
                  <Link
                    href="/waveforms"
                    className="font-medium text-primary hover:text-primary-light"
                  >
                    Open Waveform Explorer →
                  </Link>
                ) : (
                  "pending dataset"
                )}
              </li>
              <li>
                Earthquake map:{" "}
                {dataset.capabilities.map ? (
                  <Link
                    href="/map"
                    className="font-medium text-primary hover:text-primary-light"
                  >
                    Open Earthquake Map →
                  </Link>
                ) : (
                  "pending dataset"
                )}
              </li>
              <li>
                Dashboard metrics:{" "}
                {dataset.capabilities.dashboard ? "ready" : "pending dataset"}
              </li>
              <li>
                AI metadata index:{" "}
                {dataset.capabilities.aiMetadata ? "ready" : "pending dataset"}
              </li>
            </ul>
          </div>
        </div>
      </motion.section>
    </AnimatePresence>
  );
}

function DetailGroup({
  title,
  items,
}: {
  title: string;
  items: Array<[string, string]>;
}) {
  return (
    <div className="rounded-xl border border-border bg-surface p-6">
      <h3 className="font-serif text-xl font-semibold text-text">{title}</h3>
      <dl className="mt-4 space-y-3">
        {items.map(([term, value]) => (
          <div key={term}>
            <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
              {term}
            </dt>
            <dd className="mt-1 text-sm leading-relaxed text-text">{value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

function LinkGroup({
  title,
  links,
}: {
  title: string;
  links: DatasetRecord["reports"];
}) {
  return (
    <div>
      <h3 className="font-serif text-lg font-semibold text-text">{title}</h3>
      <ul className="mt-3 space-y-2">
        {links.map((link) => (
          <li key={link.path}>
            <ResourceLink link={link} />
          </li>
        ))}
      </ul>
    </div>
  );
}

function ResourceLink({ link }: { link: DatasetRecord["reports"][number] }) {
  const className =
    "text-sm text-text-muted transition-colors hover:text-primary";

  if (link.external) {
    return (
      <a
        href={link.href}
        target="_blank"
        rel="noopener noreferrer"
        className={className}
      >
        {link.label} ↗
      </a>
    );
  }

  return (
    <Link href={link.href} className={className}>
      {link.label} →
    </Link>
  );
}
