"use client";

import { motion, useReducedMotion } from "framer-motion";
import type { WorkflowStageId } from "@/lib/workflow/stages.config";
import type { LoadedWorkflowStage } from "@/lib/workflow/loader";

type WorkflowStageListProps = {
  stages: LoadedWorkflowStage[];
  selectedId: WorkflowStageId;
  onSelect: (id: WorkflowStageId) => void;
};

export function WorkflowStageList({
  stages,
  selectedId,
  onSelect,
}: WorkflowStageListProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <nav aria-label="Workflow stages" className="space-y-2">
      {stages.map((stage, index) => {
        const isSelected = stage.id === selectedId;

        return (
          <div key={stage.id}>
            <motion.button
              type="button"
              onClick={() => onSelect(stage.id)}
              whileHover={shouldReduceMotion ? undefined : { scale: 1.01 }}
              whileTap={shouldReduceMotion ? undefined : { scale: 0.99 }}
              className={[
                "w-full rounded-xl border px-4 py-4 text-left transition-colors",
                isSelected
                  ? "border-primary bg-primary text-white shadow-sm"
                  : "border-border bg-surface-elevated text-text hover:border-primary/30 hover:bg-white",
              ].join(" ")}
              aria-current={isSelected ? "step" : undefined}
            >
              <p
                className={[
                  "text-xs font-semibold uppercase tracking-wider",
                  isSelected ? "text-white/80" : "text-text-muted",
                ].join(" ")}
              >
                Stage {stage.order}
              </p>
              <p className="mt-1 font-serif text-lg font-semibold">{stage.title}</p>
            </motion.button>

            {index < stages.length - 1 && (
              <div
                aria-hidden="true"
                className="flex justify-center py-2 text-text-muted"
              >
                ↓
              </div>
            )}
          </div>
        );
      })}
    </nav>
  );
}
