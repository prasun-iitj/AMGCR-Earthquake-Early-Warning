import fs from "node:fs";
import path from "node:path";
import { resolveRepoPath } from "@/lib/content/paths";
import { siteConfig } from "@/lib/navigation";

const PHASE_REPORT_FILES = [
  "IRIS_DATASET_REPORT.md",
  "EDA_REPORT.md",
  "SIGNAL_ANALYSIS_REPORT.md",
  "PREPROCESSING_REPORT.md",
  "FEATURE_ENGINEERING_REPORT.md",
  "RESULTS_AND_DISCUSSION.md",
] as const;

export type RepositoryStats = {
  documentation: number;
  reports: number;
  figures: number;
  researchPhases: number;
  githubRelease: string;
  releaseDate: string | null;
  validationStatus: string | null;
  platformVersion: string;
  scienceVersion: string;
  analysisScripts: number;
  pilotEvents: number | null;
};

function countMarkdownFiles(directory: string): number {
  if (!fs.existsSync(directory)) {
    return 0;
  }

  return fs
    .readdirSync(directory)
    .filter((entry) => entry.endsWith(".md")).length;
}

function countAnalysisScripts(): number {
  const analysisDir = resolveRepoPath("scripts/analysis");
  if (!fs.existsSync(analysisDir)) {
    return 0;
  }

  return fs
    .readdirSync(analysisDir)
    .filter((entry) => entry.endsWith(".py")).length;
}

function readPilotEventCount(): number | null {
  const manifestPath = resolveRepoPath(
    "data/manifests/iris_california_pilot_events.csv",
  );
  if (!fs.existsSync(manifestPath)) {
    return null;
  }

  const lines = fs
    .readFileSync(manifestPath, "utf8")
    .split("\n")
    .filter((line) => line.trim().length > 0);

  return Math.max(lines.length - 1, 0);
}

function readValidationSummary(): {
  figureCount: number;
  status: string | null;
  timestamp: string | null;
} {
  const validationPath = resolveRepoPath("FINAL_SUBMISSION/VALIDATION_SUMMARY.json");
  if (!fs.existsSync(validationPath)) {
    return { figureCount: 0, status: null, timestamp: null };
  }

  try {
    const data = JSON.parse(fs.readFileSync(validationPath, "utf8")) as {
      figure_count_on_disk?: number;
      outputs_missing?: string[];
      figures_missing_on_disk?: string[];
      timestamp_utc?: string;
    };

    const status =
      (data.outputs_missing?.length ?? 0) === 0 &&
      (data.figures_missing_on_disk?.length ?? 0) === 0
        ? "PASS"
        : "CHECK";

    return {
      figureCount: data.figure_count_on_disk ?? 0,
      status,
      timestamp: data.timestamp_utc ?? null,
    };
  } catch {
    return { figureCount: 0, status: null, timestamp: null };
  }
}

function countPhaseReports(): number {
  const docsDir = resolveRepoPath("docs");
  return PHASE_REPORT_FILES.filter((file) =>
    fs.existsSync(path.join(docsDir, file)),
  ).length;
}

function readReleaseDate(): string | null {
  const releaseSummaryPath = resolveRepoPath("RELEASE_SUMMARY_v1.0.md");
  if (!fs.existsSync(releaseSummaryPath)) {
    return null;
  }

  const match = fs
    .readFileSync(releaseSummaryPath, "utf8")
    .match(/\*\*Date:\*\*\s*(.+)/);
  return match?.[1]?.trim() ?? null;
}

export function getRepositoryStats(): RepositoryStats {
  const docsDir = resolveRepoPath("docs");
  const reportsDir = resolveRepoPath("reports");
  const validation = readValidationSummary();

  return {
    documentation: countMarkdownFiles(docsDir),
    reports: countMarkdownFiles(reportsDir),
    figures: validation.figureCount,
    researchPhases: countPhaseReports(),
    githubRelease: `v${siteConfig.scienceVersion}`,
    releaseDate: readReleaseDate(),
    validationStatus: validation.status,
    platformVersion: siteConfig.version,
    scienceVersion: siteConfig.scienceVersion,
    analysisScripts: countAnalysisScripts(),
    pilotEvents: readPilotEventCount(),
  };
}
