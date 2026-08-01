import type { Metadata } from "next";
import Link from "next/link";
import { Section } from "@/components/ui/Section";
import { documents } from "@/lib/content/documents";

export const metadata: Metadata = {
  title: "Resources",
  description:
    "Documentation and research resources rendered from the repository.",
};

export default function ResourcesPage() {
  const docEntries = documents.filter((doc) => doc.href.startsWith("/docs/"));
  const report = documents.find((doc) => doc.slug === "research-report-final");

  return (
    <>
      <Section
        eyebrow="Resources"
        title="Documentation and research resources"
        subtitle="All content is rendered directly from repository Markdown at build time. No duplicate copies are maintained in the website."
      >
        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Research dashboard
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              High-level project overview — metrics, pipeline progress, and quick navigation.
            </p>
            <Link
              href="/dashboard"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              Open dashboard →
            </Link>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Results explorer
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Browse generated figures and CSV tables from the pilot pipeline.
            </p>
            <Link
              href="/results"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              Open results explorer →
            </Link>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Dataset explorer
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Understand pilot sources, data journey, and downloadable artefacts.
            </p>
            <Link
              href="/dataset"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              Explore datasets →
            </Link>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Waveform explorer
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Inspect pilot earthquake waveforms, processing stages, and event metadata.
            </p>
            <Link
              href="/waveforms"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              Browse waveforms →
            </Link>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Earthquake map
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              View pilot event locations and connect markers to waveforms and reports.
            </p>
            <Link
              href="/map"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              Open earthquake map →
            </Link>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              GitHub integration
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Repository overview, releases, structure, and direct GitHub links.
            </p>
            <Link
              href="/github"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              View GitHub page →
            </Link>
          </article>

          <article className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Documentation index
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              Browse governance documents and the repository README.
            </p>
            <Link
              href="/docs"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
            >
              View all documentation →
            </Link>
            <ul className="mt-6 space-y-3 border-t border-border pt-6">
              {docEntries.map((doc) => (
                <li key={doc.slug}>
                  <Link
                    href={doc.href}
                    className="text-sm text-text-muted transition-colors hover:text-primary"
                  >
                    {doc.title}
                  </Link>
                </li>
              ))}
            </ul>
          </article>

          {report && (
            <article className="rounded-xl border border-border bg-surface-elevated p-6">
              <h2 className="font-serif text-xl font-semibold text-text">
                Final research report
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                {report.description}
              </p>
              <p className="mt-4 font-mono text-xs text-text-muted">
                {report.sourcePath}
              </p>
              <Link
                href={report.href}
                className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
              >
                Read research report →
              </Link>
            </article>
          )}
        </div>
      </Section>
    </>
  );
}
