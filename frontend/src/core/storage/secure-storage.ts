/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/secure-storage.ts
 * =============================================================================
 *
 * Controlled storage boundary for application data.
 *
 * IMPORTANT
 * ---------
 * Browser storage is not a cryptographically secure secret store.
 *
 * Data stored in localStorage or sessionStorage can be accessed by JavaScript
 * running in the same origin.
 *
 * This abstraction therefore provides:
 * - Centralized storage access
 * - Strict storage-key validation
 * - Safe delegation to the configured storage provider
 * - Error isolation
 * - Type-safe reads and writes
 * - Expiration support
 * - No direct browser API usage by feature modules
 *
 * It does NOT provide:
 * - Encryption
 * - XSS protection
 * - HttpOnly semantics
 * - Protection from malicious same-origin JavaScript
 *
 * =============================================================================
 */

import {
    BaseStorage,
    type StorageEntry,
    type StorageSetOptions,
    type StorageValue,
    type StorageProvider,
} from "./storage";

import type {
    StorageKey,
} from "./keys";

/* =============================================================================
 * Errors
 * =============================================================================
 */

/**
 * Base error for controlled storage operations.
 */
export class StorageError
    extends Error
{
    public readonly operation: string;

    public readonly key?: StorageKey;

    public readonly cause?: unknown;

    public constructor(
        message: string,
        options: {
            readonly operation: string;
            readonly key?: StorageKey;
            readonly cause?: unknown;
        },
    ) {
        super(message);

        this.name =
            "StorageError";

        this.operation =
            options.operation;

        this.key =
            options.key;

        this.cause =
            options.cause;
    }
}

/* =============================================================================
 * Configuration
 * =============================================================================
 */

export interface SecureStorageOptions {
    /**
     * Whether storage errors should be swallowed.
     *
     * Defaults to true.
     */
    readonly suppressErrors?: boolean;
}

/* =============================================================================
 * Secure Storage
 * =============================================================================
 */

/**
 * Controlled storage facade.
 *
 * This class intentionally depends on the StorageProvider abstraction instead
 * of directly accessing localStorage or sessionStorage.
 */
export class SecureStorage
    extends BaseStorage
{
    private readonly provider: StorageProvider;

    private readonly suppressErrors: boolean;

    public constructor(
        provider: StorageProvider,
        options: SecureStorageOptions = {},
    ) {
        super();

        this.provider =
            provider;

        this.suppressErrors =
            options.suppressErrors ??
            true;
    }

    /**
     * Return whether the underlying storage provider is available.
     */
    public isAvailable(): boolean {
        return this.provider.isAvailable();
    }

    /**
     * Return whether a key exists.
     */
    public has(
        key: StorageKey,
    ): boolean {
        try {
            return this.provider.has(
                key,
            );
        } catch (error) {
            return this.handleFailure(
                "has",
                key,
                error,
                false,
            );
        }
    }

    /**
     * Read a stored value.
     */
    public get<T = StorageValue>(
        key: StorageKey,
    ): T | null {
        try {
            return this.provider.get<T>(
                key,
            );
        } catch (error) {
            return this.handleFailure(
                "get",
                key,
                error,
                null,
            );
        }
    }

    /**
     * Persist a value.
     */
    public set<T = StorageValue>(
        key: StorageKey,
        value: T,
        options?: StorageSetOptions,
    ): void {
        try {
            this.provider.set<T>(
                key,
                value,
                options,
            );
        } catch (error) {
            this.handleFailure(
                "set",
                key,
                error,
                undefined,
            );
        }
    }

    /**
     * Remove a stored value.
     */
    public remove(
        key: StorageKey,
    ): void {
        try {
            this.provider.remove(
                key,
            );
        } catch (error) {
            this.handleFailure(
                "remove",
                key,
                error,
                undefined,
            );
        }
    }

    /**
     * Remove all DatavionOS entries.
     */
    public clear(): void {
        try {
            this.provider.clear();
        } catch (error) {
            this.handleFailure(
                "clear",
                undefined,
                error,
                undefined,
            );
        }
    }

    /**
     * Return all keys managed by the provider.
     */
    public keys(): readonly StorageKey[] {
        try {
            return this.provider.keys();
        } catch (error) {
            return this.handleFailure(
                "keys",
                undefined,
                error,
                [],
            );
        }
    }

    /**
     * Return the number of stored entries.
     */
    public size(): number {
        try {
            return this.provider.size();
        } catch (error) {
            return this.handleFailure(
                "size",
                undefined,
                error,
                0,
            );
        }
    }

    /**
     * Read a complete storage entry.
     *
     * The underlying StorageProvider stores complete entries internally, but
     * does not expose raw entry metadata as part of its public contract.
     *
     * Therefore this method returns a controlled diagnostic representation.
     */
    public getEntry<T = StorageValue>(
        key: StorageKey,
    ): StorageEntry<T> | null {
        const value =
            this.get<T>(
                key,
            );

        if (
            value === null
        ) {
            return null;
        }

        const now =
            new Date().toISOString();

        return {
            value,
            createdAt: now,
            updatedAt: now,
        };
    }

    /**
     * Persist a value with an expiration timestamp.
     */
    public setWithExpiration<
        T = StorageValue,
    >(
        key: StorageKey,
        value: T,
        expiresAt: string,
    ): void {
        this.set(
            key,
            value,
            {
                expiresAt,
            },
        );
    }

    /**
     * Execute a storage operation while applying the configured error policy.
     */
    private handleFailure<T>(
        operation: string,
        key: StorageKey | undefined,
        error: unknown,
        fallback: T,
    ): T {
        if (
            this.suppressErrors
        ) {
            return fallback;
        }

        throw new StorageError(
            `DatavionOS storage operation "${operation}" failed.`,
            {
                operation,
                key,
                cause: error,
            },
        );
    }
}
