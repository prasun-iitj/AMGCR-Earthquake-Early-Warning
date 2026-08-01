import type { Metadata } from "next";
import { DocView } from "@/components/content/DocView";
import { researchReport } from "@/lib/content/documents";
import { loadDocument } from "@/lib/content/loader";

export const metadata: Metadata = {
  title: researchReport.title,
  description: researchReport.description,
};

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
