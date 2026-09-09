/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/domain/types.ts
 * =============================================================================
 *
 * Authentication feature type compatibility boundary.
 *
 * IMPORTANT
 * ---------
 * Canonical authentication contracts live in:
 *
 *     @/core/types/auth
 *
 * This module intentionally contains no independent authentication models.
 *
 * Feature-level authentication code may import these types from this module
 * for backward compatibility, while the actual contracts remain owned by
 * the core authentication domain.
 *
 * Design Principles
 * -----------------
 * - Single Source of Truth
 * - No Duplicate Domain Models
 * - Backward Compatible Imports
 * - Backend Contract Aligned
 * - Strong TypeScript Typing
 * - Enterprise Ready
 * =============================================================================
 */

export type {
    AuthenticatedUser,
    AuthResult,
    AuthSession,
    AuthTokenPair,
    AuthUser,
    AuthUserIdentity,
    AuthenticationResponse,
    ChangePasswordRequest,
    CurrentUser,
    CurrentUserRequest,
    CurrentUserResponse,
    ForgotPasswordRequest,
    LoginRequest,
    LoginOtpResponse,
    LoginOTPRequestResponse,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    OAuthAccount,
    OAuthLoginRequest,
    OAuthLoginResponse,
    OTP,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    RegisterResponse,
    ResendVerificationRequest,
    ResetPasswordRequest,
    TokenPair,
    UserProfile,
    UserSession,
    VerifyEmailRequest,
    VerifyLoginOtpRequest,
    VerifyLoginOTPRequest,
} from "@/core/types/auth";
