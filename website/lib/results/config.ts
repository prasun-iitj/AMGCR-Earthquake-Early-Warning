export type FigurePhase =
  | "eda"
  | "signal-analysis"
  | "preprocessing"
  | "feature-engineering";

export type TablePhase = FigurePhase;

export const figurePhaseLabels: Record<FigurePhase, string> = {
  eda: "EDA",
  "signal-analysis": "Signal Analysis",
  preprocessing: "Preprocessing",
  "feature-engineering": "Feature Engineering",
};

export const phaseReportPaths: Record<FigurePhase, string> = {
  eda: "docs/EDA_REPORT.md",
  "signal-analysis": "docs/SIGNAL_ANALYSIS_REPORT.md",
  preprocessing: "docs/PREPROCESSING_REPORT.md",
  "feature-engineering": "docs/FEATURE_ENGINEERING_REPORT.md",
};

export function classifyFigure(filename: string): FigurePhase {
  if (filename.startsWith("signal_analysis_")) {
    return "signal-analysis";
  }
  if (filename.startsWith("preprocessing_")) {
    return "preprocessing";
  }
  if (filename.startsWith("feature_")) {
    return "feature-engineering";
  }
  return "eda";
}

export function figureTitle(filename: string): string {
  const base = filename.replace(/\.png$/i, "");

  const knownTitles: Record<string, string> = {
    example_waveform_raw: "Example Waveform (Raw)",
    magnitude_histogram: "Magnitude Histogram",
    events_over_time: "Events Over Time",
    station_usage_frequency: "Station Usage Frequency",
    feature_engineering_fft_spectra: "FFT Spectra",
    feature_correlation_heatmap: "Feature Correlation Heatmap",
    feature_distributions: "Feature Distributions",
    feature_boxplots_by_station: "Feature Boxplots by Station",
  };

  if (knownTitles[base]) {
    return knownTitles[base];
  }

  if (base.startsWith("signal_analysis_")) {
    return `Signal Analysis — ${base.replace("signal_analysis_", "")}`;
  }

  if (base.startsWith("preprocessing_")) {
    return `Preprocessing — ${base.replace("preprocessing_", "")}`;
  }

  return base.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

export const tableDefinitions = [
  {
    filename: "event_summary.csv",
    phase: "eda" as const,
    title: "Event Summary",
    description:
      "One row per manifest event with hypocenter, magnitude, station, and waveform metadata.",
    reportPath: "docs/EDA_REPORT.md",
  },
  {
    filename: "station_summary.csv",
    phase: "eda" as const,
    title: "Station Summary",
    description:
      "Aggregated station usage counts and duration statistics for manifest waveforms.",
    reportPath: "docs/EDA_REPORT.md",
  },
  {
    filename: "signal_analysis_per_event.csv",
    phase: "signal-analysis" as const,
    title: "Signal Analysis per Event",
    description:
      "STA/LTA metrics, SNR proxies, and pick metadata for each pilot event.",
    reportPath: "docs/SIGNAL_ANALYSIS_REPORT.md",
  },
  {
    filename: "preprocessing_quality_metrics.csv",
    phase: "preprocessing" as const,
    title: "Preprocessing Quality Metrics",
    description:
      "Before/after SNR and processing metrics for each preprocessed trace.",
    reportPath: "docs/PREPROCESSING_REPORT.md",
  },
  {
    filename: "feature_matrix.csv",
    phase: "feature-engineering" as const,
    title: "Feature Matrix",
    description: "Eight events by eighteen ML-ready feature columns.",
    reportPath: "docs/FEATURE_ENGINEERING_REPORT.md",
  },
  {
    filename: "feature_correlation_matrix.csv",
    phase: "feature-engineering" as const,
    title: "Feature Correlation Matrix",
    description: "Pearson correlation matrix across engineered features.",
    reportPath: "docs/FEATURE_ENGINEERING_REPORT.md",
  },
];

export const figurePhaseOrder: FigurePhase[] = [
  "eda",
  "signal-analysis",
  "preprocessing",
  "feature-engineering",
];
