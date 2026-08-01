import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { WaveformExplorer } from "@/components/waveforms/WaveformExplorer";
import { loadWaveformExplorer } from "@/lib/waveforms/loader";

export const metadata: Metadata = {
  title: "Waveform Explorer",
  description:
    "Interactive preview of California pilot earthquake waveforms — event metadata, processing stages, and repository-derived series.",
};

export default function WaveformsPage() {
  const data = loadWaveformExplorer();

  return (
    <>
      <section className="border-b border-border bg-surface py-12 md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Breadcrumbs
            items={[{ label: "Home", href: "/" }, { label: "Waveform Explorer" }]}
          />
          <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
            Waveform explorer
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-text-muted">
            Browse pilot earthquake waveforms grouped by dataset. Each event links
            to acquisition context, processing stages, generated figures, and the
            wider research workflow.
          </p>
          <div className="mt-6 flex flex-wrap gap-4 text-sm">
            <Link
              href="/dataset#california-pilot"
              className="font-medium text-primary hover:text-primary-light"
            >
              Dataset Explorer →
            </Link>
            <Link
              href="/workflow#signal-analysis"
              className="font-medium text-primary hover:text-primary-light"
            >
              Signal analysis workflow →
            </Link>
            <Link
              href="/map"
              className="font-medium text-primary hover:text-primary-light"
            >
              Earthquake Map →
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

      <WaveformExplorer data={data} />
    </>
  );
}
