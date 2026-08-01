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
        <p className="mt-3 text-lg text-text-muted">{document.description}</p>
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
