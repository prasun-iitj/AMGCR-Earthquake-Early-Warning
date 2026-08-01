/**
 * Waveform explorer types — designed for map (Phase 8), dashboard (Phase 9), and AI (v3).
 */

import type { DatasetLink } from "@/lib/dataset/types";

export type WaveformStage = "raw" | "detrended" | "filtered" | "normalized";

export type WaveformSeries = {
  times: number[];
  raw: number[];
  detrended: number[];
  filtered: number[];
  normalized: number[];
  samplingRateHz: number;
  originalSampleCount: number;
  downsampledPointCount: number;
};

/** Viewport state for future zoom/pan — not fully implemented in Phase 7. */
export type WaveformViewport = {
  startTimeS: number;
  endTimeS: number;
  /** Future: multi-channel overlay comparison */
  channels: string[];
};

export type WaveformPreviewFigure = {
  label: string;
  filename: string;
  publicUrl: string;
  available: boolean;
  reportHref: string;
  reportExternal: boolean;
};

export type WaveformRecord = {
  id: string;
  eventId: string;
  datasetId: string;
  datasetName: string;
  stationId: string;
  channel: string;
  magnitude: number;
  magnitudeType: string;
  originTimeUtc: string;
  latitude: number | null;
  longitude: number | null;
  depthKm: number | null;
  durationS: number;
  samplingRateHz: number;
  waveformFile: string;
  pPickTimeS: number | null;
  snrPeak: number | null;
  staLtaThreshold: number | null;
  seriesAvailable: boolean;
  series: WaveformSeries | null;
  previewFigures: {
    signalAnalysis: WaveformPreviewFigure;
    preprocessing: WaveformPreviewFigure;
  };
  relatedReports: DatasetLink[];
  relatedDocs: DatasetLink[];
  workflowStages: DatasetLink[];
  featureLinks: DatasetLink[];
  npzSourcePath: string;
  npzLink: DatasetLink;
  /** Serializable metadata for dashboard / AI indexing (v3). */
  metadata: Record<string, string | number | boolean | null>;
};

export type WaveformDatasetGroup = {
  datasetId: string;
  datasetName: string;
  status: "active" | "planned";
  waveforms: WaveformRecord[];
  waveformCount: number;
};

export type LoadedWaveformExplorer = {
  groups: WaveformDatasetGroup[];
  waveforms: WaveformRecord[];
  defaultWaveformId: string | null;
  totalWaveforms: number;
  seriesAvailableCount: number;
};
