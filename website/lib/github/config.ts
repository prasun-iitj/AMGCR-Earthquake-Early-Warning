/**
 * Static GitHub repository metadata — no live API polling.
 * Update release/tag fields when tagging new repository releases.
 */

export const githubIntegration = {
  owner: "amgcr",
  name: "AMGCR_Earthquake_Research",
  fullName: "amgcr/AMGCR_Earthquake_Research",
  description:
    "Reproducible ObsPy/FDSN earthquake early warning research — California pilot, open documentation, Version 2.0 platform.",
  defaultBranch: "main",
  latestTag: "v1.0.0",
  latestRelease: "v1.0.0",
  releaseName: "Submission Release",
  releaseDate: "29 July 2026",
  licenseLabel: "Academic research — see repository",
  topics: [
    "earthquake-early-warning",
    "obspy",
    "fdsn",
    "seismology",
    "reproducible-research",
  ],
  issuesEnabled: true,
  discussionsEnabled: false,
  wikiEnabled: false,
} as const;

export type GithubLink = {
  label: string;
  description: string;
  href: string;
  external: true;
};

export function buildGithubUrls(baseUrl: string) {
  const repo = baseUrl.replace(/\/$/, "");
  return {
    repository: repo,
    releases: `${repo}/releases`,
    latestRelease: `${repo}/releases/tag/${githubIntegration.latestTag}`,
    issues: `${repo}/issues`,
    discussions: `${repo}/discussions`,
    tags: `${repo}/tags`,
    actions: `${repo}/actions`,
    source: `${repo}/tree/${githubIntegration.defaultBranch}`,
  };
}

export function buildGithubQuickLinks(baseUrl: string): GithubLink[] {
  const urls = buildGithubUrls(baseUrl);
  const links: GithubLink[] = [
    {
      label: "Repository",
      description: "Browse source code, docs, and submission assets.",
      href: urls.repository,
      external: true,
    },
    {
      label: "Releases",
      description: "Tagged submission releases and release notes.",
      href: urls.releases,
      external: true,
    },
    {
      label: "Latest tag",
      description: `${githubIntegration.latestTag} · ${githubIntegration.releaseName}`,
      href: urls.latestRelease,
      external: true,
    },
    {
      label: "Issues",
      description: "Report bugs or ask questions about the research repository.",
      href: urls.issues,
      external: true,
    },
  ];

  if (githubIntegration.discussionsEnabled) {
    links.push({
      label: "Discussions",
      description: "Community Q&A and research discussion.",
      href: urls.discussions,
      external: true,
    });
  }

  return links;
}
