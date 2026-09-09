/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/composition.ts
 * =============================================================================
 *
 * Authentication dependency composition.
 *
 * This module is the composition root for the frontend authentication
 * subsystem.
 *
 * Responsibilities
 * ----------------
 * - Construct storage providers
 * - Construct SecureStorage boundaries
 * - Construct TokenStorage and UserStorage
 * - Configure the canonical application API client
 * - Connect the API client to token and tenant providers
 * - Construct AuthService
 *
 * Important architectural rule
 * -----------------------------
 * DatavionOS uses ONE canonical application ApiClient.
 *
 * The authentication composition layer configures that client with the
 * runtime dependencies required by authenticated requests.
 *
 * Bootstrap, feature services, authentication services, and other application
 * services must therefore resolve the same canonical ApiClient instance.
 *
 * Architecture
 * ------------
 *
 *     AuthRuntime
 *          |
 *          +-------------------+
 *          |                   |
 *          v                   v
 *     TokenStorage        UserStorage
 *          |                   |
 *          v                   v
 *     Token Provider      Tenant Provider
 *          |                   |
 *          +---------+---------+
 *                    |
 *                    v
 *            Canonical ApiClient
 *                    |
 *                    v
 *               AuthService
 *
 * Design Principles
 * -----------------
 * - Dependency Injection
 * - Explicit Composition
 * - No Duplicate API Clients
 * - No Hidden Feature-Level Clients
 * - Single Responsibility
 * - SSR Safe
 * - Testable
 * - Enterprise Ready
 *
 * =============================================================================
 */

import {
    apiClient as canonicalApiClient,
    type ApiClient,
    type ApiTenantProvider,
} from "@/core/api";

import {
    localStorageService,
    SecureStorage,
    TokenStorage,
    UserStorage,
} from "@/core/storage";

import {
    AuthService,
} from "./service";

/* =============================================================================
 * Types
 * =============================================================================
 */

/**
 * Complete authentication runtime.
 *
 * The runtime contains the concrete dependencies required by AuthProvider
 * and authentication-aware application services.
 */
export interface AuthRuntime {
    /**
     * Canonical application API client.
     *
     * This MUST be the same instance exposed by @/core/api.
     */
    readonly api: ApiClient;

    /**
     * Controlled storage boundary.
     */
    readonly secureStorage: SecureStorage;

    /**
     * Authentication token storage.
     */
    readonly tokenStorage: TokenStorage;

    /**
     * Current-user persistence.
     */
    readonly userStorage: UserStorage;

    /**
     * Authentication business service.
     */
    readonly service: AuthService;
}

/**
 * Optional authentication composition overrides.
 *
 * These overrides make the composition root testable and allow isolated
 * application runtimes to provide a dedicated ApiClient or tenant provider.
 */
export interface AuthCompositionOptions {
    /**
     * Optional API client override.
     *
     * Tests and isolated application runtimes can provide their own
     * ApiClient instance.
     *
     * In the normal application runtime this is omitted and the canonical
     * application ApiClient is used.
     */
    readonly apiClient?: ApiClient;

    /**
     * Optional tenant provider.
     *
     * When omitted, tenant context is resolved from UserStorage.
     */
    readonly tenantProvider?: ApiTenantProvider;
}

/* =============================================================================
 * Tenant Provider
 * =============================================================================
 */

/**
 * Create a tenant provider backed by persisted user context.
 *
 * Authentication requests that occur before tenant resolution return null.
 */
function createTenantProvider(
    userStorage: UserStorage,
): ApiTenantProvider {
    return {
        getTenantId(): string | null {
            return userStorage.getTenantId();
        },
    };
}

/* =============================================================================
 * Composition
 * =============================================================================
 */

/**
 * Construct the complete authentication runtime.
 *
 * The normal application runtime deliberately uses the canonical ApiClient
 * imported from @/core/api.
 *
 * This is critical because other infrastructure such as platform bootstrap
 * also imports that same canonical instance.
 *
 * Consequently:
 *
 *     AuthRuntime.api === apiClient
 *
 * for the normal application runtime.
 */
export function createAuthRuntime(
    options: AuthCompositionOptions = {},
): AuthRuntime {
    /* -------------------------------------------------------------------------
     * Storage
     * -------------------------------------------------------------------------
     */

    /**
     * Browser storage remains behind the storage abstraction.
     */
    const secureStorage =
        new SecureStorage(
            localStorageService,
        );

    /**
     * Authentication persistence.
     */
    const tokenStorage =
        new TokenStorage(
            secureStorage,
        );

    /**
     * Current-user persistence.
     */
    const userStorage =
        new UserStorage(
            secureStorage,
        );

    /* -------------------------------------------------------------------------
     * Tenant Context
     * -------------------------------------------------------------------------
     */

    /**
     * Tenant context.
     *
     * A caller can override this when DatavionOS introduces a dedicated
     * tenant/session context provider.
     */
    const tenantProvider =
        options.tenantProvider ??
        createTenantProvider(
            userStorage,
        );

    /* -------------------------------------------------------------------------
     * API Runtime Dependencies
     * -------------------------------------------------------------------------
     */

    /**
     * Token provider exposed to the API transport layer.
     *
     * The provider reads the current token at request time rather than
     * capturing a token during application startup.
     */
    const tokenProvider = {
        getAccessToken(): string | null {
            return tokenStorage.getAccessToken();
        },
    };

    /* -------------------------------------------------------------------------
     * Canonical API Client
     * -------------------------------------------------------------------------
     */

    /**
     * Use an explicitly supplied ApiClient for isolated/test runtimes.
     *
     * Otherwise use the ONE canonical application ApiClient.
     *
     * Do NOT create another application ApiClient here.
     */
    const api =
        options.apiClient ??
        canonicalApiClient;

    /**
     * Configure the API client with the authentication runtime.
     *
     * This updates the canonical client's request interceptor so every
     * authenticated request can resolve the current access token.
     *
     * It also supplies the tenant provider used for X-Tenant-ID.
     */
    api.setRuntime({
        tokenProvider,
        tenantProvider,
    });

    /* -------------------------------------------------------------------------
     * Authentication Service
     * -------------------------------------------------------------------------
     */

    /**
     * Authentication business service.
     */
    const service =
        new AuthService({
            api,
            tokenStorage,
            userStorage,
        });

    /* -------------------------------------------------------------------------
     * Runtime
     * -------------------------------------------------------------------------
     */

    return {
        api,
        secureStorage,
        tokenStorage,
        userStorage,
        service,
    };
}

/* =============================================================================
 * Default Runtime
 * =============================================================================
 */

/**
 * Default application authentication runtime.
 *
 * Application code should consume this composed runtime rather than manually
 * constructing authentication dependencies.
 *
 * The default runtime configures the canonical @/core/api ApiClient.
 */
export const authRuntime =
    createAuthRuntime();
