/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/session-storage.ts
 * =============================================================================
 *
 * SessionStorage implementation.
 *
 * Concrete browser storage provider backed by window.sessionStorage.
 *
 * All common browser-storage behavior is inherited from BrowserStorage.
 * =============================================================================
 */

import { BrowserStorage } from "./browser-storage";

/**
 * DatavionOS SessionStorage provider.
 */
export class SessionStorage extends BrowserStorage {
    /**
     * Return the browser sessionStorage instance.
     *
     * Browser access is only evaluated when the provider is actually used,
     * keeping the class safe during Next.js SSR/build execution.
     */
    protected get storage(): Storage {
        return window.sessionStorage;
    }
}

/**
 * Shared SessionStorage provider instance.
 */
export const sessionStorageService =
    new SessionStorage();
