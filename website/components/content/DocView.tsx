import { DocPageShell } from "@/components/content/Breadcrumbs";
import {
  DocNavigation,
  TableOfContents,
} from "@/components/content/DocNavigation";
import { MarkdownRenderer } from "@/components/content/MarkdownRenderer";
import type { BreadcrumbItem } from "@/components/content/Breadcrumbs";
import { getDocumentNavigation } from "@/lib/content/documents";
import type { LoadedDocument } from "@/lib/content/loader";

type DocViewProps = {
  document: LoadedDocument;
  breadcrumbs: BreadcrumbItem[];
};

export function DocView({ document, breadcrumbs }: DocViewProps) {
  const { previous, next } = getDocumentNavigation(document.slug);

  return (
    <DocPageShell
      breadcrumbs={breadcrumbs}
      sourcePath={document.sourcePath}
      sidebar={<TableOfContents headings={document.headings} />}
    >
      <header className="mb-10 border-b border-border pb-8">
        <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
          {document.title}
        </h1>
        {document.subtitle && (
          <p className="mt-2 text-xl font-medium text-primary md:text-2xl">
            {document.subtitle}
          </p>
        )}
        <p className="mt-3 text-base text-text-muted md:text-lg">{document.description}</p>

        {Boolean(
          document.frontmatter &&
            (document.frontmatter.date ||
              document.frontmatter.version ||
              document.frontmatter.document ||
              document.frontmatter.programme)
        ) && (
          <div className="mt-5 flex flex-wrap gap-2 text-xs">
            {document.frontmatter.document ? (
              <span className="rounded-md border border-border bg-surface px-2.5 py-1 font-semibold text-text">
                {String(document.frontmatter.document)}
              </span>
            ) : null}
            {document.frontmatter.version ? (
              <span className="rounded-md border border-border bg-surface px-2.5 py-1 font-medium text-text">
                v{String(document.frontmatter.version)}
              </span>
            ) : null}
            {document.frontmatter.date ? (
              <span className="rounded-md border border-border bg-surface px-2.5 py-1 text-text-muted">
                {String(document.frontmatter.date)}
              </span>
            ) : null}
            {document.frontmatter.programme ? (
              <span className="rounded-md border border-border bg-surface px-2.5 py-1 text-text-muted">
                {String(document.frontmatter.programme)}
              </span>
            ) : null}
          </div>
        )}
      </header>

      <div className="mb-8 lg:hidden">
        <details className="rounded-lg border border-border bg-surface p-4">
          <summary className="cursor-pointer text-sm font-semibold text-text">
            Table of contents
          </summary>
          <div className="mt-4">
            <TableOfContents headings={document.headings} />
          </div>
        </details>
      </div>

      <MarkdownRenderer content={document.content} sourcePath={document.sourcePath} />

      <DocNavigation
        previous={previous ? { title: previous.title, href: previous.href } : null}
        next={next ? { title: next.title, href: next.href } : null}
      />
    </DocPageShell>
  );
}
