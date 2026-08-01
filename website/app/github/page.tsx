import type { Metadata } from "next";
import {
  GithubLinks,
  GithubOverview,
  GithubSiteLinks,
  GithubStructure,
} from "@/components/github/GithubPageSections";
import { loadGithubPage } from "@/lib/github/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "GitHub Integration",
  description:
    "Repository overview, release information, structure, and direct links to GitHub — static configuration, no authentication required.",
  path: "/github",
});

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
