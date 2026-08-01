import type { Metadata } from "next";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { DatasetExplorer } from "@/components/dataset/DatasetExplorer";
import { DatasetJourney } from "@/components/dataset/DatasetJourney";
import { loadDatasetExplorer } from "@/lib/dataset/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "Dataset Explorer",
  description:
    "Explore the California FDSN pilot dataset — sources, journey, outputs, and planned regional expansions.",
  path: "/dataset",
});

export default function DatasetPage() {
  const data = loadDatasetExplorer();

  return (
    <>
      <section className="border-b border-border bg-surface py-12 md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Breadcrumbs
            items={[{ label: "Home", href: "/" }, { label: "Dataset Explorer" }]}
          />
          <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
            Dataset explorer
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-text-muted">
            Understand what data was collected, where it came from, how it flows
            through the research pipeline, and what outputs were generated —
            with architecture ready for future waveform, map, and dashboard
            modules.
          </p>
        </div>
      </section>

      <DatasetExplorer data={data} />
      <DatasetJourney steps={data.journey} />
    </>
  );
}
