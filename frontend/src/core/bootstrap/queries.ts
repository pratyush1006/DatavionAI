/**
 * =============================================================================
 * DatavionOS
 * File: src/core/bootstrap/queries.ts
 * =============================================================================
 *
 * Platform bootstrap TanStack Query definitions.
 *
 * Responsibilities
 * ----------------
 * - Define the canonical platform bootstrap query.
 * - Provide the stable bootstrap query key.
 * - Define bootstrap-specific cache policy.
 *
 * This module does NOT:
 *
 * - Perform HTTP requests directly.
 * - Create an Axios client.
 * - Manage authentication.
 * - Manage React context.
 * - Resolve tenant permissions.
 *
 * HTTP transport belongs to:
 *
 *     @/core/bootstrap/api
 *
 * Server-state management belongs to:
 *
 *     @/core/query
 *
 * =============================================================================
 */

import {
  queryOptions,
} from "@tanstack/react-query";

import {
  fetchPlatformBootstrap,
} from "./api";

import {
  BOOTSTRAP_QUERY_KEY,
} from "./keys";

import type {
  PlatformBootstrap,
} from "./types";

/* =============================================================================
 * Cache Policy
 * =============================================================================
 */

/**
 * Bootstrap freshness window.
 *
 * Five minutes provides a reasonable balance between:
 *
 * - avoiding unnecessary bootstrap requests
 * - reflecting tenant/runtime configuration changes
 * - preserving application navigation performance
 */
const BOOTSTRAP_STALE_TIME =
  5 * 60 * 1000;

/**
 * Bootstrap garbage-collection window.
 */
const BOOTSTRAP_GC_TIME =
  30 * 60 * 1000;

/* =============================================================================
 * Query Definition
 * =============================================================================
 */

/**
 * Return the canonical platform bootstrap query options.
 *
 * The returned options object can be consumed by:
 *
 * - useQuery
 * - useSuspenseQuery
 * - QueryClient.fetchQuery
 * - QueryClient.prefetchQuery
 *
 * The query function is the canonical bootstrap API function.
 */
export function platformBootstrapQuery() {
  return queryOptions<
    PlatformBootstrap
  >({
    queryKey:
      BOOTSTRAP_QUERY_KEY,

    queryFn:
      fetchPlatformBootstrap,

    staleTime:
      BOOTSTRAP_STALE_TIME,

    gcTime:
      BOOTSTRAP_GC_TIME,
  });
}
