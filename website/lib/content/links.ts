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

  if (normalized.endsWith(".md")) {
    return `${githubRepoUrl}/blob/main/${normalized}`;
  }

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

export function isExternalHref(href: string): boolean {
  return (
    href.startsWith("http://") ||
    href.startsWith("https://") ||
    href.startsWith("mailto:")
  );
}
