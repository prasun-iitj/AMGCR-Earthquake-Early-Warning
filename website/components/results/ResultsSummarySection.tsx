"use client";

import { motion, useReducedMotion } from "framer-motion";
import type { ResultsSummary } from "@/lib/results/descriptions";

type ResultsSummarySectionProps = {
  summary: ResultsSummary;
};

export function ResultsSummarySection({ summary }: ResultsSummarySectionProps) {
  const shouldReduceMotion = useReducedMotion();

  const items = [
    {
      label: "Pilot events",
      value: summary.pilotEvents ?? "—",
      detail: "California manifest",
    },
    {
      label: "Figures",
      value: summary.figures,
      detail: "PNG outputs in reports/figures/",
    },
    {
      label: "Tables",
      value: summary.tables,
      detail: "CSV summaries in reports/tables/",
    },
    {
      label: "Reports",
      value: summary.reports,
      detail: "Markdown in reports/",
    },
    {
      label: "Research phases",
      value: summary.researchPhases,
      detail: "Completed phase reports",
    },
    {
      label: "Features",
      value: summary.featureCount ?? "—",
      detail: "From feature_summary.json",
    },
    {
      label: "GitHub release",
      value: summary.githubRelease,
      detail: summary.releaseDate ?? "Submission release",
    },
    {
      label: "Current version",
      value: summary.platformVersion,
      detail: `Science v${summary.scienceVersion}${
        summary.validationStatus ? ` · ${summary.validationStatus}` : ""
      }`,
    },
  ];

  return (
    <section className="border-b border-border bg-surface-elevated py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Results summary
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            Pilot outputs at a glance
          </h2>
          <p className="mt-3 text-text-muted">
            Metrics loaded from repository JSON summaries, manifests, and
            directory scans at build time.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {items.map((item, index) => (
            <motion.article
              key={item.label}
              initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.25, delay: index * 0.03 }}
              className="rounded-xl border border-border bg-surface px-5 py-4"
            >
              <p className="text-sm font-medium text-text-muted">{item.label}</p>
              <p className="mt-2 font-serif text-3xl font-semibold text-primary">
                {item.value}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-text-muted">
                {item.detail}
              </p>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
