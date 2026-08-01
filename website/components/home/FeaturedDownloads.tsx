import Link from "next/link";
import { Section } from "@/components/ui/Section";
import { Button } from "@/components/ui/Button";
import { featuredDownloads } from "@/lib/home/content";

export function FeaturedDownloads() {
  return (
    <Section
      eyebrow="Resources"
      title="Featured downloads"
      subtitle="Primary artefacts for examiners, researchers, and collaborators."
    >
      <div className="grid gap-6 md:grid-cols-3">
        {featuredDownloads.map((item) => (
          <article
            key={item.title}
            className="flex h-full flex-col rounded-xl border border-border bg-surface-elevated p-6 shadow-sm transition-colors hover:border-primary/25"
          >
            <h3 className="font-serif text-xl font-semibold text-text">
              {item.title}
            </h3>
            <p className="mt-3 flex-1 text-sm leading-relaxed text-text-muted">
              {item.description}
            </p>
            <div className="mt-6">
              {item.external ? (
                <a
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex text-sm font-medium text-primary transition-colors hover:text-primary-light"
                >
                  {item.cta} →
                </a>
              ) : (
                <Link
                  href={item.href}
                  className="inline-flex text-sm font-medium text-primary transition-colors hover:text-primary-light"
                >
                  {item.cta} →
                </Link>
              )}
            </div>
          </article>
        ))}
      </div>

      <div className="mt-8 text-center">
        <Button href="/resources" variant="outline">
          Browse all resources
        </Button>
      </div>
    </Section>
  );
}
