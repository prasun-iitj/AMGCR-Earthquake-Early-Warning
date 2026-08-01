/**
 * Dashboard types — shaped for future ResearchContext consumption (post Phase 9).
 */

export type ResearchSummary = {
  platformVersion: string;
  scienceVersion: string;
  githubRelease: string;
  releaseDate: string | null;
  researchStatus: string;
  validationStatus: string | null;
  californiaPilotStatus: string;
  europePhaseStatus: string;
};

export type DatasetMetrics = {
  eventCount: number | null;
  stationCount: number | null;
  waveformCount: number | null;
  timeRangeStart: string | null;
  timeRangeEnd: string | null;
  magnitudeMin: number | null;
  magnitudeMax: number | null;
  samplingRateHz: number | null;
  channels: string[];
  featureMatrixShape: string | null;
};

export type RepositoryMetrics = {
  documentationCount: number;
  reportCount: number;
  figureCount: number;
  tableCount: number;
  jsonSummaryCount: number;
  workflowPhaseCount: number;
  websiteVersion: string;
  researchVersion: string;
  analysisScriptCount: number;
};

export type PipelinePhaseStatus = "complete" | "current" | "planned";

export type PipelinePhase = {
  id: string;
  label: string;
  description: string;
  status: PipelinePhaseStatus;
  href: string;
  external: boolean;
};

export type QuickNavCard = {
  title: string;
  description: string;
  href: string;
  external?: boolean;
};

export type TimelineMilestone = {
  label: string;
  detail: string;
  status: "complete" | "current" | "planned";
};

/** Serializable dashboard snapshot for future ResearchContext provider. */
export type ResearchDashboardSnapshot = {
  summary: ResearchSummary;
  dataset: DatasetMetrics;
  repository: RepositoryMetrics;
  pipeline: PipelinePhase[];
  quickNav: QuickNavCard[];
  timeline: TimelineMilestone[];
  generatedAtUtc: string | null;
};

export type LoadedDashboard = ResearchDashboardSnapshot;
