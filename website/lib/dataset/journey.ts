import type { DatasetJourneyStep } from "@/lib/dataset/types";
import { githubRepoUrl } from "@/lib/content/paths";

export const datasetJourneySteps: DatasetJourneyStep[] = [
  {
    id: "source",
    label: "IRIS / EarthScope",
    description: "USGS events and EarthScope waveforms via ObsPy FDSN clients.",
    href: `${githubRepoUrl}/blob/main/docs/IRIS_DATASET_REPORT.md`,
    external: true,
    phase: "acquisition",
  },
  {
    id: "miniseed",
    label: "MiniSEED",
    description: "Raw vertical broadband recordings stored under data/raw/iris/.",
    href: `${githubRepoUrl}/blob/main/docs/DATA_AVAILABILITY_STATEMENT.md`,
    external: true,
    phase: "acquisition",
  },
  {
    id: "manifest",
    label: "Manifest",
    description: "Tracked event metadata CSV linking catalog entries to waveform files.",
    href: "/dataset#downloads",
    external: false,
    phase: "acquisition",
  },
  {
    id: "eda",
    label: "EDA",
    description: "Exploratory inspection, magnitude coverage, and station usage summaries.",
    href: "/workflow#eda",
    external: false,
    phase: "eda",
  },
  {
    id: "signal-analysis",
    label: "Signal Analysis",
    description: "STA/LTA metrics, SNR proxies, and onsite trigger characterisation.",
    href: "/workflow#signal-analysis",
    external: false,
    phase: "signal-analysis",
  },
  {
    id: "preprocessing",
    label: "Preprocessing",
    description: "Detrending, band-limited filtering, and documented quality metrics.",
    href: "/workflow#preprocessing",
    external: false,
    phase: "preprocessing",
  },
  {
    id: "feature-matrix",
    label: "Feature Matrix",
    description: "Eight events by eighteen ML-ready features from processed traces.",
    href: "/results",
    external: false,
    phase: "feature-engineering",
  },
  {
    id: "final-report",
    label: "Final Report",
    description: "Consolidated submission narrative (D-F1) with interpretation and limitations.",
    href: "/research/report",
    external: false,
    phase: "results",
  },
];
