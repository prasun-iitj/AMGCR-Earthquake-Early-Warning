import { documents } from "@/lib/content/documents";

/** Static app routes included in sitemap and internal linking helpers. */
export const staticRoutes = [
  { path: "/", priority: 1, changeFrequency: "weekly" as const },
  { path: "/about", priority: 0.8, changeFrequency: "monthly" as const },
  { path: "/dashboard", priority: 0.9, changeFrequency: "weekly" as const },
  { path: "/research", priority: 0.9, changeFrequency: "weekly" as const },
  { path: "/research/report", priority: 0.9, changeFrequency: "monthly" as const },
  { path: "/workflow", priority: 0.85, changeFrequency: "monthly" as const },
  { path: "/results", priority: 0.85, changeFrequency: "weekly" as const },
  { path: "/dataset", priority: 0.85, changeFrequency: "weekly" as const },
  { path: "/waveforms", priority: 0.85, changeFrequency: "weekly" as const },
  { path: "/map", priority: 0.85, changeFrequency: "weekly" as const },
  { path: "/docs", priority: 0.8, changeFrequency: "monthly" as const },
  { path: "/resources", priority: 0.75, changeFrequency: "monthly" as const },
  { path: "/github", priority: 0.7, changeFrequency: "monthly" as const },
  { path: "/contact", priority: 0.6, changeFrequency: "yearly" as const },
] as const;

export function getDocRoutes() {
  return documents
    .filter((doc) => doc.href.startsWith("/docs/"))
    .map((doc) => ({
      path: doc.href,
      priority: 0.7,
      changeFrequency: "monthly" as const,
    }));
}

export function getAllSitemapPaths(): string[] {
  return [...staticRoutes.map((r) => r.path), ...getDocRoutes().map((r) => r.path)];
}
