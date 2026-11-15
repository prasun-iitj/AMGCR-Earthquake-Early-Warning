export type FigurePhase =
  | "eda"
  | "signal-analysis"
  | "preprocessing"
  | "feature-engineering"
  | "swiss-transfer"
  | "swiss-validation";

export type TablePhase = FigurePhase;

export const figurePhaseLabels: Record<FigurePhase, string> = {
  eda: "EDA",
  "signal-analysis": "Signal Analysis",
  preprocessing: "Preprocessing",
  "feature-engineering": "Feature Engineering",
  "swiss-transfer": "Swiss Transfer (Set A)",
  "swiss-validation": "Swiss Validation (Set C)",
};

export const phaseReportPaths: Record<FigurePhase, string> = {
  eda: "docs/EDA_REPORT.md",
  "signal-analysis": "docs/SIGNAL_ANALYSIS_REPORT.md",
  preprocessing: "docs/PREPROCESSING_REPORT.md",
  "feature-engineering": "docs/FEATURE_ENGINEERING_REPORT.md",
  "swiss-transfer": "docs/SED_SWITZERLAND_DATASET_REPORT.md",
  "swiss-validation": "docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md",
};

export function classifyFigure(filename: string): FigurePhase {
  if (filename.startsWith("swiss_val_") || filename.startsWith("val_")) {
    return "swiss-validation";
  }
  if (filename.startsWith("swiss_sig_") || filename.startsWith("swiss_")) {
    return "swiss-transfer";
  }
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
    fig01_trigger_vs_reference_timing: "Trigger vs Reference Timing (Set C)",
    fig02_timing_error_distribution: "Timing Error Distribution (Set C)",
    fig03_event_detection_coverage: "Event Detection Coverage (Set C)",
    fig01_representative_3c_waveform: "Representative 3C Waveform (Set A)",
    fig02_response_correction_hhz: "Response Correction HHZ (Set A)",
    fig03_noise_vs_event_window: "Noise vs Event Window (Set A)",
    fig04_sta_lta_example: "STA/LTA Example (Set A)",
    fig04b_sta_lta_additional_class: "STA/LTA Additional Class (Set A)",
    fig05_snr_distribution: "SNR Distribution (Set A)",
    fig06_trigger_latency_distribution: "Trigger Latency Distribution (Set A)",
    fig07_peak_amplitude_distribution: "Peak Amplitude Distribution (Set A)",
    fig08_station_event_map: "Swiss Station Event Map",
    fig09_distance_vs_amplitude: "Distance vs Amplitude (Set A)",
    fig10_california_swiss_structural_comparison: "California vs Swiss Comparison",
  };

  if (knownTitles[base]) {
    return knownTitles[base];
  }

  const cleanBase = base.replace(/^(swiss_val_|swiss_sig_)/, "");
  if (knownTitles[cleanBase]) {
    return knownTitles[cleanBase];
  }

  if (base.startsWith("signal_analysis_")) {
    return `Signal Analysis — ${base.replace("signal_analysis_", "")}`;
  }

  if (base.startsWith("preprocessing_")) {
    return `Preprocessing — ${base.replace("preprocessing_", "")}`;
  }

  return base.replace(/^(swiss_val_|swiss_sig_)/, "").replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

export const tableDefinitions = [
  {
    filename: "event_summary.csv",
    phase: "eda" as const,
    title: "Event Summary (California)",
    description:
      "One row per manifest event with hypocenter, magnitude, station, and waveform metadata.",
    reportPath: "docs/EDA_REPORT.md",
  },
  {
    filename: "station_summary.csv",
    phase: "eda" as const,
    title: "Station Summary (California)",
    description:
      "Aggregated station usage counts and duration statistics for manifest waveforms.",
    reportPath: "docs/EDA_REPORT.md",
  },
  {
    filename: "signal_analysis_per_event.csv",
    phase: "signal-analysis" as const,
    title: "Signal Analysis per Event (California)",
    description:
      "STA/LTA metrics, SNR proxies, and pick metadata for each pilot event.",
    reportPath: "docs/SIGNAL_ANALYSIS_REPORT.md",
  },
  {
    filename: "preprocessing_quality_metrics.csv",
    phase: "preprocessing" as const,
    title: "Preprocessing Quality Metrics (California)",
    description:
      "Before/after SNR and processing metrics for each preprocessed trace.",
    reportPath: "docs/PREPROCESSING_REPORT.md",
  },
  {
    filename: "feature_matrix.csv",
    phase: "feature-engineering" as const,
    title: "Feature Matrix (California)",
    description: "Eight events by eighteen ML-ready feature columns.",
    reportPath: "docs/FEATURE_ENGINEERING_REPORT.md",
  },
  {
    filename: "feature_correlation_matrix.csv",
    phase: "feature-engineering" as const,
    title: "Feature Correlation Matrix (California)",
    description: "Pearson correlation matrix across engineered features.",
    reportPath: "docs/FEATURE_ENGINEERING_REPORT.md",
  },
  {
    filename: "validation_event_summary.csv",
    phase: "swiss-validation" as const,
    title: "Swiss Validation Event Summary (Set C)",
    description:
      "15 locked events evaluated at frozen threshold 8.0 against independent SED reference picks.",
    reportPath: "docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md",
  },
  {
    filename: "validation_trace_metrics.csv",
    phase: "swiss-validation" as const,
    title: "Swiss Validation Trace Metrics (Set C)",
    description:
      "All 550 station-event records with STA/LTA onsets, timing errors, and noise metrics.",
    reportPath: "docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md",
  },
  {
    filename: "swiss_event_summary.csv",
    phase: "swiss-transfer" as const,
    title: "Swiss Pilot Event Summary (Set A)",
    description:
      "20 SED development events across 120 three-component records in Switzerland.",
    reportPath: "docs/SED_SWITZERLAND_DATASET_REPORT.md",
  },
  {
    filename: "swiss_station_summary.csv",
    phase: "swiss-transfer" as const,
    title: "Swiss Station Summary (Set A)",
    description:
      "Summary of CH broadband network stations used in the Swiss methods-transfer pilot.",
    reportPath: "docs/SED_SWITZERLAND_DATASET_REPORT.md",
  },
];

export const figurePhaseOrder: FigurePhase[] = [
  "eda",
  "signal-analysis",
  "preprocessing",
  "feature-engineering",
  "swiss-transfer",
  "swiss-validation",
];
