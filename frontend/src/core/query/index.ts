/**
 * =============================================================================
 * DatavionOS
 * File: src/core/query/index.ts
 * =============================================================================
 *
 * Public entry point for the DatavionOS server-state/query subsystem.
 *
 * Query infrastructure is intentionally kept small.
 *
 * Feature-specific query definitions belong to their respective feature:
 *
 *     @/features/<area>/<feature>/api
 *
 * This module owns only generic TanStack Query infrastructure shared by the
 * application.
 *
 * Design Principles
 * -----------------
 * - Stable public API
 * - Explicit exports
 * - Centralized QueryClient
 * - No feature UI dependencies
 * - No feature-specific API definitions
 * - Enterprise Ready
 * =============================================================================
 */

/* =============================================================================
 * Query Client
 * =============================================================================
 */

export {
  createQueryClient,
  queryClient,
} from "./query-client";

/* =============================================================================
 * Query Provider
 * =============================================================================
 */

export {
  QueryProvider,
} from "./provider";

export type {
  QueryProviderProps,
} from "./provider";
