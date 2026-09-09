/**
 * =============================================================================
 * DatavionOS
 * File: src/core/types/auth.ts
 * =============================================================================
 *
 * Canonical authentication contracts for the DatavionOS frontend.
 *
 * This is the SINGLE SOURCE OF TRUTH for authentication types.
 *
 * Architecture
 * ------------
 *
 *     @/core/types/auth
 *              |
 *              +--------------------+
 *              |                    |
 *              v                    v
 *       @/core/auth/types     Feature modules
 *              |
 *              v
 *      AuthService / Store / Provider
 *
 * Design Principles
 * -----------------
 * - Single Source of Truth
 * - Backend Contract Aligned
 * - Strict TypeScript
 * - Immutable Contracts
 * - Multi-Tenant SaaS Ready
 * - SSR Safe
 * - No React Dependencies
 * - No API/transport dependencies
 * - Enterprise Ready
 * =============================================================================
 */

import type {
  UUID,
  ISODateTime,
} from "./api";

/* =============================================================================
 * Enumerations
 * =============================================================================
 */

export enum OAuthProvider {
  GOOGLE = "GOOGLE",
  MICROSOFT = "MICROSOFT",
}

export enum OTPChannel {
  EMAIL = "EMAIL",
  SMS = "SMS",
  WHATSAPP = "WHATSAPP",
  AUTHENTICATOR = "AUTHENTICATOR",
}

export enum OTPPurpose {
  EMAIL_VERIFICATION = "EMAIL_VERIFICATION",
  PASSWORD_RESET = "PASSWORD_RESET",
  LOGIN = "LOGIN",
  MFA = "MFA",
}

export enum UserSessionStatus {
  ACTIVE = "ACTIVE",
  REVOKED = "REVOKED",
  EXPIRED = "EXPIRED",
}

export enum LoginAttemptStatus {
  SUCCESS = "SUCCESS",
  FAILED = "FAILED",
  BLOCKED = "BLOCKED",
}

export enum LoginFailureReason {
  INVALID_PASSWORD = "INVALID_PASSWORD",
  USER_NOT_FOUND = "USER_NOT_FOUND",
  USER_INACTIVE = "USER_INACTIVE",
  EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED",
  ACCOUNT_LOCKED = "ACCOUNT_LOCKED",
}

/* =============================================================================
 * Authentication Lifecycle
 * =============================================================================
 */

/**
 * Authentication lifecycle status.
 *
 * This is frontend runtime state and is intentionally separate from
 * backend authentication response contracts.
 */
export type AuthStatus =
  | "unknown"
  | "unauthenticated"
  | "authenticating"
  | "authenticated"
  | "refreshing"
  | "logging_out";

/* =============================================================================
 * User
 * =============================================================================
 */

/**
 * Canonical authenticated user representation.
 */
export interface AuthenticatedUser {
  readonly id: UUID;

  readonly email: string;

  readonly first_name: string;

  readonly last_name: string;

  readonly phone: string;

  readonly employee_id: string | null;

  readonly is_verified: boolean;

  readonly is_active: boolean;

  readonly is_staff: boolean;

  readonly is_superuser: boolean;

  readonly is_internal_user: boolean;

  readonly organization: UUID | null;

  readonly last_login: ISODateTime | null;

  readonly created_at: ISODateTime;

  readonly updated_at: ISODateTime;
}

/**
 * User identity used by authentication runtime consumers.
 */
export type AuthUserIdentity =
  Pick<
    AuthenticatedUser,
    | "id"
    | "email"
    | "first_name"
    | "last_name"
  >;

/**
 * Canonical frontend authentication user.
 */
export type AuthUser =
  AuthenticatedUser;

/**
 * User profile/preferences.
 */
export interface UserProfile {
  readonly avatar: string | null;

  readonly timezone: string;

  readonly language: string;

  readonly theme: string;

  readonly locale: string;
}

/**
 * Current authenticated user.
 */
export interface CurrentUser
  extends AuthenticatedUser {
  readonly profile:
    | UserProfile
    | null;
}

/* =============================================================================
 * JWT
 * =============================================================================
 */

export interface TokenPair {
  readonly access: string;

  readonly refresh: string;
}

export type AuthTokenPair =
  TokenPair;

export interface RefreshTokenRequest {
  readonly refresh: string;
}

export interface RefreshTokenResponse {
  readonly access: string;
}

/* =============================================================================
 * Authentication Requests
 * =============================================================================
 */

export interface RegisterRequest {
  readonly email: string;

  readonly password: string;

  readonly first_name: string;

  readonly last_name: string;

  readonly organization_name: string;

  readonly organization_type: string;
}

export interface LoginRequest {
  readonly email: string;

  readonly password: string;
}

export interface VerifyLoginOtpRequest {
  readonly otp_id: UUID;

  readonly otp: string;
}

/**
 * Backward-compatible OTP request naming.
 */
export type VerifyLoginOTPRequest =
  VerifyLoginOtpRequest;

export interface LogoutRequest {
  readonly refresh: string;
}

export interface ForgotPasswordRequest {
  readonly email: string;
}

export interface ResetPasswordRequest {
  readonly email: string;

  readonly otp: string;

  readonly new_password: string;
}

export interface ChangePasswordRequest {
  readonly current_password: string;

  readonly new_password: string;
}

export interface VerifyEmailRequest {
  readonly email: string;

  readonly otp: string;
}

export interface ResendVerificationRequest {
  readonly email: string;
}

/* =============================================================================
 * Authentication Responses
 * =============================================================================
 */

/**
 * Login step-one response.
 *
 * POST /api/auth/login/
 *
 * Credentials are validated and an OTP challenge is generated.
 *
 * No JWT tokens are issued at this stage.
 */
export interface LoginOtpResponse {
  readonly otp_id: UUID;

  readonly requires_otp:
    | boolean
    | "True"
    | "False";

  readonly expires_at:
    | ISODateTime
    | null;
}

/**
 * Backward-compatible OTP response naming.
 */
export type LoginOTPRequestResponse =
  LoginOtpResponse;

/**
 * Completed authentication response.
 *
 * POST /api/auth/login/verify-otp/
 *
 * IMPORTANT:
 * The current backend returns ONLY the JWT token pair here.
 *
 * Example:
 *
 * {
 *   "success": true,
 *   "message": "Login successful.",
 *   "data": {
 *     "access": "...",
 *     "refresh": "..."
 *   }
 * }
 *
 * The authenticated user is retrieved separately through:
 *
 * GET /api/auth/me/
 */
export type AuthenticationResponse = TokenPair;

/**
 * LoginResponse represents the first step of the login workflow.
 */
export type LoginResponse =
  LoginOtpResponse;

/**
 * Completed authentication result.
 */
export type AuthResult =
  AuthenticationResponse;

/**
 * Explicit name for the completed login authentication response.
 */
export type LoginAuthenticationResponse =
  AuthenticationResponse;

export interface LogoutResponse {
  readonly success: boolean;
}

/**
 * Registration response.
 */
export interface RegisterResponse {
  readonly user?: CurrentUser;

  readonly organization_id?: UUID;

  readonly message?: string;

  readonly requires_email_verification?: boolean;
}

/**
 * Current-user request marker.
 */
export interface CurrentUserRequest {
  readonly include_profile?: boolean;
}

/**
 * Current-user response.
 */
export type CurrentUserResponse =
  CurrentUser;

/* =============================================================================
 * Authentication Session
 * =============================================================================
 */

export interface AuthSession {
  readonly user: CurrentUser;

  readonly tokens: TokenPair;
}

/* =============================================================================
 * Authentication Runtime State
 * =============================================================================
 */

/**
 * Canonical in-memory authentication state.
 *
 * AuthenticationResponse represents backend data.
 * AuthState represents frontend runtime state.
 */
export interface AuthState {
  readonly status: AuthStatus;

  readonly user:
    | AuthUser
    | null;

  readonly isAuthenticated: boolean;

  readonly isInitialized: boolean;

  readonly error: string | null;
}

/**
 * Initial authentication state.
 */
export const INITIAL_AUTH_STATE: AuthState =
  Object.freeze({
    status: "unknown",
    user: null,
    isAuthenticated: false,
    isInitialized: false,
    error: null,
  });

/**
 * Return whether authentication state is authenticated.
 */
export function isAuthenticatedState(
  state: AuthState,
): boolean {
  return (
    state.isAuthenticated === true &&
    state.status === "authenticated" &&
    state.user !== null
  );
}

/* =============================================================================
 * Legacy Authentication State
 * =============================================================================
 */

/**
 * Authentication state exposed by older consumers.
 *
 * Kept as a compatibility contract.
 *
 * New runtime state management should use AuthState.
 */
export interface AuthenticationState {
  readonly isAuthenticated: boolean;

  readonly isLoading: boolean;

  readonly user:
    | CurrentUser
    | null;

  readonly accessToken: string | null;

  readonly refreshToken: string | null;
}

/* =============================================================================
 * Authentication Context
 * =============================================================================
 */

export interface AuthenticationContextValue
  extends AuthenticationState {
  /**
   * Start login with email and password.
   *
   * This validates credentials and returns the OTP challenge.
   */
  login(
    request: LoginRequest,
  ): Promise<LoginOtpResponse>;

  /**
   * Complete login by verifying the OTP.
   *
   * Returns the completed authentication response containing the JWT tokens.
   *
   * The current user is resolved separately by the authentication service.
   */
  verifyLoginOtp(
    request: VerifyLoginOtpRequest,
  ): Promise<AuthenticationResponse>;

  register(
    request: RegisterRequest,
  ): Promise<void>;

  logout(): Promise<void>;

  refresh(): Promise<void>;

  forgotPassword(
    request: ForgotPasswordRequest,
  ): Promise<void>;

  resetPassword(
    request: ResetPasswordRequest,
  ): Promise<void>;

  verifyEmail(
    request: VerifyEmailRequest,
  ): Promise<void>;

  resendVerification(
    request: ResendVerificationRequest,
  ): Promise<void>;
}

/* =============================================================================
 * OAuth
 * =============================================================================
 */

export interface OAuthLoginRequest {
  readonly provider: OAuthProvider;

  readonly token: string;
}

export type OAuthLoginResponse = AuthenticationResponse;

export interface OAuthAccount {
  readonly id: UUID;

  readonly provider: OAuthProvider;

  readonly provider_user_id: string;

  readonly provider_username: string;

  readonly email: string;

  readonly avatar_url: string;

  readonly metadata:
    Readonly<
      Record<string, unknown>
    >;

  readonly token_metadata:
    Readonly<
      Record<string, unknown>
    >;

  readonly last_login_at:
    | ISODateTime
    | null;

  readonly last_synced_at:
    | ISODateTime
    | null;

  readonly is_active: boolean;
}

/**
 * Return whether a provider is supported.
 */
export function isOAuthProvider(
  value: string,
): value is OAuthProvider {
  return (
    value ===
      OAuthProvider.GOOGLE ||
    value ===
      OAuthProvider.MICROSOFT
  );
}

/* =============================================================================
 * OTP
 * =============================================================================
 */

export interface OTP {
  readonly id: UUID;

  readonly recipient: string;

  readonly channel: OTPChannel;

  readonly purpose: OTPPurpose;

  readonly expires_at: ISODateTime;

  readonly attempts: number;

  readonly max_attempts: number;

  readonly resend_count: number;

  readonly is_used: boolean;

  readonly used_at:
    | ISODateTime
    | null;

  readonly created_at: ISODateTime;
}

export interface OTPContext {
  readonly otp_id: UUID;

  readonly purpose: OTPPurpose;

  readonly channel: OTPChannel;

  readonly expires_at: ISODateTime;
}

export interface OTPState {
  readonly context: OTPContext | null;

  readonly isVerifying: boolean;

  readonly error: string | null;
}

/**
 * Return whether a value is a supported OTP purpose.
 */
export function isOTPPurpose(
  value: string,
): value is OTPPurpose {
  return (
    value ===
      OTPPurpose.EMAIL_VERIFICATION ||
    value ===
      OTPPurpose.PASSWORD_RESET ||
    value ===
      OTPPurpose.LOGIN ||
    value ===
      OTPPurpose.MFA
  );
}

/* =============================================================================
 * User Session
 * =============================================================================
 */

export interface UserSession {
  readonly id: UUID;

  readonly refresh_token_id: string;

  readonly status: UserSessionStatus;

  readonly device: string;

  readonly browser: string;

  readonly operating_system: string;

  readonly ip_address:
    | string
    | null;

  readonly location: string;

  readonly user_agent: string;

  readonly last_activity_at: ISODateTime;

  readonly revoked_at:
    | ISODateTime
    | null;

  readonly created_at: ISODateTime;
}

/* =============================================================================
 * Login Attempt
 * =============================================================================
 */

export interface LoginAttempt {
  readonly id: UUID;

  readonly email: string;

  readonly status: LoginAttemptStatus;

  readonly failure_reason:
    | LoginFailureReason
    | "";

  readonly ip_address:
    | string
    | null;

  readonly device: string;

  readonly location: string;

  readonly user_agent: string;

  readonly created_at: ISODateTime;
}
