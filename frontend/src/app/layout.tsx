import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ApplicationProviders } from "@/providers/application-providers";
import { ThemeProvider } from "@/providers/theme-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "QuickTrust - GRC Platform",
  description: "Open-source, agent-first GRC platform",
  robots: { index: false, follow: false },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <ApplicationProviders>{children}</ApplicationProviders>
        </ThemeProvider>
      </body>
    </html>
  );
}
