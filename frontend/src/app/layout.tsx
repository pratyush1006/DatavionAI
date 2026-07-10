/**
 * Root layout for the Datavion AI application.
 */

import type { Metadata } from "next";
import { Inter } from "next/font/google";

import "./globals.css";

import { env } from "@/core/config/env";
import { AppProvider } from "@/core/providers/app-provider";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: env.appName,
  description: "Enterprise Hospital Information System",
};

type RootLayoutProps = Readonly<{
  children: React.ReactNode;
}>;

export default function RootLayout({
  children,
}: RootLayoutProps) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
    >
      <body className={inter.className}>
        <AppProvider>
          {children}
        </AppProvider>
      </body>
    </html>
  );
}
