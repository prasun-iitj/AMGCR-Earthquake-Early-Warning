import fs from "node:fs";
import { resolveRepoPath } from "@/lib/content/paths";
import { getRepositoryStats } from "@/lib/content/stats";

export function parseEdaFigureDescriptions(): Record<string, string> {
  const reportPath = resolveRepoPath("docs/EDA_REPORT.md");
  if (!fs.existsSync(reportPath)) {
    return {};
  }

  const content = fs.readFileSync(reportPath, "utf8");
  const descriptions: Record<string, string> = {};
  const regex =
    /###\s+\d+\.\d+\s+`([^`]+)`[\s\S]*?\*\*Purpose:\*\*\s*([^\n]+)/g;

  for (const match of content.matchAll(regex)) {
    descriptions[match[1]] = match[2].trim();
  }

  return descriptions;
}

export function parseFeatureFigureDescriptions(): Record<string, string> {
  const reportPath = resolveRepoPath("docs/FEATURE_ENGINEERING_REPORT.md");
  if (!fs.existsSync(reportPath)) {
    return {};
  }

  const content = fs.readFileSync(reportPath, "utf8");
  const descriptions: Record<string, string> = {};
  const regex =
    /\|\s*[^|]+\|\s*`reports\/figures\/([^`]+)`\s*\|\s*([^|]+)\s*\|/g;

  for (const match of content.matchAll(regex)) {
    descriptions[match[1]] = match[2].trim();
  }

  return descriptions;
}

export function defaultFigureDescription(
  filename: string,
  phase: string,
): string {
  if (filename.startsWith("signal_analysis_")) {
    const shortId = filename
      .replace("signal_analysis_", "")
      .replace(".png", "");
    return `Four-panel signal analysis figure (raw, normalized, STA/LTA, P marker) for event ${shortId}.`;
  }

  if (filename.startsWith("preprocessing_")) {
    const shortId = filename.replace("preprocessing_", "").replace(".png", "");
    return `Processing comparison (raw → detrended → filtered → normalized) for event ${shortId}.`;
  }

  return `Research figure from the ${phase} phase of the California pilot pipeline.`;
}

export function getResultsSummary() {
  const stats = getRepositoryStats();
  const featureSummaryPath = resolveRepoPath("reports/features/feature_summary.json");

  let featureCount: number | null = null;
  if (fs.existsSync(featureSummaryPath)) {
    try {
      const data = JSON.parse(fs.readFileSync(featureSummaryPath, "utf8")) as {
        n_features?: number;
      };
      featureCount = data.n_features ?? null;
    } catch {
      featureCount = null;
    }
  }

  const figuresDir = resolveRepoPath("reports/figures");
  const figuresOnDisk = fs.existsSync(figuresDir)
    ? fs.readdirSync(figuresDir).filter((file) => file.endsWith(".png")).length
    : 0;

  const tablesDir = resolveRepoPath("reports/tables");
  const tablesOnDisk = fs.existsSync(tablesDir)
    ? fs.readdirSync(tablesDir).filter((file) => file.endsWith(".csv")).length
    : 0;

  return {
    pilotEvents: stats.pilotEvents,
    figures: figuresOnDisk || stats.figures,
    reports: stats.reports,
    researchPhases: stats.researchPhases,
    featureCount,
    githubRelease: stats.githubRelease,
    platformVersion: stats.platformVersion,
    scienceVersion: stats.scienceVersion,
    releaseDate: stats.releaseDate,
    validationStatus: stats.validationStatus,
    documentation: stats.documentation,
    tables: tablesOnDisk,
  };
}

export type ResultsSummary = ReturnType<typeof getResultsSummary>;
