import { Section } from "@/components/ui/Section";
import type { RepositoryMetrics } from "@/lib/dashboard/types";

type RepositoryMetricsSectionProps = {
  metrics: RepositoryMetrics;
};

export function RepositoryMetricsSection({ metrics }: RepositoryMetricsSectionProps) {
  const items = [
    {
      label: "Documentation",
      value: metrics.documentationCount,
      detail: "Markdown files in docs/",
    },
    {
      label: "Reports",
      value: metrics.reportCount,
      detail: "Markdown files in reports/",
    },
    {
      label: "Figures",
      value: metrics.figureCount,
      detail: "From validation summary",
    },
    {
      label: "Tables",
      value: metrics.tableCount,
      detail: "CSV files in reports/tables/",
    },
    {
      label: "JSON summaries",
      value: metrics.jsonSummaryCount,
      detail: "Structured outputs under reports/",
    },
    {
      label: "Workflow phases",
      value: metrics.workflowPhaseCount,
      detail: "Stages in Workflow Explorer",
    },
    {
      label: "Website version",
      value: metrics.websiteVersion,
      detail: "Platform release tag",
    },
    {
      label: "Research version",
      value: `v${metrics.researchVersion}`,
      detail: "Frozen science release",
    },
    {
      label: "Analysis scripts",
      value: metrics.analysisScriptCount,
      detail: "Python scripts under scripts/analysis/",
    },
  ];

  return (
    <Section
      id="repository-metrics"
      eyebrow="Repository"
      title="Repository metrics"
      subtitle="Build-time inventory of documentation, outputs, and tooling in the research repository."
      variant="muted"
    >
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <article
            key={item.label}
            className="rounded-xl border border-border bg-surface-elevated px-6 py-5 shadow-sm"
          >
            <p className="text-sm font-medium text-text-muted">{item.label}</p>
            <p className="mt-2 font-serif text-3xl font-semibold text-primary">
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
