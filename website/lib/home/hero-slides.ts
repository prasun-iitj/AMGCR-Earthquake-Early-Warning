/**
 * Hero slides — user-provided earthquake / seismic / research PNGs in website/public/hero/
 * Files: slide-1.png … slide-5.png (numbered to match source image names)
 */
export type HeroSlide = {
  id: string;
  src: string;
  alt: string;
  credit: string;
};

export const heroSlides: HeroSlide[] = [
  {
    id: "earth-from-space",
    src: "/hero/slide-1.png",
    alt: "Earth viewed from orbit with a satellite — global geophysical monitoring",
    credit: "Project imagery",
  },
  {
    id: "seismic-station",
    src: "/hero/slide-2.png",
    alt: "Remote seismic monitoring station with solar panels near a volcanic landscape",
    credit: "Project imagery",
  },
  {
    id: "seismograph-trace",
    src: "/hero/slide-3.png",
    alt: "Seismograph stylus recording earthquake waveforms on grid paper",
    credit: "Project imagery",
  },
  {
    id: "seismic-waveform",
    src: "/hero/slide-4.png",
    alt: "Abstract seismic waveform visualization — digital signal traces",
    credit: "Project imagery",
  },
  {
    id: "surface-rupture",
    src: "/hero/slide-5.png",
    alt: "Aerial view of earthquake surface rupture displacing railroad tracks",
    credit: "Project imagery",
  },
];

export const heroSlideIntervalMs = 4000;
/** ~30% of interval — keeps crossfade proportional (was 2200ms at 7s) */
export const heroSlideFadeMs = 1200;
/** Zoom spans display + crossfade so motion doesn't freeze before the fade */
export const heroSlideZoomMs = heroSlideIntervalMs + heroSlideFadeMs;
