import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: ["/api/", "/dashboard", "/login", "/signup", "/reset-password", "/invite/", "/portal"] },
      { userAgent: "Bytespider", disallow: "/" },
    ],
    sitemap: "https://quicktrustapp.com/sitemap.xml",
  };
}
