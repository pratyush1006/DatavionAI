/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/browser-storage.ts
 * =============================================================================
 *
 * Shared browser storage implementation.
 *
 * Provides the common implementation for browser-based storage providers
 * such as LocalStorage and SessionStorage.
 *
 * Responsibilities
 * ----------------
 * - Browser availability detection
 * - Safe JSON serialization
 * - Safe JSON deserialization
 * - Automatic expiration handling
 * - Corrupted entry cleanup
 * - Namespace-aware key discovery
 * - Shared CRUD operations
 * - Enterprise-grade error handling
 *
 * Design Principles
 * -----------------
 * - DRY
 * - SOLID
 * - Type Safe
 * - Testable
 * - SSR Safe
 * - Enterprise Ready
 *
 * =============================================================================
 */

import {
    ALL_STORAGE_KEYS,
    STORAGE_NAMESPACE,
    type StorageKey,
} from "./keys";

import {
    BaseStorage,
    type StorageEntry,
    type StorageSetOptions,
    type StorageValue,
} from "./storage";

/**
 * Shared implementation for browser storage providers.
 */
export abstract class BrowserStorage
    extends BaseStorage
{
    /**
     * Concrete implementations must return the browser Storage instance.
     */
    protected abstract get storage(): Storage;

    /**
     * Return whether browser storage is available.
     */
    public isAvailable(): boolean {
        if (
            typeof window ===
            "undefined"
        ) {
            return false;
        }

        try {
            const storage =
                this.storage;

            const key =
                "__datavion_storage_test__";

            storage.setItem(
                key,
                key,
            );

            storage.removeItem(
                key,
            );

            return true;
        } catch {
            return false;
        }
    }

    /**
     * Return whether a key exists.
     */
    public has(
        key: StorageKey,
    ): boolean {
        return this.get(
            key,
        ) !== null;
    }

    /**
     * Read a value.
     *
     * Expired entries are removed automatically.
     */
    public get<T = StorageValue>(
        key: StorageKey,
    ): T | null {
        const entry =
            this.readEntry<T>(
                key,
            );

        if (!entry) {
            return null;
        }

        if (
            entry.expiresAt &&
            new Date(
                entry.expiresAt,
            ) <= new Date()
        ) {
            this.remove(
                key,
            );

            return null;
        }

        return entry.value;
    }

    /**
     * Persist a value.
     */
    public set<T = StorageValue>(
        key: StorageKey,
        value: T,
        options?: StorageSetOptions,
    ): void {
        if (
            !this.isAvailable()
        ) {
            return;
        }

        const now =
            new Date().toISOString();

        const existing =
            this.readEntry<T>(
                key,
            );

        const entry: StorageEntry<T> = {
            value,
            createdAt:
                existing?.createdAt ??
                now,
            updatedAt: now,
            expiresAt:
                options?.expiresAt,
        };

        this.storage.setItem(
            key,
            JSON.stringify(
                entry,
            ),
        );
    }

    /**
     * Remove a value.
     */
    public remove(
        key: StorageKey,
    ): void {
        if (
            !this.isAvailable()
        ) {
            return;
        }

        this.storage.removeItem(
            key,
        );
    }

    /**
     * Remove every DatavionOS storage key.
     */
    public clear(): void {
        if (
            !this.isAvailable()
        ) {
            return;
        }

        for (
            const key of this.keys()
        ) {
            this.storage.removeItem(
                key,
            );
        }
    }

    /**
     * Return every DatavionOS storage key currently stored.
     */
    public keys(): readonly StorageKey[] {
        if (
            !this.isAvailable()
        ) {
            return [];
        }

        const keys: StorageKey[] = [];

        for (
            let index = 0;
            index < this.storage.length;
            index++
        ) {
            const key =
                this.storage.key(
                    index,
                );

            if (
                key &&
                key.startsWith(
                    `${STORAGE_NAMESPACE}:`,
                ) &&
                this.isKnownKey(
                    key,
                )
            ) {
                keys.push(
                    key,
                );
            }
        }

        return keys;
    }

    /**
     * Read a complete storage entry.
     */
    protected readEntry<
        T = StorageValue,
    >(
        key: StorageKey,
    ): StorageEntry<T> | null {
        if (
            !this.isAvailable()
        ) {
            return null;
        }

        const raw =
            this.storage.getItem(
                key,
            );

        if (!raw) {
            return null;
        }

        try {
            return JSON.parse(
                raw,
            ) as StorageEntry<T>;
        } catch {
            this.remove(
                key,
            );

            return null;
        }
    }

    /**
     * Return whether the supplied key belongs to DatavionOS.
     */
    protected isKnownKey(
        key: string,
    ): key is StorageKey {
        return ALL_STORAGE_KEYS.includes(
            key as StorageKey,
        );
    }

    /**
     * Remove every expired storage entry.
     */
    public cleanupExpired(): void {
        for (
            const key of this.keys()
        ) {
            this.get(
                key,
            );
        }
    }

    /**
     * Return a snapshot of every stored entry.
     *
     * Intended for diagnostics only.
     */
    public entries(): ReadonlyMap<
        StorageKey,
        StorageEntry
    > {
        const entries =
            new Map<
                StorageKey,
                StorageEntry
            >();

        for (
            const key of this.keys()
        ) {
            const entry =
                this.readEntry(
                    key,
                );

            if (entry) {
                entries.set(
                    key,
                    entry,
                );
            }
        }

        return entries;
    }
}
