import Link from "next/link";
import type { DatasetJourneyStep } from "@/lib/dataset/types";

type DatasetJourneyProps = {
  steps: DatasetJourneyStep[];
};

export function DatasetJourney({ steps }: DatasetJourneyProps) {
  return (
    <section className="py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Dataset journey
          </p>
          <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
            From FDSN source to final report
          </h2>
          <p className="mt-3 text-text-muted">
            Follow how California pilot data moves through acquisition, analysis,
            and submission deliverables. SVG pipeline visuals will replace text
            arrows in a future workflow UI enhancement.
          </p>
        </div>

        <div className="mx-auto max-w-2xl">
          {steps.map((step, index) => (
            <div key={step.id}>
              <JourneyStepCard step={step} />
              {index < steps.length - 1 && (
                <div
                  aria-hidden="true"
                  className="flex justify-center py-2 text-lg text-text-muted"
                >
                  ↓
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function JourneyStepCard({ step }: { step: DatasetJourneyStep }) {
  const className =
    "group block rounded-xl border border-border bg-surface-elevated p-5 shadow-sm transition-colors hover:border-primary/30 hover:bg-white";

  const content = (
    <>
      <div className="flex items-start justify-between gap-4">
        <h3 className="font-serif text-lg font-semibold text-text group-hover:text-primary">
          {step.label}
        </h3>
        <span className="text-sm text-text-muted">→</span>
      </div>
      <p className="mt-2 text-sm leading-relaxed text-text-muted">
        {step.description}
      </p>
    </>
  );

  if (step.external) {
    return (
      <a
        href={step.href}
        target="_blank"
        rel="noopener noreferrer"
        className={className}
      >
        {content}
      </a>
    );
  }

  return (
    <Link href={step.href} className={className}>
      {content}
    </Link>
  );
}
