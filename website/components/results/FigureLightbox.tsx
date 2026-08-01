"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect } from "react";
import type { ResultFigure } from "@/lib/results/loader";

type FigureLightboxProps = {
  figures: ResultFigure[];
  activeFigure: ResultFigure | null;
  onClose: () => void;
  onNavigate: (figure: ResultFigure) => void;
};

export function FigureLightbox({
  figures,
  activeFigure,
  onClose,
  onNavigate,
}: FigureLightboxProps) {
  const shouldReduceMotion = useReducedMotion();
  const activeIndex = activeFigure
    ? figures.findIndex((figure) => figure.id === activeFigure.id)
    : -1;

  const previous =
    activeIndex > 0 ? figures[activeIndex - 1] : figures[figures.length - 1];
  const next =
    activeIndex >= 0 && activeIndex < figures.length - 1
      ? figures[activeIndex + 1]
      : figures[0];

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (!activeFigure) {
        return;
      }

      if (event.key === "Escape") {
        onClose();
      }
      if (event.key === "ArrowLeft") {
        onNavigate(previous);
      }
      if (event.key === "ArrowRight") {
        onNavigate(next);
      }
    },
    [activeFigure, next, onClose, onNavigate, previous],
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  useEffect(() => {
    document.body.style.overflow = activeFigure ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [activeFigure]);

  return (
    <AnimatePresence>
      {activeFigure && (
        <motion.div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: shouldReduceMotion ? 0 : 0.2 }}
        >
          <button
            type="button"
            aria-label="Close figure viewer"
            className="absolute inset-0 bg-primary/80 backdrop-blur-sm"
            onClick={onClose}
          />

          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label={activeFigure.title}
            initial={shouldReduceMotion ? false : { opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={shouldReduceMotion ? undefined : { opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.2 }}
            className="relative z-[101] flex max-h-[90vh] w-full max-w-5xl flex-col overflow-hidden rounded-xl border border-border bg-surface-elevated shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-border px-4 py-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-accent">
                  {activeFigure.phaseLabel}
                </p>
                <h3 className="font-serif text-lg font-semibold text-text">
                  {activeFigure.title}
                </h3>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg border border-border px-3 py-1.5 text-sm text-text-muted transition-colors hover:bg-surface"
              >
                Close
              </button>
            </div>

            <div className="relative max-h-[60vh] min-h-[240px] flex-1 bg-surface">
              {activeFigure.available ? (
                <Image
                  src={activeFigure.publicUrl}
                  alt={activeFigure.title}
                  fill
                  className="object-contain p-4"
                  sizes="(max-width: 1024px) 100vw, 960px"
                  priority
                />
              ) : (
                <div className="flex h-full items-center justify-center p-8 text-sm text-text-muted">
                  Figure not available locally. Regenerate via analysis scripts per
                  D-S1.
                </div>
              )}
            </div>

            <div className="space-y-3 border-t border-border px-4 py-4">
              <p className="text-sm leading-relaxed text-text-muted">
                {activeFigure.description}
              </p>
              <ReportLink figure={activeFigure} />
            </div>

            <div className="flex items-center justify-between gap-3 border-t border-border px-4 py-3">
              <button
                type="button"
                onClick={() => onNavigate(previous)}
                className="rounded-lg border border-border px-3 py-2 text-sm transition-colors hover:border-primary/30 hover:bg-surface"
              >
                ← Previous
              </button>
              <span className="text-xs text-text-muted">
                {activeIndex + 1} / {figures.length}
              </span>
              <button
                type="button"
                onClick={() => onNavigate(next)}
                className="rounded-lg border border-border px-3 py-2 text-sm transition-colors hover:border-primary/30 hover:bg-surface"
              >
                Next →
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function ReportLink({ figure }: { figure: ResultFigure }) {
  if (figure.reportExternal) {
    return (
      <a
        href={figure.reportHref}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex text-sm font-medium text-primary hover:text-primary-light"
      >
        View related report →
      </a>
    );
  }

  return (
    <Link
      href={figure.reportHref}
      className="inline-flex text-sm font-medium text-primary hover:text-primary-light"
    >
      View related report →
    </Link>
  );
}
