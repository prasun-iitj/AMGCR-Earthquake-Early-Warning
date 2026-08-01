"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { isNavItemActive, mobileNavSections } from "@/lib/navigation-utils";
import { mainNav, siteConfig } from "@/lib/navigation";

const GlobalSearch = dynamic(
  () => import("@/components/search/GlobalSearch").then((mod) => mod.GlobalSearch),
  { ssr: false },
);

function cn(...classes: Array<string | undefined | false>) {
  return classes.filter(Boolean).join(" ");
}

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = mobileOpen || searchOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen, searchOpen]);

  const closeSearch = () => {
    setSearchOpen(false);
  };

  const openSearch = () => {
    setSearchOpen(true);
  };

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMobileOpen(false);
        setSearchOpen(false);
        return;
      }

      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setSearchOpen((open) => !open);
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  return (
    <>
      <header className="sticky top-0 z-50 border-b border-border bg-surface-elevated text-text shadow-sm backdrop-blur supports-[backdrop-filter]:bg-surface-elevated/95">
        <div className="mx-auto flex min-h-16 max-w-[1600px] items-center gap-3 px-4 py-2 sm:px-5 lg:px-6">
          <Link
            href="/"
            className="group shrink-0 transition-colors hover:text-primary-light"
            aria-label={siteConfig.name}
          >
            {siteConfig.nameLines.map((line) => (
              <span
                key={line}
                className="block whitespace-nowrap font-serif text-sm font-semibold leading-tight text-primary sm:text-base lg:text-[1.05rem]"
              >
                {line}
              </span>
            ))}
            <span className="mt-0.5 hidden whitespace-nowrap text-xs text-text-muted sm:block">
              {siteConfig.tagline}
            </span>
          </Link>

          <nav
            aria-label="Main navigation"
            className="hidden min-w-0 flex-1 justify-center lg:flex"
          >
            <div className="flex items-center gap-0.5 xl:gap-1">
              {mainNav.map((item) => {
                const isActive = isNavItemActive(pathname, item.href);

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "rounded-lg px-2 py-2 text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30 xl:px-2.5 xl:text-sm",
                      isActive
                        ? "bg-primary/10 text-primary"
                        : "text-text hover:bg-surface hover:text-primary",
                    )}
                    aria-current={isActive ? "page" : undefined}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </nav>

          <div className="flex shrink-0 items-center gap-2">
            <button
              type="button"
              onClick={openSearch}
              className="hidden items-center gap-2 rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-muted transition-colors hover:border-primary/30 hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30 sm:inline-flex"
              aria-label="Open search"
            >
              <span>Search</span>
              <kbd className="hidden rounded border border-border px-1.5 py-0.5 text-[0.65rem] lg:inline">
                Ctrl K
              </kbd>
            </button>

            <span className="hidden rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-text-muted lg:inline">
              v{siteConfig.version}
            </span>

            <button
              type="button"
              onClick={openSearch}
              className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-border text-text-muted transition-colors hover:bg-surface hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30 sm:hidden"
              aria-label="Open search"
            >
              <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="7" />
                <path d="M20 20l-3-3" strokeLinecap="round" />
              </svg>
            </button>

            <button
              type="button"
              className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-surface text-text transition-colors hover:border-primary/40 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30 lg:hidden"
              aria-expanded={mobileOpen}
              aria-controls="mobile-navigation"
              aria-label={mobileOpen ? "Close menu" : "Open menu"}
              onClick={() => setMobileOpen((open) => !open)}
            >
              <svg
                aria-hidden="true"
                viewBox="0 0 24 24"
                className="h-5 w-5"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                {mobileOpen ? (
                  <path d="M6 6l12 12M18 6L6 18" strokeLinecap="round" />
                ) : (
                  <path d="M4 7h16M4 12h16M4 17h16" strokeLinecap="round" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {mobileOpen ? (
          <nav
            id="mobile-navigation"
            aria-label="Mobile navigation"
            className="max-h-[calc(100vh-4rem)] overflow-y-auto border-t border-border bg-surface-elevated lg:hidden"
          >
            <div className="mx-auto max-w-[1600px] space-y-6 px-4 py-4 sm:px-5">
              <button
                type="button"
                onClick={() => {
                  setMobileOpen(false);
                  openSearch();
                }}
                className="flex w-full items-center justify-between rounded-lg border border-border bg-surface px-3 py-3 text-left text-sm font-medium text-text"
              >
                <span>Search documentation</span>
                <span className="text-xs text-text-muted">Ctrl K</span>
              </button>

              {mobileNavSections.map((section) => (
                <div key={section.label}>
                  <p className="px-3 text-xs font-semibold uppercase tracking-wider text-text-muted">
                    {section.label}
                  </p>
                  <div className="mt-2 space-y-1">
                    {section.items.map((item) => {
                      const isActive = isNavItemActive(pathname, item.href);
                      return (
                        <Link
                          key={item.href}
                          href={item.href}
                          onClick={() => setMobileOpen(false)}
                          className={cn(
                            "block rounded-lg px-3 py-3 text-base font-medium transition-colors",
                            isActive
                              ? "bg-primary/8 text-primary"
                              : "text-text-muted hover:bg-surface hover:text-text",
                          )}
                          aria-current={isActive ? "page" : undefined}
                        >
                          {item.label}
                        </Link>
                      );
                    })}
                  </div>
                </div>
              ))}

              <p className="px-3 text-xs text-text-muted">
                Platform {siteConfig.version} · Science {siteConfig.scienceVersion}
              </p>
            </div>
          </nav>
        ) : null}
      </header>

      <GlobalSearch open={searchOpen} onClose={closeSearch} />
    </>
  );
}
