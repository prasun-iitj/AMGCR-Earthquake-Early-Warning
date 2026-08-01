import type { ReactNode } from "react";
import { Section } from "@/components/ui/Section";
import { projectHighlights } from "@/lib/home/content";

const iconMap: Record<string, ReactNode> = {
  reference: (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
      <path d="M4 19.5A2.5 2.5 0 016.5 17H20" strokeLinecap="round" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" />
    </svg>
  ),
  pilot: (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 3v18M3 12h18" strokeLinecap="round" />
    </svg>
  ),
  europe: (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
      <path d="M12 21a9 9 0 100-18 9 9 0 000 18z" />
      <path d="M3.6 9h16.8M3.6 15h16.8M12 3c-2.5 2.8-3.8 6-3.8 9s1.3 6.2 3.8 9c2.5-2.8 3.8-6 3.8-9s-1.3-6.2-3.8-9z" />
    </svg>
  ),
  pipeline: (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
      <path d="M4 6h16M4 12h10M4 18h16" strokeLinecap="round" />
    </svg>
  ),
  opensource: (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
      <path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .3-2.5 1.5-3.5C18.5 14 21 12.5 21 9c0-4-3.5-7-8-7S5 5 5 9c0 3.5 2.5 5 6.5 6.5 1.2 1 1.5 2.5 1.5 3.5V22" strokeLinecap="round" />
    </svg>
  ),
  reproducible: (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="1.75">
      <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" />
    </svg>
  ),
};

export function ProjectHighlights() {
  return (
    <Section
      eyebrow="Project highlights"
      title="What this research delivers"
      subtitle="A certificate-grade earthquake early warning workflow designed for transparency, transfer to European networks, and open reproducibility."
    >
      <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
        {projectHighlights.map((item) => (
          <article
            key={item.title}
            className="rounded-xl border border-border bg-surface-elevated p-6 shadow-sm transition-colors hover:border-primary/25"
          >
            <div className="mb-4 inline-flex rounded-lg bg-primary/8 p-3 text-primary">
              {iconMap[item.icon]}
            </div>
            <h3 className="font-serif text-xl font-semibold text-text">
              {item.title}
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-text-muted">
              {item.description}
            </p>
          </article>
        ))}
      </div>
    </Section>
  );
}
