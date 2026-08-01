import type { ReactNode } from "react";
import { Breadcrumbs, type BreadcrumbItem } from "@/components/content/Breadcrumbs";

type PageHeaderProps = {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  breadcrumbs?: BreadcrumbItem[];
  children?: ReactNode;
};

/** Blue band header used on inner pages (dashboard, resources, etc.). */
export function PageHeader({
  eyebrow,
  title,
  subtitle,
  breadcrumbs,
  children,
}: PageHeaderProps) {
  return (
    <section className="border-b border-border bg-primary py-12 text-white md:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {breadcrumbs && breadcrumbs.length > 0 ? (
          <div className="[&_nav_a]:text-white/80 [&_nav_a:hover]:text-white [&_nav_ol]:text-white/70 [&_nav_span]:text-white">
            <Breadcrumbs items={breadcrumbs} />
          </div>
        ) : null}
        {eyebrow ? (
          <p className="mt-2 text-sm font-semibold uppercase tracking-wider text-white/80">
            {eyebrow}
          </p>
        ) : null}
        <h1 className="mt-2 font-serif text-3xl font-semibold tracking-tight md:text-4xl">
          {title}
        </h1>
        {subtitle ? (
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-white/85">
            {subtitle}
          </p>
        ) : null}
        {children}
      </div>
    </section>
  );
}
