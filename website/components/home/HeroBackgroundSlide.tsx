"use client";

import { memo, useEffect, useRef } from "react";

type HeroBackgroundSlideProps = {
  src: string;
  isActive: boolean;
  fadeMs: number;
  zoomDurationMs: number;
  reduceMotion: boolean;
};

const MAX_ZOOM = 1.1;

/**
 * Ken Burns zoom that keeps moving through the crossfade and holds
 * the final scale — avoids the snap-back bug from CSS animation reset.
 * Scale is driven via --hero-scale on the DOM (rAF), not React state.
 */
function HeroBackgroundSlideComponent({
  src,
  isActive,
  fadeMs,
  zoomDurationMs,
  reduceMotion,
}: HeroBackgroundSlideProps) {
  const imgRef = useRef<HTMLImageElement>(null);
  const frameRef = useRef(0);

  useEffect(() => {
    const img = imgRef.current;
    if (!img || reduceMotion) {
      if (img && reduceMotion) {
        img.style.setProperty("--hero-scale", "1");
      }
      return;
    }

    if (!isActive) {
      // Keep current scale and let any in-flight zoom finish during fade-out.
      return;
    }

    cancelAnimationFrame(frameRef.current);
    img.style.setProperty("--hero-scale", "1");
    const start = performance.now();

    const tick = (now: number) => {
      const progress = Math.min((now - start) / zoomDurationMs, 1);
      const eased = 1 - (1 - progress) ** 2;
      const scale = 1 + eased * (MAX_ZOOM - 1);
      img.style.setProperty("--hero-scale", String(scale));

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(tick);
      }
    };

    frameRef.current = requestAnimationFrame(tick);
  }, [isActive, reduceMotion, zoomDurationMs]);

  useEffect(
    () => () => {
      cancelAnimationFrame(frameRef.current);
    },
    [],
  );

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      ref={imgRef}
      src={src}
      alt=""
      decoding="async"
      loading={isActive ? "eager" : "lazy"}
      fetchPriority={isActive ? "high" : "auto"}
      className="absolute inset-0 h-full w-full object-cover will-change-[transform,opacity]"
      style={{
        opacity: isActive ? 1 : 0,
        transform: "scale(var(--hero-scale, 1))",
        transitionProperty: "opacity",
        transitionDuration: `${fadeMs}ms`,
        transitionTimingFunction: "ease-in-out",
      }}
    />
  );
}

export const HeroBackgroundSlide = memo(HeroBackgroundSlideComponent);
