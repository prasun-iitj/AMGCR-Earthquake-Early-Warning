import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { mainNav } from "@/lib/navigation";

type ErrorPageShellProps = {
  statusCode: string;
  title: string;
  description: string;
  showRetry?: boolean;
  onRetry?: () => void;
};

export function ErrorPageShell({
  statusCode,
  title,
  description,
  showRetry = false,
  onRetry,
}: ErrorPageShellProps) {
  return (
    <section className="flex min-h-[60vh] items-center py-16 md:py-24">
      <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
        <p className="text-sm font-semibold uppercase tracking-wider text-accent">
          {statusCode}
        </p>
        <h1 className="mt-3 font-serif text-3xl font-semibold tracking-tight text-text md:text-4xl">
          {title}
        </h1>
        <p className="mt-4 text-lg leading-relaxed text-text-muted">{description}</p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button href="/" variant="primary">
            Return home
          </Button>
          {showRetry && onRetry ? (
            <button
              type="button"
              onClick={onRetry}
              className="inline-flex items-center justify-center rounded-lg border border-border bg-surface px-5 py-2.5 text-sm font-medium text-text transition-colors hover:border-primary/30 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30"
            >
              Try again
            </button>
          ) : null}
          <Button href="/resources" variant="outline">
            Browse resources
          </Button>
        </div>
        <nav aria-label="Suggested pages" className="mt-12">
          <p className="text-sm font-medium text-text">Popular destinations</p>
          <ul className="mt-4 flex flex-wrap justify-center gap-2">
            {mainNav.slice(0, 6).map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="rounded-full border border-border bg-surface-elevated px-3 py-1.5 text-sm text-text-muted transition-colors hover:border-primary/30 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30"
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </section>
  );
}
