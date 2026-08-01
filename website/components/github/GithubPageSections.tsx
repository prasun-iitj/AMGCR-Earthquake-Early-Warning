import Link from "next/link";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import type { LoadedGithubPage } from "@/lib/github/loader";

type GithubOverviewProps = {
  data: LoadedGithubPage;
};

export function GithubOverview({ data }: GithubOverviewProps) {
  const { integration, urls, stats } = data;

  const overviewItems = [
    { label: "Repository", value: integration.fullName },
    { label: "Default branch", value: integration.defaultBranch },
    { label: "Latest release", value: integration.latestRelease },
    { label: "Latest tag", value: integration.latestTag },
    { label: "Release date", value: integration.releaseDate },
    { label: "Website version", value: data.platformVersion },
    { label: "Science version", value: `v${stats.scienceVersion}` },
  ];

  return (
    <section className="border-b border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <Breadcrumbs
          items={[{ label: "Home", href: "/" }, { label: "GitHub Integration" }]}
        />
        <h1 className="font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
          GitHub repository
        </h1>
        <p className="mt-4 max-w-3xl text-lg leading-relaxed text-text-muted">
          {integration.description}
        </p>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {overviewItems.map((item) => (
            <article
              key={item.label}
              className="rounded-xl border border-border bg-surface-elevated px-5 py-4"
            >
              <p className="text-sm font-medium text-text-muted">{item.label}</p>
              <p className="mt-2 font-serif text-xl font-semibold text-primary">
                {item.value}
              </p>
            </article>
          ))}
        </div>

        <div className="mt-8 flex flex-wrap gap-3">
          <a
            href={urls.repository}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-light"
          >
            Open repository ↗
          </a>
          <a
            href={urls.latestRelease}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex rounded-lg border border-border px-4 py-2 text-sm font-medium text-text hover:border-primary/30"
          >
            View {integration.latestTag} release ↗
          </a>
        </div>
      </div>
    </section>
  );
}

type GithubLinksProps = {
  links: LoadedGithubPage["quickLinks"];
};

export function GithubLinks({ links }: GithubLinksProps) {
  return (
    <section className="border-t border-border bg-surface-elevated py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="font-serif text-2xl font-semibold text-text">Direct links</h2>
        <p className="mt-2 max-w-2xl text-text-muted">
          Static links to GitHub surfaces — no authentication or live API polling required.
        </p>
        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-xl border border-border bg-surface p-5 transition-colors hover:border-primary/30"
            >
              <h3 className="font-serif text-lg font-semibold text-text">{link.label}</h3>
              <p className="mt-2 text-sm text-text-muted">{link.description}</p>
              <p className="mt-3 text-sm font-medium text-primary">Open on GitHub ↗</p>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

type GithubStructureProps = {
  structure: LoadedGithubPage["structure"];
  stats: LoadedGithubPage["stats"];
};

export function GithubStructure({ structure, stats }: GithubStructureProps) {
  return (
    <section className="border-t border-border bg-surface py-12 md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="font-serif text-2xl font-semibold text-text">Repository structure</h2>
        <p className="mt-2 text-text-muted">
          Key top-level paths in the research repository · {stats.documentation} docs ·{" "}
          {stats.reports} reports · {stats.figures} figures
        </p>
        <ul className="mt-8 space-y-3">
          {structure.map((entry) => (
            <li key={entry.path}>
              <a
                href={entry.href}
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col gap-1 rounded-xl border border-border bg-surface-elevated p-4 transition-colors hover:border-primary/30 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <p className="font-mono text-sm font-semibold text-text">{entry.name}</p>
                  <p className="mt-1 text-sm text-text-muted">{entry.description}</p>
                </div>
                <span className="text-sm font-medium text-primary">Browse ↗</span>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

type GithubSiteLinksProps = {
  urls: LoadedGithubPage["urls"];
};

export function GithubSiteLinks({ urls }: GithubSiteLinksProps) {
  return (
    <section className="border-t border-border bg-surface-elevated py-8">
      <div className="mx-auto flex max-w-7xl flex-wrap gap-4 px-4 text-sm sm:px-6 lg:px-8">
        <Link href="/docs" className="font-medium text-primary hover:text-primary-light">
          Documentation →
        </Link>
        <Link href="/dashboard" className="font-medium text-primary hover:text-primary-light">
          Research dashboard →
        </Link>
        <Link href="/resources" className="font-medium text-primary hover:text-primary-light">
          Resources →
        </Link>
        <a
          href={urls.tags}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium text-primary hover:text-primary-light"
        >
          All tags on GitHub ↗
        </a>
      </div>
    </section>
  );
}
