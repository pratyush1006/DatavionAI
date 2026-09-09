/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/errors.ts
 * =============================================================================
 *
 * API error definitions and classification utilities.
 *
 * Responsibilities
 * ----------------
 * • Define stable frontend API error codes
 * • Map HTTP status codes to API error codes
 * • Provide safe user-facing fallback messages
 * • Identify authentication errors
 * • Identify retryable errors
 * • Keep error classification independent from Axios
 *
 * Design Principles
 * -----------------
 * • Backend contract aligned
 * • Framework agnostic
 * • No React dependencies
 * • No Axios dependency
 * • Stable error vocabulary
 * • Enterprise Ready
 * =============================================================================
 */

import type {
    ApiError,
    ApiHttpError,
    ApiMeta,
    JsonValue,
} from "@/core/types";

/* =============================================================================
 * Error Codes
 * =============================================================================
 */

export const API_ERROR_CODES = Object.freeze({
    BAD_REQUEST:
        "BAD_REQUEST",

    UNAUTHENTICATED:
        "UNAUTHENTICATED",

    FORBIDDEN:
        "FORBIDDEN",

    RESOURCE_NOT_FOUND:
        "RESOURCE_NOT_FOUND",

    OPERATION_NOT_ALLOWED:
        "OPERATION_NOT_ALLOWED",

    RESOURCE_CONFLICT:
        "RESOURCE_CONFLICT",

    UNSUPPORTED_MEDIA_TYPE:
        "UNSUPPORTED_MEDIA_TYPE",

    RATE_LIMIT_EXCEEDED:
        "RATE_LIMIT_EXCEEDED",

    INTERNAL_SERVER_ERROR:
        "INTERNAL_SERVER_ERROR",

    INVALID_API_RESPONSE:
        "INVALID_API_RESPONSE",

    NETWORK_ERROR:
        "NETWORK_ERROR",

    REQUEST_TIMEOUT:
        "REQUEST_TIMEOUT",

    REQUEST_CANCELLED:
        "REQUEST_CANCELLED",

    API_ERROR:
        "API_ERROR",
} as const);

export type ApiErrorCode =
    (typeof API_ERROR_CODES)[keyof typeof API_ERROR_CODES];

/* =============================================================================
 * HTTP Status Mapping
 * =============================================================================
 */

/**
 * Convert HTTP status to a stable frontend error code.
 */
export function getApiErrorCode(
    statusCode?: number,
): ApiErrorCode {
    switch (statusCode) {
        case 400:
            return API_ERROR_CODES.BAD_REQUEST;

        case 401:
            return API_ERROR_CODES.UNAUTHENTICATED;

        case 403:
            return API_ERROR_CODES.FORBIDDEN;

        case 404:
            return API_ERROR_CODES.RESOURCE_NOT_FOUND;

        case 405:
            return API_ERROR_CODES.OPERATION_NOT_ALLOWED;

        case 409:
            return API_ERROR_CODES.RESOURCE_CONFLICT;

        case 415:
            return API_ERROR_CODES.UNSUPPORTED_MEDIA_TYPE;

        case 429:
            return API_ERROR_CODES.RATE_LIMIT_EXCEEDED;

        case 500:
        case 501:
        case 502:
        case 503:
        case 504:
            return API_ERROR_CODES.INTERNAL_SERVER_ERROR;

        default:
            return API_ERROR_CODES.API_ERROR;
    }
}

/* =============================================================================
 * Fallback Messages
 * =============================================================================
 */

/**
 * Return a safe user-facing message for an HTTP status.
 */
export function getApiErrorMessage(
    statusCode?: number,
): string {
    switch (statusCode) {
        case 400:
            return "The request is invalid.";

        case 401:
            return "Authentication is required.";

        case 403:
            return "You do not have permission to perform this operation.";

        case 404:
            return "The requested resource was not found.";

        case 405:
            return "The requested operation is not allowed.";

        case 409:
            return "The requested operation conflicts with existing data.";

        case 415:
            return "The submitted content type is not supported.";

        case 429:
            return "Too many requests. Please try again later.";

        case 500:
        case 501:
        case 502:
        case 503:
        case 504:
            return "An unexpected server error occurred.";

        default:
            return "The request failed.";
    }
}

/* =============================================================================
 * Error Construction
 * =============================================================================
 */

/**
 * Create a normalized API HTTP error.
 */
export function createApiHttpError(
    options: {
        readonly statusCode: number;

        readonly error?: Partial<ApiError>;

        readonly meta?: ApiMeta | null;

        readonly details?: JsonValue;
    },
): ApiHttpError {
    const code =
        options.error?.code ??
        getApiErrorCode(
            options.statusCode,
        );

    const message =
        options.error?.message ??
        getApiErrorMessage(
            options.statusCode,
        );

    const details =
        options.error?.details ??
        options.details ??
        null;

    return {
        statusCode:
            options.statusCode,

        code,

        message,

        details,

        meta:
            options.meta ??
            null,
    };
}

/* =============================================================================
 * Error Classification
 * =============================================================================
 */

/**
 * Determine whether an error represents an authentication failure.
 */
export function isAuthenticationError(
    error: Pick<
        ApiHttpError,
        "statusCode" | "code"
    >,
): boolean {
    return (
        error.statusCode === 401 ||
        error.code ===
            API_ERROR_CODES.UNAUTHENTICATED
    );
}

/**
 * Determine whether an error represents a permission failure.
 */
export function isAuthorizationError(
    error: Pick<
        ApiHttpError,
        "statusCode" | "code"
    >,
): boolean {
    return (
        error.statusCode === 403 ||
        error.code ===
            API_ERROR_CODES.FORBIDDEN
    );
}

/**
 * Determine whether an error represents a missing resource.
 */
export function isNotFoundError(
    error: Pick<
        ApiHttpError,
        "statusCode" | "code"
    >,
): boolean {
    return (
        error.statusCode === 404 ||
        error.code ===
            API_ERROR_CODES.RESOURCE_NOT_FOUND
    );
}

/**
 * Determine whether an error represents a conflict.
 */
export function isConflictError(
    error: Pick<
        ApiHttpError,
        "statusCode" | "code"
    >,
): boolean {
    return (
        error.statusCode === 409 ||
        error.code ===
            API_ERROR_CODES.RESOURCE_CONFLICT
    );
}

/**
 * Determine whether an error is caused by rate limiting.
 */
export function isRateLimitError(
    error: Pick<
        ApiHttpError,
        "statusCode" | "code"
    >,
): boolean {
    return (
        error.statusCode === 429 ||
        error.code ===
            API_ERROR_CODES.RATE_LIMIT_EXCEEDED
    );
}

/**
 * Determine whether an error is retryable.
 *
 * Authentication failures are deliberately excluded because they require
 * authentication recovery rather than blind retrying.
 */
export function isRetryableError(
    error: Pick<
        ApiHttpError,
        "statusCode" | "code"
    >,
): boolean {
    if (
        isAuthenticationError(
            error,
        )
    ) {
        return false;
    }

    return (
        error.statusCode === 408 ||
        error.statusCode === 425 ||
        error.statusCode === 429 ||
        error.statusCode >= 500
    );
}

/* =============================================================================
 * Error Type Guards
 * =============================================================================
 */

/**
 * Determine whether an unknown value is an ApiHttpError.
 */
export function isApiHttpError(
    value: unknown,
): value is ApiHttpError {
    if (
        value === null ||
        typeof value !==
            "object"
    ) {
        return false;
    }

    const candidate =
        value as Record<
            string,
            unknown
        >;

    return (
        typeof candidate.statusCode ===
            "number" &&
        typeof candidate.code ===
            "string" &&
        typeof candidate.message ===
            "string" &&
        "details" in candidate &&
        "meta" in candidate
    );
}

/**
 * Determine whether a value is a known API error code.
 */
export function isApiErrorCode(
    value: string,
): value is ApiErrorCode {
    return (
        Object.values(
            API_ERROR_CODES,
        ) as readonly string[]
    ).includes(value);
}
