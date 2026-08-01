import type { Metadata } from "next";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { WorkflowExplorer } from "@/components/workflow/WorkflowExplorer";
import { Section } from "@/components/ui/Section";
import { loadWorkflowStages } from "@/lib/workflow/loader";

export const metadata: Metadata = {
  title: "Workflow Explorer",
  description:
    "Interactive explorer for the California FDSN research pipeline — stages, artefacts, and repository links.",
};

export default function WorkflowPage() {
  const stages = loadWorkflowStages();

  return (
    <>
      <Section
        variant="muted"
        container={false}
        className="border-b border-border py-12 md:py-16"
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Breadcrumbs
            items={[
              { label: "Home", href: "/" },
              { label: "Workflow Explorer" },
            ]}
          />
          <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
            Interactive workflow explorer
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-text-muted">
            Select a pipeline stage to view its purpose, inputs, outputs, and
            links to reports, figures, documentation, and scripts — all derived
            from existing repository content at build time.
          </p>
        </div>
      </Section>

      <WorkflowExplorer stages={stages} />
    </>
  );
}
