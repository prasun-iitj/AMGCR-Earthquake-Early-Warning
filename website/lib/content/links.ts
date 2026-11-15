import path from "node:path";
import { sourcePathToHref } from "@/lib/content/documents";
import { githubRepoUrl } from "@/lib/content/paths";

function normalizeRepoPath(href: string): string {
  return href.replace(/\\/g, "/").replace(/^\.\//, "");
}

function resolveRelativePath(href: string, currentSourcePath: string): string {
  if (href.startsWith("/")) {
    return href.slice(1);
  }

  const baseDir = path.posix.dirname(currentSourcePath.replace(/\\/g, "/"));
  return normalizeRepoPath(path.posix.normalize(path.posix.join(baseDir, href)));
}

export function rewriteMarkdownHref(
  href: string | undefined,
  currentSourcePath: string,
): string | undefined {
  if (!href) {
    return href;
  }

  if (
    href.startsWith("http://") ||
    href.startsWith("https://") ||
    href.startsWith("mailto:") ||
    href.startsWith("#")
  ) {
    return href;
  }

  const normalized = normalizeRepoPath(href);

  if (sourcePathToHref[normalized]) {
    return sourcePathToHref[normalized];
  }

  // Root-relative links go straight to GitHub. Relative links (including .md files that sit next to
  // the current document) are resolved against the current document below, so sibling documents in
  // docs/ map to their portal routes instead of a non-existent repository-root path.
  if (href.startsWith("/")) {
    return `${githubRepoUrl}/blob/main/${normalized}`;
  }

  const resolved = resolveRelativePath(href, currentSourcePath);
  if (sourcePathToHref[resolved]) {
    return sourcePathToHref[resolved];
  }

  if (resolved.endsWith(".md")) {
    return `${githubRepoUrl}/blob/main/${resolved}`;
  }

  return `${githubRepoUrl}/blob/main/${resolved}`;
}

/**
 * Resolve a Markdown image path. Figures copied by scripts/sync-results-assets.mjs are served from
 * /data-figures and /final-figures; any other repository image falls back to raw.githubusercontent.com.
 */
export function rewriteMarkdownImageSrc(
  src: string | undefined,
  currentSourcePath: string,
): string | undefined {
  if (!src || /^(https?:|data:|\/)/.test(src)) {
    return src;
  }

  const resolved = resolveRelativePath(src, currentSourcePath);
  const name = path.posix.basename(resolved);

  if (resolved.startsWith("reports/figures/data/")) {
    return `/data-figures/${name}`;
  }
  if (resolved.startsWith("reports/figures/final/")) {
    return `/final-figures/${name}`;
  }

  const rawBase = githubRepoUrl.replace("https://github.com/", "https://raw.githubusercontent.com/");
  return `${rawBase}/main/${resolved}`;
}

export function isExternalHref(href: string): boolean {
  return (
    href.startsWith("http://") ||
    href.startsWith("https://") ||
    href.startsWith("mailto:")
  );
}
