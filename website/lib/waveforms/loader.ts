import fs from "node:fs";
import path from "node:path";
import { resolveRepoPath } from "@/lib/content/paths";
import { resolveStageLink } from "@/lib/workflow/stages.config";
import { groupWaveformsByDataset } from "@/lib/waveforms/registry";
import type {
  LoadedWaveformExplorer,
  WaveformDatasetGroup,
  WaveformRecord,
  WaveformSeries,
} from "@/lib/waveforms/types";

type EventSummaryRow = {
  eventId: string;
  originTimeUtc: string;
  latitude: string;
  longitude: string;
  depthKm: string;
  magnitude: string;
  magnitudeType: string;
  stationId: string;
  channel: string;
  samplingRateHz: string;
  durationS: string;
  waveformFile: string;
};

type SignalMetrics = {
  p_pick_time_s?: number;
  snr_peak?: number;
  sta_lta_threshold?: number;
};

type ExportedWaveformJson = {
  short_id: string;
  event_id?: string;
  dataset_id?: string;
  sampling_rate_hz?: number;
  original_sample_count?: number;
  downsampled_point_count?: number;
  p_pick_time_s?: number;
  snr_peak?: number;
  series?: {
    times: number[];
    raw: number[];
    detrended: number[];
    filtered: number[];
    normalized: number[];
  };
  signal_metrics?: SignalMetrics;
};

function parseCsvLine(line: string): string[] {
  const values: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];

    if (char === '"') {
      inQuotes = !inQuotes;
      continue;
    }

    if (char === "," && !inQuotes) {
      values.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  values.push(current.trim());
  return values;
}

function extractShortId(eventId: string): string {
  const marker = "_query_eventid_";
  const formatMarker = "_format_quakeml";
  const start = eventId.indexOf(marker);
  if (start === -1) {
    return eventId;
  }
  const from = start + marker.length;
  const end = eventId.indexOf(formatMarker, from);
  return end === -1 ? eventId.slice(from) : eventId.slice(from, end);
}

function toLink(label: string, repoPath: string) {
  const { href, external } = resolveStageLink(repoPath);
  return { label, path: repoPath, href, external };
}

function loadEventSummaryRows(): EventSummaryRow[] {
  const csvPath = resolveRepoPath("reports/tables/event_summary.csv");
  if (!fs.existsSync(csvPath)) {
    return [];
  }

  const lines = fs
    .readFileSync(csvPath, "utf8")
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0);

  if (lines.length < 2) {
    return [];
  }

  return lines.slice(1).map((line) => {
    const [
      eventId,
      originTimeUtc,
      latitude,
      longitude,
      depthKm,
      magnitude,
      magnitudeType,
      stationId,
      channel,
      samplingRateHz,
      durationS,
      waveformFile,
    ] = parseCsvLine(line);

    return {
      eventId,
      originTimeUtc,
      latitude,
      longitude,
      depthKm,
      magnitude,
      magnitudeType,
      stationId,
      channel,
      samplingRateHz,
      durationS,
      waveformFile,
    };
  });
}

function loadSignalMetrics(shortId: string): SignalMetrics {
  const metricsPath = resolveRepoPath(
    `reports/signal_analysis/${shortId}_metrics.json`,
  );
  if (!fs.existsSync(metricsPath)) {
    return {};
  }
  return JSON.parse(fs.readFileSync(metricsPath, "utf8")) as SignalMetrics;
}

function loadExportedSeries(shortId: string): WaveformSeries | null {
  const publicJson = path.join(process.cwd(), "public/waveforms", `${shortId}.json`);
  const repoJson = resolveRepoPath(
    `website/public/waveforms/${shortId}.json`,
  );

  const jsonPath = fs.existsSync(publicJson)
    ? publicJson
    : fs.existsSync(repoJson)
      ? repoJson
      : null;

  if (!jsonPath) {
    return null;
  }

  const payload = JSON.parse(
    fs.readFileSync(jsonPath, "utf8"),
  ) as ExportedWaveformJson;

  if (!payload.series) {
    return null;
  }

  return {
    times: payload.series.times,
    raw: payload.series.raw,
    detrended: payload.series.detrended,
    filtered: payload.series.filtered,
    normalized: payload.series.normalized,
    samplingRateHz: payload.sampling_rate_hz ?? 40,
    originalSampleCount: payload.original_sample_count ?? payload.series.times.length,
    downsampledPointCount:
      payload.downsampled_point_count ?? payload.series.times.length,
  };
}

function figureAvailable(filename: string): boolean {
  const figuresDir = resolveRepoPath("reports/figures");
  const publicDir = path.join(process.cwd(), "public/figures");
  return (
    fs.existsSync(path.join(figuresDir, filename)) ||
    fs.existsSync(path.join(publicDir, filename))
  );
}

function buildPreviewFigure(
  shortId: string,
  phase: "signalAnalysis" | "preprocessing",
): WaveformRecord["previewFigures"]["signalAnalysis"] {
  const filename =
    phase === "signalAnalysis"
      ? `signal_analysis_${shortId}.png`
      : `preprocessing_${shortId}.png`;
  const reportPath =
    phase === "signalAnalysis"
      ? "docs/SIGNAL_ANALYSIS_REPORT.md"
      : "docs/PREPROCESSING_REPORT.md";
  const reportLink = resolveStageLink(reportPath);

  return {
    label:
      phase === "signalAnalysis"
        ? "Signal analysis figure"
        : "Preprocessing figure",
    filename,
    publicUrl: `/figures/${filename}`,
    available: figureAvailable(filename),
    reportHref: reportLink.href,
    reportExternal: reportLink.external,
  };
}

function buildCaliforniaWaveform(row: EventSummaryRow): WaveformRecord {
  const shortId = extractShortId(row.eventId);
  const signalMetrics = loadSignalMetrics(shortId);
  const series = loadExportedSeries(shortId);
  const signalReport = toLink("Signal analysis report", "docs/SIGNAL_ANALYSIS_REPORT.md");
  const preprocessingReport = toLink(
    "Preprocessing report",
    "docs/PREPROCESSING_REPORT.md",
  );
  const edaReport = toLink("EDA report", "docs/EDA_REPORT.md");
  const featureReport = toLink(
    "Feature engineering report",
    "docs/FEATURE_ENGINEERING_REPORT.md",
  );
  const irisReport = toLink("IRIS dataset report", "docs/IRIS_DATASET_REPORT.md");
  const finalReport = toLink("Final research report", "reports/Research_Report_Final.md");

  return {
    id: shortId,
    eventId: row.eventId,
    datasetId: "california-pilot",
    datasetName: "California Pilot",
    stationId: row.stationId,
    channel: row.channel,
    magnitude: Number.parseFloat(row.magnitude),
    magnitudeType: row.magnitudeType,
    originTimeUtc: row.originTimeUtc,
    latitude: Number.parseFloat(row.latitude),
    longitude: Number.parseFloat(row.longitude),
    depthKm: Number.parseFloat(row.depthKm),
    durationS: Number.parseFloat(row.durationS),
    samplingRateHz: Number.parseFloat(row.samplingRateHz),
    waveformFile: row.waveformFile,
    pPickTimeS: signalMetrics.p_pick_time_s ?? null,
    snrPeak: signalMetrics.snr_peak ?? null,
    staLtaThreshold: signalMetrics.sta_lta_threshold ?? null,
    seriesAvailable: series !== null,
    series,
    previewFigures: {
      signalAnalysis: buildPreviewFigure(shortId, "signalAnalysis"),
      preprocessing: buildPreviewFigure(shortId, "preprocessing"),
    },
    relatedReports: [
      irisReport,
      edaReport,
      signalReport,
      preprocessingReport,
      featureReport,
      finalReport,
    ],
    relatedDocs: [
      toLink("Dataset overview", "docs/DATASET.md"),
      toLink("Data availability", "docs/DATA_AVAILABILITY_STATEMENT.md"),
      toLink("Reproducibility", "docs/REPRODUCIBILITY_STATEMENT.md"),
    ],
    workflowStages: [
      { ...toLink("Acquisition", "docs/IRIS_DATASET_REPORT.md"), label: "Acquisition" },
      { label: "EDA", path: "docs/EDA_REPORT.md", href: "/workflow#eda", external: false },
      {
        label: "Signal analysis",
        path: "docs/SIGNAL_ANALYSIS_REPORT.md",
        href: "/workflow#signal-analysis",
        external: false,
      },
      {
        label: "Preprocessing",
        path: "docs/PREPROCESSING_REPORT.md",
        href: "/workflow#preprocessing",
        external: false,
      },
      {
        label: "Feature engineering",
        path: "docs/FEATURE_ENGINEERING_REPORT.md",
        href: "/workflow#feature-engineering",
        external: false,
      },
    ],
    featureLinks: [
      toLink("Event summary table", "reports/tables/event_summary.csv"),
      toLink("Signal analysis per event", "reports/tables/signal_analysis_per_event.csv"),
      toLink("Preprocessing quality metrics", "reports/tables/preprocessing_quality_metrics.csv"),
      toLink("Feature matrix", "reports/tables/feature_matrix.csv"),
    ],
    npzSourcePath: `reports/preprocessing/${shortId}_stages.npz`,
    npzLink: toLink("Preprocessing stages NPZ", `reports/preprocessing/${shortId}_stages.npz`),
    metadata: {
      waveform_id: shortId,
      event_id: row.eventId,
      dataset_id: "california-pilot",
      station_id: row.stationId,
      channel: row.channel,
      magnitude: Number.parseFloat(row.magnitude),
      origin_time_utc: row.originTimeUtc,
      sampling_rate_hz: Number.parseFloat(row.samplingRateHz),
      duration_s: Number.parseFloat(row.durationS),
      p_pick_time_s: signalMetrics.p_pick_time_s ?? null,
      snr_peak: signalMetrics.snr_peak ?? null,
      series_available: series !== null,
    },
  };
}

export function loadWaveformExplorer(): LoadedWaveformExplorer {
  const californiaWaveforms = loadEventSummaryRows().map(buildCaliforniaWaveform);

  const californiaGroup: WaveformDatasetGroup = {
    datasetId: "california-pilot",
    datasetName: "California Pilot",
    status: "active",
    waveforms: californiaWaveforms,
    waveformCount: californiaWaveforms.length,
  };

  const groups = groupWaveformsByDataset([californiaGroup]);
  const waveforms = californiaWaveforms;

  return {
    groups,
    waveforms,
    defaultWaveformId: waveforms[0]?.id ?? null,
    totalWaveforms: waveforms.length,
    seriesAvailableCount: waveforms.filter((waveform) => waveform.seriesAvailable).length,
  };
}

/** Phase 8 hook: resolve waveform metadata by id for map selection. */
export function getWaveformById(id: string): WaveformRecord | null {
  return loadWaveformExplorer().waveforms.find((waveform) => waveform.id === id) ?? null;
}

/** Phase 9 / v3 hook: export serializable waveform metadata index. */
export function getWaveformMetadataIndex(): Record<
  string,
  WaveformRecord["metadata"]
> {
  return Object.fromEntries(
    loadWaveformExplorer().waveforms.map((waveform) => [
      waveform.id,
      waveform.metadata,
    ]),
  );
}
