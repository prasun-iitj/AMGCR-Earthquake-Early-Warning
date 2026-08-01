import type { Metadata } from "next";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import { documents } from "@/lib/content/documents";

export const metadata: Metadata = {
  title: "Research",
  description: "Research portal for AMGCR Earthquake Research documentation and reports.",
};

export default function ResearchPage() {
  const report = documents.find((doc) => doc.slug === "research-report-final");

  return (
    <>
      <Section
        eyebrow="Research"
        title="Research portal"
        subtitle="Explore the final research report and supporting documentation rendered from the repository."
      >
        <div className="grid gap-6 md:grid-cols-3">
          {report && (
            <article className="rounded-xl border border-border bg-surface-elevated p-6 shadow-sm">
              <h2 className="font-serif text-xl font-semibold text-text">
                {report.title}
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                {report.description}
              </p>
              <div className="mt-6">
                <Button href={report.href} variant="primary">
                  Read full report
                </Button>
              </div>
            </article>
          )}

          <article className="rounded-xl border border-border bg-surface-elevated p-6 shadow-sm">
            <h2 className="font-serif text-xl font-semibold text-text">
              Workflow explorer
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Interactive pipeline stages with links to reports, artefacts, figures,
              and scripts from the repository.
            </p>
            <div className="mt-6">
              <Button href="/workflow" variant="secondary">
                Open workflow explorer
              </Button>
            </div>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6 shadow-sm">
            <h2 className="font-serif text-xl font-semibold text-text">
              Documentation
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Project charter, status updates, and repository overview — all
              sourced from existing Markdown files.
            </p>
            <div className="mt-6">
              <Button href="/docs" variant="outline">
                Browse documentation
              </Button>
            </div>
          </article>
        </div>
      </Section>

      <Section variant="muted" title="Available in later phases">
        <ul className="grid gap-4 md:grid-cols-2">
          {[
            "Interactive charts and feature exploration",
            "Event map and dataset explorer",
            "Waveform viewer",
            "Submission PDF viewing",
          ].map((item) => (
            <li
              key={item}
              className="flex items-start gap-3 rounded-lg border border-border bg-surface-elevated px-4 py-3 text-sm text-text-muted"
            >
              <span
                aria-hidden="true"
                className="mt-1 h-2 w-2 shrink-0 rounded-full bg-accent"
              />
              {item}
            </li>
          ))}
        </ul>
      </Section>
    </>
  );
}
