/**
 * Authentication storage service.
 */

import type {
  AuthSession,
  AuthTokens,
  User,
} from "../domain/types";

const ACCESS_TOKEN_KEY = "datavion.access";
const REFRESH_TOKEN_KEY = "datavion.refresh";
const USER_KEY = "datavion.user";

export const authStorage = {
  getAccessToken(): string | null {
    return localStorage.getItem(
      ACCESS_TOKEN_KEY,
    );
  },

  setAccessToken(
    token: string,
  ): void {
    localStorage.setItem(
      ACCESS_TOKEN_KEY,
      token,
    );
  },

  getRefreshToken(): string | null {
    return localStorage.getItem(
      REFRESH_TOKEN_KEY,
    );
  },

  setRefreshToken(
    token: string,
  ): void {
    localStorage.setItem(
      REFRESH_TOKEN_KEY,
      token,
    );
  },

  getUser(): User | null {
    const value = localStorage.getItem(
      USER_KEY,
    );

    if (!value) {
      return null;
    }

    return JSON.parse(value) as User;
  },

  setUser(
    user: User,
  ): void {
    localStorage.setItem(
      USER_KEY,
      JSON.stringify(user),
    );
  },

  saveSession(
    session: AuthSession,
  ): void {
    this.setAccessToken(
      session.tokens.access,
    );

    this.setRefreshToken(
      session.tokens.refresh,
    );

    this.setUser(
      session.user,
    );
  },

  clear(): void {
    localStorage.removeItem(
      ACCESS_TOKEN_KEY,
    );

    localStorage.removeItem(
      REFRESH_TOKEN_KEY,
    );

    localStorage.removeItem(
      USER_KEY,
    );
  },
};
