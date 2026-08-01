import path from "node:path";

/** Repository root (parent of website/) — used for build-time Markdown reads. */
export function getRepoRoot(): string {
  return path.resolve(process.cwd(), "..");
}

export function resolveRepoPath(relativePath: string): string {
  return path.join(getRepoRoot(), relativePath);
}

export const githubRepoUrl =
  process.env.NEXT_PUBLIC_GITHUB_REPO_URL ??
  "https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning";
