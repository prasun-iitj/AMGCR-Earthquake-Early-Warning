import Link from "next/link";
import { githubRepoUrl } from "@/lib/content/paths";
import { footerQuickLinks } from "@/lib/navigation-utils";
import { mainNav, siteConfig } from "@/lib/navigation";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-border bg-primary text-white">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
          <div className="lg:col-span-2">
            <p className="font-serif text-lg font-semibold">{siteConfig.name}</p>
            <p className="mt-3 max-w-md text-sm leading-relaxed text-white/75">
              {siteConfig.description}
            </p>
            <p className="mt-4 text-xs text-white/60">
              Platform v{siteConfig.version} · Science v{siteConfig.scienceVersion}
            </p>
            <p className="mt-2 text-xs text-white/60">
              Press <kbd className="rounded border border-white/20 px-1">Ctrl K</kbd> to search
              documentation
            </p>
          </div>

          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-white/80">
              Navigation
            </p>
            <ul className="mt-4 space-y-2">
              {mainNav.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="text-sm text-white/75 transition-colors hover:text-white"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-white/80">
              Quick links
            </p>
            <ul className="mt-4 space-y-2">
              {footerQuickLinks.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="text-sm text-white/75 transition-colors hover:text-white"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 grid gap-6 border-t border-white/15 pt-6 md:grid-cols-2">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-white/80">
              Connect
            </p>
            <ul className="mt-4 space-y-2 text-sm text-white/75">
              <li>
                <Link href="/github" className="transition-colors hover:text-white">
                  GitHub integration
                </Link>
              </li>
              <li>
                <a
                  href={githubRepoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="transition-colors hover:text-white"
                >
                  GitHub repository ↗
                </a>
              </li>
              <li>
                <Link href="/contact" className="transition-colors hover:text-white">
                  Contact
                </Link>
              </li>
              <li>
                <span className="text-white/60">
                  License: Academic research — see repository
                </span>
              </li>
            </ul>
          </div>
          <div className="flex flex-col justify-end text-xs text-white/60 md:text-right">
            <p>
              © {currentYear} {siteConfig.name}. All rights reserved.
            </p>
            <p className="mt-2">
              Repository remains the single source of truth · v{siteConfig.scienceVersion}{" "}
              science freeze
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
