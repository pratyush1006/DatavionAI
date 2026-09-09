/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/local-storage.ts
 * =============================================================================
 *
 * LocalStorage implementation.
 *
 * Concrete browser storage provider backed by window.localStorage.
 *
 * All common browser-storage behavior is inherited from BrowserStorage.
 * =============================================================================
 */

import { BrowserStorage } from "./browser-storage";

/**
 * DatavionOS LocalStorage provider.
 */
export class LocalStorage extends BrowserStorage {
    /**
     * Return the browser localStorage instance.
     *
     * Browser access is only evaluated when the provider is actually used,
     * keeping the class safe during Next.js SSR/build execution.
     */
    protected get storage(): Storage {
        return window.localStorage;
    }
}

/**
 * Shared LocalStorage provider instance.
 */
export const localStorageService =
    new LocalStorage();
