import { githubRepoUrl } from "@/lib/content/paths";
import type {
  PipelinePhase,
  QuickNavCard,
  TimelineMilestone,
} from "@/lib/dashboard/types";

export const pipelinePhases: PipelinePhase[] = [
  {
    id: "acquisition",
    label: "Data Acquisition",
    description: "USGS events and EarthScope MiniSEED via ObsPy FDSN.",
    status: "complete",
    href: "/workflow#acquisition",
    external: false,
  },
  {
    id: "eda",
    label: "EDA",
    description: "Dataset summaries, magnitude coverage, waveform inspection.",
    status: "complete",
    href: "/workflow#eda",
    external: false,
  },
  {
    id: "signal-analysis",
    label: "Signal Analysis",
    description: "STA/LTA metrics, SNR proxies, and P-pick characterisation.",
    status: "complete",
    href: "/workflow#signal-analysis",
    external: false,
  },
  {
    id: "preprocessing",
    label: "Preprocessing",
    description: "Detrending, band-limited filtering, and quality metrics.",
    status: "complete",
    href: "/workflow#preprocessing",
    external: false,
  },
  {
    id: "feature-engineering",
    label: "Feature Engineering",
    description: "Eighteen ML-ready features per pilot event.",
    status: "complete",
    href: "/workflow#feature-engineering",
    external: false,
  },
  {
    id: "results",
    label: "Results",
    description: "Interpretation, limitations, and submission narrative.",
    status: "complete",
    href: "/research/report",
    external: false,
  },
  {
    id: "swiss-transfer",
    label: "Swiss Transfer (Set A)",
    description: "20 Swiss SED events, 120 3C waveforms, and response removal.",
    status: "complete",
    href: "/docs/swiss-sed-dataset-report",
    external: false,
  },
  {
    id: "swiss-validation",
    label: "Swiss Validation (Set C)",
    description: "15 events, 550 records evaluated at frozen threshold 8.0.",
    status: "complete",
    href: "/docs/swiss-validation-results",
    external: false,
  },
  {
    id: "ml-feasibility",
    label: "ML Feasibility Audit (STEP 3A, historical)",
    description: "STEP 3A returned NO-GO on unlabelled tables; resolved by SED analyst picks in STEP ML-1A.",
    status: "complete",
    href: "/docs/swiss-ml-feasibility-audit",
    external: false,
  },
  {
    id: "ml-supervised",
    label: "Supervised ML (STEP ML-1A to ML-4)",
    description: "RF and XGBoost trained on Set A, evaluated on 15 unseen Set C events (offline benchmark).",
    status: "complete",
    href: "/ml-evaluation",
    external: false,
  },
  {
    id: "website",
    label: "Website Platform",
    description: "Version 2.0 interactive research platform (synced for v2.1).",
    status: "current",
    href: "/",
    external: false,
  },
  {
    id: "deployment",
    label: "Deployment",
    description: "Static hosting and CI pipeline per deployment plan.",
    status: "planned",
    href: `${githubRepoUrl}/blob/main/docs/V2_DEPLOYMENT_PLAN.md`,
    external: true,
  },
];

export const quickNavCards: QuickNavCard[] = [
  {
    title: "Dataset Explorer",
    description: "Sources, journey, and downloadable pilot artefacts.",
    href: "/dataset",
  },
  {
    title: "Waveform Explorer",
    description: "Interactive waveform previews and processing stages.",
    href: "/waveforms",
  },
  {
    title: "Earthquake Map",
    description: "Geolocated events with cross-links to waveforms.",
    href: "/map",
  },
  {
    title: "Workflow Explorer",
    description: "Seven-stage pipeline with reports, figures, and scripts.",
    href: "/workflow",
  },
  {
    title: "Results Explorer",
    description: "Generated figures and CSV tables by research phase.",
    href: "/results",
  },
  {
    title: "Research Report",
    description: "Final submission narrative rendered from repository Markdown.",
    href: "/research/report",
  },
  {
    title: "ML Evaluation",
    description: "Set A to Set C results, figures, disclosures and downloads.",
    href: "/ml-evaluation",
  },
  {
    title: "Documentation",
    description: "Governance documents and repository README.",
    href: "/docs",
  },
  {
    title: "Resources",
    description: "Documentation portal and featured downloads.",
    href: "/resources",
  },
];

export const dashboardTimeline: TimelineMilestone[] = [
  {
    label: "Version 1.0",
    detail: "Submission release · California science frozen 2026-07-29",
    status: "complete",
  },
  {
    label: "California Pilot",
    detail: "8 events · IRIS/EarthScope · 8×18 feature matrix · validation PASS",
    status: "complete",
  },
  {
    label: "Website Platform",
    detail: "Version 2.0 interactive platform live with 19 routes",
    status: "complete",
  },
  {
    label: "Swiss Transfer (Set A)",
    detail: "20 events · 120 3C waveforms · response removal & STA/LTA transfer",
    status: "complete",
  },
  {
    label: "Swiss Validation (Set C)",
    detail: "15 events · 550 records · frozen 8.0 threshold · 72.9% detection",
    status: "complete",
  },
  {
    label: "ML Feasibility Audit (historical)",
    detail: "STEP 3A: NO-GO on unlabelled tables, later unblocked by SED analyst picks (ML-1A)",
    status: "complete",
  },
  {
    label: "Supervised ML (ML-1A to ML-4)",
    detail: "2026-11-12 · RF/XGBoost trained on Set A, evaluated on 15 unseen Set C events · offline benchmark",
    status: "complete",
  },
  {
    label: "Version 2.1 Sync",
    detail: "Platform maintenance & content sync for Swiss validation results",
    status: "current",
  },
  {
    label: "Future Europe (v3.0)",
    detail: "ORFEUS/EIDA expansion · independent labels · leakage-free AI",
    status: "planned",
  },
];
