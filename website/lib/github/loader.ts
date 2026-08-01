import fs from "node:fs";
import { getRepositoryStats } from "@/lib/content/stats";
import { githubRepoUrl, resolveRepoPath } from "@/lib/content/paths";
import {
  buildGithubQuickLinks,
  buildGithubUrls,
  githubIntegration,
} from "@/lib/github/config";
import { siteConfig } from "@/lib/navigation";

export type RepoStructureEntry = {
  name: string;
  path: string;
  type: "directory" | "file";
  description: string;
  href: string;
};

export type LoadedGithubPage = {
  integration: typeof githubIntegration;
  urls: ReturnType<typeof buildGithubUrls>;
  quickLinks: ReturnType<typeof buildGithubQuickLinks>;
  stats: ReturnType<typeof getRepositoryStats>;
  platformVersion: string;
  structure: RepoStructureEntry[];
};

const STRUCTURE_ENTRIES: Array<Omit<RepoStructureEntry, "href">> = [
  {
    name: "docs/",
    path: "docs",
    type: "directory",
    description: "Governance, phase reports, and Version 2 planning documents.",
  },
  {
    name: "reports/",
    path: "reports",
    type: "directory",
    description: "Generated figures, tables, JSON summaries, and final report.",
  },
  {
    name: "data/",
    path: "data",
    type: "directory",
    description: "Manifests and dataset metadata (raw waveforms via D-S2).",
  },
  {
    name: "src/",
    path: "src",
    type: "directory",
    description: "EarthESND reference implementation and acquisition utilities.",
  },
  {
    name: "scripts/",
    path: "scripts",
    type: "directory",
    description: "Download and analysis scripts for reproducible pipeline runs.",
  },
  {
    name: "website/",
    path: "website",
    type: "directory",
    description: "Version 2.0 interactive research platform (this site).",
  },
  {
    name: "FINAL_SUBMISSION/",
    path: "FINAL_SUBMISSION",
    type: "directory",
    description: "Submission package PDFs, validation summary, and presentation.",
  },
  {
    name: "README.md",
    path: "README.md",
    type: "file",
    description: "Repository overview and quick start.",
  },
];

function structureHref(repoPath: string): string {
  return `${githubRepoUrl}/blob/${githubIntegration.defaultBranch}/${repoPath}`;
}

function existsInRepo(relativePath: string): boolean {
  return fs.existsSync(resolveRepoPath(relativePath));
}

export function loadGithubPage(): LoadedGithubPage {
  const urls = buildGithubUrls(githubRepoUrl);

  const structure = STRUCTURE_ENTRIES.filter((entry) => existsInRepo(entry.path)).map(
    (entry) => ({
      ...entry,
      href: structureHref(entry.path),
    }),
  );

  return {
    integration: githubIntegration,
    urls,
    quickLinks: buildGithubQuickLinks(githubRepoUrl),
    stats: getRepositoryStats(),
    platformVersion: siteConfig.version,
    structure,
  };
}

/** Count top-level repository entries for overview display. */
export function countTopLevelEntries(): number {
  const repoRoot = resolveRepoPath(".");
  if (!fs.existsSync(repoRoot)) {
    return 0;
  }

  return fs.readdirSync(repoRoot).filter((entry) => !entry.startsWith(".")).length;
}
