import type { Metadata } from "next";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";

export const metadata: Metadata = {
  title: "Contact",
  description: "Contact placeholder for the AMGCR Earthquake Research platform.",
};

export default function ContactPage() {
  return (
    <>
      <Section
        eyebrow="Contact"
        title="Get in touch"
        subtitle="A contact form and links may be added in a later phase. This page is a structural placeholder."
      >
        <div className="grid gap-8 lg:grid-cols-2">
          <div className="rounded-xl border border-border bg-surface-elevated p-6">
            <h3 className="font-serif text-xl font-semibold text-text">
              Contact form placeholder
            </h3>
            <p className="mt-3 text-sm text-text-muted">
              No form submission backend is included in Phase 1. A static
              contact section or mailto link can be added when requirements are
              confirmed.
            </p>
            <form className="mt-6 space-y-4" aria-label="Contact form placeholder">
              <div>
                <label
                  htmlFor="name"
                  className="mb-2 block text-sm font-medium text-text"
                >
                  Name
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  disabled
                  placeholder="Your name"
                  className="w-full rounded-lg border border-border bg-surface px-4 py-3 text-sm text-text-muted"
                />
              </div>
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-medium text-text"
                >
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  disabled
                  placeholder="you@example.com"
                  className="w-full rounded-lg border border-border bg-surface px-4 py-3 text-sm text-text-muted"
                />
              </div>
              <div>
                <label
                  htmlFor="message"
                  className="mb-2 block text-sm font-medium text-text"
                >
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows={4}
                  disabled
                  placeholder="Your message"
                  className="w-full rounded-lg border border-border bg-surface px-4 py-3 text-sm text-text-muted"
                />
              </div>
              <Button type="button" disabled variant="primary">
                Send message (disabled)
              </Button>
            </form>
          </div>

          <div className="space-y-6">
            <article className="rounded-xl border border-border bg-surface-elevated p-6">
              <h3 className="font-serif text-xl font-semibold text-text">
                Repository
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                Scientific source code, reports, and data documentation live in
                the project repository. A GitHub link will be added in a later
                phase.
              </p>
            </article>
            <article className="rounded-xl border border-border bg-surface-elevated p-6">
              <h3 className="font-serif text-xl font-semibold text-text">
                Programme context
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                Placeholder for certificate programme affiliation, author details,
                and professional links. No personal information is included in
                Phase 1.
              </p>
            </article>
          </div>
        </div>
      </Section>
    </>
  );
}
