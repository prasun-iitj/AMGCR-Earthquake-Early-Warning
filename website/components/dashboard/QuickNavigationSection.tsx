import Link from "next/link";
import { Section } from "@/components/ui/Section";
import type { QuickNavCard } from "@/lib/dashboard/types";

type QuickNavigationSectionProps = {
  cards: QuickNavCard[];
};

export function QuickNavigationSection({ cards }: QuickNavigationSectionProps) {
  return (
    <Section
      id="quick-nav"
      eyebrow="Navigation"
      title="Quick navigation"
      subtitle="Jump directly to interactive explorers and documentation rendered from the repository."
      variant="muted"
    >
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card) => (
          <article
            key={card.title}
            className="rounded-xl border border-border bg-surface-elevated p-5 shadow-sm transition-colors hover:border-primary/30"
          >
            <h3 className="font-serif text-lg font-semibold text-text">
              {card.title}
            </h3>
            <p className="mt-2 text-sm leading-relaxed text-text-muted">
              {card.description}
            </p>
            {card.external ? (
              <a
                href={card.href}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-flex text-sm font-medium text-primary hover:text-primary-light"
              >
                Open ↗
              </a>
            ) : (
              <Link
                href={card.href}
                className="mt-4 inline-flex text-sm font-medium text-primary hover:text-primary-light"
              >
                Open →
              </Link>
            )}
          </article>
        ))}
      </div>
    </Section>
  );
}
