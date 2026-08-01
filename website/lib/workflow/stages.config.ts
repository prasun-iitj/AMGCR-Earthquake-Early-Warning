import { githubRepoUrl } from "@/lib/content/paths";
import { sourcePathToHref } from "@/lib/content/documents";

export type WorkflowStageId =
  | "acquisition"
  | "eda"
  | "signal-analysis"
  | "preprocessing"
  | "feature-engineering"
  | "results-discussion"
  | "final-deliverables";

export type StagePathEntry = {
  label: string;
  path: string;
};

export type WorkflowStageConfig = {
  id: WorkflowStageId;
  title: string;
  order: number;
  primaryReport: string;
  purposeSection?: string;
  script?: string;
  inputs: StagePathEntry[];
  outputs: StagePathEntry[];
  reports: StagePathEntry[];
  documentation: StagePathEntry[];
  figurePaths: string[];
  figureDirectoryPrefixes?: string[];
};

export const workflowStageConfigs: WorkflowStageConfig[] = [
  {
    id: "acquisition",
    title: "Data Acquisition",
    order: 1,
    primaryReport: "docs/IRIS_DATASET_REPORT.md",
    purposeSection: "## 1. FDSN services used",
    script: "scripts/download/download_iris_california_pilot.py",
    inputs: [
      { label: "USGS FDSN event catalog", path: "https://earthquake.usgs.gov" },
      { label: "EarthScope waveform services", path: "https://service.earthscope.org" },
    ],
    outputs: [
      { label: "Event manifest (CSV)", path: "data/manifests/iris_california_pilot_events.csv" },
      { label: "Raw MiniSEED waveforms", path: "data/raw/iris/" },
      { label: "Acquisition report", path: "docs/IRIS_DATASET_REPORT.md" },
    ],
    reports: [{ label: "IRIS Dataset Report", path: "docs/IRIS_DATASET_REPORT.md" }],
    documentation: [
      { label: "Dataset conventions", path: "docs/DATASET.md" },
      { label: "Data availability statement", path: "docs/DATA_AVAILABILITY_STATEMENT.md" },
    ],
    figurePaths: [],
  },
  {
    id: "eda",
    title: "EDA",
    order: 2,
    primaryReport: "docs/EDA_REPORT.md",
    purposeSection: "## 1. Scope",
    script: "scripts/analysis/run_california_pilot_eda.py",
    inputs: [
      { label: "Event manifest", path: "data/manifests/iris_california_pilot_events.csv" },
      { label: "Raw waveforms", path: "data/raw/iris/" },
    ],
    outputs: [
      { label: "Dataset summary (JSON)", path: "reports/eda/dataset_summary.json" },
      { label: "MiniSEED inspection (CSV)", path: "reports/eda/mseed_file_inspection.csv" },
      { label: "EDA run metadata", path: "reports/eda/eda_run_metadata.json" },
      { label: "Event summary table", path: "reports/tables/event_summary.csv" },
      { label: "Station summary table", path: "reports/tables/station_summary.csv" },
    ],
    reports: [{ label: "EDA Report", path: "docs/EDA_REPORT.md" }],
    documentation: [{ label: "IRIS Dataset Report", path: "docs/IRIS_DATASET_REPORT.md" }],
    figurePaths: [
      "reports/figures/example_waveform_raw.png",
      "reports/figures/magnitude_histogram.png",
      "reports/figures/events_over_time.png",
      "reports/figures/station_usage_frequency.png",
    ],
  },
  {
    id: "signal-analysis",
    title: "Signal Analysis",
    order: 3,
    primaryReport: "docs/SIGNAL_ANALYSIS_REPORT.md",
    purposeSection: "## 1. Scope and methods",
    inputs: [
      { label: "Manifest-linked MiniSEED files", path: "data/raw/iris/" },
      { label: "Event manifest", path: "data/manifests/iris_california_pilot_events.csv" },
    ],
    outputs: [
      { label: "Per-event metrics (JSON)", path: "reports/signal_analysis/" },
      { label: "Signal analysis summary", path: "reports/signal_analysis/signal_analysis_summary.json" },
      { label: "Per-event table (CSV)", path: "reports/tables/signal_analysis_per_event.csv" },
    ],
    reports: [{ label: "Signal Analysis Report", path: "docs/SIGNAL_ANALYSIS_REPORT.md" }],
    documentation: [{ label: "EDA Report", path: "docs/EDA_REPORT.md" }],
    figurePaths: [],
    figureDirectoryPrefixes: ["signal_analysis_"],
  },
  {
    id: "preprocessing",
    title: "Preprocessing",
    order: 4,
    primaryReport: "docs/PREPROCESSING_REPORT.md",
    purposeSection: "## 1. Why each step matters for EEW",
    inputs: [
      { label: "Raw MiniSEED waveforms", path: "data/raw/iris/" },
      { label: "Signal analysis metrics", path: "reports/signal_analysis/" },
    ],
    outputs: [
      { label: "Preprocessing config", path: "reports/preprocessing/preprocessing_config.json" },
      { label: "Stage traces (NPZ)", path: "reports/preprocessing/" },
      { label: "Preprocessing summary", path: "reports/preprocessing/preprocessing_summary.json" },
      { label: "Quality metrics table", path: "reports/tables/preprocessing_quality_metrics.csv" },
    ],
    reports: [{ label: "Preprocessing Report", path: "docs/PREPROCESSING_REPORT.md" }],
    documentation: [{ label: "Signal Analysis Report", path: "docs/SIGNAL_ANALYSIS_REPORT.md" }],
    figurePaths: [],
    figureDirectoryPrefixes: ["preprocessing_"],
  },
  {
    id: "feature-engineering",
    title: "Feature Engineering",
    order: 5,
    primaryReport: "docs/FEATURE_ENGINEERING_REPORT.md",
    purposeSection: "## 1. Feature matrix",
    inputs: [
      { label: "Preprocessed stage traces (NPZ)", path: "reports/preprocessing/" },
      { label: "P-pick times from signal analysis", path: "reports/signal_analysis/" },
    ],
    outputs: [
      { label: "Feature matrix (CSV)", path: "reports/features/feature_matrix.csv" },
      { label: "Feature summary (JSON)", path: "reports/features/feature_summary.json" },
      { label: "Correlation matrix", path: "reports/tables/feature_correlation_matrix.csv" },
      { label: "Per-event features (JSON)", path: "reports/features/per_event_features.json" },
    ],
    reports: [{ label: "Feature Engineering Report", path: "docs/FEATURE_ENGINEERING_REPORT.md" }],
    documentation: [{ label: "Preprocessing Report", path: "docs/PREPROCESSING_REPORT.md" }],
    figurePaths: [
      "reports/figures/feature_engineering_fft_spectra.png",
      "reports/figures/feature_correlation_heatmap.png",
      "reports/figures/feature_distributions.png",
      "reports/figures/feature_boxplots_by_station.png",
    ],
  },
  {
    id: "results-discussion",
    title: "Results & Discussion",
    order: 6,
    primaryReport: "docs/RESULTS_AND_DISCUSSION.md",
    purposeSection: "## 1. End-to-end workflow summary",
    inputs: [
      { label: "All phase reports and artefacts", path: "reports/" },
      { label: "Phase documentation", path: "docs/" },
    ],
    outputs: [
      { label: "Final research report (Markdown)", path: "reports/Research_Report_Final.md" },
      { label: "Interpretation document", path: "docs/RESULTS_AND_DISCUSSION.md" },
    ],
    reports: [
      { label: "Results & Discussion", path: "docs/RESULTS_AND_DISCUSSION.md" },
      { label: "Final Research Report", path: "reports/Research_Report_Final.md" },
    ],
    documentation: [
      { label: "Project Charter", path: "docs/PROJECT_CHARTER.md" },
      { label: "Research Direction", path: "docs/RESEARCH_DIRECTION.md" },
    ],
    figurePaths: [],
    figureDirectoryPrefixes: [
      "example_waveform_",
      "magnitude_",
      "events_",
      "station_",
      "signal_analysis_",
      "preprocessing_",
      "feature_",
    ],
  },
  {
    id: "final-deliverables",
    title: "Final Deliverables",
    order: 7,
    primaryReport: "FINAL_SUBMISSION/FINAL_SUBMISSION_README.md",
    purposeSection: "## Purpose",
    inputs: [
      { label: "Consolidated research narrative", path: "reports/Research_Report_Final.md" },
      { label: "Presentation assets", path: "reports/Presentation_Outline_D-F2.md" },
    ],
    outputs: [
      { label: "Submission package", path: "FINAL_SUBMISSION/" },
      { label: "Validation summary", path: "FINAL_SUBMISSION/VALIDATION_SUMMARY.json" },
      { label: "Reproducibility statement", path: "docs/REPRODUCIBILITY_STATEMENT.md" },
    ],
    reports: [
      { label: "Final Research Report", path: "reports/Research_Report_Final.md" },
      { label: "Submission README", path: "FINAL_SUBMISSION/FINAL_SUBMISSION_README.md" },
    ],
    documentation: [
      { label: "Reproducibility statement (D-S1)", path: "docs/REPRODUCIBILITY_STATEMENT.md" },
      { label: "Data availability statement (D-S2)", path: "docs/DATA_AVAILABILITY_STATEMENT.md" },
      { label: "Release summary v1.0", path: "RELEASE_SUMMARY_v1.0.md" },
    ],
    figurePaths: [],
  },
];

export function githubBlobUrl(repoPath: string): string {
  if (repoPath.startsWith("http://") || repoPath.startsWith("https://")) {
    return repoPath;
  }
  return `${githubRepoUrl}/blob/main/${repoPath.replace(/\\/g, "/")}`;
}

export function resolveStageLink(path: string): {
  href: string;
  external: boolean;
} {
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return { href: path, external: true };
  }

  const normalized = path.replace(/\\/g, "/");
  const siteHref = sourcePathToHref[normalized];
  if (siteHref) {
    return { href: siteHref, external: false };
  }

  if (normalized.endsWith("/")) {
    return { href: githubBlobUrl(normalized), external: true };
  }

  return { href: githubBlobUrl(normalized), external: true };
}

export function getStageById(id: WorkflowStageId) {
  return workflowStageConfigs.find((stage) => stage.id === id);
}

export function getAdjacentStages(id: WorkflowStageId) {
  const index = workflowStageConfigs.findIndex((stage) => stage.id === id);
  return {
    previous: index > 0 ? workflowStageConfigs[index - 1] : null,
    next:
      index >= 0 && index < workflowStageConfigs.length - 1
        ? workflowStageConfigs[index + 1]
        : null,
  };
}
