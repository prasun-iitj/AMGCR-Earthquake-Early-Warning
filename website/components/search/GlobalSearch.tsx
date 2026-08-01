"use client";

import Link from "next/link";
import { useCallback, useEffect, useId, useMemo, useRef, useState } from "react";
import { groupResultsByDocument, searchIndex } from "@/lib/search/query";
import type { SearchIndex, SearchResult } from "@/lib/search/types";

type GlobalSearchProps = {
  open: boolean;
  onClose: () => void;
};

export function GlobalSearch({ open, onClose }: GlobalSearchProps) {
  const dialogTitleId = useId();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState<SearchIndex | null>(null);
  const [error, setError] = useState<string | null>(null);
  const indexPromiseRef = useRef<Promise<SearchIndex> | null>(null);

  const loadIndex = useCallback(() => {
    if (index) {
      return Promise.resolve(index);
    }

    if (!indexPromiseRef.current) {
      indexPromiseRef.current = fetch("/search-index.json")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Search index unavailable");
          }
          return response.json() as Promise<SearchIndex>;
        })
        .then((payload) => {
          setIndex(payload);
          setError(null);
          return payload;
        })
        .catch(() => {
          setError(
            "Search index could not be loaded. Run the build script to regenerate it.",
          );
          indexPromiseRef.current = null;
          throw new Error("Search index unavailable");
        });
    }

    return indexPromiseRef.current;
  }, [index]);

  useEffect(() => {
    if (!open) {
      return;
    }

    void loadIndex();
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const timer = window.setTimeout(() => inputRef.current?.focus(), 0);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.clearTimeout(timer);
    };
  }, [loadIndex, open]);

  const handleClose = useCallback(() => {
    setQuery("");
    onClose();
  }, [onClose]);

  const results = useMemo(() => {
    if (!index || !query.trim()) {
      return [] as SearchResult[];
    }
    return groupResultsByDocument(searchIndex(index, query, 24));
  }, [index, query]);

  useEffect(() => {
    if (!open) {
      return;
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        handleClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleClose, open]);

  if (!open) {
    return null;
  }

  const loading = !index && !error;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-start justify-center bg-black/40 px-4 py-8 sm:py-16"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) {
          handleClose();
        }
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={dialogTitleId}
        className="w-full max-w-2xl overflow-hidden rounded-xl border border-border bg-surface-elevated shadow-2xl"
      >
        <div className="border-b border-border px-4 py-3">
          <label htmlFor={`${dialogTitleId}-input`} className="sr-only">
            Search documentation
          </label>
          <input
            ref={inputRef}
            id={`${dialogTitleId}-input`}
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search docs, reports, and research content…"
            className="w-full bg-transparent text-base text-text outline-none placeholder:text-text-muted"
            autoComplete="off"
          />
          <p id={dialogTitleId} className="mt-2 text-xs text-text-muted">
            Search titles, headings, and content snippets ·{" "}
            <kbd className="rounded border border-border px-1">Esc</kbd> to close
          </p>
        </div>

        <div className="max-h-[min(60vh,520px)] overflow-y-auto p-2">
          {loading ? (
            <p className="px-3 py-6 text-sm text-text-muted">Loading search index…</p>
          ) : null}
          {error ? <p className="px-3 py-6 text-sm text-accent">{error}</p> : null}
          {!loading && !error && query.trim() && results.length === 0 ? (
            <p className="px-3 py-6 text-sm text-text-muted">
              No matches for &ldquo;{query}&rdquo;
            </p>
          ) : null}
          {!query.trim() && !loading ? (
            <p className="px-3 py-6 text-sm text-text-muted">
              Try keywords such as &ldquo;California&rdquo;, &ldquo;preprocessing&rdquo;,
              or &ldquo;reproducibility&rdquo;.
            </p>
          ) : null}

          <ul className="space-y-1">
            {results.map((result) => (
              <li key={result.id}>
                <SearchResultLink result={result} onNavigate={handleClose} />
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function SearchResultLink({
  result,
  onNavigate,
}: {
  result: SearchResult;
  onNavigate: () => void;
}) {
  const className =
    "block rounded-lg px-3 py-3 transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30";

  const content = (
    <>
      <div className="flex flex-wrap items-center gap-2">
        <p className="font-medium text-text">{result.documentTitle}</p>
        {result.sectionHeading ? (
          <span className="rounded-full bg-surface px-2 py-0.5 text-xs text-text-muted">
            {result.sectionHeading}
          </span>
        ) : null}
        {result.external ? (
          <span className="text-xs text-text-muted">GitHub ↗</span>
        ) : null}
      </div>
      <p className="mt-1 line-clamp-2 text-sm text-text-muted">{result.excerpt}</p>
      <p className="mt-2 font-mono text-[0.65rem] text-text-muted">{result.sourcePath}</p>
    </>
  );

  if (result.external) {
    return (
      <a
        href={result.href}
        target="_blank"
        rel="noopener noreferrer"
        className={className}
        onClick={onNavigate}
      >
        {content}
      </a>
    );
  }

  return (
    <Link href={result.href} className={className} onClick={onNavigate}>
      {content}
    </Link>
  );
}
