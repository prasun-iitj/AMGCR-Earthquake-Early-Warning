/** Shared navigation helpers for active state and breadcrumbs. */

export function isNavItemActive(pathname: string, href: string): boolean {
  if (href === "/") {
    return pathname === "/";
  }

  if (href === "/research") {
    return pathname === "/research" || pathname.startsWith("/research/");
  }

  if (href === "/docs") {
    return pathname === "/docs" || pathname.startsWith("/docs/");
  }

  return pathname === href || pathname.startsWith(`${href}/`);
}

export const footerQuickLinks = [
  { label: "Professor Handover Guide", href: "/docs/professor-handover-guide" },
  { label: "Data Collection & Analysis", href: "/data-analysis" },
  { label: "ML Evaluation", href: "/ml-evaluation" },
  { label: "Dashboard", href: "/dashboard" },
  { label: "Dataset", href: "/dataset" },
  { label: "Waveforms", href: "/waveforms" },
  { label: "Map", href: "/map" },
  { label: "Workflow", href: "/workflow" },
  { label: "Results", href: "/results" },
  { label: "Documentation", href: "/docs" },
  { label: "GitHub", href: "/github" },
  { label: "Resources", href: "/resources" },
] as const;

export const mobileNavSections = [
  {
    label: "Overview",
    items: [
      { label: "Home", href: "/" },
      { label: "Data Collection & Analysis", href: "/data-analysis" },
      { label: "Dashboard", href: "/dashboard" },
      { label: "Research", href: "/research" },
    ],
  },
  {
    label: "Explorers",
    items: [
      { label: "Workflow", href: "/workflow" },
      { label: "Results", href: "/results" },
      { label: "ML Evaluation", href: "/ml-evaluation" },
      { label: "Dataset", href: "/dataset" },
      { label: "Waveforms", href: "/waveforms" },
      { label: "Map", href: "/map" },
    ],
  },
  {
    label: "Project",
    items: [
      { label: "Documentation", href: "/docs" },
      { label: "Resources", href: "/resources" },
      { label: "GitHub", href: "/github" },
      { label: "About", href: "/about" },
      { label: "Contact", href: "/contact" },
    ],
  },
] as const;
