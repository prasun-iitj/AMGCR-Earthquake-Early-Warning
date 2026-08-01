import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/PageHeader";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import { buildPageMetadata } from "@/lib/seo/metadata";
import { githubRepoUrl } from "@/lib/content/paths";

export const metadata: Metadata = buildPageMetadata({
  title: "Contact",
  description:
    "Contact the AMGCR Earthquake Early Warning Research team — repository links and programme context.",
  path: "/contact",
});

export default function ContactPage() {
  return (
    <>
      <PageHeader
        breadcrumbs={[
          { label: "Home", href: "/" },
          { label: "Contact" },
        ]}
        eyebrow="Contact"
        title="Get in touch"
        subtitle="Reach the researcher via email or explore the open research repository. No form backend is included in this static platform."
      />

      <Section>
        <div className="grid gap-8 lg:grid-cols-2">
          <div className="rounded-xl border border-border bg-surface-elevated p-6">
            <h2 className="font-serif text-xl font-semibold text-text">
              Contact form placeholder
            </h2>
            <p className="mt-3 text-sm text-text-muted">
              No form submission backend is included. Use the email links on the
              About page or the repository for direct contact.
            </p>
            <form className="mt-6 space-y-4" aria-label="Contact form placeholder">
              <div>
                <label htmlFor="name" className="mb-2 block text-sm font-medium text-text">
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
                <label htmlFor="email" className="mb-2 block text-sm font-medium text-text">
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
                <label htmlFor="message" className="mb-2 block text-sm font-medium text-text">
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
              <h2 className="font-serif text-xl font-semibold text-text">Repository</h2>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                Scientific source code, reports, and data documentation live in the
                project repository.
              </p>
              <a
                href={githubRepoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-flex text-sm font-medium text-primary hover:text-primary-light"
              >
                Open GitHub repository ↗
              </a>
            </article>
            <article className="rounded-xl border border-border bg-surface-elevated p-6">
              <h2 className="font-serif text-xl font-semibold text-text">Researcher profile</h2>
              <p className="mt-3 text-sm leading-relaxed text-text-muted">
                Academic background, supervision, and professional links are available on
                the About page.
              </p>
              <Button href="/about" variant="outline" className="mt-4">
                View About page
              </Button>
            </article>
          </div>
        </div>
      </Section>
    </>
  );
}
