import { Section } from "@/components/ui/Section";
import { timelineSteps } from "@/lib/home/content";

export function TimelinePreview() {
  return (
    <Section
      variant="muted"
      eyebrow="Timeline"
      title="Project timeline"
      subtitle="From frozen v1.0 submission science to the Version 2.0 interactive platform."
    >
      <ol className="relative mx-auto max-w-4xl">
        {timelineSteps.map((step, index) => (
          <li key={step.label} className="relative flex gap-4 pb-10 last:pb-0">
            {index < timelineSteps.length - 1 && (
              <span
                aria-hidden="true"
                className="absolute left-[15px] top-8 h-[calc(100%-1rem)] w-px bg-border"
              />
            )}
            <span
              className={[
                "relative z-10 mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-xs font-semibold",
                step.status === "complete"
                  ? "border-success bg-success/10 text-success"
                  : "border-accent bg-accent/10 text-accent",
              ].join(" ")}
            >
              {index + 1}
            </span>
            <div className="min-w-0 pt-0.5">
              <h3 className="font-serif text-lg font-semibold text-text">
                {step.label}
              </h3>
              <p className="mt-1 text-sm text-text-muted">{step.detail}</p>
            </div>
          </li>
        ))}
      </ol>
    </Section>
  );
}
