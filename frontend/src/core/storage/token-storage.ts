/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/token-storage.ts
 * =============================================================================
 *
 * Authentication token storage.
 *
 * Responsibilities
 * ----------------
 * • Store access tokens
 * • Store refresh tokens
 * • Read authentication tokens
 * • Determine whether authentication tokens exist
 * • Clear authentication tokens
 * • Keep token persistence isolated from authentication business logic
 *
 * Security Note
 * -------------
 * This class does not make browser storage cryptographically secure.
 *
 * SecureStorage provides the controlled persistence boundary, but tokens stored
 * in browser-accessible storage remain accessible to same-origin JavaScript.
 *
 * The backend authentication strategy should ultimately determine whether
 * refresh tokens are persisted in browser storage or migrated to HttpOnly,
 * Secure, SameSite cookies.
 *
 * Design Principles
 * -----------------
 * • Single Responsibility
 * • Dependency Inversion
 * • Provider Agnostic
 * • Type Safe
 * • SSR Safe
 * • No Direct Browser API Access
 * • Enterprise Ready
 * =============================================================================
 */

import {
    STORAGE_KEYS,
} from "./keys";

import {
    SecureStorage,
} from "./secure-storage";

/* =============================================================================
 * Types
 * =============================================================================
 */

/**
 * Authentication token pair returned by the backend.
 */
export interface AuthTokens {
    readonly access: string;

    readonly refresh: string;
}

/**
 * Optional token expiration configuration.
 */
export interface TokenStorageOptions {
    /**
     * Optional expiration timestamp for the access token.
     */
    readonly accessExpiresAt?: string;

    /**
     * Optional expiration timestamp for the refresh token.
     */
    readonly refreshExpiresAt?: string;
}

/* =============================================================================
 * Token Storage
 * =============================================================================
 */

/**
 * Authentication token persistence service.
 */
export class TokenStorage {
    private readonly storage: SecureStorage;

    /**
     * Create token storage.
     */
    public constructor(
        storage: SecureStorage,
    ) {
        this.storage = storage;
    }

    /**
     * Store an access token.
     */
    public setAccessToken(
        token: string,
        expiresAt?: string,
    ): void {
        const normalizedToken =
            token.trim();

        if (!normalizedToken) {
            throw new Error(
                "Access token cannot be empty.",
            );
        }

        this.storage.set(
            STORAGE_KEYS.ACCESS_TOKEN,
            normalizedToken,
            expiresAt
                ? {
                      expiresAt,
                  }
                : undefined,
        );
    }

    /**
     * Store a refresh token.
     */
    public setRefreshToken(
        token: string,
        expiresAt?: string,
    ): void {
        const normalizedToken =
            token.trim();

        if (!normalizedToken) {
            throw new Error(
                "Refresh token cannot be empty.",
            );
        }

        this.storage.set(
            STORAGE_KEYS.REFRESH_TOKEN,
            normalizedToken,
            expiresAt
                ? {
                      expiresAt,
                  }
                : undefined,
        );
    }

    /**
     * Store both authentication tokens.
     */
    public setTokens(
        tokens: AuthTokens,
        options?: TokenStorageOptions,
    ): void {
        const accessToken =
            tokens.access.trim();

        const refreshToken =
            tokens.refresh.trim();

        if (!accessToken) {
            throw new Error(
                "Access token cannot be empty.",
            );
        }

        if (!refreshToken) {
            throw new Error(
                "Refresh token cannot be empty.",
            );
        }

        this.setAccessToken(
            accessToken,
            options?.accessExpiresAt,
        );

        try {
            this.setRefreshToken(
                refreshToken,
                options?.refreshExpiresAt,
            );
        } catch (error) {
            /*
             * Avoid leaving a newly written access token behind when the
             * refresh-token write fails.
             */
            this.storage.remove(
                STORAGE_KEYS.ACCESS_TOKEN,
            );

            throw error;
        }
    }

    /**
     * Return the access token.
     */
    public getAccessToken(): string | null {
        return this.storage.get<string>(
            STORAGE_KEYS.ACCESS_TOKEN,
        );
    }

    /**
     * Return the refresh token.
     */
    public getRefreshToken(): string | null {
        return this.storage.get<string>(
            STORAGE_KEYS.REFRESH_TOKEN,
        );
    }

    /**
     * Return both tokens.
     *
     * Returns null when either token is unavailable.
     */
    public getTokens(): AuthTokens | null {
        const access =
            this.getAccessToken();

        const refresh =
            this.getRefreshToken();

        if (!access || !refresh) {
            return null;
        }

        return {
            access,
            refresh,
        };
    }

    /**
     * Return whether an access token exists.
     */
    public hasAccessToken(): boolean {
        return this.storage.has(
            STORAGE_KEYS.ACCESS_TOKEN,
        );
    }

    /**
     * Return whether a refresh token exists.
     */
    public hasRefreshToken(): boolean {
        return this.storage.has(
            STORAGE_KEYS.REFRESH_TOKEN,
        );
    }

    /**
     * Return whether a complete authentication session exists.
     */
    public hasTokens(): boolean {
        return (
            this.hasAccessToken() &&
            this.hasRefreshToken()
        );
    }

    /**
     * Remove the access token.
     */
    public clearAccessToken(): void {
        this.storage.remove(
            STORAGE_KEYS.ACCESS_TOKEN,
        );
    }

    /**
     * Remove the refresh token.
     */
    public clearRefreshToken(): void {
        this.storage.remove(
            STORAGE_KEYS.REFRESH_TOKEN,
        );
    }

    /**
     * Remove all authentication tokens.
     */
    public clear(): void {
        this.storage.remove(
            STORAGE_KEYS.ACCESS_TOKEN,
        );

        this.storage.remove(
            STORAGE_KEYS.REFRESH_TOKEN,
        );
    }

    /**
     * Replace the current access token.
     *
     * Useful after JWT refresh.
     */
    public replaceAccessToken(
        token: string,
        expiresAt?: string,
    ): void {
        this.setAccessToken(
            token,
            expiresAt,
        );
    }

    /**
     * Replace the current refresh token.
     *
     * Useful when the backend rotates refresh tokens.
     */
    public replaceRefreshToken(
        token: string,
        expiresAt?: string,
    ): void {
        this.setRefreshToken(
            token,
            expiresAt,
        );
    }
}

/**
 * Token storage factory.
 *
 * A factory is used instead of constructing a SecureStorage instance here so
 * the concrete storage provider can be selected by the composition root.
 */
export function createTokenStorage(
    storage: SecureStorage,
): TokenStorage {
    return new TokenStorage(
        storage,
    );
}
