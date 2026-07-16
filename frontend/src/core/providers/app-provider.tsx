"use client";

import type { ReactNode } from "react";

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
        {children}
      </ThemeProvider>
    </QueryProvider>
  );
}
