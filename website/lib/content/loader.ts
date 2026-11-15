import fs from "node:fs";
import matter from "gray-matter";
import GithubSlugger from "github-slugger";
import { resolveRepoPath } from "@/lib/content/paths";
import { documentBySlug, type DocumentDefinition } from "@/lib/content/documents";

export type TocHeading = {
  level: number;
  text: string;
  slug: string;
};

export type LoadedDocument = {
  slug: string;
  title: string;
  subtitle?: string;
  description: string;
  sourcePath: string;
  href: string;
  content: string;
  frontmatter: Record<string, unknown>;
  headings: TocHeading[];
};

function stripInlineMarkdown(text: string): string {
  return text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/<[^>]+>/g, "")
    .trim();
}

function cleanDocumentContent(content: string): string {
  // Normalize Windows CRLF to LF
  let cleaned = content.replace(/\r\n/g, "\n");

  // Strip top <div align="center">...</div> cover/title block if present
  cleaned = cleaned.replace(/^\s*<div align=["']?center["']?>[\s\S]*?<\/div>\s*(---\s*)?/i, "");

  // Strip initial # H1 heading to avoid duplicating the page header
  cleaned = cleaned.replace(/^\s*#\s+[^\n]+\n+/, "");

  return cleaned.trim();
}

export function extractHeadings(markdown: string): TocHeading[] {
  const normalized = markdown.replace(/\r\n/g, "\n");
  const slugger = new GithubSlugger();
  const headings: TocHeading[] = [];

  for (const line of normalized.split("\n")) {
    const match = line.match(/^(#{2,3})\s+(.+)$/);
    if (!match) {
      continue;
    }

    const level = match[1].length;
    const text = stripInlineMarkdown(match[2]);
    if (
      !text ||
      text.toLowerCase() === "table of contents" ||
      text.toLowerCase().startsWith("appendix f")
    ) {
      continue;
    }

    headings.push({
      level,
      text,
      slug: slugger.slug(text),
    });
  }

  return headings;
}

export function loadDocument(definition: DocumentDefinition): LoadedDocument {
  const absolutePath = resolveRepoPath(definition.sourcePath);

  if (!fs.existsSync(absolutePath)) {
    throw new Error(
      `Document not found: ${definition.sourcePath} (resolved to ${absolutePath})`,
    );
  }

  const raw = fs.readFileSync(absolutePath, "utf8");
  const { content, data } = matter(raw);
  const cleanedContent = cleanDocumentContent(content);
  const headings = extractHeadings(cleanedContent);

  const title =
    typeof data.title === "string" && data.title.trim()
      ? data.title.trim()
      : definition.title;

  const subtitle =
    typeof data.subtitle === "string" && data.subtitle.trim()
      ? data.subtitle.trim()
      : undefined;

  return {
    slug: definition.slug,
    title,
    subtitle,
    description: definition.description,
    sourcePath: definition.sourcePath,
    href: definition.href,
    content: cleanedContent,
    frontmatter: data,
    headings,
  };
}

export function loadDocumentBySlug(slug: string): LoadedDocument {
  const definition = documentBySlug[slug];
  if (!definition) {
    throw new Error(`Unknown document slug: ${slug}`);
  }
  return loadDocument(definition);
}
