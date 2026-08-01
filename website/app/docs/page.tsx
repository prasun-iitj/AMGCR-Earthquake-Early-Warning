import type { Metadata } from "next";
import Link from "next/link";
import { Section } from "@/components/ui/Section";
import { documents } from "@/lib/content/documents";

export const metadata: Metadata = {
  title: "Documentation",
  description:
    "Documentation index for AMGCR Earthquake Research — rendered from repository Markdown.",
};

const categoryLabels = {
  overview: "Overview",
  governance: "Governance",
  research: "Research",
} as const;

export default function DocumentationIndexPage() {
  const grouped = documents.reduce<
    Record<string, typeof documents>
  >((acc, doc) => {
    const key = doc.category;
    acc[key] = acc[key] ? [...acc[key], doc] : [doc];
    return acc;
  }, {});

  return (
    <>
      <Section
        eyebrow="Documentation"
        title="Documentation index"
        subtitle="These pages render Markdown directly from the repository at build time. The GitHub repository remains the single source of truth."
      >
        <div className="space-y-10">
          {(Object.keys(categoryLabels) as Array<keyof typeof categoryLabels>).map(
            (category) => {
              const items = grouped[category];
              if (!items?.length) {
                return null;
              }

              return (
                <section key={category}>
                  <h2 className="mb-4 font-serif text-2xl font-semibold text-text">
                    {categoryLabels[category]}
                  </h2>
                  <ul className="grid gap-4 md:grid-cols-2">
                    {items.map((doc) => (
                      <li key={doc.slug}>
                        <Link
                          href={doc.href}
                          className="group block h-full rounded-xl border border-border bg-surface-elevated p-6 shadow-sm transition-colors hover:border-primary/30"
                        >
                          <h3 className="font-serif text-xl font-semibold text-text group-hover:text-primary">
                            {doc.title}
                          </h3>
                          <p className="mt-2 text-sm leading-relaxed text-text-muted">
                            {doc.description}
                          </p>
                          <p className="mt-4 font-mono text-xs text-text-muted">
                            {doc.sourcePath}
                          </p>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </section>
              );
            },
          )}
        </div>
      </Section>
    </>
  );
}
