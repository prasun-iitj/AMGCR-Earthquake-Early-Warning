"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { FigureLightbox } from "@/components/results/FigureLightbox";
import type { ResultFigure } from "@/lib/results/loader";

type FigureGalleryProps = {
  groups: Array<{
    phase: string;
    label: string;
    figures: ResultFigure[];
  }>;
};

export function FigureGallery({ groups }: FigureGalleryProps) {
  const allFigures = groups.flatMap((group) => group.figures);
  const [activeFigure, setActiveFigure] = useState<ResultFigure | null>(null);

  if (allFigures.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-border bg-surface p-8 text-center text-sm text-text-muted">
        No figures discovered in reports/figures/. Run the analysis scripts to
        regenerate PNG outputs per the reproducibility statement.
      </div>
    );
  }

  return (
    <>
      <div className="space-y-12">
        {groups.map((group) =>
          group.figures.length > 0 ? (
            <section key={group.phase}>
              <h3 className="mb-6 font-serif text-2xl font-semibold text-text">
                {group.label}
              </h3>
              <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
                {group.figures.map((figure) => (
                  <button
                    key={figure.id}
                    type="button"
                    onClick={() => setActiveFigure(figure)}
                    className="group overflow-hidden rounded-xl border border-border bg-surface-elevated text-left shadow-sm transition-colors hover:border-primary/30"
                  >
                    <div className="relative aspect-[4/3] bg-surface">
                      {figure.available ? (
                        <Image
                          src={figure.publicUrl}
                          alt={figure.title}
                          fill
                          className="object-cover transition-transform duration-200 group-hover:scale-[1.02]"
                          sizes="(max-width: 640px) 100vw, (max-width: 1280px) 50vw, 33vw"
                        />
                      ) : (
                        <div className="flex h-full items-center justify-center px-4 text-xs text-text-muted">
                          Preview unavailable
                        </div>
                      )}
                    </div>
                    <div className="space-y-2 p-4">
                      <p className="text-xs font-semibold uppercase tracking-wider text-accent">
                        {figure.phaseLabel}
                      </p>
                      <h4 className="font-serif text-lg font-semibold text-text group-hover:text-primary">
                        {figure.title}
                      </h4>
                      <p className="line-clamp-2 text-sm text-text-muted">
                        {figure.description}
                      </p>
                      <CardReportLink figure={figure} />
                    </div>
                  </button>
                ))}
              </div>
            </section>
          ) : null,
        )}
      </div>

      <FigureLightbox
        figures={allFigures}
        activeFigure={activeFigure}
        onClose={() => setActiveFigure(null)}
        onNavigate={setActiveFigure}
      />
    </>
  );
}

function CardReportLink({ figure }: { figure: ResultFigure }) {
  if (figure.reportExternal) {
    return (
      <a
        href={figure.reportHref}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 inline-flex text-sm font-medium text-primary hover:text-primary-light"
        onClick={(event) => event.stopPropagation()}
      >
        Related report ↗
      </a>
    );
  }

  return (
    <Link
      href={figure.reportHref}
      className="mt-3 inline-flex text-sm font-medium text-primary hover:text-primary-light"
      onClick={(event) => event.stopPropagation()}
    >
      Related report →
    </Link>
  );
}
