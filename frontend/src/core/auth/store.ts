/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/store.ts
 * =============================================================================
 *
 * Authentication state store.
 *
 * This module owns frontend authentication state only.
 *
 * It intentionally does NOT:
 *
 * - Make HTTP requests
 * - Persist JWT tokens directly
 * - Access localStorage/sessionStorage
 * - Contain React-specific logic
 * - Implement authentication business operations
 *
 * Authentication operations belong to AuthService.
 * Token persistence belongs to TokenStorage.
 * User persistence belongs to UserStorage.
 *
 * Design Principles
 * -----------------
 * - Single Responsibility
 * - Framework Agnostic
 * - Immutable State Updates
 * - Observable
 * - SSR Safe
 * - Strong Type Safety
 * - Enterprise Ready
 * =============================================================================
 */

import {
  INITIAL_AUTH_STATE,
  isAuthenticatedState,
} from "./types";

import type {
  AuthState,
  AuthStatus,
  AuthUser,
} from "./types";

/* =============================================================================
 * Types
 * =============================================================================
 */

/**
 * Listener invoked whenever authentication state changes.
 */
export type AuthStateListener = (
  state: AuthState,
) => void;

/**
 * Partial state accepted by internal state updates.
 */
export type AuthStatePatch =
  Partial<AuthState>;

/**
 * Authentication store contract.
 */
export interface AuthStore {
  getState(): AuthState;

  setState(
    patch: AuthStatePatch,
  ): void;

  setStatus(
    status: AuthStatus,
  ): void;

  setUser(
    user: AuthUser | null,
  ): void;

  setError(
    error: string | null,
  ): void;

  setInitialized(
    initialized: boolean,
  ): void;

  authenticate(
    user: AuthUser,
  ): void;

  unauthenticate(): void;

  reset(): void;

  subscribe(
    listener: AuthStateListener,
  ): () => void;
}

/* =============================================================================
 * Store Implementation
 * =============================================================================
 */

/**
 * In-memory authentication state store.
 *
 * This store deliberately remains small and focused.
 * It is not a generic application state-management framework.
 */
export class AuthenticationStore
  implements AuthStore
{
  private state: AuthState =
    Object.freeze({
      ...INITIAL_AUTH_STATE,
    });

  private readonly listeners =
    new Set<AuthStateListener>();

  /* ===========================================================================
   * State
   * ===========================================================================
   */

  /**
   * Return the current authentication state.
   */
  public getState(): AuthState {
    return this.state;
  }

  /**
   * Update authentication state.
   *
   * State is replaced rather than mutated.
   */
  public setState(
    patch: AuthStatePatch,
  ): void {
    const nextState: AuthState = {
      ...this.state,
      ...patch,
    };

    if (
      this.isSameState(
        this.state,
        nextState,
      )
    ) {
      return;
    }

    this.state =
      Object.freeze(
        nextState,
      );

    this.notify();
  }

  /**
   * Set authentication lifecycle status.
   */
  public setStatus(
    status: AuthStatus,
  ): void {
    const isAuthenticated =
      status === "authenticated";

    this.setState({
      status,
      isAuthenticated,
    });
  }

  /**
   * Set the authenticated user.
   *
   * A null user always represents an unauthenticated state.
   */
  public setUser(
    user: AuthUser | null,
  ): void {
    if (user === null) {
      this.setState({
        user: null,
        isAuthenticated: false,
        status: "unauthenticated",
      });

      return;
    }

    this.setState({
      user,
      isAuthenticated: true,
      status: "authenticated",
    });
  }

  /**
   * Set the authentication error.
   */
  public setError(
    error: string | null,
  ): void {
    this.setState({
      error,
    });
  }

  /**
   * Mark authentication initialization as complete.
   */
  public setInitialized(
    initialized: boolean,
  ): void {
    this.setState({
      isInitialized:
        initialized,
    });
  }

  /* ===========================================================================
   * Authentication State
   * ===========================================================================
   */

  /**
   * Mark the session as authenticated.
   */
  public authenticate(
    user: AuthUser,
  ): void {
    this.setState({
      status: "authenticated",
      user,
      isAuthenticated: true,
      isInitialized: true,
      error: null,
    });
  }

  /**
   * Clear the authenticated state.
   */
  public unauthenticate(): void {
    this.setState({
      status: "unauthenticated",
      user: null,
      isAuthenticated: false,
      isInitialized: true,
      error: null,
    });
  }

  /**
   * Reset the store to its initial state.
   */
  public reset(): void {
    const initialState =
      Object.freeze({
        ...INITIAL_AUTH_STATE,
      });

    if (
      this.isSameState(
        this.state,
        initialState,
      )
    ) {
      return;
    }

    this.state =
      initialState;

    this.notify();
  }

  /* ===========================================================================
   * Subscriptions
   * ===========================================================================
   */

  /**
   * Subscribe to authentication state changes.
   *
   * Returns an unsubscribe function.
   */
  public subscribe(
    listener: AuthStateListener,
  ): () => void {
    this.listeners.add(
      listener,
    );

    return () => {
      this.listeners.delete(
        listener,
      );
    };
  }

  /**
   * Notify all active subscribers.
   */
  private notify(): void {
    const state =
      this.state;

    for (
      const listener of
      this.listeners
    ) {
      listener(state);
    }
  }

  /* ===========================================================================
   * Comparison
   * ===========================================================================
   */

  /**
   * Avoid unnecessary state notifications.
   *
   * User identity intentionally uses reference equality.
   * Remaining fields use primitive equality.
   */
  private isSameState(
    current: AuthState,
    next: AuthState,
  ): boolean {
    return (
      current.status ===
        next.status &&
      current.user ===
        next.user &&
      current.isAuthenticated ===
        next.isAuthenticated &&
      current.isInitialized ===
        next.isInitialized &&
      current.error ===
        next.error
    );
  }
}

/* =============================================================================
 * Default Store
 * =============================================================================
 */

/**
 * Application-level authentication store.
 *
 * This contains only in-memory state.
 * It does not persist credentials.
 */
export const authStore =
  new AuthenticationStore();

/* =============================================================================
 * Helpers
 * =============================================================================
 */

/**
 * Return whether the store currently represents an authenticated state.
 */
export function isAuthenticated(): boolean {
  return isAuthenticatedState(
    authStore.getState(),
  );
}

/**
 * Return the currently authenticated user.
 */
export function getAuthenticatedUser():
  | AuthUser
  | null {
  return authStore.getState()
    .user;
}
