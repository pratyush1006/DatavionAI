/**
 * Authentication domain types.
 */

export interface User {
  readonly id: number;

  readonly email: string;

  readonly username: string;

  readonly firstName: string;

  readonly lastName: string;

  readonly isVerified: boolean;

  readonly isStaff: boolean;

  readonly isActive: boolean;
}

export interface LoginRequest {
  readonly email: string;

  readonly password: string;
}

export interface LoginResponse {
  readonly access: string;

  readonly refresh: string;

  readonly user: User;
}

export interface AuthTokens {
  readonly access: string;

  readonly refresh: string;
}

export interface AuthSession {
  readonly user: User;

  readonly tokens: AuthTokens;
}

export interface RefreshTokenRequest {
  readonly refresh: string;
}

export interface RefreshTokenResponse {
  readonly access: string;
}
