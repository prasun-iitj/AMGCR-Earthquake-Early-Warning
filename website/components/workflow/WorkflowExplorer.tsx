"use client";

import { useEffect, useMemo, useState } from "react";
import { WorkflowAccordion } from "@/components/workflow/WorkflowAccordion";
import { WorkflowStageDetail } from "@/components/workflow/WorkflowStageDetail";
import { WorkflowStageList } from "@/components/workflow/WorkflowStageList";
import type { LoadedWorkflowStage } from "@/lib/workflow/loader";
import type { WorkflowStageId } from "@/lib/workflow/stages.config";

type WorkflowExplorerProps = {
  stages: LoadedWorkflowStage[];
};

function isWorkflowStageId(value: string, stages: LoadedWorkflowStage[]): value is WorkflowStageId {
  return stages.some((stage) => stage.id === value);
}

export function WorkflowExplorer({ stages }: WorkflowExplorerProps) {
  const [selectedId, setSelectedId] = useState<WorkflowStageId>(() => {
    if (typeof window === "undefined") {
      return stages[0]?.id ?? "acquisition";
    }
    const hash = window.location.hash.replace("#", "");
    if (hash && isWorkflowStageId(hash, stages)) {
      return hash;
    }
    return stages[0]?.id ?? "acquisition";
  });

  useEffect(() => {
    const applyHash = () => {
      const hash = window.location.hash.replace("#", "");
      if (hash && isWorkflowStageId(hash, stages)) {
        setSelectedId(hash);
      }
    };

    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, [stages]);

  const selectStage = (id: WorkflowStageId) => {
    setSelectedId(id);
    window.history.replaceState(null, "", `#${id}`);
  };

  const selectedStage = useMemo(
    () => stages.find((stage) => stage.id === selectedId) ?? stages[0],
    [selectedId, stages],
  );

  const selectedIndex = stages.findIndex((stage) => stage.id === selectedStage.id);
  const previous = selectedIndex > 0 ? stages[selectedIndex - 1] : null;
  const next =
    selectedIndex >= 0 && selectedIndex < stages.length - 1
      ? stages[selectedIndex + 1]
      : null;

  return (
    <div className="mx-auto max-w-7xl px-4 pb-16 pt-8 sm:px-6 lg:px-8">
      <div className="hidden gap-8 lg:grid lg:grid-cols-[320px_minmax(0,1fr)]">
        <div>
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-text-muted">
            Pipeline
          </p>
          <WorkflowStageList
            stages={stages}
            selectedId={selectedStage.id}
            onSelect={selectStage}
          />
        </div>

        <WorkflowStageDetail
          stage={selectedStage}
          previous={previous}
          next={next}
          onSelectStage={selectStage}
        />
      </div>

      <div className="lg:hidden">
        <WorkflowAccordion
          stages={stages}
          selectedId={selectedStage.id}
          onSelect={selectStage}
        />

        <nav
          aria-label="Stage navigation"
          className="mt-6 grid gap-3 sm:grid-cols-2"
        >
          {previous ? (
            <button
              type="button"
              onClick={() => selectStage(previous.id)}
              className="rounded-lg border border-border bg-surface-elevated px-4 py-3 text-left text-sm transition-colors hover:border-primary/30"
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
              onClick={() => selectStage(next.id)}
              className="rounded-lg border border-border bg-surface-elevated px-4 py-3 text-right text-sm transition-colors hover:border-primary/30 sm:col-start-2"
            >
              <span className="block text-xs font-semibold uppercase tracking-wider text-text-muted">
                Next stage
              </span>
              <span className="mt-1 font-medium text-text">{next.title} →</span>
            </button>
          ) : null}
        </nav>
      </div>
    </div>
  );
}
