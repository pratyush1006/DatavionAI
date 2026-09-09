/**
 * =============================================================================
 * DatavionOS
 * File: src/core/query/query-client.ts
 * =============================================================================
 *
 * Central TanStack Query client configuration.
 *
 * Responsibilities
 * ----------------
 * • Configure query caching
 * • Configure retry behavior
 * • Configure stale/cache policies
 * • Provide a single QueryClient instance
 *
 * This module does NOT:
 *
 * • Perform HTTP requests directly
 * • Access Axios
 * • Access authentication storage
 * • Contain feature-specific queries
 *
 * API transport belongs to:
 *
 *     @/core/api
 *
 * Server-state management belongs here.
 *
 * Design Principles
 * -----------------
 * • Centralized configuration
 * • Predictable caching
 * • Authentication-aware retry policy
 * • SSR compatible
 * • Enterprise Ready
 * =============================================================================
 */

import {
    QueryClient,
} from "@tanstack/react-query";

import {
    ApiClientError,
    isAuthenticationError,
    isRateLimitError,
} from "@/core/api";

/* =============================================================================
 * Constants
 * =============================================================================
 */

/**
 * Default time for which query data is considered fresh.
 *
 * Five minutes is a reasonable platform default. Individual clinical modules
 * can override this for data requiring stronger freshness guarantees.
 */
const DEFAULT_STALE_TIME =
    5 * 60 * 1000;

/**
 * Default time for retaining inactive query data.
 *
 * Thirty minutes provides useful navigation performance without allowing
 * inactive healthcare data to remain cached indefinitely.
 */
const DEFAULT_GC_TIME =
    30 * 60 * 1000;

/**
 * Maximum automatic query retries.
 */
const DEFAULT_RETRY_COUNT =
    2;

/* =============================================================================
 * Retry Policy
 * =============================================================================
 */

/**
 * Determine whether a failed query should be retried.
 *
 * Authentication failures are never blindly retried.
 * Permission failures are never retried.
 * Rate limiting is left to the server/client policy rather than repeatedly
 * hammering the endpoint.
 */
function shouldRetryQuery(
    failureCount: number,
    error: unknown,
): boolean {
    if (
        failureCount >=
        DEFAULT_RETRY_COUNT
    ) {
        return false;
    }

    if (
        error instanceof
        ApiClientError
    ) {
        if (
            isAuthenticationError(
                error,
            )
        ) {
            return false;
        }

        if (
            error.statusCode ===
            403
        ) {
            return false;
        }

        if (
            isRateLimitError(
                error,
            )
        ) {
            return false;
        }

        /*
         * Retry network, timeout and server errors.
         */
        return (
            error.statusCode ===
                0 ||
            error.statusCode >=
                500
        );
    }

    /*
     * Unknown errors are conservatively retried.
     */
    return true;
}

/**
 * Determine whether a failed mutation should be retried.
 *
 * Mutations are deliberately not retried by default because repeating a
 * mutation can create duplicate clinical/business operations.
 */
function shouldRetryMutation(): boolean {
    return false;
}

/* =============================================================================
 * Query Client Factory
 * =============================================================================
 */

/**
 * Create a configured TanStack Query client.
 *
 * A factory is preferred over exporting only a singleton because:
 *
 * • Tests can create isolated clients.
 * • SSR can create request-scoped clients.
 * • Future application shells can provide different configurations.
 */
export function createQueryClient(): QueryClient {
    return new QueryClient({
        defaultOptions: {
            queries: {
                staleTime:
                    DEFAULT_STALE_TIME,

                gcTime:
                    DEFAULT_GC_TIME,

                retry:
                    shouldRetryQuery,

                refetchOnWindowFocus:
                    false,

                refetchOnReconnect:
                    true,

                refetchOnMount:
                    true,
            },

            mutations: {
                retry:
                    shouldRetryMutation,
            },
        },
    });
}

/* =============================================================================
 * Application Query Client
 * =============================================================================
 */

/**
 * Browser/application-level QueryClient.
 *
 * The singleton is appropriate for the client-side Next.js application.
 *
 * Do not use this singleton for server request-scoped data fetching.
 */
export const queryClient =
    createQueryClient();
