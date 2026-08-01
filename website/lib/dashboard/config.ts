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
    id: "website",
    label: "Website",
    description: "Version 2.0 interactive research platform (explorers live).",
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
    detail: "Submission release · science frozen 2026-07-29",
    status: "complete",
  },
  {
    label: "California Pilot",
    detail: "8 events · IRIS/EarthScope · 8×18 feature matrix",
    status: "complete",
  },
  {
    label: "Submission",
    detail: "D-F1–F4 deliverables · validation PASS",
    status: "complete",
  },
  {
    label: "Website Development",
    detail: "Version 2.0 platform · explorers and dashboard",
    status: "current",
  },
  {
    label: "Version 2",
    detail: "Interactive portal · Europe expansion planned",
    status: "current",
  },
  {
    label: "Future Europe",
    detail: "ORFEUS/EIDA dataset expansion · same pipeline pattern",
    status: "planned",
  },
  {
    label: "Version 3 AI",
    detail: "AI-ready architecture · assistant and semantic search",
    status: "planned",
  },
];
