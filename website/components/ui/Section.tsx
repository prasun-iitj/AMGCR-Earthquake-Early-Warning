import type { ReactNode } from "react";

type SectionVariant = "default" | "muted" | "accent";

const variantStyles: Record<SectionVariant, string> = {
  default: "bg-surface-elevated",
  muted: "bg-surface",
  accent: "bg-primary text-white",
};

type SectionProps = {
  id?: string;
  title?: string;
  subtitle?: string;
  eyebrow?: string;
  variant?: SectionVariant;
  container?: boolean;
  className?: string;
  children: ReactNode;
};

function cn(...classes: Array<string | undefined | false>) {
  return classes.filter(Boolean).join(" ");
}

export function Section({
  id,
  title,
  subtitle,
  eyebrow,
  variant = "default",
  container = true,
  className,
  children,
}: SectionProps) {
  const isAccent = variant === "accent";

  return (
    <section id={id} className={cn("py-16 md:py-24", variantStyles[variant], className)}>
      <div className={cn(container && "mx-auto max-w-7xl px-4 sm:px-6 lg:px-8")}>
        {(eyebrow || title || subtitle) && (
          <header className="mb-10 max-w-3xl">
            {eyebrow && (
              <p
                className={cn(
                  "mb-3 text-sm font-semibold uppercase tracking-wider",
                  isAccent ? "text-white/80" : "text-accent",
                )}
              >
                {eyebrow}
              </p>
            )}
            {title && (
              <h2
                className={cn(
                  "font-serif text-3xl font-semibold tracking-tight md:text-4xl",
                  isAccent ? "text-white" : "text-text",
                )}
              >
                {title}
              </h2>
            )}
            {subtitle && (
              <p
                className={cn(
                  "mt-4 text-lg leading-relaxed",
                  isAccent ? "text-white/85" : "text-text-muted",
                )}
              >
                {subtitle}
              </p>
            )}
          </header>
        )}
        {children}
      </div>
    </section>
  );
}
