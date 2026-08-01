import type { Metadata } from "next";
import type { Viewport } from "next";
import { Inter, Source_Serif_4 } from "next/font/google";
import { Layout } from "@/components/layout/Layout";
import { WebsiteJsonLd } from "@/components/seo/WebsiteJsonLd";
import { createRootMetadata } from "@/lib/seo/metadata";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const sourceSerif = Source_Serif_4({
  variable: "--font-source-serif",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = createRootMetadata();

export const viewport: Viewport = {
  colorScheme: "light",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${sourceSerif.variable} h-full antialiased`}
      style={{ colorScheme: "light" }}
    >
      <body className="min-h-full bg-surface text-text">
        <WebsiteJsonLd />
        <Layout>{children}</Layout>
      </body>
    </html>
  );
}
