import type { Metadata } from "next";
import { HeroSection } from "@/components/home/HeroSection";
import { ProjectHighlights } from "@/components/home/ProjectHighlights";
import { WorkflowPreview } from "@/components/home/WorkflowPreview";
import { RepositoryStatistics } from "@/components/home/RepositoryStatistics";
import { TimelinePreview } from "@/components/home/TimelinePreview";
import { FeaturedDownloads } from "@/components/home/FeaturedDownloads";
import { getRepositoryStats } from "@/lib/content/stats";
import { heroContent } from "@/lib/home/content";
import { siteConfig } from "@/lib/navigation";

export const metadata: Metadata = {
  title: siteConfig.name,
  description: heroContent.description,
};

export default function HomePage() {
  const stats = getRepositoryStats();

  return (
    <>
      <HeroSection />
      <ProjectHighlights />
      <WorkflowPreview />
      <RepositoryStatistics stats={stats} />
      <TimelinePreview />
      <FeaturedDownloads />
    </>
  );
}
