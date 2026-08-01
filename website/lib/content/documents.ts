export type DocumentCategory = "overview" | "governance" | "research";

export type DocumentDefinition = {
  slug: string;
  title: string;
  description: string;
  sourcePath: string;
  href: string;
  category: DocumentCategory;
  order: number;
};

/** Supported repository Markdown files (single source of truth — no duplicates). */
export const documents: DocumentDefinition[] = [
  {
    slug: "readme",
    title: "Repository README",
    description: "Project overview, release status, and repository structure.",
    sourcePath: "README.md",
    href: "/docs/readme",
    category: "overview",
    order: 1,
  },
  {
    slug: "project-charter",
    title: "Project Charter",
    description: "Authoritative vision, scope, status, and priorities.",
    sourcePath: "docs/PROJECT_CHARTER.md",
    href: "/docs/project-charter",
    category: "governance",
    order: 2,
  },
  {
    slug: "project-status",
    title: "Project Status",
    description: "Current milestones and Version 2.0 roadmap summary.",
    sourcePath: "docs/PROJECT_STATUS.md",
    href: "/docs/project-status",
    category: "governance",
    order: 3,
  },
  {
    slug: "research-report-final",
    title: "Final Research Report",
    description:
      "Primary submission narrative (D-F1) — California FDSN pilot science.",
    sourcePath: "reports/Research_Report_Final.md",
    href: "/research/report",
    category: "research",
    order: 4,
  },
];

export const documentBySlug = Object.fromEntries(
  documents.map((doc) => [doc.slug, doc]),
) as Record<string, DocumentDefinition>;

export const docsIndexEntries = documents.filter(
  (doc) => doc.href.startsWith("/docs/"),
);

export const researchReport = documents.find(
  (doc) => doc.slug === "research-report-final",
)!;

export function getDocumentNavigation(slug: string) {
  const index = documents.findIndex((doc) => doc.slug === slug);
  if (index === -1) {
    return { previous: null, next: null };
  }

  return {
    previous: index > 0 ? documents[index - 1] : null,
    next: index < documents.length - 1 ? documents[index + 1] : null,
  };
}

export function getDocumentByHref(href: string): DocumentDefinition | undefined {
  return documents.find((doc) => doc.href === href);
}

/** Map repository-relative Markdown paths to site routes. */
export const sourcePathToHref: Record<string, string> = Object.fromEntries(
  documents.flatMap((doc) => [
    [doc.sourcePath, doc.href],
    [doc.sourcePath.replace(/\//g, "\\"), doc.href],
  ]),
);
