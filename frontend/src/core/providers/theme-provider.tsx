/**
 * =============================================================================
 * DatavionOS
 * File: src/core/providers/theme-provider.tsx
 * =============================================================================
 *
 * Global application theme provider.
 *
 * Responsibilities
 * ----------------
 * • Provide light/dark/system theme support
 * • Prevent theme logic from leaking into feature modules
 * • Keep theme configuration centralized
 *
 * Design Principles
 * -----------------
 * • Thin provider
 * • Client-side only
 * • SSR compatible
 * • No feature dependencies
 * • Enterprise Ready
 * =============================================================================
 */

"use client";

import type {
    ReactNode,
} from "react";

import {
    ThemeProvider as NextThemesProvider,
} from "next-themes";

/* =============================================================================
 * Types
 * =============================================================================
 */

type ThemeProviderProps =
    Readonly<{
        children: ReactNode;
    }>;

/* =============================================================================
 * Provider
 * =============================================================================
 */

export function ThemeProvider({
    children,
}: ThemeProviderProps) {
    return (
        <NextThemesProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
        >
            {children}
        </NextThemesProvider>
    );
}
