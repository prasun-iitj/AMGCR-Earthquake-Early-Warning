import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { MapExplorer } from "@/components/map/MapExplorer";
import { loadMapExplorer } from "@/lib/map/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "Earthquake Map",
  description:
    "Interactive map of California pilot earthquake events with links to datasets, waveforms, workflow, and results.",
  path: "/map",
});

export default function MapPage() {
  const data = loadMapExplorer();

  return (
    <>
      <section className="border-b border-border bg-surface py-12 md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Breadcrumbs
            items={[{ label: "Home", href: "/" }, { label: "Earthquake Map" }]}
          />
          <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
            Earthquake map
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-text-muted">
            Explore where pilot earthquake events occurred across California.
            Select markers to connect locations with datasets, waveforms, workflow
            stages, and generated research outputs.
          </p>
          <div className="mt-6 flex flex-wrap gap-4 text-sm">
            <Link
              href="/dataset#california-pilot"
              className="font-medium text-primary hover:text-primary-light"
            >
              Dataset Explorer →
            </Link>
            <Link
              href="/waveforms"
              className="font-medium text-primary hover:text-primary-light"
            >
              Waveform Explorer →
            </Link>
            <Link
              href="/workflow#signal-analysis"
              className="font-medium text-primary hover:text-primary-light"
            >
              Workflow Explorer →
            </Link>
            <Link
              href="/results"
              className="font-medium text-primary hover:text-primary-light"
            >
              Results Explorer →
            </Link>
          </div>
        </div>
      </section>

      <MapExplorer data={data} />
    </>
  );
}
