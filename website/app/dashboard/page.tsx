import type { Metadata } from "next";
import { Breadcrumbs } from "@/components/content/Breadcrumbs";
import { DatasetMetricsSection } from "@/components/dashboard/DatasetMetricsSection";
import { PipelineProgressSection } from "@/components/dashboard/PipelineProgressSection";
import { ProjectTimelineSection } from "@/components/dashboard/ProjectTimelineSection";
import { QuickNavigationSection } from "@/components/dashboard/QuickNavigationSection";
import { RepositoryMetricsSection } from "@/components/dashboard/RepositoryMetricsSection";
import { ResearchSummarySection } from "@/components/dashboard/ResearchSummarySection";
import { loadDashboard } from "@/lib/dashboard/loader";

export const metadata: Metadata = {
  title: "Research Dashboard",
  description:
    "High-level overview of AMGCR earthquake research — dataset metrics, repository inventory, pipeline progress, and quick navigation.",
};

export default function DashboardPage() {
  const dashboard = loadDashboard();

  return (
    <>
      <section className="border-b border-border bg-primary py-12 text-white md:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="[&_nav_a]:text-white/80 [&_nav_a:hover]:text-white [&_nav_ol]:text-white/70 [&_nav_span]:text-white">
            <Breadcrumbs
              items={[
                { label: "Home", href: "/" },
                { label: "Research Dashboard" },
              ]}
            />
          </div>
          <p className="text-sm font-semibold uppercase tracking-wider text-white/80">
            Research dashboard
          </p>
          <h1 className="mt-2 font-serif text-3xl font-semibold tracking-tight md:text-4xl">
            Project overview
          </h1>
          <p className="mt-4 max-w-3xl text-lg leading-relaxed text-white/85">
            A static, build-time summary of the complete AMGCR research project —
            California pilot metrics, repository inventory, pipeline status, and
            navigation to all interactive explorers.
          </p>
          {dashboard.generatedAtUtc ? (
            <p className="mt-4 text-xs text-white/60">
              Dataset summary generated {dashboard.generatedAtUtc.slice(0, 19).replace("T", " ")} UTC
            </p>
          ) : null}
        </div>
      </section>

      <ResearchSummarySection summary={dashboard.summary} />
      <DatasetMetricsSection metrics={dashboard.dataset} />
      <RepositoryMetricsSection metrics={dashboard.repository} />
      <PipelineProgressSection phases={dashboard.pipeline} />
      <QuickNavigationSection cards={dashboard.quickNav} />
      <ProjectTimelineSection milestones={dashboard.timeline} />

      <section className="border-t border-border bg-surface py-8">
        <div className="mx-auto max-w-7xl px-4 text-xs text-text-muted sm:px-6 lg:px-8">
          Dashboard data is loaded at build time and designed for future
          ResearchContext integration without component redesign.
        </div>
      </section>
    </>
  );
}
