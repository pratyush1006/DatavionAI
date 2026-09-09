/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/contracts.ts
 * =============================================================================
 *
 * Shared API infrastructure contracts.
 *
 * This module contains interfaces shared by the API client, request
 * interceptors, response interceptors, and authentication composition layer.
 *
 * Design Principles
 * -----------------
 * • Single ownership of shared contracts
 * • Dependency inversion
 * • No Axios dependency
 * • No React dependency
 * • No business logic
 * • Easy unit testing
 * • Enterprise Ready
 * =============================================================================
 */

/* =============================================================================
 * Token Provider
 * =============================================================================
 */

/**
 * Provides the current authentication access token.
 *
 * The API layer does not know where the token is stored.
 */
export interface ApiTokenProvider {
    getAccessToken(): string | null;
}

/* =============================================================================
 * Tenant Provider
 * =============================================================================
 */

/**
 * Provides the currently active tenant identifier.
 *
 * Tenant resolution belongs to the application/authentication layer.
 * The API transport layer only consumes the resolved value.
 */
export interface ApiTenantProvider {
    getTenantId(): string | null;
}

/* =============================================================================
 * Request ID Provider
 * =============================================================================
 */

/**
 * Generates request correlation identifiers.
 *
 * Request IDs allow frontend requests to be correlated with backend logs
 * through the X-Request-ID header.
 */
export interface ApiRequestIdProvider {
    generate(): string;
}

/* =============================================================================
 * Authentication Refresh
 * =============================================================================
 */

/**
 * Performs an access-token refresh.
 *
 * The implementation is injected by the authentication composition layer.
 *
 * This prevents the dependency cycle:
 *
 *     ApiClient
 *         ↓
 *     AuthService
 *         ↓
 *     ApiClient
 */
export interface ApiTokenRefreshProvider {
    refreshAccessToken(): Promise<string>;
}

/* =============================================================================
 * Authentication Failure
 * =============================================================================
 */

/**
 * Called when authentication can no longer be recovered.
 */
export interface ApiAuthenticationFailureHandler {
    onAuthenticationFailure(
        error: unknown,
    ): void;
}

/* =============================================================================
 * API Runtime Dependencies
 * =============================================================================
 */

/**
 * Complete dependencies required by the API transport layer.
 */
export interface ApiRuntimeDependencies {
    readonly tokenProvider: ApiTokenProvider;

    readonly tenantProvider: ApiTenantProvider;

    readonly requestIdProvider: ApiRequestIdProvider;
}

/**
 * Optional authentication dependencies used by response interceptors.
 */
export interface ApiAuthenticationDependencies {
    readonly refreshProvider?: ApiTokenRefreshProvider;

    readonly authenticationFailureHandler?: ApiAuthenticationFailureHandler;

    readonly onRefreshStart?: () => void;

    readonly onRefreshSuccess?: () => void;

    readonly onRefreshFailure?: (
        error: unknown,
    ) => void;
}

/* =============================================================================
 * API Request Context
 * ============================================================================= */

/**
 * Request-level authentication options.
 */
export interface ApiRequestContext {
    /**
     * Skip the Authorization header.
     */
    readonly skipAuth?: boolean;

    /**
     * Skip the tenant header.
     */
    readonly skipTenant?: boolean;

    /**
     * Skip X-Request-ID generation.
     */
    readonly skipRequestId?: boolean;
}

/* =============================================================================
 * API Client Options
 * ============================================================================= */

/**
 * Options used when constructing the API client.
 */
export interface ApiClientOptions {
    readonly runtime: ApiRuntimeDependencies;

    readonly authentication?: ApiAuthenticationDependencies;
}

/* =============================================================================
 * Default Providers
 * =============================================================================
 */

/**
 * Provider used when authentication has not yet been configured.
 */
export const EMPTY_TOKEN_PROVIDER: ApiTokenProvider =
    Object.freeze({
        getAccessToken(): string | null {
            return null;
        },
    });

/**
 * Provider used before tenant context has been resolved.
 */
export const EMPTY_TENANT_PROVIDER: ApiTenantProvider =
    Object.freeze({
        getTenantId(): string | null {
            return null;
        },
    });

/**
 * Default request ID provider.
 *
 * Uses crypto.randomUUID when available and falls back to a generated
 * identifier for older environments.
 */
export const DEFAULT_REQUEST_ID_PROVIDER: ApiRequestIdProvider =
    Object.freeze({
        generate(): string {
            if (
                typeof crypto !==
                    "undefined" &&
                typeof crypto.randomUUID ===
                    "function"
            ) {
                return crypto.randomUUID();
            }

            return [
                "dv",
                Date.now().toString(36),
                Math.random()
                    .toString(36)
                    .slice(2),
            ].join("-");
        },
    });
