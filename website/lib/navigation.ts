export type NavItem = {
  label: string;
  href: string;
  /** Shorter label used in the desktop header below the 2xl breakpoint. */
  shortLabel?: string;
  /** Shown inline in the desktop header; other items go into the "More" menu. */
  primary?: boolean;
};

export const mainNav: NavItem[] = [
  { label: "Home", href: "/", primary: true },
  { label: "Data Collection & Analysis", shortLabel: "Data & Analysis", href: "/data-analysis", primary: true },
  { label: "Dashboard", href: "/dashboard" },
  { label: "Research", href: "/research", primary: true },
  { label: "Workflow", href: "/workflow", primary: true },
  { label: "Results", href: "/results", primary: true },
  { label: "ML Evaluation", href: "/ml-evaluation", primary: true },
  { label: "Dataset", href: "/dataset", primary: true },
  { label: "Waveforms", href: "/waveforms" },
  { label: "Map", href: "/map" },
  { label: "Resources", href: "/resources" },
  { label: "About", href: "/about" },
  { label: "Contact", href: "/contact" },
  { label: "Reviewer Guide", shortLabel: "Review Guide", href: "/review-guide" },
];

export const siteConfig = {
  name: "AMGCR Earthquake Early Warning Research",
  nameLines: ["AMGCR Earthquake", "Early Warning Research"] as const,
  tagline: "Interactive Research Platform",
  description:
    "AMGCR (Assessment and Management of Geological and Climate Related Risk): an IIT Jodhpur major research project on AI-assisted seismic signal analysis and P-wave detection, with documented data, methods, results and limitations.",
  /** Primary institutional identity (hero label, metadata, footer). */
  identity: "An IIT Jodhpur major research project",
  /** Expanded project name, as supplied by the project team. */
  expandedName: "Assessment and Management of Geological and Climate Related Risk",
  version: "2.0.0",
  scienceVersion: "1.0.0",
};
