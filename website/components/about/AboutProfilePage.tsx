import Link from "next/link";
import type { ReactNode } from "react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import {
  academicSupervisor,
  acknowledgements,
  researchArea,
  researchInterests,
  researchProject,
  researchTimeline,
  researcher,
  researcherBio,
  technologiesUsed,
} from "@/lib/about/profile";
import { githubRepoUrl } from "@/lib/content/paths";
import { siteConfig } from "@/lib/navigation";

function IconLinkedIn() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

function IconGitHub() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor">
      <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
    </svg>
  );
}

function IconEmail() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.75">
      <path d="M4 6h16v12H4z" strokeLinejoin="round" />
      <path d="M4 7l8 6 8-6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconWeb() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.75">
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18M12 3a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" strokeLinecap="round" />
    </svg>
  );
}

function ProfileLink({
  href,
  label,
  icon,
  external = true,
}: {
  href: string;
  label: string;
  icon: ReactNode;
  external?: boolean;
}) {
  const className =
    "inline-flex items-center gap-2 rounded-lg border border-border bg-surface px-3 py-2 text-sm font-medium text-text transition-colors hover:border-primary/30 hover:text-primary";

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={className}>
        {icon}
        {label}
      </a>
    );
  }

  return (
    <Link href={href} className={className}>
      {icon}
      {label}
    </Link>
  );
}

export function AboutProfilePage() {
  return (
    <>
      <PageHeader
        breadcrumbs={[
          { label: "Home", href: "/" },
          { label: "About" },
        ]}
        eyebrow="About"
        title="Researcher profile"
        subtitle="Academic background, research focus, and supervision for the AMGCR earthquake early warning programme."
      />

      {/* Profile card + IIT Jodhpur branding */}
      <Section className="py-12 md:py-16">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,340px)_1fr] lg:items-start">
          <aside className="rounded-2xl border border-border bg-surface-elevated p-6 shadow-sm lg:sticky lg:top-24">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-3 py-1.5">
              <span
                aria-hidden="true"
                className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-white"
              >
                IIT
              </span>
              <span className="text-xs font-semibold uppercase tracking-wider text-primary">
                {researcher.instituteShort} · AIDE
              </span>
            </div>

            <div className="mx-auto mb-5 flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br from-primary/15 to-primary/5 ring-2 ring-primary/15">
              <span className="font-serif text-3xl font-semibold text-primary">
                {researcher.name
                  .split(" ")
                  .map((part) => part[0])
                  .join("")
                  .slice(0, 2)}
              </span>
            </div>

            <h2 className="text-center font-serif text-2xl font-semibold text-text">
              {researcher.name}
            </h2>
            <p className="mt-1 text-center text-sm text-text-muted">
              {researcher.program}
            </p>
            <p className="mt-1 text-center font-mono text-xs text-text-muted">
              {researcher.rollNumber}
            </p>

            <dl className="mt-6 space-y-3 border-t border-border pt-6 text-sm">
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  Institute
                </dt>
                <dd className="mt-1 text-text">{researcher.institute}</dd>
              </div>
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  Department
                </dt>
                <dd className="mt-1 text-text">{researcher.department}</dd>
              </div>
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  Research area
                </dt>
                <dd className="mt-1 leading-relaxed text-text-muted">{researchArea}</dd>
              </div>
            </dl>

            <div className="mt-6 flex flex-col gap-2 border-t border-border pt-6">
              <ProfileLink
                href={`mailto:${researcher.instituteEmail}`}
                label="Institute email"
                icon={<IconEmail />}
                external={false}
              />
              <ProfileLink
                href={`mailto:${researcher.personalEmail}`}
                label="Personal email"
                icon={<IconEmail />}
                external={false}
              />
              <ProfileLink
                href={researcher.linkedIn}
                label="LinkedIn"
                icon={<IconLinkedIn />}
              />
              <ProfileLink
                href={researcher.github}
                label="GitHub"
                icon={<IconGitHub />}
              />
            </div>
          </aside>

          <div className="min-w-0 space-y-12">
            <section id="about-researcher" aria-labelledby="about-researcher-heading">
              <h2
                id="about-researcher-heading"
                className="font-serif text-2xl font-semibold text-text md:text-3xl"
              >
                1. About the Researcher
              </h2>
              <div className="mt-4 space-y-4 text-base leading-relaxed text-text-muted">
                {researcherBio.map((paragraph) => (
                  <p key={paragraph.slice(0, 40)}>{paragraph}</p>
                ))}
              </div>
            </section>

            <section id="research-interests" aria-labelledby="research-interests-heading">
              <h2
                id="research-interests-heading"
                className="font-serif text-2xl font-semibold text-text md:text-3xl"
              >
                2. Research Interests
              </h2>
              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                {researchInterests.map((item) => (
                  <article
                    key={item.title}
                    className="rounded-xl border border-border bg-surface-elevated p-5"
                  >
                    <h3 className="font-serif text-lg font-semibold text-text">
                      {item.title}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-text-muted">
                      {item.description}
                    </p>
                  </article>
                ))}
              </div>
            </section>

            <section id="research-project" aria-labelledby="research-project-heading">
              <h2
                id="research-project-heading"
                className="font-serif text-2xl font-semibold text-text md:text-3xl"
              >
                3. Research Project
              </h2>
              <div className="mt-4 rounded-xl border border-border bg-surface-elevated p-6">
                <h3 className="font-serif text-xl font-semibold text-text">
                  {researchProject.title}
                </h3>
                <p className="mt-3 leading-relaxed text-text-muted">
                  {researchProject.summary}
                </p>
                <ul className="mt-5 space-y-2 border-t border-border pt-5">
                  {researchProject.highlights.map((item) => (
                    <li
                      key={item}
                      className="flex gap-2 text-sm leading-relaxed text-text-muted"
                    >
                      <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
                      {item}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/research"
                  className="mt-6 inline-flex text-sm font-medium text-primary hover:text-primary-light"
                >
                  Explore research portal →
                </Link>
              </div>
            </section>

            <section id="academic-supervision" aria-labelledby="academic-supervision-heading">
              <h2
                id="academic-supervision-heading"
                className="font-serif text-2xl font-semibold text-text md:text-3xl"
              >
                4. Academic Supervision
              </h2>
              <div className="mt-4 rounded-xl border border-primary/20 bg-primary/5 p-6">
                <p className="text-sm leading-relaxed text-text-muted">
                  This research project is carried out under the guidance of{" "}
                  <a
                    href={academicSupervisor.profileUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium text-primary hover:text-primary-light"
                  >
                    {academicSupervisor.name}
                  </a>
                  .
                </p>
                <dl className="mt-5 space-y-3 text-sm">
                  <div>
                    <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                      Designation
                    </dt>
                    <dd className="mt-1 text-text">{academicSupervisor.designation}</dd>
                  </div>
                  <div>
                    <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                      Department
                    </dt>
                    <dd className="mt-1 text-text">{academicSupervisor.department}</dd>
                  </div>
                  <div>
                    <dt className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                      Research interests
                    </dt>
                    <dd className="mt-2">
                      <ul className="space-y-1.5 text-text-muted">
                        {academicSupervisor.researchInterests.map((interest) => (
                          <li key={interest} className="flex gap-2">
                            <span aria-hidden="true" className="text-primary">
                              ·
                            </span>
                            {interest}
                          </li>
                        ))}
                      </ul>
                    </dd>
                  </div>
                </dl>
                <article className="mt-6 rounded-xl border border-border bg-surface-elevated p-5 shadow-sm">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                    Faculty profile
                  </h3>
                  <div className="mt-3">
                    <ProfileLink
                      href={academicSupervisor.profileUrl}
                      label="Official faculty website"
                      icon={<IconWeb />}
                    />
                  </div>
                  <a
                    href={academicSupervisor.profileUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-3 inline-flex items-center gap-2 break-all text-sm font-medium text-primary hover:text-primary-light"
                  >
                    <IconWeb />
                    {academicSupervisor.profileUrl.replace(/^https:\/\//, "")} ↗
                  </a>
                </article>
              </div>
            </section>

            <section id="contact-profiles" aria-labelledby="contact-profiles-heading">
              <h2
                id="contact-profiles-heading"
                className="font-serif text-2xl font-semibold text-text md:text-3xl"
              >
                5. Contact &amp; Professional Profiles
              </h2>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <article className="rounded-xl border border-border bg-surface-elevated p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                    Institute contact
                  </h3>
                  <a
                    href={`mailto:${researcher.instituteEmail}`}
                    className="mt-2 inline-flex items-center gap-2 text-primary hover:text-primary-light"
                  >
                    <IconEmail />
                    {researcher.instituteEmail}
                  </a>
                </article>
                <article className="rounded-xl border border-border bg-surface-elevated p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                    Personal contact
                  </h3>
                  <a
                    href={`mailto:${researcher.personalEmail}`}
                    className="mt-2 inline-flex items-center gap-2 text-primary hover:text-primary-light"
                  >
                    <IconEmail />
                    {researcher.personalEmail}
                  </a>
                </article>
                <article className="rounded-xl border border-border bg-surface-elevated p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                    LinkedIn
                  </h3>
                  <a
                    href={researcher.linkedIn}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 inline-flex items-center gap-2 text-primary hover:text-primary-light"
                  >
                    <IconLinkedIn />
                    Professional profile ↗
                  </a>
                </article>
                <article className="rounded-xl border border-border bg-surface-elevated p-5">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
                    GitHub
                  </h3>
                  <a
                    href={researcher.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 inline-flex items-center gap-2 text-primary hover:text-primary-light"
                  >
                    <IconGitHub />
                    @prasun-iitj ↗
                  </a>
                </article>
              </div>
            </section>

            <section id="acknowledgements" aria-labelledby="acknowledgements-heading">
              <h2
                id="acknowledgements-heading"
                className="font-serif text-2xl font-semibold text-text md:text-3xl"
              >
                6. Acknowledgements
              </h2>
              <ul className="mt-4 space-y-3">
                {acknowledgements.map((item) => (
                  <li
                    key={item.slice(0, 48)}
                    className="flex gap-3 text-sm leading-relaxed text-text-muted"
                  >
                    <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {item}
                  </li>
                ))}
              </ul>
            </section>
          </div>
        </div>
      </Section>

      <Section variant="muted" title="Research timeline" eyebrow="Timeline">
        <ol className="relative mx-auto max-w-3xl">
          {researchTimeline.map((step, index) => (
            <li key={step.label} className="relative flex gap-4 pb-10 last:pb-0">
              {index < researchTimeline.length - 1 && (
                <span
                  aria-hidden="true"
                  className="absolute left-[15px] top-8 h-[calc(100%-1rem)] w-px bg-border"
                />
              )}
              <span
                className={[
                  "relative z-10 mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-xs font-semibold",
                  step.status === "complete"
                    ? "border-success bg-success/10 text-success"
                    : "border-accent bg-accent/10 text-accent",
                ].join(" ")}
              >
                {index + 1}
              </span>
              <div className="min-w-0 pt-0.5">
                <h3 className="font-serif text-lg font-semibold text-text">
                  {step.label}
                </h3>
                <p className="mt-1 text-sm text-text-muted">{step.detail}</p>
              </div>
            </li>
          ))}
        </ol>
      </Section>

      <Section title="Technologies & platform" eyebrow="Stack">
        <div className="grid gap-8 lg:grid-cols-2">
          <div>
            <h3 className="font-serif text-xl font-semibold text-text">
              Technologies used
            </h3>
            <ul className="mt-4 flex flex-wrap gap-2">
              {technologiesUsed.map((tech) => (
                <li
                  key={tech}
                  className="rounded-full border border-border bg-surface-elevated px-3 py-1.5 text-sm text-text-muted"
                >
                  {tech}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-xl border border-border bg-surface-elevated p-6">
            <h3 className="font-serif text-xl font-semibold text-text">
              Current version &amp; repository
            </h3>
            <dl className="mt-4 space-y-3 text-sm">
              <div className="flex justify-between gap-4 border-b border-border pb-3">
                <dt className="text-text-muted">Platform version</dt>
                <dd className="font-mono font-medium text-text">v{siteConfig.version}</dd>
              </div>
              <div className="flex justify-between gap-4 border-b border-border pb-3">
                <dt className="text-text-muted">Science release</dt>
                <dd className="font-mono font-medium text-text">
                  v{siteConfig.scienceVersion}
                </dd>
              </div>
            </dl>
            <a
              href={githubRepoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-5 inline-flex items-center gap-2 text-sm font-medium text-primary hover:text-primary-light"
            >
              <IconGitHub />
              AMGCR research repository ↗
            </a>
          </div>
        </div>
      </Section>
    </>
  );
}
