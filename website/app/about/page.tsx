import type { Metadata } from "next";
import { AboutProfilePage } from "@/components/about/AboutProfilePage";
import { buildPageMetadata } from "@/lib/seo/metadata";

export const metadata: Metadata = buildPageMetadata({
  title: "About",
  description:
    "Researcher profile — Prasun Kumar Tripathi, M.Tech AI at IIT Jodhpur (AIDE). AMGCR, an IIT Jodhpur major research project, with its academic association with the Swiss Certificate Programme.",
  path: "/about",
});

export default function AboutPage() {
  return <AboutProfilePage />;
}
