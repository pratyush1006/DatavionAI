/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/keys.ts
 * =============================================================================
 *
 * Centralized storage keys.
 *
 * This file defines every browser storage key used by DatavionOS.
 * No module should hardcode storage keys.
 *
 * Design Principles
 * -----------------
 * • Single Source of Truth
 * • Immutable
 * • Type Safe
 * • Version Ready
 * • Multi-tenant SaaS Ready
 * • Enterprise Ready
 *
 * Usage
 * -----
 * import { STORAGE_KEYS } from "@/core/storage";
 *
 * localStorage.setItem(
 *     STORAGE_KEYS.ACCESS_TOKEN,
 *     token,
 * );
 * =============================================================================
 */

/**
 * Storage namespace.
 *
 * Allows future migration/versioning without
 * breaking existing deployments.
 */
export const STORAGE_NAMESPACE = "datavion";

/**
 * Storage version.
 *
 * Increment when storage schema changes.
 */
export const STORAGE_VERSION = "v1";

/**
 * Build a namespaced storage key.
 */
const createKey = (
    key: string,
): string => `${STORAGE_NAMESPACE}:${STORAGE_VERSION}:${key}`;

/**
 * Centralized browser storage keys.
 */
export const STORAGE_KEYS = Object.freeze({
    /**
     * Authentication
     */
    ACCESS_TOKEN: createKey("access_token"),

    REFRESH_TOKEN: createKey("refresh_token"),

    CURRENT_USER: createKey("current_user"),

    AUTH_STATE: createKey("auth_state"),

    /**
     * Platform Bootstrap
     */
    BOOTSTRAP: createKey("bootstrap"),

    FEATURE_FLAGS: createKey("feature_flags"),

    PERMISSIONS: createKey("permissions"),

    NAVIGATION: createKey("navigation"),

    DASHBOARD: createKey("dashboard"),

    /**
     * Organization
     */
    CURRENT_TENANT: createKey("current_tenant"),

    CURRENT_ORGANIZATION: createKey("current_organization"),

    /**
     * User Preferences
     */
    THEME: createKey("theme"),

    LANGUAGE: createKey("language"),

    LOCALE: createKey("locale"),

    TIMEZONE: createKey("timezone"),

    /**
     * UI
     */
    SIDEBAR_COLLAPSED: createKey("sidebar_collapsed"),

    LAST_ROUTE: createKey("last_route"),

    /**
     * Notifications
     */
    NOTIFICATION_SETTINGS: createKey("notification_settings"),

    /**
     * Miscellaneous
     */
    DEVICE_ID: createKey("device_id"),

    SESSION_ID: createKey("session_id"),
} as const);

/**
 * Union type of all storage keys.
 */
export type StorageKey =
    (typeof STORAGE_KEYS)[keyof typeof STORAGE_KEYS];

/**
 * Storage categories.
 */
export enum StorageArea {
    LOCAL = "local",

    SESSION = "session",
}

/**
 * Default storage area.
 */
export const DEFAULT_STORAGE_AREA = StorageArea.LOCAL;

/**
 * Export immutable list of all keys.
 */
export const ALL_STORAGE_KEYS = Object.freeze(
    Object.values(STORAGE_KEYS),
);

/**
 * Type guard.
 */
export function isStorageKey(
    value: string,
): value is StorageKey {
    return ALL_STORAGE_KEYS.includes(value as StorageKey);
}
