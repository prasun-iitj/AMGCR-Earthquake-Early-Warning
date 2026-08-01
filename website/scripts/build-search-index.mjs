import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import GithubSlugger from "github-slugger";
import matter from "gray-matter";

const websiteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = path.resolve(websiteRoot, "..");

const GITHUB_REPO_URL =
  process.env.NEXT_PUBLIC_GITHUB_REPO_URL ??
  "https://github.com/amgcr/AMGCR_Earthquake_Research";

const SITE_ROUTES = {
  "README.md": "/docs/readme",
  "docs/PROJECT_CHARTER.md": "/docs/project-charter",
  "docs/PROJECT_STATUS.md": "/docs/project-status",
  "reports/Research_Report_Final.md": "/research/report",
};

const INDEX_ROOTS = ["README.md", "docs", "reports"];

function resolveRepoPath(relativePath) {
  return path.join(repoRoot, relativePath);
}

function stripMarkdown(text) {
  return text
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/!\[[^\]]*\]\([^)]+\)/g, " ")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/^\s*[-*+]\s+/gm, "")
    .replace(/^\s*\d+\.\s+/gm, "")
    .replace(/\|/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function excerptFrom(text, maxLength = 180) {
  const plain = stripMarkdown(text);
  if (plain.length <= maxLength) {
    return plain;
  }
  return `${plain.slice(0, maxLength).trim()}…`;
}

function resolveHref(sourcePath, headingSlug) {
  const normalized = sourcePath.replace(/\\/g, "/");
  const siteHref = SITE_ROUTES[normalized];

  if (siteHref) {
    return {
      href: headingSlug ? `${siteHref}#${headingSlug}` : siteHref,
      external: false,
    };
  }

  const blob = `${GITHUB_REPO_URL}/blob/main/${normalized}`;
  return {
    href: headingSlug ? `${blob}#${headingSlug}` : blob,
    external: true,
  };
}

function documentTitle(sourcePath, frontmatter, content) {
  if (typeof frontmatter.title === "string" && frontmatter.title.trim()) {
    return frontmatter.title.trim();
  }

  const h1 = content.match(/^#\s+(.+)$/m);
  if (h1?.[1]) {
    return stripMarkdown(h1[1]);
  }

  return path.basename(sourcePath, ".md").replace(/_/g, " ");
}

function collectMarkdownFiles() {
  const files = [];

  for (const root of INDEX_ROOTS) {
    const absolute = resolveRepoPath(root);
    if (!fs.existsSync(absolute)) {
      continue;
    }

    const stat = fs.statSync(absolute);
    if (stat.isFile() && root.endsWith(".md")) {
      files.push(root);
      continue;
    }

    if (!stat.isDirectory()) {
      continue;
    }

    const walk = (directory, relativePrefix) => {
      for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
        const relative = path.posix.join(relativePrefix, entry.name);
        const entryAbsolute = path.join(directory, entry.name);
        if (entry.isDirectory()) {
          walk(entryAbsolute, relative);
          continue;
        }
        if (entry.name.endsWith(".md")) {
          files.push(relative.replace(/\\/g, "/"));
        }
      }
    };

    walk(absolute, root);
  }

  return files.sort();
}

function splitSections(content) {
  const lines = content.split("\n");
  const sections = [];
  let currentHeading = null;
  let currentLines = [];

  const pushSection = () => {
    const body = currentLines.join("\n").trim();
    if (currentHeading || body) {
      sections.push({ heading: currentHeading, body });
    }
    currentLines = [];
  };

  for (const line of lines) {
    const headingMatch = line.match(/^#{2,4}\s+(.+)$/);
    if (headingMatch) {
      pushSection();
      currentHeading = stripMarkdown(headingMatch[1]);
      continue;
    }
    currentLines.push(line);
  }

  pushSection();
  return sections;
}

function normalizeSearchText(title, heading, keywords, excerpt) {
  return [title, heading, ...keywords, excerpt]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function buildRecordsForFile(relativePath) {
  const absolutePath = resolveRepoPath(relativePath);
  const raw = fs.readFileSync(absolutePath, "utf8");
  const { content, data } = matter(raw);
  const title = documentTitle(relativePath, data, content);
  const records = [];

  const introSection = content.split(/^##\s+/m)[0]?.trim() ?? "";
  const introLink = resolveHref(relativePath);
  const introExcerpt = excerptFrom(introSection || content);

  records.push({
    id: `${relativePath}::document`,
    documentTitle: title,
    sectionHeading: null,
    href: introLink.href,
    external: introLink.external,
    sourcePath: relativePath,
    keywords: [title, path.basename(relativePath, ".md")],
    excerpt: introExcerpt,
    searchableText: normalizeSearchText(title, null, [title], introExcerpt),
  });

  for (const section of splitSections(content)) {
    if (!section.heading) {
      continue;
    }

    const slugger = new GithubSlugger();
    const headingSlug = slugger.slug(section.heading);
    const link = resolveHref(relativePath, headingSlug);
    const sectionExcerpt = excerptFrom(section.body);
    const keywords = [title, section.heading];

    records.push({
      id: `${relativePath}::${headingSlug}`,
      documentTitle: title,
      sectionHeading: section.heading,
      href: link.href,
      external: link.external,
      sourcePath: relativePath,
      keywords,
      excerpt: sectionExcerpt,
      searchableText: normalizeSearchText(
        title,
        section.heading,
        keywords,
        sectionExcerpt,
      ),
    });
  }

  return records;
}

export function buildSearchIndexScript() {
  const records = collectMarkdownFiles().flatMap(buildRecordsForFile);

  return {
    schemaVersion: 1,
    generatedAtUtc: new Date().toISOString(),
    recordCount: records.length,
    records,
  };
}

const index = buildSearchIndexScript();
const outputDir = path.join(websiteRoot, "public");
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(path.join(outputDir, "search-index.json"), JSON.stringify(index), "utf8");
console.log(
  `[build-search-index] Wrote ${index.recordCount} records to public/search-index.json`,
);
