/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/index.ts
 * =============================================================================
 *
 * Public API boundary for the DatavionOS frontend API subsystem.
 *
 * Feature modules should import from:
 *
 *     @/core/api
 *
 * Internal implementation files should not be imported directly by features.
 *
 * Design Principles
 * -----------------
 * - Stable public API
 * - Explicit exports
 * - Single ownership of contracts
 * - No circular dependencies
 * - Transport/framework separation
 * - Dependency inversion
 * - Single canonical application API client
 * - Enterprise Ready
 *
 * =============================================================================
 */

/* =============================================================================
 * API Client
 * =============================================================================
 */

export {
  ApiClient,
  ApiClientError,
  createApiClient,
} from "./client";

export type {
  ApiClientConfig,
  ApiRequestConfig,
} from "./client";

/* =============================================================================
 * Application API Factory
 * =============================================================================
 *
 * The application-level singleton is owned by factory.ts.
 *
 * client.ts owns the transport implementation.
 * factory.ts owns application composition and singleton creation.
 * =============================================================================
 */

export {
  apiClient,
  createApplicationApiClient,
} from "./factory";

export type {
  ApiClientFactoryOptions,
} from "./factory";

/* =============================================================================
 * API Configuration
 * =============================================================================
 */

export {
  API_BASE_URL,
  API_CONFIG,
  API_TIMEOUT,
  API_VERSION,
  API_WITH_CREDENTIALS,
  buildApiUrl,
  isApiUrl,
} from "./config";

export type {
  ApiConfig,
} from "./config";

/* =============================================================================
 * API Contracts
 * =============================================================================
 */

export {
  DEFAULT_REQUEST_ID_PROVIDER,
  EMPTY_TENANT_PROVIDER,
  EMPTY_TOKEN_PROVIDER,
} from "./contracts";

export type {
  ApiAuthenticationFailureHandler,
  ApiAuthenticationDependencies,
  ApiClientOptions,
  ApiRequestContext,
  ApiRequestIdProvider,
  ApiRuntimeDependencies,
  ApiTenantProvider,
  ApiTokenProvider,
  ApiTokenRefreshProvider,
} from "./contracts";

/* =============================================================================
 * API Errors
 * =============================================================================
 */

export {
  API_ERROR_CODES,
  createApiHttpError,
  getApiErrorCode,
  getApiErrorMessage,
  isApiErrorCode,
  isApiHttpError,
  isAuthenticationError,
  isAuthorizationError,
  isConflictError,
  isNotFoundError,
  isRateLimitError,
  isRetryableError,
} from "./errors";

export type {
  ApiErrorCode,
} from "./errors";

/* =============================================================================
 * API Interceptors
 * =============================================================================
 */

export {
  createRequestInterceptor,
  ejectResponseInterceptor,
  installResponseInterceptors,
  shouldSkipAuthentication,
  shouldSkipRequestId,
  shouldSkipTenant,
} from "./interceptors";

export type {
  InterceptorRequestConfig,
  RequestInterceptorDependencies,
  ResponseInterceptorDependencies,
} from "./interceptors";

/* =============================================================================
 * API Response Utilities
 * =============================================================================
 */

export {
  unwrapData,
} from "./response";
