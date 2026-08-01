import fs from "node:fs";
import path from "node:path";
import { getRepositoryStats } from "@/lib/content/stats";
import { resolveRepoPath } from "@/lib/content/paths";
import {
  dashboardTimeline,
  pipelinePhases,
  quickNavCards,
} from "@/lib/dashboard/config";
import type {
  DatasetMetrics,
  LoadedDashboard,
  RepositoryMetrics,
  ResearchSummary,
} from "@/lib/dashboard/types";
import { workflowStageConfigs } from "@/lib/workflow/stages.config";

function countJsonSummaries(): number {
  const reportsDir = resolveRepoPath("reports");
  if (!fs.existsSync(reportsDir)) {
    return 0;
  }

  let count = 0;
  const walk = (directory: string) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        walk(absolute);
        continue;
      }
      if (entry.name.endsWith(".json")) {
        count += 1;
      }
    }
  };

  walk(reportsDir);
  return count;
}

function countTables(): number {
  const tablesDir = resolveRepoPath("reports/tables");
  if (!fs.existsSync(tablesDir)) {
    return 0;
  }

  return fs.readdirSync(tablesDir).filter((file) => file.endsWith(".csv")).length;
}

function loadDatasetMetrics(): DatasetMetrics {
  const summaryPath = resolveRepoPath("reports/eda/dataset_summary.json");
  const featureSummaryPath = resolveRepoPath("reports/features/feature_summary.json");

  if (!fs.existsSync(summaryPath)) {
    return {
      eventCount: null,
      stationCount: null,
      waveformCount: null,
      timeRangeStart: null,
      timeRangeEnd: null,
      magnitudeMin: null,
      magnitudeMax: null,
      samplingRateHz: null,
      channels: [],
      featureMatrixShape: null,
    };
  }

  const summary = JSON.parse(fs.readFileSync(summaryPath, "utf8")) as {
    n_events_manifest?: number;
    n_unique_stations_manifest?: number;
    n_mseed_files_in_manifest?: number;
    channels?: string[];
    sampling_rates_hz_unique?: number[];
    magnitude?: { min?: number; max?: number };
    time_coverage?: { first_origin_utc?: string; last_origin_utc?: string };
  };

  let featureMatrixShape: string | null = null;
  if (fs.existsSync(featureSummaryPath)) {
    const featureSummary = JSON.parse(
      fs.readFileSync(featureSummaryPath, "utf8"),
    ) as { n_features?: number; n_events?: number };
    if (featureSummary.n_events && featureSummary.n_features) {
      featureMatrixShape = `${featureSummary.n_events}×${featureSummary.n_features}`;
    } else if (featureSummary.n_features && summary.n_events_manifest) {
      featureMatrixShape = `${summary.n_events_manifest}×${featureSummary.n_features}`;
    }
  }

  return {
    eventCount: summary.n_events_manifest ?? null,
    stationCount: summary.n_unique_stations_manifest ?? null,
    waveformCount: summary.n_mseed_files_in_manifest ?? null,
    timeRangeStart: summary.time_coverage?.first_origin_utc ?? null,
    timeRangeEnd: summary.time_coverage?.last_origin_utc ?? null,
    magnitudeMin: summary.magnitude?.min ?? null,
    magnitudeMax: summary.magnitude?.max ?? null,
    samplingRateHz: summary.sampling_rates_hz_unique?.[0] ?? null,
    channels: summary.channels ?? [],
    featureMatrixShape,
  };
}

function buildResearchSummary(stats: ReturnType<typeof getRepositoryStats>): ResearchSummary {
  return {
    platformVersion: stats.platformVersion,
    scienceVersion: stats.scienceVersion,
    githubRelease: stats.githubRelease,
    releaseDate: stats.releaseDate,
    researchStatus:
      stats.validationStatus === "PASS"
        ? "v1.0 submission complete"
        : "Active research platform",
    validationStatus: stats.validationStatus,
    californiaPilotStatus: "Complete",
    europePhaseStatus: "Planned (ORFEUS/EIDA expansion)",
  };
}

function buildRepositoryMetrics(
  stats: ReturnType<typeof getRepositoryStats>,
): RepositoryMetrics {
  return {
    documentationCount: stats.documentation,
    reportCount: stats.reports,
    figureCount: stats.figures,
    tableCount: countTables(),
    jsonSummaryCount: countJsonSummaries(),
    workflowPhaseCount: workflowStageConfigs.length,
    websiteVersion: stats.platformVersion,
    researchVersion: stats.scienceVersion,
    analysisScriptCount: stats.analysisScripts,
  };
}

function readGeneratedTimestamp(): string | null {
  const summaryPath = resolveRepoPath("reports/eda/dataset_summary.json");
  if (!fs.existsSync(summaryPath)) {
    return null;
  }

  try {
    const summary = JSON.parse(fs.readFileSync(summaryPath, "utf8")) as {
      generated_at_utc?: string;
    };
    return summary.generated_at_utc ?? null;
  } catch {
    return null;
  }
}

export function loadDashboard(): LoadedDashboard {
  const stats = getRepositoryStats();

  return {
    summary: buildResearchSummary(stats),
    dataset: loadDatasetMetrics(),
    repository: buildRepositoryMetrics(stats),
    pipeline: pipelinePhases,
    quickNav: quickNavCards,
    timeline: dashboardTimeline,
    generatedAtUtc: readGeneratedTimestamp(),
  };
}

/** Future ResearchContext hook: return serializable dashboard snapshot. */
export function getDashboardSnapshot(): LoadedDashboard {
  return loadDashboard();
}
