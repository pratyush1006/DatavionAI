"use client";

import type { ReactNode } from "react";

import { QueryProvider } from "./query-provider";
import { ThemeProvider } from "./theme-provider";

import { AuthProvider } from "@/core/auth";

type AppProviderProps = Readonly<{
  children: ReactNode;
}>;

export function AppProvider({
  children,
}: AppProviderProps) {
  return (
    <QueryProvider>
      <AuthProvider>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </AuthProvider>
    </QueryProvider>
  );
}
