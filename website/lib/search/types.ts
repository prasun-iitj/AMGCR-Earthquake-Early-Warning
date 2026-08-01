/**
 * Search index types — v3 semantic search can replace index source without UI changes.
 */

export type SearchRecord = {
  id: string;
  documentTitle: string;
  sectionHeading: string | null;
  href: string;
  external: boolean;
  sourcePath: string;
  keywords: string[];
  excerpt: string;
  /** Normalized searchable text (title + heading + keywords + excerpt). */
  searchableText: string;
};

export type SearchIndex = {
  schemaVersion: 1;
  generatedAtUtc: string;
  recordCount: number;
  records: SearchRecord[];
};

export type SearchResult = SearchRecord & {
  score: number;
  matchedOn: Array<"title" | "heading" | "keywords" | "content">;
};
