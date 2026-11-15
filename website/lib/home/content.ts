import { githubRepoUrl } from "@/lib/content/paths";

export const heroContent = {
  eyebrow: "An IIT Jodhpur major research project",
  title: "Reproducible AI-Assisted Earthquake Early Warning Research",
  subtitle: "AMGCR: Assessment and Management of Geological and Climate Related Risk",
  metaDescription:
    "AMGCR, an IIT Jodhpur major research project on AI-assisted seismic signal analysis and P-wave detection, with documented data, methods, independent evaluation and limitations.",
  description:
    "AI-assisted seismic signal analysis and P-wave detection: waveform acquisition, signal preprocessing, feature engineering, machine-learning classification of candidate windows, independent Swiss validation and comparison with traditional STA/LTA detection. Datasets, methodology, results and limitations are documented for reproducibility. This is an offline research benchmark, not an operational warning system.",
  ctas: [
    { label: "Explore Research", href: "/research", variant: "primary" as const },
    { label: "View Data & Analysis", href: "/data-analysis", variant: "outline" as const },
    { label: "Explore ML Evaluation", href: "/ml-evaluation", variant: "outline" as const },
    { label: "Read Research Documentation", href: "/docs", variant: "outline" as const },
  ],
};

export const projectHighlights = [
  {
    title: "EarthESND Reference",
    description:
      "Complete reference implementation (88 tests) for literature-aligned architecture and AI methodology — not the geographic endpoint.",
    icon: "reference",
  },
  {
    title: "California Pilot",
    description:
      "Completed IRIS/EarthScope pilot with ObsPy acquisition, eight events, and an 8×18 feature matrix frozen at submission.",
    icon: "pilot",
  },
  {
    title: "Europe Research Direction",
    description:
      "Primary long-term focus on European seismic networks, with California serving as the methods laboratory.",
    icon: "europe",
  },
  {
    title: "End-to-End Pipeline",
    description:
      "Acquisition through EDA, signal analysis, preprocessing, feature engineering, and formal interpretation.",
    icon: "pipeline",
  },
  {
    title: "Open Source",
    description:
      "Python, ObsPy, and FDSN-based scripts with manifests, JSON summaries, and version-controlled documentation.",
    icon: "opensource",
  },
  {
    title: "Reproducible Research",
    description:
      "Reproducibility and data availability statements, validation PASS, and a frozen v1.0.0 submission release.",
    icon: "reproducible",
  },
] as const;

export type WorkflowStep = {
  id: string;
  title: string;
  description: string;
  href: string;
  external?: boolean;
};

export const workflowSteps: WorkflowStep[] = [
  {
    id: "acquisition",
    title: "Data Acquisition",
    description: "USGS events and EarthScope waveforms via ObsPy FDSN.",
    href: "/workflow#acquisition",
  },
  {
    id: "eda",
    title: "EDA",
    description: "Dataset summaries, magnitude coverage, and waveform inspection.",
    href: "/workflow#eda",
  },
  {
    id: "signal-analysis",
    title: "Signal Analysis",
    description: "STA/LTA metrics, SNR proxies, and onsite trigger characterisation.",
    href: "/workflow#signal-analysis",
  },
  {
    id: "preprocessing",
    title: "Preprocessing",
    description: "Band-limited filtering and documented quality metrics.",
    href: "/workflow#preprocessing",
  },
  {
    id: "feature-engineering",
    title: "Feature Engineering",
    description: "Eighteen ML-ready features per event from processed traces.",
    href: "/workflow#feature-engineering",
  },
  {
    id: "results-discussion",
    title: "Results & Discussion",
    description: "Interpretation, limitations, and European transfer context.",
    href: "/workflow#results-discussion",
  },
  {
    id: "final-deliverables",
    title: "Final Deliverables",
    description: "Report, presentation, submission package, and compliance statements.",
    href: "/workflow#final-deliverables",
  },
];

export const timelineSteps = [
  {
    label: "Swiss Certificate Programme association",
    detail:
      "The research began with an academic association with the Swiss Certificate Programme; its v1.0.0 submission (2026-07-29) froze the California pilot science.",
    status: "complete" as const,
  },
  {
    label: "California pilot",
    detail: "8 events from USGS and EarthScope/IRIS; waveform analysis, preprocessing and an 8×18 feature matrix (frozen).",
    status: "complete" as const,
  },
  {
    label: "Swiss seismic datasets",
    detail: "SED/ETH data: Set A (20 events, 120 three-component records) and Set C (15 events, 550 vertical-component records), with manual first-P picks.",
    status: "complete" as const,
  },
  {
    label: "Features and models",
    detail: "Engineered window features; Random Forest and XGBoost with event-grouped cross-validation.",
    status: "complete" as const,
  },
  {
    label: "Independent Swiss validation",
    detail: "Frozen models evaluated on 15 unseen Set C events and compared with STA/LTA (offline benchmark; stations are shared with Set A).",
    status: "complete" as const,
  },
  {
    label: "IIT Jodhpur major research project",
    detail: "Documented methodology, results and limitations presented on this research platform for academic review.",
    status: "current" as const,
  },
];

export const featuredDownloads = [
  {
    title: "Data Collection & Analysis",
    description: "Original sources, acquisition, raw data, preprocessing, Swiss Set A and Set C, features and reproduction.",
    href: "/data-analysis",
    cta: "Open data journey",
    external: false,
  },
  {
    title: "ML Evaluation",
    description: "Offline window-classification benchmark: Set A cross-validation, independent Set C results and disclosures.",
    href: "/ml-evaluation",
    cta: "Open ML results",
    external: false,
  },
  {
    title: "Professor Handover Guide",
    description: "Entry point for academic review: overview, navigation, limitations, checklist and discussion notes.",
    href: "/docs/professor-handover-guide",
    cta: "Read the guide",
    external: false,
  },
  {
    title: "Final Report",
    description: "Primary submission narrative (D-F1) rendered from repository Markdown.",
    href: "/research/report",
    cta: "Read report",
    external: false,
  },
  {
    title: "Presentation",
    description: "24-slide oral defence deck (D-F2) in the submission package.",
    href: `${githubRepoUrl}/blob/main/FINAL_SUBMISSION/Presentation.pdf`,
    cta: "View on GitHub",
    external: true,
  },
  {
    title: "GitHub Repository",
    description: "Single source of truth for science, scripts, reports, and submission assets.",
    href: githubRepoUrl,
    cta: "Open repository",
    external: true,
  },
];
