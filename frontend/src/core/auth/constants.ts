import { API_BASE_URL } from "@/core/api/config";
/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/constants.ts
 * =============================================================================
 *
 * Authentication constants.
 *
 * Single source of truth for frontend authentication configuration.
 *
 * Design Principles
 * -----------------
 * - Single Source of Truth
 * - Immutable
 * - Backend Aligned
 * - Type Safe
 * - No magic strings
 * - Enterprise Ready
 * =============================================================================
 */

/* =============================================================================
 * Authentication Routes
 * =============================================================================
 */

export const AUTH_ROUTES = Object.freeze({
    LOGIN: "/login",

    REGISTER: "/register",

    VERIFY_EMAIL: "/verify-email",

    FORGOT_PASSWORD: "/forgot-password",

    RESET_PASSWORD: "/reset-password",

    CHANGE_PASSWORD: "/change-password",

    AUTH_CALLBACK: "/auth/callback",
} as const);

/* =============================================================================
 * Authentication API Paths
 * =============================================================================
 *
 * These paths are relative to the configured API base URL.
 *
 * Current API base:
 *
 *     ${API_BASE_URL}
 *
 * Therefore:
 *
 *     /auth/login/
 *
 * resolves to:
 *
 *     ${API_BASE_URL}/auth/login/
 *
 * IMPORTANT
 * ---------
 * Do not add /accounts to these paths.
 * The canonical backend authentication routes are mounted directly below
 * /api/auth/.
 * =============================================================================
 */

export const AUTH_API_PATHS = Object.freeze({
    REGISTER:
        "/auth/register/",

    LOGIN:
        "/auth/login/",

    VERIFY_LOGIN_OTP:
        "/auth/login/verify-otp/",

    LOGOUT:
        "/auth/logout/",

    REFRESH:
        "/auth/refresh/",

    ME:
        "/auth/me/",

    VERIFY_EMAIL:
        "/auth/verify-email/",

    RESEND_EMAIL_VERIFICATION:
        "/auth/resend-verification/",

    FORGOT_PASSWORD:
        "/auth/forgot-password/",

    RESET_PASSWORD:
        "/auth/reset-password/",

    CHANGE_PASSWORD:
        "/auth/change-password/",

    OAUTH:
        "/auth/oauth/",
} as const);

/* =============================================================================
 * OAuth
 * =============================================================================
 */

export const OAUTH_PROVIDERS = Object.freeze({
    GOOGLE: "GOOGLE",

    MICROSOFT: "MICROSOFT",
} as const);

/* =============================================================================
 * OTP
 * =============================================================================
 */

export const OTP_CONFIG = Object.freeze({
    LENGTH: 6,

    DEFAULT_EXPIRY_SECONDS: 600,

    RESEND_INTERVAL_SECONDS: 30,

    MAX_ATTEMPTS: 5,

    PASSWORD_RESET_EXPIRY_SECONDS: 1_800,
} as const);

/**
 * OTP purposes.
 *
 * Values mirror the backend OTPPurpose choices.
 */
export const OTP_PURPOSES = Object.freeze({
    EMAIL_VERIFICATION:
        "EMAIL_VERIFICATION",

    PASSWORD_RESET:
        "PASSWORD_RESET",

    LOGIN:
        "LOGIN",

    MFA:
        "MFA",
} as const);

/* =============================================================================
 * Authentication Timing
 * =============================================================================
 */

export const AUTH_TIMING = Object.freeze({
    /**
     * Maximum time allowed for an API authentication request.
     */
    REQUEST_TIMEOUT_MS: 30_000,

    /**
     * Delay used while restoring authentication state.
     */
    INITIALIZATION_DELAY_MS: 0,

    /**
     * Delay before retrying a failed token refresh.
     */
    REFRESH_RETRY_DELAY_MS: 1_000,
} as const);

/* =============================================================================
 * Authentication Headers
 * =============================================================================
 */

export const AUTH_HEADERS = Object.freeze({
    AUTHORIZATION:
        "Authorization",

    REQUEST_ID:
        "X-Request-ID",

    TENANT_ID:
        "X-Tenant-ID",
} as const);

/**
 * Authorization scheme used for JWT access tokens.
 */
export const AUTH_SCHEME =
    "Bearer";

/* =============================================================================
 * Authentication Storage
 * =============================================================================
 */

export const AUTH_STORAGE = Object.freeze({
    ACCESS_TOKEN:
        "ACCESS_TOKEN",

    REFRESH_TOKEN:
        "REFRESH_TOKEN",

    CURRENT_USER:
        "CURRENT_USER",

    AUTH_STATE:
        "AUTH_STATE",

    CURRENT_TENANT:
        "CURRENT_TENANT",

    CURRENT_ORGANIZATION:
        "CURRENT_ORGANIZATION",
} as const);

/* =============================================================================
 * Authentication Error Codes
 * =============================================================================
 */

export const AUTH_ERROR_CODES = Object.freeze({
    UNAUTHENTICATED:
        "UNAUTHENTICATED",

    INVALID_CREDENTIALS:
        "INVALID_CREDENTIALS",

    INVALID_OTP:
        "INVALID_OTP",

    OTP_EXPIRED:
        "OTP_EXPIRED",

    OTP_MAX_ATTEMPTS:
        "OTP_MAX_ATTEMPTS",

    EMAIL_NOT_VERIFIED:
        "EMAIL_NOT_VERIFIED",

    ACCOUNT_INACTIVE:
        "ACCOUNT_INACTIVE",

    ACCOUNT_LOCKED:
        "ACCOUNT_LOCKED",

    TOKEN_EXPIRED:
        "TOKEN_EXPIRED",

    TOKEN_INVALID:
        "TOKEN_INVALID",

    REFRESH_FAILED:
        "REFRESH_FAILED",

    SESSION_EXPIRED:
        "SESSION_EXPIRED",

    OAUTH_FAILED:
        "OAUTH_FAILED",

    REGISTRATION_FAILED:
        "REGISTRATION_FAILED",

    PASSWORD_RESET_FAILED:
        "PASSWORD_RESET_FAILED",
} as const);

/* =============================================================================
 * Authentication Redirects
 * =============================================================================
 */

export const AUTH_REDIRECTS = Object.freeze({
    AFTER_LOGIN:
        "/dashboard",

    AFTER_LOGOUT:
        "/login",

    AFTER_REGISTER:
        "/verify-email",

    AFTER_EMAIL_VERIFICATION:
        "/login",

    AFTER_PASSWORD_RESET:
        "/login",

    UNAUTHENTICATED:
        "/login",

    FORBIDDEN:
        "/403",
} as const);

/* =============================================================================
 * Password Policy
 * =============================================================================
 *
 * These values are UI guidance only.
 *
 * The backend remains authoritative for password validation.
 * =============================================================================
 */

export const PASSWORD_POLICY =
    Object.freeze({
        MIN_LENGTH: 8,

        MAX_LENGTH: 128,

        REQUIRE_UPPERCASE: true,

        REQUIRE_LOWERCASE: true,

        REQUIRE_NUMBER: true,

        REQUIRE_SPECIAL_CHARACTER: true,
    } as const);

/* =============================================================================
 * Type Helpers
 * =============================================================================
 */

export type AuthRoute =
    (typeof AUTH_ROUTES)[keyof typeof AUTH_ROUTES];

export type AuthApiPath =
    (typeof AUTH_API_PATHS)[keyof typeof AUTH_API_PATHS];

export type OAuthProvider =
    (typeof OAUTH_PROVIDERS)[keyof typeof OAUTH_PROVIDERS];

export type OTPPurpose =
    (typeof OTP_PURPOSES)[keyof typeof OTP_PURPOSES];

export type AuthErrorCode =
    (typeof AUTH_ERROR_CODES)[keyof typeof AUTH_ERROR_CODES];

/* =============================================================================
 * Type Guards
 * =============================================================================
 */

/**
 * Return whether a value is a supported OAuth provider.
 */
export function isOAuthProvider(
    value: string,
): value is OAuthProvider {
    return (
        value ===
            OAUTH_PROVIDERS.GOOGLE ||
        value ===
            OAUTH_PROVIDERS.MICROSOFT
    );
}

/**
 * Return whether a value is a supported OTP purpose.
 */
export function isOTPPurpose(
    value: string,
): value is OTPPurpose {
    return (
        value ===
            OTP_PURPOSES.EMAIL_VERIFICATION ||
        value ===
            OTP_PURPOSES.PASSWORD_RESET ||
        value ===
            OTP_PURPOSES.LOGIN ||
        value ===
            OTP_PURPOSES.MFA
    );
}
