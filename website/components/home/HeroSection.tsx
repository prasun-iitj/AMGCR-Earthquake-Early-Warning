import { Button } from "@/components/ui/Button";
import { heroContent } from "@/lib/home/content";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden border-b border-primary-light/30 bg-primary py-20 md:py-28">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(196,92,38,0.15),transparent_50%)]"
      />
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-white/80">
            {heroContent.eyebrow}
          </p>
          <h1 className="font-serif text-4xl font-semibold leading-tight tracking-tight text-white md:text-5xl lg:text-6xl">
            {heroContent.title}
          </h1>
          <p className="mt-4 text-xl font-medium text-white/90 md:text-2xl">
            {heroContent.subtitle}
          </p>
          <p className="mt-6 max-w-3xl text-lg leading-relaxed text-white/85">
            {heroContent.description}
          </p>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <Button href={heroContent.primaryCta.href} variant="primary" size="lg">
              {heroContent.primaryCta.label}
            </Button>
            <Button
              href={heroContent.secondaryCta.href}
              variant="outline"
              size="lg"
              className="border-white/30 bg-transparent text-white hover:border-white/50 hover:bg-white/10 hover:text-white"
            >
              {heroContent.secondaryCta.label}
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
