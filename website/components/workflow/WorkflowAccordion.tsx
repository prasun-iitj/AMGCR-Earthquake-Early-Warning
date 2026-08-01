"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { ResourceList } from "@/components/workflow/ResourceList";
import type { WorkflowStageId } from "@/lib/workflow/stages.config";
import type { LoadedWorkflowStage } from "@/lib/workflow/loader";

type WorkflowAccordionProps = {
  stages: LoadedWorkflowStage[];
  selectedId: WorkflowStageId;
  onSelect: (id: WorkflowStageId) => void;
};

export function WorkflowAccordion({
  stages,
  selectedId,
  onSelect,
}: WorkflowAccordionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <div className="space-y-3 lg:hidden">
      {stages.map((stage, index) => {
        const isOpen = stage.id === selectedId;

        return (
          <article
            key={stage.id}
            className="overflow-hidden rounded-xl border border-border bg-surface-elevated"
          >
            <button
              type="button"
              onClick={() => onSelect(stage.id)}
              className="flex w-full items-center justify-between gap-4 px-4 py-4 text-left"
              aria-expanded={isOpen}
            >
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  Stage {stage.order}
                </p>
                <p className="mt-1 font-serif text-lg font-semibold text-text">
                  {stage.title}
                </p>
              </div>
              <span className="text-text-muted">{isOpen ? "−" : "+"}</span>
            </button>

            <AnimatePresence initial={false}>
              {isOpen && (
                <motion.div
                  initial={shouldReduceMotion ? false : { height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={shouldReduceMotion ? undefined : { height: 0, opacity: 0 }}
                  transition={{ duration: 0.24, ease: "easeOut" }}
                  className="overflow-hidden"
                >
                  <div className="space-y-6 border-t border-border px-4 py-4">
                    <section>
                      <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                        Purpose
                      </h3>
                      <p className="mt-2 text-sm leading-relaxed text-text-muted">
                        {stage.purpose}
                      </p>
                    </section>
                    <ResourceList title="Inputs" items={stage.inputs} />
                    <ResourceList title="Outputs" items={stage.outputs} />
                    <ResourceList title="Related reports" items={stage.reports} />
                    <ResourceList
                      title="Related documentation"
                      items={stage.documentation}
                    />
                    <ResourceList title="Related figures" items={stage.figures} />
                    <ResourceList title="Related scripts" items={stage.scripts} />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {index < stages.length - 1 && (
              <div
                aria-hidden="true"
                className="flex justify-center py-1 text-sm text-text-muted"
              >
                ↓
              </div>
            )}
          </article>
        );
      })}
    </div>
  );
}
