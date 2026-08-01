import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { DocView } from "@/components/content/DocView";
import { documentBySlug, docsIndexEntries } from "@/lib/content/documents";
import { loadDocumentBySlug } from "@/lib/content/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return docsIndexEntries.map((doc) => ({ slug: doc.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const definition = documentBySlug[slug];

  if (!definition || !definition.href.startsWith("/docs/")) {
    return buildPageMetadata({
      title: "Documentation",
      description: "Documentation for AMGCR Earthquake Research.",
      path: "/docs",
    });
  }

  return buildPageMetadata({
    title: definition.title,
    description: definition.description,
    path: definition.href,
  });
}

export default async function DocumentationPage({ params }: PageProps) {
  const { slug } = await params;
  const definition = documentBySlug[slug];

  if (!definition || !definition.href.startsWith("/docs/")) {
    notFound();
  }

  const document = loadDocumentBySlug(slug);

  return (
    <DocView
      document={document}
      breadcrumbs={[
        { label: "Home", href: "/" },
        { label: "Documentation", href: "/docs" },
        { label: document.title },
      ]}
    />
  );
}
