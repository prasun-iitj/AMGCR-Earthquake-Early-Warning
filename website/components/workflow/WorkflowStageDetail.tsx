"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import { ResourceList } from "@/components/workflow/ResourceList";
import type { WorkflowStageId } from "@/lib/workflow/stages.config";
import type { LoadedWorkflowStage } from "@/lib/workflow/loader";

type WorkflowStageDetailProps = {
  stage: LoadedWorkflowStage;
  previous: LoadedWorkflowStage | null;
  next: LoadedWorkflowStage | null;
  onSelectStage: (id: WorkflowStageId) => void;
};

export function WorkflowStageDetail({
  stage,
  previous,
  next,
  onSelectStage,
}: WorkflowStageDetailProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={stage.id}
        initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={shouldReduceMotion ? undefined : { opacity: 0, y: -8 }}
        transition={{ duration: 0.22, ease: "easeOut" }}
        className="rounded-xl border border-border bg-surface-elevated p-6 shadow-sm md:p-8"
      >
        <div className="mb-6 border-b border-border pb-6">
          <p className="text-sm font-semibold uppercase tracking-wider text-accent">
            Stage {stage.order}
          </p>
          <h2 className="mt-2 font-serif text-2xl font-semibold text-text md:text-3xl">
            {stage.title}
          </h2>
        </div>

        <section className="mb-8">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
            Purpose
          </h3>
          <p className="mt-3 text-sm leading-relaxed text-text-muted">
            {stage.purpose}
          </p>
        </section>

        <div className="grid gap-8 lg:grid-cols-2">
          <ResourceList title="Inputs" items={stage.inputs} />
          <ResourceList title="Outputs" items={stage.outputs} />
          <ResourceList title="Related reports" items={stage.reports} />
          <ResourceList title="Related documentation" items={stage.documentation} />
          <ResourceList title="Related figures" items={stage.figures} />
          <ResourceList title="Related scripts" items={stage.scripts} />
        </div>

        <nav
          aria-label="Stage navigation"
          className="mt-10 flex flex-col gap-3 border-t border-border pt-6 sm:flex-row sm:justify-between"
        >
          {previous ? (
            <button
              type="button"
              onClick={() => onSelectStage(previous.id)}
              className="rounded-lg border border-border bg-surface px-4 py-3 text-left text-sm transition-colors hover:border-primary/30 hover:bg-white"
            >
              <span className="block text-xs font-semibold uppercase tracking-wider text-text-muted">
                Previous stage
              </span>
              <span className="mt-1 font-medium text-text">← {previous.title}</span>
            </button>
          ) : (
            <div />
          )}

          {next ? (
            <button
              type="button"
              onClick={() => onSelectStage(next.id)}
              className="rounded-lg border border-border bg-surface px-4 py-3 text-right text-sm transition-colors hover:border-primary/30 hover:bg-white sm:ml-auto"
            >
              <span className="block text-xs font-semibold uppercase tracking-wider text-text-muted">
                Next stage
              </span>
              <span className="mt-1 font-medium text-text">{next.title} →</span>
            </button>
          ) : null}
        </nav>

        <p className="mt-6 text-xs text-text-muted">
          Primary report:{" "}
          {stage.reports[0]?.external ? (
            <a
              href={stage.reports[0].href}
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-primary hover:text-primary-light"
            >
              {stage.reports[0].path}
            </a>
          ) : (
            <Link
              href={stage.reports[0]?.href ?? "#"}
              className="font-mono text-primary hover:text-primary-light"
            >
              {stage.reports[0]?.path}
            </Link>
          )}
        </p>
      </motion.div>
    </AnimatePresence>
  );
}
