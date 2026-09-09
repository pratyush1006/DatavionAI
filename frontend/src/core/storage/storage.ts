/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/storage.ts
 * =============================================================================
 *
 * Base storage abstraction.
 *
 * Every browser storage implementation (LocalStorage, SessionStorage,
 * SecureStorage, IndexedDB, etc.) must implement this contract.
 *
 * This abstraction keeps the application independent from browser APIs
 * and makes storage implementations easily testable.
 *
 * Design Principles
 * -----------------
 * - Interface Driven
 * - SOLID
 * - Testable
 * - Type Safe
 * - Framework Agnostic
 * - JSON Safe
 * - Enterprise Ready
 *
 * =============================================================================
 */

import type {
    StorageKey,
} from "./keys";

/* =============================================================================
 * Storage Values
 * =============================================================================
 */

/**
 * Primitive value supported by DatavionOS storage.
 */
export type StoragePrimitive =
    | string
    | number
    | boolean
    | null;

/**
 * JSON-compatible value.
 *
 * This type is retained as the default transport/storage representation.
 *
 * Generic application objects are intentionally accepted by the storage
 * provider API because TypeScript interfaces do not necessarily satisfy a
 * recursive JSON index signature structurally.
 */
export type StorageValue =
    | StoragePrimitive
    | readonly StorageValue[]
    | {
          readonly [key: string]: StorageValue;
      };

/* =============================================================================
 * Storage Options
 * =============================================================================
 */

/**
 * Options used when persisting a storage value.
 */
export interface StorageSetOptions {
    /**
     * Optional expiration timestamp.
     *
     * Expected format:
     * UTC ISO-8601 datetime.
     */
    readonly expiresAt?: string;
}

/* =============================================================================
 * Storage Entry
 * =============================================================================
 */

/**
 * Complete persisted storage entry.
 */
export interface StorageEntry<
    T = StorageValue,
> {
    /**
     * Stored value.
     */
    readonly value: T;

    /**
     * Entry creation timestamp.
     */
    readonly createdAt: string;

    /**
     * Last update timestamp.
     */
    readonly updatedAt: string;

    /**
     * Optional expiration timestamp.
     */
    readonly expiresAt?: string;
}

/* =============================================================================
 * Storage Provider Contract
 * =============================================================================
 */

/**
 * Framework-agnostic storage provider contract.
 *
 * Generic values are intentionally unconstrained at the TypeScript boundary.
 * Concrete implementations are responsible for JSON serialization.
 */
export interface StorageProvider {
    /**
     * Return whether storage is available.
     */
    isAvailable(): boolean;

    /**
     * Return whether the key exists.
     */
    has(
        key: StorageKey,
    ): boolean;

    /**
     * Read a value.
     */
    get<T = StorageValue>(
        key: StorageKey,
    ): T | null;

    /**
     * Persist a value.
     */
    set<T = StorageValue>(
        key: StorageKey,
        value: T,
        options?: StorageSetOptions,
    ): void;

    /**
     * Remove a single key.
     */
    remove(
        key: StorageKey,
    ): void;

    /**
     * Remove every DatavionOS storage value.
     */
    clear(): void;

    /**
     * Return every DatavionOS storage key.
     */
    keys(): readonly StorageKey[];

    /**
     * Return the number of stored entries.
     */
    size(): number;
}

/* =============================================================================
 * Abstract Storage
 * =============================================================================
 */

/**
 * Base implementation for all DatavionOS storage providers.
 */
export abstract class BaseStorage
    implements StorageProvider
{
    /**
     * Return whether storage is available.
     */
    public abstract isAvailable(): boolean;

    /**
     * Return whether a key exists.
     */
    public abstract has(
        key: StorageKey,
    ): boolean;

    /**
     * Read a value.
     */
    public abstract get<T = StorageValue>(
        key: StorageKey,
    ): T | null;

    /**
     * Persist a value.
     */
    public abstract set<T = StorageValue>(
        key: StorageKey,
        value: T,
        options?: StorageSetOptions,
    ): void;

    /**
     * Remove a single key.
     */
    public abstract remove(
        key: StorageKey,
    ): void;

    /**
     * Remove every DatavionOS storage value.
     */
    public abstract clear(): void;

    /**
     * Return every DatavionOS storage key.
     */
    public abstract keys(): readonly StorageKey[];

    /**
     * Return the number of stored entries.
     */
    public size(): number {
        return this.keys().length;
    }
}
