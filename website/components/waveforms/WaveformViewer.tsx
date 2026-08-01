"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import type {
  WaveformRecord,
  WaveformStage,
  WaveformViewport,
} from "@/lib/waveforms/types";

const stageLabels: Record<WaveformStage, string> = {
  raw: "Raw",
  detrended: "Detrended",
  filtered: "Filtered",
  normalized: "Normalized",
};

const defaultViewport: WaveformViewport = {
  startTimeS: 0,
  endTimeS: 300,
  channels: ["BHZ"],
};

type WaveformViewerProps = {
  waveform: WaveformRecord;
};

export function WaveformViewer({ waveform }: WaveformViewerProps) {
  const [stage, setStage] = useState<WaveformStage>("filtered");
  const [viewport] = useState<WaveformViewport>(defaultViewport);

  const chart = useMemo(() => {
    if (!waveform.series) {
      return null;
    }

    const { times } = waveform.series;
    const values = waveform.series[stage];
    const width = 900;
    const height = 320;
    const padding = { top: 16, right: 16, bottom: 36, left: 56 };
    const plotWidth = width - padding.left - padding.right;
    const plotHeight = height - padding.top - padding.bottom;

    const visibleIndices = times.reduce<number[]>((indices, time, index) => {
      if (time >= viewport.startTimeS && time <= viewport.endTimeS) {
        indices.push(index);
      }
      return indices;
    }, []);

    const visibleTimes = visibleIndices.map((index) => times[index]);
    const visibleValues = visibleIndices.map((index) => values[index]);

    if (visibleTimes.length === 0) {
      return null;
    }

    const minTime = visibleTimes[0];
    const maxTime = visibleTimes[visibleTimes.length - 1];
    const minValue = Math.min(...visibleValues);
    const maxValue = Math.max(...visibleValues);
    const valueRange = maxValue - minValue || 1;

    const points = visibleTimes.map((time, index) => {
      const x =
        padding.left +
        ((time - minTime) / (maxTime - minTime || 1)) * plotWidth;
      const y =
        padding.top +
        plotHeight -
        ((visibleValues[index] - minValue) / valueRange) * plotHeight;
      return `${x},${y}`;
    });

    const pPickX =
      waveform.pPickTimeS != null &&
      waveform.pPickTimeS >= minTime &&
      waveform.pPickTimeS <= maxTime
        ? padding.left +
          ((waveform.pPickTimeS - minTime) / (maxTime - minTime || 1)) * plotWidth
        : null;

    return {
      width,
      height,
      padding,
      plotWidth,
      plotHeight,
      path: points.join(" "),
      minTime,
      maxTime,
      minValue,
      maxValue,
      pPickX,
    };
  }, [stage, viewport.endTimeS, viewport.startTimeS, waveform]);

  const previewFigure = waveform.previewFigures.preprocessing.available
    ? waveform.previewFigures.preprocessing
    : waveform.previewFigures.signalAnalysis;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wider text-accent">
          Waveform viewer
        </p>
        <h2 className="mt-2 font-serif text-2xl font-semibold text-text">
          {waveform.id} · {waveform.stationId}
        </h2>
        <p className="mt-2 text-sm text-text-muted">
          Processed preview from repository NPZ stages. Full-resolution data
          remains in the research repository.
        </p>
      </div>

      {waveform.series ? (
        <>
          <div
            className="flex flex-wrap gap-2"
            role="tablist"
            aria-label="Processing stage"
          >
            {(Object.keys(stageLabels) as WaveformStage[]).map((stageId) => (
              <button
                key={stageId}
                type="button"
                role="tab"
                aria-selected={stage === stageId}
                onClick={() => setStage(stageId)}
                className={[
                  "rounded-full px-3 py-1.5 text-sm font-medium transition-colors",
                  stage === stageId
                    ? "bg-primary text-white"
                    : "border border-border bg-surface text-text-muted hover:border-primary/30 hover:text-text",
                ].join(" ")}
              >
                {stageLabels[stageId]}
              </button>
            ))}
          </div>

          <div className="overflow-x-auto rounded-xl border border-border bg-surface p-4">
            {chart ? (
              <svg
                viewBox={`0 0 ${chart.width} ${chart.height}`}
                className="h-auto w-full min-w-[320px]"
                role="img"
                aria-label={`${stageLabels[stage]} waveform for ${waveform.id}`}
              >
                <rect
                  x={chart.padding.left}
                  y={chart.padding.top}
                  width={chart.plotWidth}
                  height={chart.plotHeight}
                  fill="var(--color-surface-elevated)"
                  stroke="var(--color-border)"
                />
                <polyline
                  fill="none"
                  stroke="var(--color-primary)"
                  strokeWidth="1.5"
                  points={chart.path}
                />
                {chart.pPickX != null ? (
                  <>
                    <line
                      x1={chart.pPickX}
                      x2={chart.pPickX}
                      y1={chart.padding.top}
                      y2={chart.padding.top + chart.plotHeight}
                      stroke="var(--color-accent)"
                      strokeWidth="1.5"
                      strokeDasharray="4 4"
                    />
                    <text
                      x={chart.pPickX + 4}
                      y={chart.padding.top + 14}
                      fill="var(--color-accent)"
                      fontSize="11"
                    >
                      P-pick
                    </text>
                  </>
                ) : null}
                <text
                  x={chart.padding.left}
                  y={chart.height - 10}
                  fill="var(--color-text-muted)"
                  fontSize="11"
                >
                  Time (s)
                </text>
                <text
                  x={12}
                  y={chart.padding.top + 12}
                  fill="var(--color-text-muted)"
                  fontSize="11"
                  transform={`rotate(-90 12 ${chart.padding.top + 12})`}
                >
                  Amplitude
                </text>
              </svg>
            ) : null}
          </div>

          <p className="text-xs text-text-muted">
            Showing {waveform.series.downsampledPointCount} of{" "}
            {waveform.series.originalSampleCount} samples ·{" "}
            {waveform.series.samplingRateHz} Hz · Stage: {stageLabels[stage]}
            {waveform.pPickTimeS != null
              ? ` · P-pick at ${waveform.pPickTimeS}s`
              : ""}
          </p>
        </>
      ) : (
        <div className="space-y-4">
          <div className="rounded-xl border border-dashed border-border bg-surface p-4 text-sm text-text-muted">
            Interactive series preview unavailable. Run{" "}
            <code className="rounded bg-surface-elevated px-1 py-0.5">
              python website/scripts/export-waveforms.py
            </code>{" "}
            during build to export NPZ stages, or use the static figure below.
          </div>

          {previewFigure.available ? (
            <div className="relative aspect-[4/3] overflow-hidden rounded-xl border border-border bg-surface">
              <Image
                src={previewFigure.publicUrl}
                alt={`${previewFigure.label} for ${waveform.id}`}
                fill
                className="object-contain"
                sizes="(max-width: 1280px) 100vw, 900px"
              />
            </div>
          ) : (
            <div className="rounded-xl border border-dashed border-border bg-surface p-8 text-center text-sm text-text-muted">
              No processed figure preview found in reports/figures/.
            </div>
          )}
        </div>
      )}

      <p className="text-xs text-text-muted">
        Viewer architecture supports future zoom, pan, multi-channel overlay, and
        comparison modes via viewport state without redesign.
      </p>
    </div>
  );
}
