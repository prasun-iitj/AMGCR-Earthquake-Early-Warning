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
    slug: "research-direction",
    title: "Research Direction",
    description: "Why the project shifted from EarthESND to Western & European early warning.",
    sourcePath: "docs/RESEARCH_DIRECTION.md",
    href: "/docs/research-direction",
    category: "governance",
    order: 4,
  },
  {
    slug: "roadmap",
    title: "Project Roadmap",
    description: "Development and research roadmap across v1.0, v2.0, v2.1, and v3.0.",
    sourcePath: "docs/ROADMAP.md",
    href: "/docs/roadmap",
    category: "governance",
    order: 5,
  },
  {
    slug: "swiss-sed-dataset-report",
    title: "Swiss SED Dataset Report",
    description: "Methods-transfer acquisition of 20 Swiss events across 120 three-component records.",
    sourcePath: "docs/SED_SWITZERLAND_DATASET_REPORT.md",
    href: "/docs/swiss-sed-dataset-report",
    category: "research",
    order: 6,
  },
  {
    slug: "swiss-validation-results",
    title: "Swiss Independent Validation Results",
    description: "Independent validation results (STEP 2K) on locked Set C with pre-declared STA/LTA threshold 8.0.",
    sourcePath: "docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md",
    href: "/docs/swiss-validation-results",
    category: "research",
    order: 7,
  },
  {
    slug: "swiss-ml-feasibility-audit",
    title: "Swiss ML Feasibility Audit (STEP 3A, historical)",
    description: "Historical STEP 3A audit: NO-GO for supervised ML on unlabelled Set A tables; later resolved by SED analyst picks (STEP ML-1A).",
    sourcePath: "docs/SWISS_ML_FEASIBILITY_AUDIT.md",
    href: "/docs/swiss-ml-feasibility-audit",
    category: "governance",
    order: 8,
  },
  {
    slug: "professor-handover-guide",
    title: "Professor Handover Guide",
    description: "Entry point for academic review: project overview, navigation, reproduction, data availability, inventory and figure index.",
    sourcePath: "docs/professor_handover/PROFESSOR_HANDOVER_GUIDE.md",
    href: "/docs/professor-handover-guide",
    category: "overview",
    order: 9,
  },
  {
    slug: "research-executive-summary",
    title: "Research Executive Summary",
    description: "Two-page academic summary: problem, data, methods, results and limitations.",
    sourcePath: "docs/professor_handover/RESEARCH_EXECUTIVE_SUMMARY.md",
    href: "/docs/research-executive-summary",
    category: "research",
    order: 9,
  },
  {
    slug: "research-methodology",
    title: "Research Methodology",
    description: "Acquisition, validation, preprocessing, labelling, windows, features, training and evaluation with parameters.",
    sourcePath: "docs/professor_handover/RESEARCH_METHODOLOGY.md",
    href: "/docs/research-methodology",
    category: "research",
    order: 9,
  },
  {
    slug: "research-limitations-and-open-questions",
    title: "Research Limitations and Open Questions",
    description: "Scientific limitations, documentation gaps, data-access issues and future research.",
    sourcePath: "docs/professor_handover/RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md",
    href: "/docs/research-limitations-and-open-questions",
    category: "governance",
    order: 9,
  },
  {
    slug: "professor-review-checklist",
    title: "Professor Review Checklist",
    description: "Practical checklist with the report, script or dataset behind each review item.",
    sourcePath: "docs/professor_handover/PROFESSOR_REVIEW_CHECKLIST.md",
    href: "/docs/professor-review-checklist",
    category: "governance",
    order: 9,
  },
  {
    slug: "professor-discussion-notes",
    title: "Professor Discussion Notes",
    description: "Grounded answers to likely questions about the research problem, data, methods and limits.",
    sourcePath: "docs/professor_handover/PROFESSOR_DISCUSSION_NOTES.md",
    href: "/docs/professor-discussion-notes",
    category: "governance",
    order: 9,
  },
  {
    slug: "data-collection-and-analysis-report",
    title: "Data Collection and Analysis Report",
    description: "Complete data journey: sources, acquisition, raw files, preprocessing, Set A and Set C construction, features and analysis.",
    sourcePath: "docs/DATA_COLLECTION_AND_ANALYSIS_REPORT.md",
    href: "/docs/data-collection-and-analysis-report",
    category: "research",
    order: 9,
  },
  {
    slug: "data-dictionary",
    title: "Data Dictionary",
    description: "Files, columns, labels, feature definitions, units and dataset-specific differences.",
    sourcePath: "docs/DATA_DICTIONARY.md",
    href: "/docs/data-dictionary",
    category: "research",
    order: 9,
  },
  {
    slug: "data-acquisition-and-reproduction",
    title: "Data Acquisition and Reproduction Guide",
    description: "Data-source links, download and feature-extraction commands, expected outputs and limits of reproduction.",
    sourcePath: "docs/DATA_ACQUISITION_AND_REPRODUCTION.md",
    href: "/docs/data-acquisition-and-reproduction",
    category: "research",
    order: 9,
  },
  {
    slug: "research-package",
    title: "Research Package (STEP ML-1A to ML-4)",
    description: "Consolidated overview for reviewers: datasets, preprocessing, labelling, features, models, validation, results, limitations.",
    sourcePath: "docs/RESEARCH_PACKAGE.md",
    href: "/docs/research-package",
    category: "research",
    order: 9,
  },
  {
    slug: "set-c-vertical-ml-evaluation",
    title: "STEP ML-4 Set C Evaluation Report",
    description: "Vertical-only Random Forest and XGBoost trained on Set A and evaluated on independent Set C events.",
    sourcePath: "docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md",
    href: "/docs/set-c-vertical-ml-evaluation",
    category: "research",
    order: 10,
  },
  {
    slug: "ml-reproduction-guide",
    title: "ML Reproduction Guide",
    description: "Environment, commands, expected inputs and outputs for reproducing STEP ML-2 to ML-4.",
    sourcePath: "docs/ML_REPRODUCTION_GUIDE.md",
    href: "/docs/ml-reproduction-guide",
    category: "research",
    order: 11,
  },
  {
    slug: "data-and-model-inventory",
    title: "Data and Model Inventory",
    description: "Paths, sizes, provenance and redistribution notes for data, features, models and reports.",
    sourcePath: "docs/DATA_AND_MODEL_INVENTORY.md",
    href: "/docs/data-and-model-inventory",
    category: "research",
    order: 12,
  },
  {
    slug: "final-integrity-check",
    title: "Final Integrity Check",
    description: "Read-only audit of feature importance, schema, dataset independence, threshold provenance and documentation.",
    sourcePath: "FINAL_INTEGRITY_CHECK.md",
    href: "/docs/final-integrity-check",
    category: "governance",
    order: 13,
  },
  {
    slug: "research-report-final",
    title: "Final Research Report",
    description:
      "Primary submission narrative (D-F1) — California FDSN pilot science.",
    sourcePath: "reports/Research_Report_Final.md",
    href: "/research/report",
    category: "research",
    order: 9,
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
