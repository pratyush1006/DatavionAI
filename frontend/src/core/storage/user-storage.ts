/**
 * =============================================================================
 * DatavionOS
 * File: src/core/storage/user-storage.ts
 * =============================================================================
 *
 * Authenticated user persistence.
 *
 * Responsibilities
 * ----------------
 * - Persist the authenticated user's frontend representation
 * - Retrieve the current user
 * - Remove the current user
 * - Provide a controlled persistence boundary for auth state
 * - Normalize backend field names and boolean representations
 * - Validate the canonical frontend user contract
 * - Migrate legacy persisted user representations
 *
 * This class intentionally stores user identity separately from authentication
 * tokens. Token lifecycle belongs to TokenStorage.
 *
 * Design Principles
 * -----------------
 * - Single Responsibility
 * - Strong Type Safety
 * - Provider Agnostic
 * - SSR Safe
 * - No Direct Browser API Access
 * - Backend Contract Friendly
 * - Runtime Validation
 * - Legacy Storage Migration
 * - Enterprise Ready
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
 * Authenticated user representation persisted by the frontend.
 *
 * The index signature explicitly declares compatibility with the JSON-safe
 * StorageValue contract used by SecureStorage.
 */
export interface StoredUser {
    readonly [key: string]:
        | string
        | boolean
        | null
        | undefined;

    readonly id: string;

    readonly email: string;

    readonly firstName: string;

    readonly lastName: string;

    readonly phone?: string | null;

    readonly isVerified: boolean;

    readonly isActive: boolean;

    readonly organizationId?: string | null;

    readonly tenantId?: string | null;
}

/**
 * Runtime object received from the API or legacy storage.
 *
 * The backend may use snake_case while the frontend canonical model uses
 * camelCase.
 */
type RuntimeUser = Record<
    string,
    unknown
>;

/* =============================================================================
 * Runtime Helpers
 * =============================================================================
 */

/**
 * Return the first defined value from the supplied candidates.
 */
function firstDefined(
    ...values: unknown[]
): unknown {
    for (
        const value of values
    ) {
        if (
            value !== undefined &&
            value !== null
        ) {
            return value;
        }
    }

    return undefined;
}

/**
 * Normalize a backend boolean representation.
 *
 * Accepted representations:
 *
 *     true
 *     false
 *     "true"
 *     "false"
 *     "True"
 *     "False"
 *     "TRUE"
 *     "FALSE"
 *     1
 *     0
 *     "1"
 *     "0"
 *
 * Any other value is rejected.
 */
function normalizeBoolean(
    value: unknown,
    fieldName: string,
): boolean {
    if (
        typeof value ===
        "boolean"
    ) {
        return value;
    }

    if (
        typeof value ===
        "number"
    ) {
        if (value === 1) {
            return true;
        }

        if (value === 0) {
            return false;
        }
    }

    if (
        typeof value ===
        "string"
    ) {
        const normalized =
            value
                .trim()
                .toLowerCase();

        if (
            normalized ===
            "true"
        ) {
            return true;
        }

        if (
            normalized ===
            "false"
        ) {
            return false;
        }

        if (
            normalized ===
            "1"
        ) {
            return true;
        }

        if (
            normalized ===
            "0"
        ) {
            return false;
        }
    }

    throw new Error(
        `Stored user ${fieldName} state must be boolean.`,
    );
}

/**
 * Normalize an optional string field.
 */
function normalizeOptionalString(
    value: unknown,
): string | null | undefined {
    if (
        value === undefined ||
        value === null
    ) {
        return value;
    }

    if (
        typeof value !==
        "string"
    ) {
        throw new Error(
            "Stored user optional string field must be a string or null.",
        );
    }

    return value;
}

/**
 * Normalize a required string field.
 */
function normalizeRequiredString(
    value: unknown,
    fieldName: string,
): string {
    if (
        typeof value !==
        "string"
    ) {
        throw new Error(
            `Stored user ${fieldName} must be a string.`,
        );
    }

    const normalized =
        value.trim();

    if (!normalized) {
        throw new Error(
            `Stored user ${fieldName} cannot be empty.`,
        );
    }

    return normalized;
}

/* =============================================================================
 * User Normalization
 * =============================================================================
 */

/**
 * Normalize a user received from the API or legacy storage.
 *
 * The backend and older frontend versions may represent fields using either
 * snake_case or camelCase.
 *
 * Current backend /me/ contract:
 *
 *     id
 *     email
 *     first_name
 *     last_name
 *     phone
 *     is_verified
 *
 * The backend currently does not expose an is_active field in /me/.
 *
 * Since this user has successfully completed authentication and the backend
 * has returned the authenticated current-user representation, the frontend
 * canonical session representation treats the authenticated user as active.
 */
function normalizeUser(
    user: StoredUser,
): StoredUser {
    const runtimeUser =
        user as unknown as RuntimeUser;

    const id =
        normalizeRequiredString(
            firstDefined(
                runtimeUser.id,
                runtimeUser.user_id,
                runtimeUser.pk,
            ),
            "ID",
        );

    const email =
        normalizeRequiredString(
            firstDefined(
                runtimeUser.email,
                runtimeUser.username,
            ),
            "email",
        );

    const firstNameValue =
        firstDefined(
            runtimeUser.firstName,
            runtimeUser.first_name,
            runtimeUser.firstname,
            "",
        );

    const lastNameValue =
        firstDefined(
            runtimeUser.lastName,
            runtimeUser.last_name,
            runtimeUser.lastname,
            "",
        );

    const firstName =
        typeof firstNameValue ===
        "string"
            ? firstNameValue
            : "";

    const lastName =
        typeof lastNameValue ===
        "string"
            ? lastNameValue
            : "";

    /* -------------------------------------------------------------------------
     * Verification State
     * -------------------------------------------------------------------------
     */

    const isVerifiedValue =
        firstDefined(
            runtimeUser.isVerified,
            runtimeUser.is_verified,
            runtimeUser.verified,
            runtimeUser.email_verified,
            runtimeUser.emailVerified,
        );

    const isVerified =
        normalizeBoolean(
            isVerifiedValue,
            "verification",
        );

    /* -------------------------------------------------------------------------
     * Active State
     * -------------------------------------------------------------------------
     *
     * The current backend /me/ response does not expose is_active.
     *
     * If the backend explicitly provides an active state, honor it.
     * Otherwise, an authenticated /me/ response is treated as active.
     */

    const isActiveValue =
        firstDefined(
            runtimeUser.isActive,
            runtimeUser.is_active,
            runtimeUser.active,
        );

    const isActive =
        isActiveValue ===
        undefined
            ? true
            : normalizeBoolean(
                isActiveValue,
                "active",
            );

    /* -------------------------------------------------------------------------
     * Optional Fields
     * -------------------------------------------------------------------------
     */

    const phone =
        normalizeOptionalString(
            firstDefined(
                runtimeUser.phone,
                runtimeUser.phone_number,
                runtimeUser.phoneNumber,
            ),
        );

    const organizationId =
        normalizeOptionalString(
            firstDefined(
                runtimeUser.organizationId,
                runtimeUser.organization_id,
            ),
        );

    const tenantId =
        normalizeOptionalString(
            firstDefined(
                runtimeUser.tenantId,
                runtimeUser.tenant_id,
            ),
        );

    /* -------------------------------------------------------------------------
     * Canonical User
     * -------------------------------------------------------------------------
     */

    const normalizedUser: StoredUser = {
        id,
        email,
        firstName,
        lastName,
        phone,
        isVerified,
        isActive,
        organizationId,
        tenantId,
    };

    return normalizedUser;
}

/* =============================================================================
 * User Storage
 * =============================================================================
 */

/**
 * Persistent authenticated-user storage.
 */
export class UserStorage {
    private readonly storage: SecureStorage;

    /**
     * Create user storage.
     */
    public constructor(
        storage: SecureStorage,
    ) {
        this.storage =
            storage;
    }

    /* =========================================================================
     * Persistence
     * ========================================================================= */

    /**
     * Persist the authenticated user.
     *
     * Runtime normalization occurs here so backend representations never leak
     * into the frontend authentication state.
     */
    public setUser(
        user: StoredUser,
    ): void {
        const normalizedUser =
            normalizeUser(
                user,
            );

        this.validateUser(
            normalizedUser,
        );

        this.storage.set(
            STORAGE_KEYS.CURRENT_USER,
            normalizedUser,
        );
    }

    /**
     * Return the currently stored user.
     *
     * Existing persisted users are normalized as a migration boundary.
     *
     * Invalid persisted authentication state is discarded instead of poisoning
     * the authentication runtime.
     */
    public getUser():
        | StoredUser
        | null {
        const storedUser =
            this.storage.get<StoredUser>(
                STORAGE_KEYS.CURRENT_USER,
            );

        if (!storedUser) {
            return null;
        }

        try {
            const normalizedUser =
                normalizeUser(
                    storedUser,
                );

            this.validateUser(
                normalizedUser,
            );

            /*
             * Always persist the canonical representation.
             *
             * This also migrates legacy snake_case fields and string booleans.
             */
            this.storage.set(
                STORAGE_KEYS.CURRENT_USER,
                normalizedUser,
            );

            return normalizedUser;
        } catch {
            /*
             * Invalid persisted authentication state must never be allowed
             * to poison the authentication runtime.
             */
            this.clearUser();

            return null;
        }
    }

    /**
     * Return whether a current user exists.
     */
    public hasUser(): boolean {
        return (
            this.getUser() !==
            null
        );
    }

    /**
     * Remove the current user.
     */
    public clearUser(): void {
        this.storage.remove(
            STORAGE_KEYS.CURRENT_USER,
        );
    }

    /**
     * Replace the currently stored user.
     */
    public replaceUser(
        user: StoredUser,
    ): void {
        this.setUser(
            user,
        );
    }

    /* =========================================================================
     * Updates
     * ========================================================================= */

    /**
     * Update selected user properties.
     *
     * The existing user must already exist.
     */
    public updateUser(
        updates: Partial<StoredUser>,
    ):
        | StoredUser
        | null {
        const currentUser =
            this.getUser();

        if (!currentUser) {
            return null;
        }

        const updatedUser:
            StoredUser = {
                ...currentUser,
                ...updates,
            };

        this.setUser(
            updatedUser,
        );

        return this.getUser();
    }

    /* =========================================================================
     * Selectors
     * ========================================================================= */

    /**
     * Return the current user's ID.
     */
    public getUserId():
        | string
        | null {
        return (
            this.getUser()?.id ??
            null
        );
    }

    /**
     * Return the current user's email.
     */
    public getUserEmail():
        | string
        | null {
        return (
            this.getUser()?.email ??
            null
        );
    }

    /**
     * Return the current user's tenant ID.
     */
    public getTenantId():
        | string
        | null {
        return (
            this.getUser()?.tenantId ??
            null
        );
    }

    /**
     * Return the current user's organization ID.
     */
    public getOrganizationId():
        | string
        | null {
        return (
            this.getUser()?.organizationId ??
            null
        );
    }

    /* =========================================================================
     * Validation
     * ========================================================================= */

    /**
     * Validate the canonical persisted identity contract.
     *
     * At this point all backend representations have already been normalized.
     */
    private validateUser(
        user: StoredUser,
    ): void {
        if (
            typeof user.id !==
                "string" ||
            !user.id.trim()
        ) {
            throw new Error(
                "Stored user ID cannot be empty.",
            );
        }

        if (
            typeof user.email !==
                "string" ||
            !user.email.trim()
        ) {
            throw new Error(
                "Stored user email cannot be empty.",
            );
        }

        if (
            typeof user.firstName !==
            "string"
        ) {
            throw new Error(
                "Stored user first name must be a string.",
            );
        }

        if (
            typeof user.lastName !==
            "string"
        ) {
            throw new Error(
                "Stored user last name must be a string.",
            );
        }

        if (
            typeof user.isVerified !==
            "boolean"
        ) {
            throw new Error(
                "Stored user verification state must be boolean.",
            );
        }

        if (
            typeof user.isActive !==
            "boolean"
        ) {
            throw new Error(
                "Stored user active state must be boolean.",
            );
        }

        if (
            user.phone !==
                undefined &&
            user.phone !==
                null &&
            typeof user.phone !==
                "string"
        ) {
            throw new Error(
                "Stored user phone must be a string or null.",
            );
        }

        if (
            user.organizationId !==
                undefined &&
            user.organizationId !==
                null &&
            typeof user.organizationId !==
                "string"
        ) {
            throw new Error(
                "Stored user organization ID must be a string or null.",
            );
        }

        if (
            user.tenantId !==
                undefined &&
            user.tenantId !==
                null &&
            typeof user.tenantId !==
                "string"
        ) {
            throw new Error(
                "Stored user tenant ID must be a string or null.",
            );
        }
    }
}

/* =============================================================================
 * Factory
 * =============================================================================
 */

/**
 * Factory for constructing user storage.
 */
export function createUserStorage(
    storage: SecureStorage,
): UserStorage {
    return new UserStorage(
        storage,
    );
}
