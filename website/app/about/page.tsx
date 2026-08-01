import type { Metadata } from "next";
import { AboutProfilePage } from "@/components/about/AboutProfilePage";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "About",
  description:
    "Researcher profile — Prasun Kumar Tripathi, M.Tech AI at IIT Jodhpur (AIDE). AMGCR earthquake early warning research.",
  path: "/about",
});

export default function AboutPage() {
  return <AboutProfilePage />;
}
