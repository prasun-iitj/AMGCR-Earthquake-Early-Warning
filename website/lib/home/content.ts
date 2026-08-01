import { githubRepoUrl } from "@/lib/content/paths";

export const heroContent = {
  eyebrow: "Swiss certificate programme · AMGCR",
  title: "Reproducible AI-Assisted Earthquake Early Warning Research",
  subtitle: "Western Seismic Regions",
  description:
    "Europe-focused earthquake early warning research with a completed California FDSN pilot, open documentation, and a reproducible workflow from raw waveforms to machine-learning-ready features.",
  primaryCta: { label: "Explore Research", href: "/research" },
  secondaryCta: { label: "View Report", href: "/research/report" },
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
    label: "Version 1.0",
    detail: "Submission release · science frozen 2026-07-29",
    status: "complete" as const,
  },
  {
    label: "California Pilot",
    detail: "8 events · IRIS/EarthScope · 8×18 features",
    status: "complete" as const,
  },
  {
    label: "Submission",
    detail: "D-F1–F4 deliverables · validation PASS",
    status: "complete" as const,
  },
  {
    label: "Version 2.0",
    detail: "Interactive research platform · documentation portal live",
    status: "current" as const,
  },
];

export const featuredDownloads = [
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
