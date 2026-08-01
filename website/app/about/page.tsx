import type { Metadata } from "next";
import { Section } from "@/components/ui/Section";

export const metadata: Metadata = {
  title: "About",
  description: "About the AMGCR Earthquake Research interactive platform.",
};

export default function AboutPage() {
  return (
    <>
      <Section
        eyebrow="About"
        title="About this platform"
        subtitle="A research-oriented website foundation for presenting reproducible earthquake science. This page uses placeholder text only."
      >
        <div className="prose prose-lg max-w-3xl text-text-muted">
          <p>
            This platform is being developed as part of Version 2.0 of the
            AMGCR Earthquake Research project. The goal is to communicate
            scientific work clearly to academic, professional, and general
            audiences without requiring visitors to navigate a code repository
            first.
          </p>
          <p>
            During Phase 1, the focus is strictly on structure and design — not
            on importing or displaying scientific content from the repository.
          </p>
        </div>
      </Section>

      <Section variant="muted" title="Design principles">
        <div className="grid gap-6 md:grid-cols-2">
          {[
            {
              title: "Evidence-led presentation",
              body: "Future phases will surface figures, tables, and reports directly from repository sources.",
            },
            {
              title: "Single source of truth",
              body: "The GitHub repository will remain the maintained scientific baseline.",
            },
            {
              title: "Accessible and responsive",
              body: "Layout, navigation, and typography are built for desktop, tablet, and mobile from the start.",
            },
            {
              title: "Free infrastructure",
              body: "The stack is chosen for static deployment on free hosting tiers with no backend required.",
            },
          ].map((item) => (
            <article
              key={item.title}
              className="rounded-xl border border-border bg-surface-elevated p-6"
            >
              <h3 className="font-serif text-xl font-semibold text-text">
                {item.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                {item.body}
              </p>
            </article>
          ))}
        </div>
      </Section>
    </>
  );
}
