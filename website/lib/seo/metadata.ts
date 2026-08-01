import type { Metadata } from "next";
import { siteConfig } from "@/lib/navigation";
import { ogImage } from "@/lib/seo/og-image";
import { getSiteUrl } from "@/lib/seo/site-url";

type BuildPageMetadataOptions = {
  title: string;
  description: string;
  path: string;
  noIndex?: boolean;
};

function buildOpenGraphImages() {
  return [
    {
      url: ogImage.path,
      width: ogImage.width,
      height: ogImage.height,
      alt: ogImage.alt,
      type: ogImage.type,
    },
  ];
}

function buildOpenGraph(title: string, description: string, url: string) {
  return {
    title,
    description,
    url,
    siteName: siteConfig.name,
    locale: "en_GB" as const,
    type: "website" as const,
    images: buildOpenGraphImages(),
  };
}

function buildTwitter(title: string, description: string) {
  return {
    card: "summary_large_image" as const,
    title,
    description,
    images: [ogImage.path],
  };
}

/** Root layout defaults — metadataBase, template, OG/Twitter fallbacks. */
export function createRootMetadata(): Metadata {
  const siteUrl = getSiteUrl();
  const fullTitle = siteConfig.name;

  return {
    metadataBase: new URL(siteUrl),
    title: {
      default: fullTitle,
      template: `%s · ${siteConfig.name}`,
    },
    description: siteConfig.description,
    applicationName: siteConfig.name,
    alternates: {
      canonical: siteUrl,
    },
    openGraph: buildOpenGraph(fullTitle, siteConfig.description, siteUrl),
    twitter: buildTwitter(fullTitle, siteConfig.description),
    robots: {
      index: true,
      follow: true,
    },
  };
}

/** Per-page metadata with canonical URL, Open Graph, and Twitter cards. */
export function buildPageMetadata({
  title,
  description,
  path,
  noIndex = false,
}: BuildPageMetadataOptions): Metadata {
  const siteUrl = getSiteUrl();
  const canonical = path === "/" ? siteUrl : `${siteUrl}${path}`;
  const ogTitle = path === "/" ? siteConfig.name : `${title} · ${siteConfig.name}`;

  return {
    title: path === "/" ? { absolute: siteConfig.name } : title,
    description,
    alternates: {
      canonical,
    },
    openGraph: buildOpenGraph(ogTitle, description, canonical),
    twitter: buildTwitter(ogTitle, description),
    robots: noIndex
      ? { index: false, follow: false }
      : { index: true, follow: true },
  };
}
