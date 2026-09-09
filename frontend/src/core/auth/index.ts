/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/index.ts
 * =============================================================================
 *
 * Public entry point for the DatavionOS authentication subsystem.
 *
 * Application code should import authentication functionality from:
 *
 *     @/core/auth
 *
 * Internal implementation files should not be imported directly by feature
 * modules.
 *
 * Design Principles
 * -----------------
 * - Stable public API
 * - Explicit exports
 * - Encapsulation
 * - Single Authentication Type System
 * - No circular dependencies
 * - Enterprise Ready
 * =============================================================================
 */

/* =============================================================================
 * Authentication Types
 * =============================================================================
 *
 * The canonical authentication contracts are owned by:
 *
 *     @/core/types/auth
 *
 * ./types is only a compatibility re-export boundary.
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

/* =============================================================================
 * Authentication Constants
 * =============================================================================
 */

export {
  AUTH_API_PATHS,
  AUTH_ERROR_CODES,
  AUTH_HEADERS,
  AUTH_REDIRECTS,
  AUTH_ROUTES,
  AUTH_SCHEME,
  AUTH_STORAGE,
  AUTH_TIMING,
  OAUTH_PROVIDERS,
  OTP_CONFIG,
  OTP_PURPOSES,
  PASSWORD_POLICY,
} from "./constants";

export type {
  AuthApiPath,
  AuthErrorCode,
  AuthRoute,
} from "./constants";

/* =============================================================================
 * Authentication Service
 * =============================================================================
 */

export {
  AuthService,
  createAuthService,
} from "./service";

export type {
  AuthServiceDependencies,
} from "./service";

/* =============================================================================
 * Authentication Store
 * =============================================================================
 */

export {
  AuthenticationStore,
  authStore,
  getAuthenticatedUser,
  isAuthenticated,
} from "./store";

export type {
  AuthStateListener,
  AuthStatePatch,
  AuthStore,
} from "./store";

/* =============================================================================
 * Authentication Provider
 * =============================================================================
 */

export {
  AuthProvider,
  useAuth,
} from "./provider";

export type {
  AuthContextValue,
  AuthProviderProps,
} from "./provider";

/* =============================================================================
 * Authentication Composition
 * =============================================================================
 */

export {
  authRuntime,
  createAuthRuntime,
} from "./composition";

export type {
  AuthCompositionOptions,
  AuthRuntime,
} from "./composition";
