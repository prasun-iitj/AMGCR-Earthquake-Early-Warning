"use client";

import { motion, useReducedMotion } from "framer-motion";
import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/Button";
import { HeroBackgroundSlide } from "@/components/home/HeroBackgroundSlide";
import { heroContent } from "@/lib/home/content";
import {
  heroSlideFadeMs,
  heroSlideIntervalMs,
  heroSlideZoomMs,
  heroSlides,
} from "@/lib/home/hero-slides";

export function HeroSection() {
  const shouldReduceMotion = useReducedMotion();
  const [activeSlide, setActiveSlide] = useState(0);

  useEffect(() => {
    if (shouldReduceMotion || heroSlides.length <= 1) {
      return;
    }

    const interval = window.setInterval(() => {
      setActiveSlide((current) => (current + 1) % heroSlides.length);
    }, heroSlideIntervalMs);

    return () => window.clearInterval(interval);
  }, [shouldReduceMotion]);

  const scrollToContent = useCallback(() => {
    window.scrollTo({
      top: window.innerHeight * 0.92,
      behavior: shouldReduceMotion ? "auto" : "smooth",
    });
  }, [shouldReduceMotion]);

  const fadeDuration = shouldReduceMotion ? 0 : 0.8;
  const slideTransitionMs = shouldReduceMotion ? 0 : heroSlideFadeMs;

  return (
    <section className="relative flex min-h-[88vh] items-center overflow-hidden border-b border-primary-light/20 md:min-h-[92vh]">
      {/* Background slideshow — HD images from /public/hero/ */}
      <div aria-hidden="true" className="absolute inset-0 overflow-hidden bg-primary">
        {heroSlides.map((slide, index) => (
          <HeroBackgroundSlide
            key={slide.id}
            src={slide.src}
            isActive={index === activeSlide}
            fadeMs={slideTransitionMs}
            zoomDurationMs={heroSlideZoomMs}
            reduceMotion={!!shouldReduceMotion}
          />
        ))}
      </div>

      {/* Cinematic overlay for text readability */}
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-gradient-to-r from-primary/88 via-primary/62 to-primary/72"
      />
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-gradient-to-t from-primary/85 via-transparent to-primary/40"
      />
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(196,92,38,0.12),transparent_55%)]"
      />

      {/* Content */}
      <div className="relative z-10 mx-auto w-full max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
        <div className="max-w-4xl">
          <motion.p
            initial={shouldReduceMotion ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: fadeDuration, delay: shouldReduceMotion ? 0 : 0.15 }}
            className="mb-4 text-sm font-semibold uppercase tracking-wider text-white/85"
          >
            {heroContent.eyebrow.left} · {heroContent.eyebrow.right}
          </motion.p>

          <motion.h1
            initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: fadeDuration, delay: shouldReduceMotion ? 0 : 0.3 }}
            className="font-serif text-4xl font-semibold leading-tight tracking-tight text-white md:text-5xl lg:text-6xl"
          >
            {heroContent.title}
          </motion.h1>

          <motion.p
            initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: fadeDuration, delay: shouldReduceMotion ? 0 : 0.45 }}
            className="mt-4 text-xl font-medium text-white/92 md:text-2xl"
          >
            {heroContent.subtitle}
          </motion.p>

          <motion.p
            initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: fadeDuration, delay: shouldReduceMotion ? 0 : 0.6 }}
            className="mt-6 max-w-3xl text-lg leading-relaxed text-white/88"
          >
            {heroContent.description}
          </motion.p>

          <motion.div
            initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: fadeDuration, delay: shouldReduceMotion ? 0 : 0.75 }}
            className="mt-10 flex flex-col gap-3 sm:flex-row"
          >
            <Button href={heroContent.primaryCta.href} variant="primary" size="lg">
              {heroContent.primaryCta.label}
            </Button>
            <Button
              href={heroContent.secondaryCta.href}
              variant="outline"
              size="lg"
              className="border-white/35 bg-white/5 text-white backdrop-blur-sm hover:border-white/55 hover:bg-white/12 hover:text-white"
            >
              {heroContent.secondaryCta.label}
            </Button>
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.button
        type="button"
        onClick={scrollToContent}
        initial={shouldReduceMotion ? false : { opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: fadeDuration, delay: shouldReduceMotion ? 0 : 1.1 }}
        className="absolute bottom-8 left-1/2 z-10 flex -translate-x-1/2 flex-col items-center gap-2 text-white/70 transition-colors hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40 focus-visible:ring-offset-2 focus-visible:ring-offset-transparent"
        aria-label="Scroll to explore project content"
      >
        <span className="text-xs font-medium uppercase tracking-widest">Explore</span>
        <motion.span
          aria-hidden="true"
          animate={shouldReduceMotion ? undefined : { y: [0, 6, 0] }}
          transition={
            shouldReduceMotion
              ? undefined
              : { duration: 1.8, repeat: Infinity, ease: "easeInOut" }
          }
          className="flex h-10 w-6 items-start justify-center rounded-full border border-white/40 p-1.5"
        >
          <span className="block h-2 w-1 rounded-full bg-white/80" />
        </motion.span>
      </motion.button>

      {/* Screen-reader slide context (decorative backgrounds) */}
      <p className="sr-only">
        Background imagery cycles through seismic research visuals:{" "}
        {heroSlides.map((slide) => slide.alt).join("; ")}
      </p>
    </section>
  );
}
