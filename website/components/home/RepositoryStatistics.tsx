import { Section } from "@/components/ui/Section";
import type { RepositoryStats } from "@/lib/content/stats";

type RepositoryStatisticsProps = {
  stats: RepositoryStats;
};

type StatItem = {
  label: string;
  value: string;
  detail?: string;
};

export function RepositoryStatistics({ stats }: RepositoryStatisticsProps) {
  const items: StatItem[] = [
    {
      label: "Documentation",
      value: String(stats.documentation),
      detail: "Markdown files in docs/",
    },
    {
      label: "Reports",
      value: String(stats.reports),
      detail: "Markdown files in reports/",
    },
    {
      label: "Figures",
      value: String(stats.figures),
      detail:
        stats.validationStatus === "PASS"
          ? "Validation summary · PASS"
          : "From validation summary",
    },
    {
      label: "Research phases",
      value: String(stats.researchPhases),
      detail: "Completed phase reports in docs/",
    },
    {
      label: "GitHub release",
      value: stats.githubRelease,
      detail: stats.releaseDate ?? "Submission release",
    },
    {
      label: "Current version",
      value: stats.platformVersion,
      detail: `Science v${stats.scienceVersion}`,
    },
  ];

  return (
    <Section
      eyebrow="Repository"
      title="Repository statistics"
      subtitle="Counts derived from the repository at build time — not hardcoded estimates."
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
            {item.detail && (
              <p className="mt-2 text-xs leading-relaxed text-text-muted">
                {item.detail}
              </p>
            )}
          </article>
        ))}
      </div>

      {(stats.pilotEvents !== null || stats.analysisScripts > 0) && (
        <p className="mt-6 text-sm text-text-muted">
          {stats.pilotEvents !== null && (
            <span>California pilot manifest: {stats.pilotEvents} events. </span>
          )}
          {stats.analysisScripts > 0 && (
            <span>Analysis scripts: {stats.analysisScripts} under scripts/analysis/.</span>
          )}
        </p>
      )}
    </Section>
  );
}
