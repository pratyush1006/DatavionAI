/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/interceptors.ts
 * =============================================================================
 *
 * Axios interceptor infrastructure.
 *
 * Responsibilities
 * ----------------
 * • Attach request correlation IDs
 * • Attach access tokens
 * • Attach tenant context
 * • Handle authentication failures
 * • Coordinate single-flight token refresh
 *
 * Design Principles
 * -----------------
 * • Transport concerns only
 * • Dependency inversion
 * • No AuthService dependency
 * • No React dependency
 * • No browser-storage dependency
 * • SSR safe
 * • Testable
 * • Enterprise Ready
 * =============================================================================
 */

import type {
    AxiosError,
    AxiosInstance,
    AxiosResponse,
    InternalAxiosRequestConfig,
} from "axios";

import {
    AxiosHeaders,
} from "axios";

import type {
    ApiAuthenticationDependencies,
    ApiOrganizationProvider,
    ApiRequestContext,
    ApiRequestIdProvider,
    ApiRuntimeDependencies,
    ApiTenantProvider,
    ApiTokenProvider,
} from "./contracts";

/* =============================================================================
 * Constants
 * =============================================================================
 */

const HEADER_AUTHORIZATION =
    "Authorization";

const HEADER_ACCEPT =
    "Accept";

const HEADER_CONTENT_TYPE =
    "Content-Type";

const HEADER_REQUEST_ID =
    "X-Request-ID";

const HEADER_TENANT_ID =
    "X-Tenant-ID";

const HEADER_ORGANIZATION_ID =
    "X-Organization-ID";

const CONTENT_TYPE_JSON =
    "application/json";

const BEARER_PREFIX =
    "Bearer ";

/* =============================================================================
 * Request Configuration
 * =============================================================================
 */

/**
 * Axios configuration extended with DatavionOS request controls.
 */
export interface InterceptorRequestConfig
    extends InternalAxiosRequestConfig,
        ApiRequestContext {
    /**
     * Prevent this request from being retried after token refresh.
     */
    _authRetry?: boolean;
}

/* =============================================================================
 * Request Dependencies
 * =============================================================================
 */

/**
 * Dependencies required by request interceptors.
 *
 * Kept as an alias to the shared runtime contract so there is only one
 * definition of these dependencies in the API subsystem.
 */
export type RequestInterceptorDependencies =
    ApiRuntimeDependencies;

/**
 * Individual provider dependencies retained as public aliases for callers
 * that need them independently.
 */
export type {
    ApiOrganizationProvider,
    ApiRequestIdProvider,
    ApiTenantProvider,
    ApiTokenProvider,
};

/* =============================================================================
 * Response Dependencies
 * =============================================================================
 */

/**
 * Dependencies required by authentication response handling.
 */
export interface ResponseInterceptorDependencies
    extends ApiAuthenticationDependencies {
    /**
     * Authentication failure callback.
     *
     * Kept as a direct callback for backwards-compatible/simple composition.
     */
    readonly onAuthenticationFailure?: (
        error: AxiosError,
    ) => void;
}

/* =============================================================================
 * Shared Refresh State
 * =============================================================================
 */

/**
 * Shared refresh promise.
 *
 * Multiple simultaneous 401 responses share this promise.
 *
 * Example:
 *
 *     Request A ─┐
 *     Request B ─┤
 *     Request C ─┼──► ONE refresh operation
 *     Request D ─┘
 */
let refreshPromise:
    | Promise<string>
    | null = null;

/* =============================================================================
 * Request Interceptor
 * =============================================================================
 */

/**
 * Create the DatavionOS request interceptor.
 */
export function createRequestInterceptor(
    dependencies: RequestInterceptorDependencies,
) {
    return (
        config: InternalAxiosRequestConfig,
    ): InternalAxiosRequestConfig => {
        const requestConfig =
            config as InterceptorRequestConfig;

        const headers =
            requestConfig.headers instanceof
            AxiosHeaders
                ? requestConfig.headers
                : new AxiosHeaders(
                      requestConfig.headers,
                  );

        headers.set(
            HEADER_ACCEPT,
            CONTENT_TYPE_JSON,
        );

        /*
         * Only set Content-Type when a body exists or the caller has not
         * explicitly supplied one.
         */
        if (
            !headers.has(
                HEADER_CONTENT_TYPE,
            )
        ) {
            headers.set(
                HEADER_CONTENT_TYPE,
                CONTENT_TYPE_JSON,
            );
        }

        /*
         * Every request gets a correlation ID unless explicitly disabled.
         */
        if (
            !requestConfig.skipRequestId
        ) {
            headers.set(
                HEADER_REQUEST_ID,
                dependencies.requestIdProvider.generate(),
            );
        }

        /*
         * Authentication headers are opt-out rather than opt-in.
         *
         * Public endpoints such as login/register must use:
         *
         *     { skipAuth: true }
         */
        if (
            !requestConfig.skipAuth
        ) {
            const accessToken =
                dependencies.tokenProvider.getAccessToken();

            if (accessToken) {
                headers.set(
                    HEADER_AUTHORIZATION,
                    `${BEARER_PREFIX}${accessToken}`,
                );
            }
        }

        /*
         * Tenant context is attached when available.
         */
        if (
            !requestConfig.skipTenant
        ) {
            const tenantId =
                dependencies.tenantProvider.getTenantId();

            if (tenantId) {
                headers.set(
                    HEADER_TENANT_ID,
                    tenantId,
                );
            }
        }

        if (
            !requestConfig.skipOrganization &&
            !requestConfig.skipTenant
        ) {
            const organizationId =
                dependencies.organizationProvider.getOrganizationId();

            if (organizationId) {
                headers.set(
                    HEADER_ORGANIZATION_ID,
                    organizationId,
                );
            }
        }

        requestConfig.headers =
            headers;

        return requestConfig;
    };
}

/* =============================================================================
 * Response Interceptor
 * =============================================================================
 */

/**
 * Install the authentication response interceptor.
 *
 * Only HTTP 401 responses are handled here.
 *
 * Other errors continue through Axios unchanged and are normalized by the
 * API client's error layer.
 */
export function installResponseInterceptors(
    client: AxiosInstance,
    dependencies: ResponseInterceptorDependencies,
): number {
    return client.interceptors.response.use(
        (
            response: AxiosResponse,
        ) => response,

        async (
            error: AxiosError,
        ) =>
            handleAuthenticationError(
                client,
                error,
                dependencies,
            ),
    );
}

/* =============================================================================
 * Authentication Failure
 * =============================================================================
 */

/**
 * Handle a 401 response.
 */
async function handleAuthenticationError(
    client: AxiosInstance,
    error: AxiosError,
    dependencies: ResponseInterceptorDependencies,
): Promise<unknown> {
    if (
        error.response?.status !==
        401
    ) {
        return Promise.reject(
            error,
        );
    }

    const request =
        error.config as
            | InterceptorRequestConfig
            | undefined;

    /*
     * No request means there is nothing safe to retry.
     */
    if (!request) {
        notifyAuthenticationFailure(
            dependencies,
            error,
        );

        return Promise.reject(
            error,
        );
    }

    /*
     * Public/unauthenticated requests must never trigger refresh.
     */
    if (
        request.skipAuth
    ) {
        notifyAuthenticationFailure(
            dependencies,
            error,
        );

        return Promise.reject(
            error,
        );
    }

    /*
     * Prevent infinite refresh loops.
     */
    if (
        request._authRetry
    ) {
        notifyAuthenticationFailure(
            dependencies,
            error,
        );

        return Promise.reject(
            error,
        );
    }

    /*
     * No refresh provider means authentication recovery has not been wired.
     */
    const refreshAccessToken =
        dependencies.refreshProvider
            ?.refreshAccessToken;

    if (
        !refreshAccessToken
    ) {
        notifyAuthenticationFailure(
            dependencies,
            error,
        );

        return Promise.reject(
            error,
        );
    }

    request._authRetry =
        true;

    try {
        const accessToken =
            await getSharedAccessToken(
                dependencies,
                refreshAccessToken,
            );

        const headers =
            request.headers instanceof
            AxiosHeaders
                ? request.headers
                : new AxiosHeaders(
                      request.headers,
                  );

        headers.set(
            HEADER_AUTHORIZATION,
            `${BEARER_PREFIX}${accessToken}`,
        );

        request.headers =
            headers;

        return client.request(
            request,
        );
    } catch (
        refreshError
    ) {
        dependencies.onRefreshFailure?.(
            refreshError,
        );

        notifyAuthenticationFailure(
            dependencies,
            error,
        );

        return Promise.reject(
            refreshError,
        );
    }
}

/* =============================================================================
 * Single-Flight Refresh
 * =============================================================================
 */

/**
 * Return a shared access token refresh operation.
 *
 * This prevents a "refresh storm" when several API requests expire
 * simultaneously.
 */
async function getSharedAccessToken(
    dependencies: ResponseInterceptorDependencies,
    refreshAccessToken: () => Promise<string>,
): Promise<string> {
    if (
        refreshPromise
    ) {
        return refreshPromise;
    }

    dependencies.onRefreshStart?.();

    refreshPromise =
        refreshAccessToken();

    try {
        const accessToken =
            await refreshPromise;

        dependencies.onRefreshSuccess?.();

        return accessToken;
    } finally {
        refreshPromise =
            null;
    }
}

/* =============================================================================
 * Authentication Failure Notification
 * =============================================================================
 */

/**
 * Notify the configured authentication failure handler.
 */
function notifyAuthenticationFailure(
    dependencies: ResponseInterceptorDependencies,
    error: AxiosError,
): void {
    /*
     * Prefer the new contract.
     */
    dependencies.authenticationFailureHandler?.onAuthenticationFailure(
        error,
    );

    /*
     * Preserve the direct callback for simple integrations.
     */
    dependencies.onAuthenticationFailure?.(
        error,
    );
}

/* =============================================================================
 * Interceptor Management
 * =============================================================================
 */

/**
 * Eject a response interceptor.
 */
export function ejectResponseInterceptor(
    client: AxiosInstance,
    interceptorId: number,
): void {
    client.interceptors.response.eject(
        interceptorId,
    );
}

/* =============================================================================
 * Request Utilities
 * =============================================================================
 */

/**
 * Determine whether authentication should be skipped.
 */
export function shouldSkipAuthentication(
    config?: ApiRequestContext,
): boolean {
    return config?.skipAuth === true;
}

/**
 * Determine whether tenant context should be skipped.
 */
export function shouldSkipTenant(
    config?: ApiRequestContext,
): boolean {
    return config?.skipTenant === true;
}

/**
 * Determine whether request-ID generation should be skipped.
 */
export function shouldSkipRequestId(
    config?: ApiRequestContext,
): boolean {
    return (
        config?.skipRequestId ===
        true
    );
}
