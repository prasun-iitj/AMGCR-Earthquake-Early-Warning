import type { Metadata } from "next";
import {
  GithubLinks,
  GithubOverview,
  GithubSiteLinks,
  GithubStructure,
} from "@/components/github/GithubPageSections";
import { loadGithubPage } from "@/lib/github/loader";

export const metadata: Metadata = {
  title: "GitHub Integration",
  description:
    "Repository overview, release information, structure, and direct links to GitHub — static configuration, no authentication required.",
};

export default function GithubPage() {
  const data = loadGithubPage();

  return (
    <>
      <GithubOverview data={data} />
      <GithubLinks links={data.quickLinks} />
      <GithubStructure structure={data.structure} stats={data.stats} />
      <GithubSiteLinks urls={data.urls} />
    </>
  );
}
