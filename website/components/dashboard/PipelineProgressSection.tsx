import Link from "next/link";
import { Section } from "@/components/ui/Section";
import type { PipelinePhase, PipelinePhaseStatus } from "@/lib/dashboard/types";

type PipelineProgressSectionProps = {
  phases: PipelinePhase[];
};

const statusStyles: Record<PipelinePhaseStatus, string> = {
  complete: "border-success/30 bg-success/10 text-success",
  current: "border-accent/30 bg-accent/10 text-accent",
  planned: "border-border bg-surface text-text-muted",
};

const statusLabels: Record<PipelinePhaseStatus, string> = {
  complete: "Complete",
  current: "In progress",
  planned: "Planned",
};

export function PipelineProgressSection({ phases }: PipelineProgressSectionProps) {
  const completeCount = phases.filter((phase) => phase.status === "complete").length;

  return (
    <Section
      id="pipeline"
      eyebrow="Pipeline"
      title="Pipeline progress"
      subtitle={`${completeCount} of ${phases.length} phases complete · science pipeline frozen at v1.0 submission`}
    >
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {phases.map((phase) => (
          <article
            key={phase.id}
            className="flex h-full flex-col rounded-xl border border-border bg-surface-elevated p-5 shadow-sm"
          >
            <div className="flex items-start justify-between gap-3">
              <h3 className="font-serif text-lg font-semibold text-text">
                {phase.label}
              </h3>
              <span
                className={[
                  "shrink-0 rounded-full border px-2 py-0.5 text-[0.65rem] font-semibold uppercase",
                  statusStyles[phase.status],
                ].join(" ")}
              >
                {statusLabels[phase.status]}
              </span>
            </div>
            <p className="mt-3 flex-1 text-sm leading-relaxed text-text-muted">
              {phase.description}
            </p>
            {phase.external ? (
              <a
                href={phase.href}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-flex text-sm font-medium text-primary hover:text-primary-light"
              >
                View details ↗
              </a>
            ) : (
              <Link
                href={phase.href}
                className="mt-4 inline-flex text-sm font-medium text-primary hover:text-primary-light"
              >
                View stage →
              </Link>
            )}
          </article>
        ))}
      </div>
    </Section>
  );
}
