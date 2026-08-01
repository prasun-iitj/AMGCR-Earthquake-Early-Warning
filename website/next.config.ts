import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/downloads",
        destination: "/resources",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
