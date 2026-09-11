import type { Metadata } from "next";
import { Plus_Jakarta_Sans, Space_Grotesk } from "next/font/google";
import Navigation from "@/components/marketing/homepage/Navigation";
import Footer from "@/components/marketing/homepage/Footer";
import ModalProvider from "@/components/marketing/homepage/ModalProvider";
import ScrollAnimationInit from "@/components/marketing/homepage/ScrollAnimationInit";
import SmoothScroll from "@/components/marketing/homepage/SmoothScroll";
import "./marketing.css";

const bodyFont = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--marketing-font-body", display: "swap" });
const displayFont = Space_Grotesk({ subsets: ["latin"], variable: "--marketing-font-display", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL("https://quicktrustapp.com"),
  title: { default: "Compliance Automation Platform | QuickTrust", template: "%s | QuickTrust" },
  description: "Map frameworks to controls, surface gaps, and get audit-ready with engineers who close them. SOC 2, ISO 27001, HIPAA. Free readiness assessment.",
  icons: { icon: "/marketing-icon.svg" },
  manifest: "/site.webmanifest",
  robots: { index: true, follow: true },
};

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`marketing ${bodyFont.variable} ${displayFont.variable} min-h-screen bg-slate-950 font-body text-slate-300 antialiased`}>
      <ModalProvider>
        <Navigation />
        <ScrollAnimationInit />
        <SmoothScroll />
        {children}
        <Footer />
      </ModalProvider>
    </div>
  );
}
