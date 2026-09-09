/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/provider.tsx
 * =============================================================================
 *
 * React authentication provider.
 *
 * Responsibilities
 * ----------------
 * - Initialize authentication state.
 * - Restore an existing authenticated session.
 * - Expose authentication state through React Context.
 * - Coordinate AuthService with AuthenticationStore.
 * - Handle authentication state transitions.
 * - Expose password-management operations through the canonical auth boundary.
 *
 * AuthenticationStore remains the single source of truth.
 *
 * React consumes the external authentication store through
 * useSyncExternalStore.
 *
 * Design Principles
 * -----------------
 * - Single Source of Truth
 * - Thin React boundary
 * - No direct browser storage access
 * - No direct HTTP access
 * - Service-driven authentication
 * - SSR Safe
 * - Strict TypeScript
 * - Concurrent React compatible
 * - Enterprise Ready
 * =============================================================================
 */

"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useSyncExternalStore,
  type ReactNode,
} from "react";

import {
  AuthService,
} from "./service";

import {
  authStore,
} from "./store";

import type {
  AuthSession,
  AuthState,
  ChangePasswordRequest,
  ForgotPasswordRequest,
  LoginOTPRequestResponse,
  LoginRequest,
  RegisterRequest,
  RegisterResponse,
  ResetPasswordRequest,
  VerifyLoginOTPRequest,
} from "./types";

/* =============================================================================
 * Context Types
 * =============================================================================
 */

export interface AuthContextValue
  extends AuthState {
  /**
   * Whether an authentication operation is currently in progress.
   */
  readonly isLoading: boolean;

  /**
   * Initialize or restore the authentication session.
   */
  initialize(): Promise<void>;

  /**
   * Request a login OTP.
   */
  requestLoginOTP(
    request: LoginRequest,
  ): Promise<LoginOTPRequestResponse>;

  /**
   * Verify the login OTP.
   */
  verifyLoginOTP(
    request: VerifyLoginOTPRequest,
  ): Promise<AuthSession>;

  /**
   * Register a new SaaS account.
   */
  register(
    request: RegisterRequest,
  ): Promise<RegisterResponse>;

  /**
   * Request a password-reset OTP.
   *
   * This operation does not require an authenticated session.
   */
  forgotPassword(
    request: ForgotPasswordRequest,
  ): Promise<void>;

  /**
   * Reset a password using the password-reset OTP.
   *
   * This operation does not require an authenticated session.
   */
  resetPassword(
    request: ResetPasswordRequest,
  ): Promise<void>;

  /**
   * Change the password for an authenticated user.
   */
  changePassword(
    request: ChangePasswordRequest,
  ): Promise<void>;

  /**
   * Refresh the current authentication session.
   */
  refresh(): Promise<void>;

  /**
   * Logout the current authentication session.
   */
  logout(): Promise<void>;

  /**
   * Clear local authentication state.
   */
  clearSession(): void;
}

/* =============================================================================
 * Context
 * =============================================================================
 */

const AuthContext =
  createContext<
    AuthContextValue | undefined
  >(undefined);

/* =============================================================================
 * Provider Props
 * =============================================================================
 */

export interface AuthProviderProps {
  readonly children: ReactNode;

  /**
   * Authentication service injected by the application composition layer.
   */
  readonly service: AuthService;
}

/* =============================================================================
 * Provider
 * =============================================================================
 */

export function AuthProvider({
  children,
  service,
}: AuthProviderProps) {
  /* ===========================================================================
   * External Store Integration
   * =========================================================================== */

  /**
   * IMPORTANT:
   *
   * AuthenticationStore methods rely on their class instance (`this`).
   *
   * We therefore MUST NOT pass:
   *
   *     authStore.getState
   *     authStore.subscribe
   *
   * directly to React.
   *
   * React invokes these callbacks independently from the authStore object.
   *
   * These wrappers preserve the correct authStore receiver.
   */
  const subscribe =
    useCallback(
      (
        listener: (
          state: AuthState,
        ) => void,
      ) => {
        return authStore.subscribe(
          listener,
        );
      },
      [],
    );

  const getSnapshot =
    useCallback(
      (): AuthState => {
        return authStore.getState();
      },
      [],
    );

  /*
   * AuthenticationStore is the single source of truth.
   */
  const state =
    useSyncExternalStore(
      subscribe,
      getSnapshot,
      getSnapshot,
    );

  /**
   * Prevent duplicate authentication initialization.
   */
  const initializationStarted =
    useRef(false);

  /**
   * Generation counter used to prevent stale asynchronous operations from
   * overwriting newer authentication state.
   */
  const authenticationGeneration =
    useRef(0);

  /* ===========================================================================
   * Initialization
   * =========================================================================== */

  const initialize =
    useCallback(
      async (): Promise<void> => {
        if (
          initializationStarted.current
        ) {
          return;
        }

        initializationStarted.current =
          true;

        const generation =
          authenticationGeneration.current;

        authStore.setState({
          status:
            "authenticating",
          error: null,
        });

        try {
          /*
           * A newer authentication operation has superseded initialization.
           */
          if (
            generation !==
            authenticationGeneration.current
          ) {
            return;
          }

          /*
           * No access token exists.
           *
           * Only mark the session unauthenticated if no newer authentication
           * operation has started.
           */
          if (
            !service.isAuthenticated()
          ) {
            if (
              generation ===
              authenticationGeneration.current
            ) {
              authStore.unauthenticate();
            }

            return;
          }

          /*
           * Retrieve the authoritative authenticated user from the backend.
           */
          const user =
            await service.getCurrentUser();

          /*
           * Do not allow stale initialization to overwrite a newer login,
           * logout, refresh, or session-clear operation.
           */
          if (
            generation !==
            authenticationGeneration.current
          ) {
            return;
          }

          authStore.authenticate(
            user,
          );
        } catch (error) {
          if (
            generation !==
            authenticationGeneration.current
          ) {
            return;
          }

          service.clearLocalSession();

          authStore.setState({
            status:
              "unauthenticated",
            user: null,
            isAuthenticated: false,
            isInitialized: true,
            error:
              getErrorMessage(
                error,
              ),
          });
        }
      },
      [service],
    );

  /* ===========================================================================
   * Initial Mount
   * =========================================================================== */

  useEffect(() => {
    void initialize();
  }, [initialize]);

  /* ===========================================================================
   * Login OTP Request
   * =========================================================================== */

  const requestLoginOTP =
    useCallback(
      async (
        request: LoginRequest,
      ): Promise<LoginOTPRequestResponse> => {
        /*
         * This authentication operation supersedes initialization.
         */
        authenticationGeneration.current +=
          1;

        authStore.setState({
          status:
            "authenticating",
          error: null,
        });

        try {
          const result =
            await service.requestLoginOTP(
              request,
            );

          /*
           * Credentials are valid, but the account is not authenticated yet.
           *
           * Authentication only becomes true after OTP verification.
           */
          authStore.setState({
            status:
              "unauthenticated",
            isAuthenticated: false,
            error: null,
          });

          return result;
        } catch (error) {
          authStore.setState({
            status:
              "unauthenticated",
            isAuthenticated: false,
            error:
              getErrorMessage(
                error,
              ),
          });

          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Login OTP Verification
   * =========================================================================== */

  const verifyLoginOTP =
    useCallback(
      async (
        request: VerifyLoginOTPRequest,
      ): Promise<AuthSession> => {
        /*
         * OTP verification is now the authoritative authentication operation.
         */
        authenticationGeneration.current +=
          1;

        const generation =
          authenticationGeneration.current;

        authStore.setState({
          status:
            "authenticating",
          error: null,
        });

        try {
          /*
           * AuthService performs:
           *
           *   1. OTP verification.
           *   2. Access-token persistence.
           *   3. Refresh-token persistence.
           *   4. /auth/me/ retrieval.
           */
          const session =
            await service.verifyLoginOTP(
              request,
            );

          /*
           * Ignore the result if another authentication operation has already
           * superseded this one.
           */
          if (
            generation !==
            authenticationGeneration.current
          ) {
            return session;
          }

          /*
           * This publishes the authenticated state to every React consumer
           * subscribed through useSyncExternalStore.
           */
          authStore.authenticate(
            session.user,
          );

          return session;
        } catch (error) {
          if (
            generation ===
            authenticationGeneration.current
          ) {
            authStore.setState({
              status:
                "unauthenticated",
              isAuthenticated: false,
              error:
                getErrorMessage(
                  error,
                ),
            });
          }

          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Registration
   * =========================================================================== */

  const register =
    useCallback(
      async (
        request: RegisterRequest,
      ): Promise<RegisterResponse> => {
        authStore.setError(
          null,
        );

        try {
          return await service.register(
            request,
          );
        } catch (error) {
          authStore.setError(
            getErrorMessage(
              error,
            ),
          );

          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Forgot Password
   * =========================================================================== */

  const forgotPassword =
    useCallback(
      async (
        request: ForgotPasswordRequest,
      ): Promise<void> => {
        /*
         * Password recovery is intentionally independent from the current
         * authenticated session.
         *
         * AuthService owns the actual HTTP request and backend contract.
         */
        try {
          await service.forgotPassword(
            request,
          );
        } catch (error) {
          /*
           * Do not mutate authentication state for a password-recovery
           * operation. The user may be completely unauthenticated.
           */
          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Reset Password
   * =========================================================================== */

  const resetPassword =
    useCallback(
      async (
        request: ResetPasswordRequest,
      ): Promise<void> => {
        /*
         * Password reset is a public authentication operation.
         *
         * AuthService handles the backend contract, including the OTP.
         */
        try {
          await service.resetPassword(
            request,
          );
        } catch (error) {
          /*
           * Do not mutate authenticated session state when the reset request
           * fails. Password-reset state belongs to the consuming feature flow.
           */
          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Change Password
   * =========================================================================== */

  const changePassword =
    useCallback(
      async (
        request: ChangePasswordRequest,
      ): Promise<void> => {
        /*
         * Change-password is an authenticated operation.
         *
         * AuthService owns the actual HTTP request and authentication context.
         */
        try {
          await service.changePassword(
            request,
          );
        } catch (error) {
          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Refresh
   * =========================================================================== */

  const refresh =
    useCallback(
      async (): Promise<void> => {
        authenticationGeneration.current +=
          1;

        const generation =
          authenticationGeneration.current;

        authStore.setStatus(
          "refreshing",
        );

        authStore.setError(
          null,
        );

        try {
          await service.refreshToken();

          const user =
            await service.getCurrentUser();

          if (
            generation !==
            authenticationGeneration.current
          ) {
            return;
          }

          authStore.authenticate(
            user,
          );
        } catch (error) {
          if (
            generation !==
            authenticationGeneration.current
          ) {
            return;
          }

          service.clearLocalSession();

          authStore.setState({
            status:
              "unauthenticated",
            user: null,
            isAuthenticated: false,
            isInitialized: true,
            error:
              getErrorMessage(
                error,
              ),
          });

          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Logout
   * =========================================================================== */

  const logout =
    useCallback(
      async (): Promise<void> => {
        authenticationGeneration.current +=
          1;

        authStore.setStatus(
          "logging_out",
        );

        authStore.setError(
          null,
        );

        try {
          await service.logout();

          authStore.unauthenticate();
        } catch (error) {
          service.clearLocalSession();

          authStore.setState({
            status:
              "unauthenticated",
            user: null,
            isAuthenticated: false,
            isInitialized: true,
            error:
              getErrorMessage(
                error,
              ),
          });

          throw error;
        }
      },
      [service],
    );

  /* ===========================================================================
   * Clear Session
   * =========================================================================== */

  const clearSession =
    useCallback(
      (): void => {
        authenticationGeneration.current +=
          1;

        service.clearLocalSession();

        authStore.unauthenticate();
      },
      [service],
    );

  /* ===========================================================================
   * Loading State
   * =========================================================================== */

  const isLoading =
    state.status ===
      "authenticating" ||
    state.status ===
      "refreshing" ||
    state.status ===
      "logging_out";

  /* ===========================================================================
   * Context Value
   * =========================================================================== */

  const value =
    useMemo<AuthContextValue>(
      () => ({
        ...state,

        isLoading,

        initialize,

        requestLoginOTP,

        verifyLoginOTP,

        register,

        forgotPassword,

        resetPassword,

        changePassword,

        refresh,

        logout,

        clearSession,
      }),
      [
        state,
        isLoading,
        initialize,
        requestLoginOTP,
        verifyLoginOTP,
        register,
        forgotPassword,
        resetPassword,
        changePassword,
        refresh,
        logout,
        clearSession,
      ],
    );

  return (
    <AuthContext.Provider
      value={value}
    >
      {children}
    </AuthContext.Provider>
  );
}

/* =============================================================================
 * Hook
 * =============================================================================
 */

export function useAuth(): AuthContextValue {
  const context =
    useContext(
      AuthContext,
    );

  if (
    context === undefined
  ) {
    throw new Error(
      "useAuth must be used inside AuthProvider.",
    );
  }

  return context;
}

/* =============================================================================
 * Error Handling
 * =============================================================================
 */

function getErrorMessage(
  error: unknown,
): string {
  if (
    error instanceof Error &&
    error.message.trim()
  ) {
    return error.message;
  }

  return (
    "An unexpected authentication error occurred."
  );
}
