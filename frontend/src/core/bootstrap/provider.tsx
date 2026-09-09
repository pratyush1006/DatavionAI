/**
 * =============================================================================
 * DatavionOS
 * File: src/core/bootstrap/provider.tsx
 * =============================================================================
 *
 * Platform bootstrap runtime provider.
 *
 * Responsibilities
 * ----------------
 * - Wait for authentication initialization.
 * - Fetch the authenticated platform bootstrap payload.
 * - Expose bootstrap runtime state through React Context.
 * - Clear bootstrap state when authentication ends.
 * - Keep server-state ownership inside TanStack Query.
 * - Provide a stable runtime boundary for application components.
 *
 * The backend is authoritative for:
 *
 * - tenant context
 * - organization context
 * - employee context
 * - roles
 * - permissions
 * - modules
 * - navigation
 * - dashboard
 * - branding
 * - feature flags
 * - subscription
 * - preferences
 *
 * This provider does NOT:
 *
 * - perform authentication
 * - resolve RBAC
 * - resolve SaaS entitlements
 * - build navigation
 * - access browser storage
 * - perform HTTP requests directly
 *
 * Architecture
 * ------------
 *
 *     QueryProvider
 *          |
 *          v
 *     AuthProvider
 *          |
 *          v
 *     BootstrapProvider
 *          |
 *          v
 *     platformBootstrapQuery()
 *          |
 *          v
 *       ApiClient
 *          |
 *          v
 *      /bootstrap/
 *
 * =============================================================================
 */

"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  type ReactNode,
} from "react";

import {
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  useAuth,
} from "@/core/auth";

import {
  platformBootstrapQuery,
} from "./queries";

import {
  BOOTSTRAP_QUERY_KEY,
} from "./keys";

import type {
  PlatformBootstrap,
} from "./types";

/* =============================================================================
 * Context
 * =============================================================================
 */

export interface BootstrapContextValue {
  /**
   * Resolved platform bootstrap payload.
   *
   * Null while authentication is unavailable or bootstrap has not completed.
   */
  readonly bootstrap:
    | PlatformBootstrap
    | null;

  /**
   * Whether the initial bootstrap request is loading.
   */
  readonly isLoading: boolean;

  /**
   * Whether bootstrap is currently being fetched.
   */
  readonly isFetching: boolean;

  /**
   * Whether the bootstrap request failed.
   */
  readonly isError: boolean;

  /**
   * Bootstrap request error.
   */
  readonly error: Error | null;

  /**
   * Refetch the bootstrap payload.
   */
  readonly refetch: () => Promise<unknown>;
}

const BootstrapContext =
  createContext<
    BootstrapContextValue | undefined
  >(undefined);

/* =============================================================================
 * Provider Props
 * =============================================================================
 */

export interface BootstrapProviderProps {
  readonly children: ReactNode;
}

/* =============================================================================
 * Provider
 * =============================================================================
 */

export function BootstrapProvider({
  children,
}: BootstrapProviderProps) {
  const {
    isInitialized,
    isAuthenticated,
  } = useAuth();

  const queryClient =
    useQueryClient();

  /**
   * Bootstrap is only allowed after authentication initialization has
   * completed and an authenticated session exists.
   */
  const enabled =
    isInitialized &&
    isAuthenticated;

  const query =
    useQuery({
      ...platformBootstrapQuery(),
      enabled,
    });

  /* ===========================================================================
   * Query State
   * =========================================================================== */

  const {
    data,
    isError,
    isFetching,
    isLoading,
    refetch,
  } = query;

  /* ===========================================================================
   * Bootstrap Cache Lifecycle
   * =========================================================================== */

  /**
   * Remove authenticated bootstrap data when the authenticated session ends.
   *
   * Bootstrap contains tenant, organization, employee, RBAC, permissions,
   * modules and other runtime information.
   *
   * Removing the query guarantees that the next authenticated session starts
   * without bootstrap data from the previous session.
   */
  useEffect(() => {
    if (
      !isInitialized ||
      isAuthenticated
    ) {
      return;
    }

    queryClient.removeQueries({
      queryKey:
        BOOTSTRAP_QUERY_KEY,
    });
  }, [
    isInitialized,
    isAuthenticated,
    queryClient,
  ]);

  /* ===========================================================================
   * Context Value
   * =========================================================================== */

  const value =
    useMemo<BootstrapContextValue>(
      () => {
        /**
         * Normalize the query error inside the memo.
         *
         * Keeping this calculation inside useMemo prevents the normalized
         * Error object from becoming a new dependency on every render.
         */
        const error =
          query.error instanceof Error
            ? query.error
            : query.error
              ? new Error(
                  String(
                    query.error,
                  ),
                )
              : null;

        return {
          /**
           * Do not expose cached bootstrap data while the application is
           * unauthenticated.
           */
          bootstrap:
            enabled
              ? (
                  data ??
                  null
                )
              : null,

          isLoading:
            enabled &&
            isLoading,

          isFetching:
            enabled &&
            isFetching,

          isError:
            enabled &&
            isError,

          error:
            enabled
              ? error
              : null,

          refetch:
            async () => {
              if (!enabled) {
                return;
              }

              return refetch();
            },
        };
      },
      [
        enabled,
        data,
        isError,
        isFetching,
        isLoading,
        query.error,
        refetch,
      ],
    );

  /* ===========================================================================
   * Render
   * =========================================================================== */

  return (
    <BootstrapContext.Provider
      value={value}
    >
      {children}
    </BootstrapContext.Provider>
  );
}

/* =============================================================================
 * Hook
 * =============================================================================
 */

/**
 * Access the current platform bootstrap runtime.
 *
 * Must be used inside BootstrapProvider.
 */
export function useBootstrap(): BootstrapContextValue {
  const context =
    useContext(
      BootstrapContext,
    );

  if (
    context === undefined
  ) {
    throw new Error(
      "useBootstrap must be used within BootstrapProvider.",
    );
  }

  return context;
}

/* =============================================================================
 * Required Bootstrap Hook
 * =============================================================================
 */

/**
 * Return the resolved platform bootstrap payload.
 *
 * Throws when bootstrap is not currently available.
 *
 * Use useBootstrap() when the caller needs loading/error state.
 */
export function useRequiredBootstrap(): PlatformBootstrap {
  const {
    bootstrap,
  } = useBootstrap();

  if (
    bootstrap === null
  ) {
    throw new Error(
      "Platform bootstrap is not available.",
    );
  }

  return bootstrap;
}
