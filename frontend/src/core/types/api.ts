/**
 * =============================================================================
 * DatavionOS
 * File: src/core/types/api.ts
 * =============================================================================
 *
 * Frontend representation of the DatavionOS API response contract.
 *
 * Backend success:
 *
 * {
 *     success: true,
 *     message: "...",
 *     data: ...,
 *     meta: {
 *         api_version: "...",
 *         timestamp: "...",
 *         request_id: "...",
 *         tenant_id: "..."
 *     }
 * }
 *
 * Backend error:
 *
 * {
 *     success: false,
 *     error: {
 *         code: "...",
 *         message: "...",
 *         details: ...
 *     },
 *     meta: {
 *         api_version: "...",
 *         timestamp: "...",
 *         request_id: "...",
 *         tenant_id: "..."
 *     }
 * }
 *
 * Design Principles
 * -----------------
 * - Backend contract aligned
 * - JSON serializable
 * - Strict TypeScript
 * - Immutable contracts
 * - No runtime dependencies
 * - Single ownership of API contracts
 * - Enterprise Ready
 *
 * =============================================================================
 */

/* =============================================================================
 * JSON Types
 * =============================================================================
 */

/**
 * JSON primitive.
 */
export type JsonPrimitive =
  | string
  | number
  | boolean
  | null;

/**
 * JSON value.
 */
export type JsonValue =
  | JsonPrimitive
  | readonly JsonValue[]
  | {
      readonly [key: string]: JsonValue;
    };

/**
 * JSON object.
 */
export type JsonObject = {
  readonly [key: string]: JsonValue;
};

/* =============================================================================
 * Common Primitives
 * =============================================================================
 */

/**
 * Universally unique identifier.
 *
 * UUID values are represented as strings at the frontend boundary.
 */
export type UUID = string;

/**
 * ISO-8601 date/time representation.
 *
 * DatavionOS backend datetime values are represented as strings at the
 * frontend transport boundary.
 */
export type ISODateTime = string;

/* =============================================================================
 * API Metadata
 * =============================================================================
 */

/**
 * Standard DatavionOS response metadata.
 *
 * Mirrors:
 *
 *     apps.common.api.responses._request_metadata()
 *
 * Additional endpoint-specific metadata should be represented by extending
 * ApiMeta rather than weakening this contract with a broad index signature.
 */
export interface ApiMeta {
  readonly api_version: string;

  readonly timestamp: string;

  readonly request_id?: string;

  readonly tenant_id?: string;
}

/* =============================================================================
 * Success Response
 * =============================================================================
 */

/**
 * Standard successful API response.
 */
export interface ApiSuccessResponse<
  T = null,
> {
  readonly success: true;

  readonly message: string;

  readonly data: T;

  readonly meta: ApiMeta;
}

/* =============================================================================
 * API Error
 * =============================================================================
 */

/**
 * Standard error payload.
 *
 * Mirrors the backend error_response() contract:
 *
 *     {
 *         "code": "...",
 *         "message": "...",
 *         "details": ...
 *     }
 */
export interface ApiError {
  readonly code: string;

  readonly message: string;

  readonly details: JsonValue;
}

/**
 * Standard error response.
 *
 * The backend currently identifies an error response through:
 *
 *     success: false
 *
 * and does not emit a top-level:
 *
 *     status: "error"
 *
 * Therefore `status` is intentionally not required here.
 */
export interface ApiErrorResponse {
  readonly success: false;

  readonly error: ApiError;

  readonly meta: ApiMeta;
}

/* =============================================================================
 * Unified Response
 * =============================================================================
 */

/**
 * Standard DatavionOS API response.
 */
export type ApiResponse<
  T = null,
> =
  | ApiSuccessResponse<T>
  | ApiErrorResponse;

/* =============================================================================
 * Pagination
 * =============================================================================
 */

/**
 * Pagination metadata.
 */
export type ApiPagination = {
  readonly count: number;

  readonly page: number;

  readonly page_size: number;

  readonly total_pages: number;

  readonly next: string | null;

  readonly previous: string | null;
};

/**
 * API metadata with pagination.
 */
export interface PaginatedApiMeta
  extends ApiMeta {
  readonly pagination: ApiPagination;
}

/**
 * Paginated successful response.
 */
export interface PaginatedApiResponse<
  T,
> {
  readonly success: true;

  readonly message: string;

  readonly data: readonly T[];

  readonly meta: PaginatedApiMeta;
}

/* =============================================================================
 * HTTP Error
 * =============================================================================
 */

/**
 * Normalized frontend HTTP error.
 */
export interface ApiHttpError {
  readonly statusCode: number;

  readonly code: string;

  readonly message: string;

  readonly details: JsonValue;

  readonly meta: ApiMeta | null;
}

/* =============================================================================
 * Request Configuration
 * =============================================================================
 */

/**
 * DatavionOS-specific request options.
 *
 * Axios owns generic request options such as:
 *
 * - signal
 * - timeout
 * - headers
 * - params
 * - method
 *
 * This interface therefore contains only DatavionOS transport concerns.
 */
export interface ApiRequestOptions {
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
 * Type Guards
 * =============================================================================
 */

/**
 * Determine whether an API response is successful.
 *
 * The generic type is preserved so response.data remains correctly typed
 * after narrowing.
 */
export function isApiSuccess<T>(
  response: ApiResponse<T>,
): response is ApiSuccessResponse<T> {
  return response.success === true;
}

/**
 * Determine whether an API response is an error.
 */
export function isApiErrorResponse<T>(
  response: ApiResponse<T>,
): response is ApiErrorResponse {
  return response.success === false;
}
