function cn(...classes: Array<string | undefined | false>) {
  return classes.filter(Boolean).join(" ");
}

type SkeletonProps = {
  className?: string;
};

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "animate-pulse rounded-lg bg-border/60",
        className,
      )}
    />
  );
}

export function PageHeaderSkeleton() {
  return (
    <div
      aria-busy="true"
      aria-label="Loading page"
      className="border-b border-border bg-primary/90 py-12 md:py-16"
    >
      <div className="mx-auto max-w-7xl space-y-4 px-4 sm:px-6 lg:px-8">
        <Skeleton className="h-4 w-32 bg-white/20" />
        <Skeleton className="h-10 w-2/3 max-w-lg bg-white/25" />
        <Skeleton className="h-5 w-full max-w-2xl bg-white/20" />
      </div>
    </div>
  );
}

type SectionSkeletonProps = {
  cards?: number;
  variant?: "default" | "muted";
};

export function SectionSkeleton({ cards = 3, variant = "default" }: SectionSkeletonProps) {
  return (
    <div
      aria-busy="true"
      aria-label="Loading content"
      className={cn(
        "py-16 md:py-24",
        variant === "muted" ? "bg-surface" : "bg-surface-elevated",
      )}
    >
      <div className="mx-auto max-w-7xl space-y-8 px-4 sm:px-6 lg:px-8">
        <div className="space-y-3">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-9 w-1/2 max-w-md" />
          <Skeleton className="h-5 w-full max-w-xl" />
        </div>
        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: cards }).map((_, index) => (
            <Skeleton key={index} className="h-44 w-full" />
          ))}
        </div>
      </div>
    </div>
  );
}

export function CardSkeleton() {
  return <Skeleton className="h-40 w-full rounded-xl" />;
}
