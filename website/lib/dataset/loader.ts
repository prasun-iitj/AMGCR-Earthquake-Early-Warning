import fs from "node:fs";
import path from "node:path";
import { resolveRepoPath } from "@/lib/content/paths";
import { loadResultsExplorerData } from "@/lib/results/loader";
import { resolveStageLink } from "@/lib/workflow/stages.config";
import { datasetJourneySteps } from "@/lib/dataset/journey";
import {
  datasetRegistry,
  defaultDatasetId,
  getRegistryEntry,
} from "@/lib/dataset/registry";
import type {
  DatasetLink,
  DatasetRecord,
  LoadedDatasetExplorer,
} from "@/lib/dataset/types";

function toLink(label: string, repoPath: string): DatasetLink {
  const { href, external } = resolveStageLink(repoPath);
  return { label, path: repoPath, href, external };
}

function loadCaliforniaPilot(): DatasetRecord {
  const edaSummaryPath = resolveRepoPath("reports/eda/dataset_summary.json");
  const featureSummaryPath = resolveRepoPath("reports/features/feature_summary.json");
  const manifestPath = "data/manifests/iris_california_pilot_events.csv";

  let edaSummary: {
    n_events_manifest?: number;
    n_unique_stations_manifest?: number;
    n_mseed_files_in_manifest?: number;
    channels?: string[];
    sampling_rates_hz_unique?: number[];
    magnitude?: { min?: number; max?: number };
    time_coverage?: { first_origin_utc?: string; last_origin_utc?: string };
    station_ids_manifest?: string[];
  } = {};

  if (fs.existsSync(edaSummaryPath)) {
    edaSummary = JSON.parse(fs.readFileSync(edaSummaryPath, "utf8"));
  }

  let featureCount: number | null = null;
  if (fs.existsSync(featureSummaryPath)) {
    const featureSummary = JSON.parse(fs.readFileSync(featureSummaryPath, "utf8")) as {
      n_features?: number;
    };
    featureCount = featureSummary.n_features ?? null;
  }

  const { figures, tables } = loadResultsExplorerData();

  const reportPaths = [
    "docs/IRIS_DATASET_REPORT.md",
    "docs/EDA_REPORT.md",
    "docs/SIGNAL_ANALYSIS_REPORT.md",
    "docs/PREPROCESSING_REPORT.md",
    "docs/FEATURE_ENGINEERING_REPORT.md",
    "docs/RESULTS_AND_DISCUSSION.md",
    "reports/Research_Report_Final.md",
  ];

  const docPaths = [
    "docs/DATASET.md",
    "docs/DATA_AVAILABILITY_STATEMENT.md",
    "docs/REPRODUCIBILITY_STATEMENT.md",
    "docs/PROJECT_CHARTER.md",
  ];

  const manifestPublic = "/datasets/iris_california_pilot_events.csv";
  const manifestExists =
    fs.existsSync(resolveRepoPath(manifestPath)) ||
    fs.existsSync(path.join(process.cwd(), "public/datasets/iris_california_pilot_events.csv"));

  const downloadCandidates: DatasetLink[] = [
    {
      label: "Event manifest (CSV)",
      path: manifestPath,
      href: manifestExists ? manifestPublic : resolveStageLink(manifestPath).href,
      external: !manifestExists,
    },
    {
      label: "Feature matrix (CSV)",
      path: "reports/tables/feature_matrix.csv",
      href: "/tables/feature_matrix.csv",
      external: false,
    },
    ...tables.map((table) => ({
      label: table.title,
      path: `reports/tables/${table.filename}`,
      href: table.downloadUrl,
      external: false,
    })),
    toLink("Final research report", "reports/Research_Report_Final.md"),
    toLink("IRIS dataset report", "docs/IRIS_DATASET_REPORT.md"),
  ];

  const downloads = Array.from(
    new Map(downloadCandidates.map((item) => [item.path, item])).values(),
  );

  const statistics = {
    eventCount: edaSummary.n_events_manifest ?? null,
    stationCount: edaSummary.n_unique_stations_manifest ?? null,
    waveformCount: edaSummary.n_mseed_files_in_manifest ?? null,
    magnitudeMin: edaSummary.magnitude?.min ?? null,
    magnitudeMax: edaSummary.magnitude?.max ?? null,
    timeRangeStart: edaSummary.time_coverage?.first_origin_utc ?? null,
    timeRangeEnd: edaSummary.time_coverage?.last_origin_utc ?? null,
    samplingRateHz: edaSummary.sampling_rates_hz_unique?.[0] ?? null,
    channels: edaSummary.channels ?? [],
    featureCount,
    figureCount: figures.length,
    tableCount: tables.length,
    reportCount: reportPaths.length,
  };

  return {
    id: "california-pilot",
    name: "California Pilot",
    region: "United States (California)",
    status: "active",
    summary:
      "Completed certificate-track pilot using USGS event metadata and EarthScope MiniSEED waveforms acquired with ObsPy.",
    source: "USGS FDSN (events) · EarthScope (waveforms)",
    acquisitionMethod: "ObsPy FDSN clients — scripts/download/download_iris_california_pilot.py",
    providers: ["USGS", "EarthScope"],
    capabilities: {
      waveforms: true,
      map: true,
      dashboard: true,
      aiMetadata: true,
    },
    statistics,
    manifestPath,
    rawDataPath: "data/raw/iris/",
    reports: reportPaths.map((reportPath) =>
      toLink(path.basename(reportPath).replace(".md", ""), reportPath),
    ),
    figures: figures.slice(0, 12).map((figure) => ({
      label: figure.title,
      path: `reports/figures/${figure.filename}`,
      href: figure.publicUrl,
      external: false,
    })),
    tables: tables.map((table) => ({
      label: table.title,
      path: `reports/tables/${table.filename}`,
      href: table.downloadUrl,
      external: false,
    })),
    documentation: docPaths.map((docPath) =>
      toLink(path.basename(docPath).replace(".md", ""), docPath),
    ),
    downloads,
    metadata: {
      dataset_id: "california-pilot",
      region: "california-usa",
      status: "active",
      fdsn_event_provider: "USGS",
      fdsn_waveform_provider: "EarthScope",
      channels: statistics.channels,
      station_ids: edaSummary.station_ids_manifest ?? [],
      science_freeze: "2026-07-29",
      feature_matrix_shape: featureCount
        ? `${statistics.eventCount ?? 8}x${featureCount}`
        : null,
    },
  };
}

function loadPlannedDataset(id: string): DatasetRecord {
  const entry = getRegistryEntry(id);
  if (!entry) {
    throw new Error(`Unknown dataset: ${id}`);
  }

  return {
    id: entry.id,
    name: entry.name,
    region: entry.region,
    status: "planned",
    summary: entry.teaser,
    source: "Not yet acquired",
    acquisitionMethod: "Planned — same manifest-and-report pattern as California pilot",
    providers: [],
    capabilities: {
      waveforms: false,
      map: false,
      dashboard: false,
      aiMetadata: false,
    },
    statistics: {
      eventCount: null,
      stationCount: null,
      waveformCount: null,
      magnitudeMin: null,
      magnitudeMax: null,
      timeRangeStart: null,
      timeRangeEnd: null,
      samplingRateHz: null,
      channels: [],
      featureCount: null,
      figureCount: null,
      tableCount: null,
      reportCount: null,
    },
    manifestPath: null,
    rawDataPath: null,
    reports: [toLink("Version 2.0 roadmap", "docs/ROADMAP.md")],
    figures: [],
    tables: [],
    documentation: [
      toLink("Research direction", "docs/RESEARCH_DIRECTION.md"),
      toLink("Project charter", "docs/PROJECT_CHARTER.md"),
    ],
    downloads: [],
    metadata: {
      dataset_id: entry.id,
      region: entry.region,
      status: "planned",
    },
  };
}

export function loadDatasetById(id: string): DatasetRecord {
  if (id === "california-pilot") {
    return loadCaliforniaPilot();
  }
  return loadPlannedDataset(id);
}

export function loadDatasetExplorer(): LoadedDatasetExplorer {
  const california = loadCaliforniaPilot();
  const planned = datasetRegistry
    .filter((entry) => entry.status === "planned")
    .map((entry) => loadPlannedDataset(entry.id));

  const datasets = [california, ...planned];

  return {
    overview: {
      activeDatasetCount: datasets.filter((d) => d.status === "active").length,
      plannedDatasetCount: datasets.filter((d) => d.status === "planned").length,
      totalEvents: california.statistics.eventCount ?? 0,
      totalStations: california.statistics.stationCount ?? 0,
    },
    datasets,
    registry: datasetRegistry,
    journey: datasetJourneySteps,
    defaultDatasetId,
  };
}

/** Future Phase 7/8/9 hook: resolve dataset for feature modules. */
export function getActiveDatasets(): DatasetRecord[] {
  return loadDatasetExplorer().datasets.filter((dataset) => dataset.status === "active");
}

/** Future v3 hook: export serializable metadata corpus for AI indexing. */
export function getDatasetMetadataIndex(): Record<string, DatasetRecord["metadata"]> {
  return Object.fromEntries(
    loadDatasetExplorer().datasets.map((dataset) => [dataset.id, dataset.metadata]),
  );
}
