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
    useEffect,
    useState,
} from "react";

type Theme = "light" | "dark";

const THEME_STORAGE_KEY = "theme";

function getResolvedTheme(): Theme {
    const preference = window.localStorage.getItem(THEME_STORAGE_KEY);

    if (preference === "light" || preference === "dark") {
        return preference;
    }

    return window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
}

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
    // Keep server and first client render identical; browser preference is
    // applied only after hydration so React never hydrates mutated <html> attrs.
    const [theme, setTheme] = useState<Theme>("light");

    useEffect(() => {
        const media = window.matchMedia("(prefers-color-scheme: dark)");
        const updateTheme = () => setTheme(getResolvedTheme());
        const updateForSystemPreference = () => {
            const preference = window.localStorage.getItem(THEME_STORAGE_KEY);
            if (preference !== "light" && preference !== "dark") {
                setTheme(media.matches ? "dark" : "light");
            }
        };

        updateTheme();
        media.addEventListener("change", updateForSystemPreference);
        window.addEventListener("storage", updateTheme);

        return () => {
            media.removeEventListener("change", updateForSystemPreference);
            window.removeEventListener("storage", updateTheme);
        };
    }, []);

    return (
        <div className={theme} style={{ colorScheme: theme }}>
            {children}
        </div>
    );
}
