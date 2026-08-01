import { Section } from "@/components/ui/Section";
import type { TimelineMilestone } from "@/lib/dashboard/types";

type ProjectTimelineSectionProps = {
  milestones: TimelineMilestone[];
};

const statusStyles = {
  complete: "border-success bg-success/10 text-success",
  current: "border-accent bg-accent/10 text-accent",
  planned: "border-border bg-surface text-text-muted",
} as const;

export function ProjectTimelineSection({ milestones }: ProjectTimelineSectionProps) {
  return (
    <Section
      id="timeline"
      eyebrow="Timeline"
      title="Project timeline"
      subtitle="From frozen v1.0 submission science through Version 2.0 platform development and future Europe / AI phases."
    >
      <ol className="relative mx-auto max-w-4xl">
        {milestones.map((milestone, index) => (
          <li key={milestone.label} className="relative flex gap-4 pb-10 last:pb-0">
            {index < milestones.length - 1 ? (
              <span
                aria-hidden="true"
                className="absolute left-[15px] top-8 h-[calc(100%-1rem)] w-px bg-border"
              />
            ) : null}
            <span
              className={[
                "relative z-10 mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-xs font-semibold",
                statusStyles[milestone.status],
              ].join(" ")}
            >
              {index + 1}
            </span>
            <div className="min-w-0 pt-0.5">
              <h3 className="font-serif text-lg font-semibold text-text">
                {milestone.label}
              </h3>
              <p className="mt-1 text-sm text-text-muted">{milestone.detail}</p>
            </div>
          </li>
        ))}
      </ol>
    </Section>
  );
}
