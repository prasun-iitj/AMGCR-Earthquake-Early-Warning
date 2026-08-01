import Link from "next/link";
import { Section } from "@/components/ui/Section";
import { Button } from "@/components/ui/Button";
import { workflowSteps } from "@/lib/home/content";

function WorkflowArrow() {
  return (
    <div aria-hidden="true" className="flex justify-center py-2 text-text-muted">
      <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 5v14M6 13l6 6 6-6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </div>
  );
}

export function WorkflowPreview() {
  return (
    <Section
      variant="muted"
      eyebrow="Workflow"
      title="Interactive workflow preview"
      subtitle="Click any stage to open the full workflow explorer with repository-linked details."
    >
      <div className="mx-auto max-w-2xl">
        {workflowSteps.map((step, index) => (
          <div key={step.title}>
            <Link
              href={step.href}
              className="group block rounded-xl border border-border bg-surface-elevated p-5 shadow-sm transition-colors hover:border-primary/30 hover:bg-white"
            >
              <div className="flex items-start justify-between gap-4">
                <h3 className="font-serif text-lg font-semibold text-text group-hover:text-primary">
                  {step.title}
                </h3>
                <span className="text-sm text-text-muted transition-transform group-hover:translate-x-0.5">
                  →
                </span>
              </div>
              <p className="mt-2 text-sm leading-relaxed text-text-muted">
                {step.description}
              </p>
            </Link>
            {index < workflowSteps.length - 1 && <WorkflowArrow />}
          </div>
        ))}
      </div>

      <div className="mt-8 text-center">
        <Button href="/workflow" variant="secondary">
          Open workflow explorer
        </Button>
      </div>
    </Section>
  );
}
