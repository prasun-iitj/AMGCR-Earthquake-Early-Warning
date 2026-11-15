import { Section } from "@/components/ui/Section";
import type { ResearchSummary } from "@/lib/dashboard/types";

type ResearchSummarySectionProps = {
  summary: ResearchSummary;
};

export function ResearchSummarySection({ summary }: ResearchSummarySectionProps) {
  const items = [
    {
      label: "Platform version",
      value: summary.platformVersion,
      detail: "Version 2.0 interactive website",
    },
    {
      label: "Research version",
      value: `v${summary.scienceVersion}`,
      detail: "Frozen submission science",
    },
    {
      label: "GitHub release",
      value: summary.githubRelease,
      detail: summary.releaseDate ?? "Submission release",
    },
    {
      label: "Research status",
      value: summary.researchStatus,
      detail:
        summary.validationStatus === "PASS"
          ? `Validation ${summary.validationStatus}`
          : "Build-time status from repository",
    },
    {
      label: "California pilot",
      value: summary.californiaPilotStatus,
      detail: "IRIS/EarthScope · 8 events complete",
    },
    {
      label: "Swiss validation (Set C)",
      value: summary.swissValidationMetrics ?? "72.9% trigger",
      detail: "15 events · 550 records · frozen 8.0",
    },
    {
      label: "Supervised ML (ML-4, offline)",
      value: "Set C F1 0.91",
      detail: "RF 0.9125 · XGB 0.9169 on 15 unseen events · STEP 3A NO-GO was resolved by ML-1A",
    },
  ];

  return (
    <Section
      id="summary"
      eyebrow="Overview"
      title="Research summary"
      subtitle="High-level project status derived from repository governance documents and submission metadata at build time."
      variant="muted"
    >
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {items.map((item) => (
          <article
            key={item.label}
            className="rounded-xl border border-border bg-surface-elevated px-6 py-5 shadow-sm"
          >
            <p className="text-sm font-medium text-text-muted">{item.label}</p>
            <p className="mt-2 font-serif text-2xl font-semibold text-primary">
              {item.value}
            </p>
            <p className="mt-2 text-xs leading-relaxed text-text-muted">
              {item.detail}
            </p>
          </article>
        ))}
      </div>
    </Section>
  );
}
