/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/types.ts
 * =============================================================================
 *
 * Authentication type compatibility boundary.
 *
 * IMPORTANT
 * ---------
 * The canonical authentication contracts live in:
 *
 *     @/core/types/auth
 *
 * This module intentionally contains no independent authentication models.
 *
 * It exists only to preserve stable imports for the authentication subsystem.
 *
 * Design Principles
 * -----------------
 * - Single Source of Truth
 * - Backward Compatible Imports
 * - No Duplicate Domain Models
 * - Backend Contract Aligned
 * - Strong TypeScript Typing
 * - Enterprise Ready
 * =============================================================================
 */

export type {
  AuthenticatedUser,
  AuthResult,
  AuthSession,
  AuthState,
  AuthStatus,
  AuthTokenPair,
  AuthUser,
  AuthUserIdentity,
  AuthenticationContextValue,
  AuthenticationResponse,
  AuthenticationState,
  ChangePasswordRequest,
  CurrentUser,
  CurrentUserRequest,
  CurrentUserResponse,
  ForgotPasswordRequest,
  LoginAttempt,
  LoginAttemptStatus,
  LoginFailureReason,
  LoginOtpResponse,
  LoginOTPRequestResponse,
  LoginRequest,
  LoginResponse,
  LogoutRequest,
  LogoutResponse,
  OAuthAccount,
  OAuthLoginRequest,
  OAuthLoginResponse,
  OTP,
  OTPContext,
  OTPState,
  RefreshTokenRequest,
  RefreshTokenResponse,
  RegisterRequest,
  RegisterResponse,
  ResendVerificationRequest,
  ResetPasswordRequest,
  TokenPair,
  UserProfile,
  UserSession,
  UserSessionStatus,
  VerifyEmailRequest,
  VerifyLoginOtpRequest,
  VerifyLoginOTPRequest,
} from "@/core/types/auth";

export {
  INITIAL_AUTH_STATE,
  isAuthenticatedState,
  isOAuthProvider,
  isOTPPurpose,
} from "@/core/types/auth";
