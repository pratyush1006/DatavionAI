/**
 * =============================================================================
 * DatavionOS
 * File: src/core/query/provider.tsx
 * =============================================================================
 *
 * TanStack Query React provider.
 *
 * Responsibilities
 * ----------------
 * - Provide QueryClient to the React tree
 * - Keep QueryClient configuration outside React components
 * - Support dependency injection for tests and alternate application shells
 *
 * This module does NOT:
 *
 * - Configure Axios
 * - Manage authentication
 * - Define feature queries
 * - Access browser storage
 *
 * Query configuration belongs to:
 *
 *     @/core/query/query-client
 *
 * API transport belongs to:
 *
 *     @/core/api
 *
 * Design Principles
 * -----------------
 * - Thin React boundary
 * - Explicit dependencies
 * - SSR conscious
 * - Testable
 * - Enterprise Ready
 * =============================================================================
 */

"use client";

import {
    QueryClient,
    QueryClientProvider,
} from "@tanstack/react-query";

import type {
    ReactNode,
} from "react";

import {
    queryClient,
} from "./query-client";

/* =============================================================================
 * Props
 * =============================================================================
 */

export interface QueryProviderProps {
    readonly children: ReactNode;

    /**
     * Optional QueryClient override.
     *
     * Useful for:
     * - Tests
     * - Storybook
     * - Alternate application shells
     */
    readonly client?: QueryClient;
}

/* =============================================================================
 * Provider
 * =============================================================================
 */

export function QueryProvider({
    children,
    client = queryClient,
}: QueryProviderProps) {
    return (
        <QueryClientProvider
            client={client}
        >
            {children}
        </QueryClientProvider>
    );
}
