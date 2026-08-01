export type NavItem = {
  label: string;
  href: string;
};

export const mainNav: NavItem[] = [
  { label: "Home", href: "/" },
  { label: "Dashboard", href: "/dashboard" },
  { label: "Research", href: "/research" },
  { label: "Workflow", href: "/workflow" },
  { label: "Results", href: "/results" },
  { label: "Dataset", href: "/dataset" },
  { label: "Waveforms", href: "/waveforms" },
  { label: "Map", href: "/map" },
  { label: "Resources", href: "/resources" },
  { label: "About", href: "/about" },
  { label: "Contact", href: "/contact" },
];

export const siteConfig = {
  name: "AMGCR Earthquake Research",
  tagline: "Interactive Research Platform",
  description:
    "A documentation-driven research portal for reproducible earthquake early warning science.",
  version: "2.0.0-beta",
  scienceVersion: "1.0.0",
};
