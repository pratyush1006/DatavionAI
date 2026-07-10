"use client";

/**
 * Application provider.
 */

import type { ReactNode } from "react";

import { AuthProvider } from "@/core/auth";

import { QueryProvider } from "./query-provider";
import { ThemeProvider } from "./theme-provider";

type AppProviderProps = Readonly<{
  children: ReactNode;
}>;

export function AppProvider({
  children,
}: AppProviderProps) {
  return (
    <QueryProvider>
      <ThemeProvider>
        <AuthProvider>
          {children}
        </AuthProvider>
      </ThemeProvider>
    </QueryProvider>
  );
}
