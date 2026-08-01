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

export function extractHeadings(markdown: string): TocHeading[] {
  const slugger = new GithubSlugger();
  const headings: TocHeading[] = [];

  for (const line of markdown.split("\n")) {
    const match = line.match(/^(#{2,4})\s+(.+)$/);
    if (!match) {
      continue;
    }

    const level = match[1].length;
    const text = stripInlineMarkdown(match[2]);
    if (!text) {
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
  const headings = extractHeadings(content);

  const title =
    typeof data.title === "string"
      ? data.title
      : headings.find((h) => h.level === 2)?.text ?? definition.title;

  return {
    slug: definition.slug,
    title,
    description: definition.description,
    sourcePath: definition.sourcePath,
    href: definition.href,
    content,
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
