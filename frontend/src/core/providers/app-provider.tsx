/**
 * =============================================================================
 * DatavionOS
 * File: src/core/providers/app-provider.tsx
 * =============================================================================
 *
 * Root application provider composition.
 *
 * Provider order:
 *
 *     QueryProvider
 *          ↓
 *     AuthProvider
 *          ↓
 *     BootstrapProvider
 *          ↓
 *     ThemeProvider
 *          ↓
 *     Application
 *
 * Authentication is established before platform bootstrap is resolved because
 * bootstrap is an authenticated runtime contract.
 *
 * Sonner is mounted once at the application root so all feature modules can
 * safely use toast.success() / toast.error().
 *
 * =============================================================================
 */

"use client";

import type {
  ReactNode,
} from "react";

import {
  Toaster,
} from "sonner";

import {
  authRuntime,
  AuthProvider,
} from "@/core/auth";

import {
  BootstrapProvider,
} from "@/core/bootstrap";

import {
  QueryProvider,
} from "@/core/query";

import {
  ThemeProvider,
} from "./theme-provider";

/* =============================================================================
 * Types
 * =============================================================================
 */

type AppProviderProps =
  Readonly<{
    children: ReactNode;
  }>;

/* =============================================================================
 * Provider Composition
 * =============================================================================
 */

export function AppProvider({
  children,
}: AppProviderProps) {
  return (
    <QueryProvider>
      <AuthProvider
        service={
          authRuntime.service
        }
      >
        <BootstrapProvider>
          <ThemeProvider>
            {children}

            <Toaster
              position="top-right"
              closeButton
            />
          </ThemeProvider>
        </BootstrapProvider>
      </AuthProvider>
    </QueryProvider>
  );
}
