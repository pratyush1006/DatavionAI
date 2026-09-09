/**
 * =============================================================================
 * DatavionOS
 * File: src/core/types/index.ts
 * =============================================================================
 *
 * Public type boundary for the DatavionOS frontend core.
 *
 * Feature modules should import shared contracts from:
 *
 *     @/core/types
 *
 * rather than reaching directly into individual type files.
 *
 * Design Principles
 * -----------------
 * - Stable public API
 * - Explicit exports
 * - No runtime dependencies
 * - No business logic
 * - Strong TypeScript boundaries
 * - Enterprise Ready
 *
 * =============================================================================
 */

/* =============================================================================
 * API
 * =============================================================================
 */

export type {
    ApiError,
    ApiErrorResponse,
    ApiHttpError,
    ApiMeta,
    ApiPagination,
    ApiRequestOptions,
    ApiResponse,
    ApiSuccessResponse,
    JsonObject,
    JsonPrimitive,
    JsonValue,
    PaginatedApiMeta,
    PaginatedApiResponse,
    UUID,
    ISODateTime,
} from "./api";

/* =============================================================================
 * Authentication Enumerations
 * =============================================================================
 */

export {
    LoginAttemptStatus,
    LoginFailureReason,
    OAuthProvider,
    OTPChannel,
    OTPPurpose,
    UserSessionStatus,
} from "./auth";

/* =============================================================================
 * Authentication Contracts
 * =============================================================================
 */

export type {
    AuthenticatedUser,
    AuthenticationContextValue,
    AuthenticationResponse,
    AuthenticationState,
    AuthSession,
    ChangePasswordRequest,
    CurrentUser,
    ForgotPasswordRequest,
    LoginAttempt,
    LoginOtpResponse,
    LoginRequest,
    LogoutRequest,
    OAuthAccount,
    OAuthLoginRequest,
    OTP,
    RefreshTokenRequest,
    RegisterRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    TokenPair,
    UserProfile,
    UserSession,
    VerifyEmailRequest,
    VerifyLoginOtpRequest,
} from "./auth";
