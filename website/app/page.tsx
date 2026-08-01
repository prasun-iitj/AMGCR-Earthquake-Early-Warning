import type { Metadata } from "next";
import { HeroSection } from "@/components/home/HeroSection";
import { ProjectHighlights } from "@/components/home/ProjectHighlights";
import { WorkflowPreview } from "@/components/home/WorkflowPreview";
import { RepositoryStatistics } from "@/components/home/RepositoryStatistics";
import { TimelinePreview } from "@/components/home/TimelinePreview";
import { FeaturedDownloads } from "@/components/home/FeaturedDownloads";
import { getRepositoryStats } from "@/lib/content/stats";
import { heroContent } from "@/lib/home/content";
import { heroSlides } from "@/lib/home/hero-slides";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "Home",
  description: heroContent.description,
  path: "/",
});

export default function HomePage() {
  const stats = getRepositoryStats();

  return (
    <>
      <link rel="preload" as="image" href={heroSlides[0]?.src ?? "/hero/slide-1.png"} />
      <HeroSection />
      <ProjectHighlights />
      <WorkflowPreview />
      <RepositoryStatistics stats={stats} />
      <TimelinePreview />
      <FeaturedDownloads />
    </>
  );
}
