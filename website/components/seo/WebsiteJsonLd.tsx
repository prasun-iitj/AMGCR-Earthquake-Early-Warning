import { getSiteUrl } from "@/lib/seo/site-url";
import { siteConfig } from "@/lib/navigation";

export function WebsiteJsonLd() {
  const data = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteConfig.name,
    description: siteConfig.description,
    url: getSiteUrl(),
    inLanguage: "en-GB",
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
