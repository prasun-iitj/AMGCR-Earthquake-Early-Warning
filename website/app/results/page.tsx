import type { Metadata } from "next";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { FigureGallery } from "@/components/results/FigureGallery";
import { ResultsSummarySection } from "@/components/results/ResultsSummarySection";
import { TablesSection } from "@/components/results/TablesSection";
import { getResultsSummary } from "@/lib/results/descriptions";
import {
  groupFiguresByPhase,
  loadResultsExplorerData,
} from "@/lib/results/loader";

export const metadata: Metadata = {
  title: "Results Explorer",
  description:
    "Browse pilot figures, CSV tables, and output summaries from the California FDSN research pipeline.",
};

export default function ResultsPage() {
  const summary = getResultsSummary();
  const { figures, tables } = loadResultsExplorerData();
  const figureGroups = groupFiguresByPhase(figures);

  return (
    <>
      <section className="border-b border-border bg-surface py-12 md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Breadcrumbs
            items={[
              { label: "Home", href: "/" },
              { label: "Results Explorer" },
            ]}
          />
          <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
            Results &amp; figures explorer
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-text-muted">
            Interactive gallery of generated figures and CSV tables from the
            completed California pilot. All assets are discovered from the
            repository at build time.
          </p>
        </div>
      </section>

      <ResultsSummarySection summary={summary} />

      <section className="py-12 md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-8 max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-wider text-accent">
              Figures
            </p>
            <h2 className="mt-2 font-serif text-3xl font-semibold text-text">
              Research figures by phase
            </h2>
            <p className="mt-3 text-text-muted">
              Click any figure to open the lightbox viewer with caption and
              previous/next navigation.
            </p>
          </div>

          <FigureGallery groups={figureGroups} />
        </div>
      </section>

      <TablesSection tables={tables} />
    </>
  );
}
