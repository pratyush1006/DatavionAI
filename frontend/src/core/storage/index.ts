/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/index.ts
 * =============================================================================
 *
 * Public entry point for the DatavionOS storage subsystem.
 *
 * Application modules should import storage functionality from this module
 * instead of reaching into individual storage implementation files.
 *
 * Example:
 *
 * import {
 *     STORAGE_KEYS,
 *     TokenStorage,
 *     UserStorage,
 * } from "@/core/storage";
 *
 * Design Principles
 * -----------------
 * • Stable public API
 * • Encapsulation
 * • Explicit exports
 * • No circular dependencies
 * • Enterprise Ready
 * =============================================================================
 */

/* =============================================================================
 * Storage Keys
 * =============================================================================
 */

export {
    ALL_STORAGE_KEYS,
    DEFAULT_STORAGE_AREA,
    STORAGE_KEYS,
    STORAGE_NAMESPACE,
    STORAGE_VERSION,
    StorageArea,
    isStorageKey,
} from "./keys";

export type {
    StorageKey,
} from "./keys";

/* =============================================================================
 * Storage Abstractions
 * =============================================================================
 */

export {
    BaseStorage,
} from "./storage";

export type {
    StorageEntry,
    StoragePrimitive,
    StorageProvider,
    StorageSetOptions,
    StorageValue,
} from "./storage";

/* =============================================================================
 * Browser Storage
 * =============================================================================
 */

export {
    BrowserStorage,
} from "./browser-storage";

/* =============================================================================
 * Local Storage
 * =============================================================================
 */

export {
    LocalStorage,
    localStorageService,
} from "./local-storage";

/* =============================================================================
 * Session Storage
 * =============================================================================
 */

export {
    SessionStorage,
    sessionStorageService,
} from "./session-storage";

/* =============================================================================
 * Secure Storage
 * =============================================================================
 */

export {
    SecureStorage,
    StorageError,
} from "./secure-storage";

export type {
    SecureStorageOptions,
} from "./secure-storage";

/* =============================================================================
 * Token Storage
 * =============================================================================
 */

export {
    TokenStorage,
    createTokenStorage,
} from "./token-storage";

export type {
    AuthTokens,
    TokenStorageOptions,
} from "./token-storage";

/* =============================================================================
 * User Storage
 * =============================================================================
 */

export {
    UserStorage,
    createUserStorage,
} from "./user-storage";

export type {
    StoredUser,
} from "./user-storage";
