/**
 * Authentication service.
 */

import { login } from "../api/mutations";

import type {
  LoginRequest,
  LoginResponse,
} from "../domain/types";

import { authStorage } from "./auth-storage";

class AuthService {
  async login(
    payload: LoginRequest,
  ): Promise<LoginResponse> {
    const response = await login(
      payload,
    );

    authStorage.saveSession({
      user: response.user,

      tokens: {
        access: response.access,
        refresh: response.refresh,
      },
    });

    return response;
  }

  logout(): void {
    authStorage.clear();
  }

  getAccessToken(): string | null {
    return authStorage.getAccessToken();
  }

  getRefreshToken(): string | null {
    return authStorage.getRefreshToken();
  }

  getCurrentUser() {
    return authStorage.getUser();
  }

  isAuthenticated(): boolean {
    return !!authStorage.getAccessToken();
  }
}

export const authService =
  new AuthService();
