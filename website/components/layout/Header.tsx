"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { isNavItemActive, mobileNavSections } from "@/lib/navigation-utils";
import { mainNav, siteConfig } from "@/lib/navigation";

const GlobalSearch = dynamic(
  () => import("@/components/search/GlobalSearch").then((mod) => mod.GlobalSearch),
  { ssr: false },
);

function cn(...classes: Array<string | undefined | false>) {
  return classes.filter(Boolean).join(" ");
}

/** Width (px) from which the inline desktop navigation is used. Below it the menu button is shown. */
const DESKTOP_NAV_QUERY = "(min-width: 1280px)";

const desktopLinkClass =
  "whitespace-nowrap rounded-lg px-2 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 2xl:px-3";

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef<HTMLLIElement>(null);
  const moreButtonRef = useRef<HTMLButtonElement>(null);

  const primaryNav = mainNav.filter((item) => item.primary);
  const moreNav = mainNav.filter((item) => !item.primary);
  const moreActive = moreNav.some((item) => isNavItemActive(pathname, item.href));

  useEffect(() => {
    document.body.style.overflow = mobileOpen || searchOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen, searchOpen]);

  // Close the mobile menu when the viewport grows into the desktop layout.
  useEffect(() => {
    const media = window.matchMedia(DESKTOP_NAV_QUERY);
    const onChange = (event: MediaQueryListEvent) => {
      if (event.matches) {
        setMobileOpen(false);
      }
    };
    media.addEventListener("change", onChange);
    return () => media.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMobileOpen(false);
        setSearchOpen(false);
        setMoreOpen((open) => {
          if (open) {
            moreButtonRef.current?.focus();
          }
          return false;
        });
        return;
      }

      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setSearchOpen((open) => !open);
      }
    };

    const onPointerDown = (event: MouseEvent) => {
      if (moreRef.current && !moreRef.current.contains(event.target as Node)) {
        setMoreOpen(false);
      }
    };

    window.addEventListener("keydown", onKeyDown);
    document.addEventListener("mousedown", onPointerDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      document.removeEventListener("mousedown", onPointerDown);
    };
  }, []);

  const openSearch = () => setSearchOpen(true);
  const closeSearch = () => setSearchOpen(false);

  return (
    <>
      <header className="sticky top-0 z-50 border-b border-border bg-surface-elevated text-text shadow-sm backdrop-blur supports-[backdrop-filter]:bg-surface-elevated/95">
        <div className="mx-auto flex min-h-16 max-w-[1600px] items-center gap-4 px-4 py-2 sm:px-5 xl:px-6">
          {/* Identity: dedicated, non-shrinking area */}
          <Link
            href="/"
            className="group shrink-0 rounded-md transition-colors hover:text-primary-light focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
            aria-label={`${siteConfig.name} — home`}
          >
            {siteConfig.nameLines.map((line) => (
              <span
                key={line}
                className="block whitespace-nowrap font-serif text-sm font-semibold leading-tight text-primary sm:text-base xl:text-[1.05rem]"
              >
                {line}
              </span>
            ))}
            <span className="mt-0.5 hidden whitespace-nowrap text-xs text-text-muted sm:block">
              {siteConfig.tagline} · v{siteConfig.version}
            </span>
          </Link>

          {/* Navigation: only from 1280px; centred in the space between identity and controls */}
          <nav
            aria-label="Main navigation"
            className="hidden min-w-0 flex-1 items-center justify-center xl:flex"
          >
            <ul className="flex items-center gap-0.5 2xl:gap-1">
              {primaryNav.map((item) => {
                const isActive = isNavItemActive(pathname, item.href);

                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={cn(
                        desktopLinkClass,
                        isActive
                          ? "bg-primary/10 text-primary"
                          : "text-text hover:bg-surface hover:text-primary",
                      )}
                      aria-current={isActive ? "page" : undefined}
                    >
                      {item.shortLabel ? (
                        <>
                          <span className="2xl:hidden">{item.shortLabel}</span>
                          <span className="hidden 2xl:inline">{item.label}</span>
                        </>
                      ) : (
                        item.label
                      )}
                    </Link>
                  </li>
                );
              })}

              <li
                className="relative"
                ref={moreRef}
                onBlur={(event) => {
                  if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
                    setMoreOpen(false);
                  }
                }}
              >
                <button
                  ref={moreButtonRef}
                  type="button"
                  onClick={() => setMoreOpen((open) => !open)}
                  aria-expanded={moreOpen}
                  aria-controls="more-navigation"
                  className={cn(
                    desktopLinkClass,
                    "inline-flex items-center gap-1",
                    moreActive || moreOpen
                      ? "bg-primary/10 text-primary"
                      : "text-text hover:bg-surface hover:text-primary",
                  )}
                >
                  More
                  <svg
                    aria-hidden="true"
                    viewBox="0 0 20 20"
                    className={cn("h-3.5 w-3.5 transition-transform", moreOpen && "rotate-180")}
                    fill="currentColor"
                  >
                    <path d="M5.5 7.5l4.5 5 4.5-5z" />
                  </svg>
                </button>
                {moreOpen ? (
                  <ul
                    id="more-navigation"
                    className="absolute right-0 top-full z-50 mt-2 w-52 rounded-xl border border-border bg-surface-elevated p-1.5 shadow-lg"
                  >
                    {moreNav.map((item) => {
                      const isActive = isNavItemActive(pathname, item.href);
                      return (
                        <li key={item.href}>
                          <Link
                            href={item.href}
                            onClick={() => setMoreOpen(false)}
                            className={cn(
                              "block whitespace-nowrap rounded-lg px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40",
                              isActive
                                ? "bg-primary/10 text-primary"
                                : "text-text hover:bg-surface hover:text-primary",
                            )}
                            aria-current={isActive ? "page" : undefined}
                          >
                            {item.label}
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                ) : null}
              </li>
            </ul>
          </nav>

          {/* Controls: search and menu button, never overlapping the navigation */}
          <div className="ml-auto flex shrink-0 items-center gap-2 xl:ml-0">
            <button
              type="button"
              onClick={openSearch}
              className="hidden items-center gap-2 rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-muted transition-colors hover:border-primary/30 hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 sm:inline-flex"
              aria-label="Open search"
            >
              <span>Search</span>
              <kbd className="hidden rounded border border-border px-1.5 py-0.5 text-[0.65rem] 2xl:inline">
                Ctrl K
              </kbd>
            </button>

            <button
              type="button"
              onClick={openSearch}
              className="inline-flex h-11 w-11 items-center justify-center rounded-lg border border-border text-text-muted transition-colors hover:bg-surface hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 sm:hidden"
              aria-label="Open search"
            >
              <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="7" />
                <path d="M20 20l-3-3" strokeLinecap="round" />
              </svg>
            </button>

            <button
              type="button"
              className="inline-flex h-11 w-11 items-center justify-center rounded-lg border border-border bg-surface text-text transition-colors hover:border-primary/40 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 xl:hidden"
              aria-expanded={mobileOpen}
              aria-controls="mobile-navigation"
              aria-label={mobileOpen ? "Close menu" : "Open menu"}
              onClick={() => setMobileOpen((open) => !open)}
            >
              <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
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
            className="max-h-[calc(100dvh-4rem)] overflow-y-auto border-t border-border bg-surface-elevated xl:hidden"
          >
            <div className="mx-auto max-w-[1600px] space-y-6 px-4 py-4 sm:px-5">
              <button
                type="button"
                onClick={() => {
                  setMobileOpen(false);
                  openSearch();
                }}
                className="flex min-h-11 w-full items-center justify-between rounded-lg border border-border bg-surface px-3 py-3 text-left text-sm font-medium text-text"
              >
                <span>Search documentation</span>
                <span className="text-xs text-text-muted">Ctrl K</span>
              </button>

              {mobileNavSections.map((section) => (
                <div key={section.label}>
                  <p className="px-3 text-xs font-semibold uppercase tracking-wider text-text-muted">
                    {section.label}
                  </p>
                  <ul className="mt-2 space-y-1">
                    {section.items.map((item) => {
                      const isActive = isNavItemActive(pathname, item.href);
                      return (
                        <li key={item.href}>
                          <Link
                            href={item.href}
                            onClick={() => setMobileOpen(false)}
                            className={cn(
                              "block min-h-11 rounded-lg px-3 py-3 text-base font-medium transition-colors",
                              isActive
                                ? "bg-primary/10 text-primary"
                                : "text-text-muted hover:bg-surface hover:text-text",
                            )}
                            aria-current={isActive ? "page" : undefined}
                          >
                            {item.label}
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
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
