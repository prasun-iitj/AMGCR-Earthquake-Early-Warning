import type { Metadata } from "next";
import { DocView } from "@/components/content/DocView";
import { researchReport } from "@/lib/content/documents";
import { loadDocument } from "@/lib/content/loader";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: researchReport.title,
  description: researchReport.description,
  path: "/research/report",
});

export default function ResearchReportPage() {
  const document = loadDocument(researchReport);

  return (
    <DocView
      document={document}
      breadcrumbs={[
        { label: "Home", href: "/" },
        { label: "Research", href: "/research" },
        { label: document.title },
      ]}
    />
  );
}
