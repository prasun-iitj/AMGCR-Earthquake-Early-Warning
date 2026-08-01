import type { SearchIndex, SearchRecord, SearchResult } from "@/lib/search/types";

function normalize(text: string): string {
  return text.toLowerCase().replace(/\s+/g, " ").trim();
}

function tokenize(query: string): string[] {
  return normalize(query)
    .split(" ")
    .filter((token) => token.length >= 2);
}

function scoreRecord(record: SearchRecord, tokens: string[]): SearchResult | null {
  if (tokens.length === 0) {
    return null;
  }

  const title = normalize(record.documentTitle);
  const heading = normalize(record.sectionHeading ?? "");
  const keywords = normalize(record.keywords.join(" "));
  const content = normalize(record.searchableText);
  let score = 0;
  const matchedOn = new Set<SearchResult["matchedOn"][number]>();

  for (const token of tokens) {
    if (title.includes(token)) {
      score += 12;
      matchedOn.add("title");
    }
    if (heading.includes(token)) {
      score += 10;
      matchedOn.add("heading");
    }
    if (keywords.includes(token)) {
      score += 8;
      matchedOn.add("keywords");
    }
    if (content.includes(token)) {
      score += 4;
      matchedOn.add("content");
    }
  }

  if (score === 0) {
    return null;
  }

  return {
    ...record,
    score,
    matchedOn: Array.from(matchedOn),
  };
}

/** Client-side instant search — replace index provider in v3 without UI redesign. */
export function searchIndex(
  index: SearchIndex,
  query: string,
  limit = 20,
): SearchResult[] {
  const tokens = tokenize(query);
  if (tokens.length === 0) {
    return [];
  }

  return index.records
    .map((record) => scoreRecord(record, tokens))
    .filter((result): result is SearchResult => result !== null)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}

export function groupResultsByDocument(results: SearchResult[]): SearchResult[] {
  const seen = new Set<string>();
  const grouped: SearchResult[] = [];

  for (const result of results) {
    const key = `${result.href}::${result.sectionHeading ?? ""}`;
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    grouped.push(result);
  }

  return grouped;
}
