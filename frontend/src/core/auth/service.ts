/**
 * =============================================================================
 * DatavionOS
 * File: src/core/auth/service.ts
 * =============================================================================
 *
 * Authentication service.
 *
 * Central business-facing authentication facade for the frontend.
 *
 * Responsibilities
 * ----------------
 * - Registration
 * - Login OTP request
 * - Login OTP verification
 * - Email verification
 * - Resend verification OTP
 * - Logout
 * - Token refresh
 * - Current-user retrieval
 * - Forgot password
 * - Reset password
 * - Change password
 * - OAuth authentication
 * - Authentication persistence
 *
 * Architecture
 * ------------
 *
 *     API
 *      |
 *      v
 *   AuthService
 *      |
 *      +---- TokenStorage
 *      |
 *      +---- UserStorage
 *
 * AuthService does not own React state.
 * AuthProvider owns runtime authentication state.
 *
 * Design Principles
 * -----------------
 * - Single Authentication Boundary
 * - API/Storage Dependency Inversion
 * - No React Dependencies
 * - No Direct Browser API Usage
 * - Strong Type Safety
 * - Backend Contract Aligned
 * - Explicit API -> Storage Mapping
 * - Concurrent Refresh Protection
 * - Enterprise Ready
 * =============================================================================
 */

import {
    AUTH_API_PATHS,
} from "./constants";

import type {
    AuthSession,
    AuthTokenPair,
    AuthUser,
    AuthenticationResponse,
    ChangePasswordRequest,
    CurrentUser,
    ForgotPasswordRequest,
    LoginOTPRequestResponse,
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    OAuthLoginRequest,
    OAuthLoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    VerifyEmailRequest,
    VerifyLoginOTPRequest,
} from "./types";

import {
    unwrapData,
    type ApiClient,
} from "@/core/api";

import {
    TokenStorage,
    UserStorage,
    type StoredUser,
} from "@/core/storage";

/* =============================================================================
 * Backend Current User Contract
 * =============================================================================
 *
 * IMPORTANT
 * ---------
 * This is intentionally separate from CurrentUser.
 *
 * The current backend /auth/me/ response currently returns:
 *
 * {
 *     id,
 *     email,
 *     first_name,
 *     last_name,
 *     phone,
 *     is_verified
 * }
 *
 * Optional fields are supported when newer backend versions expose them.
 * =============================================================================
 */

interface BackendCurrentUser {
    readonly id: string;

    readonly email: string;

    readonly first_name: string;

    readonly last_name: string;

    readonly phone: string;

    readonly is_verified: boolean;

    readonly is_active?: boolean;

    readonly employee_id?: string | null;

    readonly is_staff?: boolean;

    readonly is_superuser?: boolean;

    readonly is_internal_user?: boolean;

    readonly organization?: string | null;

    readonly last_login?: string | null;

    readonly created_at?: string;

    readonly updated_at?: string;
}

/* =============================================================================
 * Service Dependencies
 * =============================================================================
 */

/**
 * Dependencies required by AuthService.
 */
export interface AuthServiceDependencies {
    readonly api: ApiClient;

    readonly tokenStorage: TokenStorage;

    readonly userStorage: UserStorage;
}

/* =============================================================================
 * AuthService
 * =============================================================================
 */

/**
 * Central frontend authentication service.
 */
export class AuthService {
    private readonly api: ApiClient;

    private readonly tokenStorage: TokenStorage;

    private readonly userStorage: UserStorage;

    /**
     * Shared refresh operation.
     *
     * Prevents concurrent callers from issuing multiple refresh requests.
     */
    private refreshPromise:
        | Promise<AuthTokenPair>
        | null = null;

    /**
     * Construct the authentication service.
     */
    public constructor(
        dependencies: AuthServiceDependencies,
    ) {
        this.api =
            dependencies.api;

        this.tokenStorage =
            dependencies.tokenStorage;

        this.userStorage =
            dependencies.userStorage;
    }

    /* =========================================================================
     * Registration
     * =========================================================================
     */

    /**
     * Register a new DatavionOS account.
     */
    public async register(
        request: RegisterRequest,
    ): Promise<RegisterResponse> {
        const response =
            await this.api.post<
                RegisterResponse,
                RegisterRequest
            >(
                AUTH_API_PATHS.REGISTER,
                request,
                {
                    skipAuth: true,
                    skipTenant: true,
                },
            );

        return unwrapData(
            response,
        );
    }

    /* =========================================================================
     * Email Verification
     * =========================================================================
     */

    /**
     * Verify a user's email address.
     */
    public async verifyEmail(
        request: VerifyEmailRequest,
    ): Promise<AuthUser> {
        const response =
            await this.api.post<
                AuthUser,
                VerifyEmailRequest
            >(
                AUTH_API_PATHS.VERIFY_EMAIL,
                request,
                {
                    skipAuth: true,
                    skipTenant: true,
                },
            );

        return unwrapData(
            response,
        );
    }

    /**
     * Request another email verification OTP.
     */
    public async resendEmailVerification(
        email: string,
    ): Promise<void> {
        await this.api.post<
            null,
            {
                readonly email: string;
            }
        >(
            AUTH_API_PATHS.RESEND_EMAIL_VERIFICATION,
            {
                email,
            },
            {
                skipAuth: true,
                skipTenant: true,
            },
        );
    }

    /* =========================================================================
     * Login
     * =========================================================================
     */

    /**
     * Start the password + OTP login flow.
     *
     * This endpoint only creates the OTP challenge.
     *
     * No authentication tokens are persisted here.
     */
    public async requestLoginOTP(
        request: LoginRequest,
    ): Promise<LoginOTPRequestResponse> {
        const response =
            await this.api.post<
                LoginOTPRequestResponse,
                LoginRequest
            >(
                AUTH_API_PATHS.LOGIN,
                request,
                {
                    skipAuth: true,
                    skipTenant: true,
                },
            );

        return unwrapData(
            response,
        );
    }

    /**
     * Verify the login OTP.
     *
     * The verification endpoint returns the authentication token pair.
     *
     * After tokens are persisted, /auth/me/ is called to obtain the
     * authoritative current user.
     */
    public async verifyLoginOTP(
        request: VerifyLoginOTPRequest,
    ): Promise<AuthSession> {
        const response =
            await this.api.post<
                AuthenticationResponse,
                VerifyLoginOTPRequest
            >(
                AUTH_API_PATHS.VERIFY_LOGIN_OTP,
                request,
                {
                    skipAuth: true,
                    skipTenant: true,
                },
            );

        const authentication =
            unwrapData(
                response,
            );

        const tokens: AuthTokenPair = {
            access:
                authentication.access,

            refresh:
                authentication.refresh,
        };

        /*
         * Tokens must be persisted before requesting /auth/me/.
         */
        this.tokenStorage.setTokens(
            tokens,
        );

        /*
         * /auth/me/ is the authoritative source for the authenticated user.
         *
         * getCurrentUser() normalizes and persists the user.
         */
        const user =
            await this.getCurrentUser();

        return {
            user,
            tokens,
        };
    }

    /* =========================================================================
     * Current User
     * =========================================================================
     */

    /**
     * Retrieve the authoritative authenticated user.
     *
     * The backend /auth/me/ endpoint is the source of truth.
     *
     * The raw backend response is represented by BackendCurrentUser rather than
     * CurrentUser because the backend currently returns only a subset of the
     * complete frontend authentication contract.
     */
    public async getCurrentUser(): Promise<CurrentUser> {
        const response =
            await this.api.get<
                BackendCurrentUser
            >(
                AUTH_API_PATHS.ME,
            );

        const result =
            unwrapData(
                response,
            );

        /*
         * Convert the backend representation into the persistence contract.
         */
        const storedUser =
            this.toStoredUser(
                result,
            );

        this.userStorage.setUser(
            storedUser,
        );

        /*
         * Convert the backend representation into the canonical frontend
         * authentication contract.
         */
        return this.toCurrentUser(
            result,
        );
    }

    /* =========================================================================
     * Token Refresh
     * =========================================================================
     */

    /**
     * Refresh the access token.
     *
     * Concurrent callers share the same in-flight refresh operation.
     */
    public async refreshToken(): Promise<AuthTokenPair> {
        if (
            this.refreshPromise
        ) {
            return this.refreshPromise;
        }

        this.refreshPromise =
            this.performTokenRefresh();

        try {
            return await this.refreshPromise;
        } finally {
            this.refreshPromise =
                null;
        }
    }

    /**
     * Perform the actual refresh request.
     */
    private async performTokenRefresh(): Promise<AuthTokenPair> {
        const refresh =
            this.tokenStorage.getRefreshToken();

        if (!refresh) {
            throw new Error(
                "No refresh token is available.",
            );
        }

        const request: RefreshTokenRequest = {
            refresh,
        };

        const response =
            await this.api.post<
                RefreshTokenResponse,
                RefreshTokenRequest
            >(
                AUTH_API_PATHS.REFRESH,
                request,
                {
                    skipAuth: true,
                    skipTenant: true,
                },
            );

        const result =
            unwrapData(
                response,
            );

        /*
         * The current backend contract returns only a new access token.
         *
         * The existing refresh token remains the active refresh credential.
         */
        const tokens: AuthTokenPair = {
            access:
                result.access,

            refresh,
        };

        this.tokenStorage.setTokens(
            tokens,
        );

        return tokens;
    }

    /* =========================================================================
     * Logout
     * =========================================================================
     */

    /**
     * Logout the current authenticated session.
     *
     * Local credentials are cleared regardless of whether the backend logout
     * request succeeds.
     */
    public async logout(): Promise<LogoutResponse> {
        const refresh =
            this.tokenStorage.getRefreshToken();

        try {
            if (refresh) {
                const request: LogoutRequest = {
                    refresh,
                };

                const response =
                    await this.api.post<
                        LogoutResponse,
                        LogoutRequest
                    >(
                        AUTH_API_PATHS.LOGOUT,
                        request,
                    );

                return unwrapData(
                    response,
                );
            }

            return {
                success: true,
            };
        } finally {
            this.clearLocalSession();
        }
    }

    /* =========================================================================
     * Password
     * =========================================================================
     */

    /**
     * Request a password reset OTP.
     */
    public async forgotPassword(
        request: ForgotPasswordRequest,
    ): Promise<void> {
        await this.api.post<
            null,
            ForgotPasswordRequest
        >(
            AUTH_API_PATHS.FORGOT_PASSWORD,
            request,
            {
                skipAuth: true,
                skipTenant: true,
            },
        );
    }

    /**
     * Reset password using OTP.
     */
    public async resetPassword(
        request: ResetPasswordRequest,
    ): Promise<void> {
        await this.api.post<
            null,
            ResetPasswordRequest
        >(
            AUTH_API_PATHS.RESET_PASSWORD,
            request,
            {
                skipAuth: true,
                skipTenant: true,
            },
        );
    }

    /**
     * Change password for an authenticated user.
     */
    public async changePassword(
        request: ChangePasswordRequest,
    ): Promise<void> {
        await this.api.post<
            null,
            ChangePasswordRequest
        >(
            AUTH_API_PATHS.CHANGE_PASSWORD,
            request,
        );
    }

    /* =========================================================================
     * OAuth
     * =========================================================================
     */

    /**
     * Authenticate using OAuth.
     *
     * OAuth tokens are persisted first, followed by authoritative user
     * resolution through /auth/me/.
     */
    public async loginWithOAuth(
        request: OAuthLoginRequest,
    ): Promise<AuthSession> {
        const response =
            await this.api.post<
                OAuthLoginResponse,
                OAuthLoginRequest
            >(
                AUTH_API_PATHS.OAUTH,
                request,
                {
                    skipAuth: true,
                    skipTenant: true,
                },
            );

        const result =
            unwrapData(
                response,
            );

        const tokens: AuthTokenPair = {
            access:
                result.access,

            refresh:
                result.refresh,
        };

        /*
         * Persist OAuth credentials before resolving the current user.
         */
        this.tokenStorage.setTokens(
            tokens,
        );

        /*
         * Resolve the authoritative user from /auth/me/.
         */
        const user =
            await this.getCurrentUser();

        return {
            user,
            tokens,
        };
    }

    /* =========================================================================
     * Authentication State
     * =========================================================================
     */

    /**
     * Return whether a complete local authentication session exists.
     */
    public isAuthenticated(): boolean {
        return (
            this.tokenStorage.hasTokens() &&
            this.userStorage.hasUser()
        );
    }

    /**
     * Return the persisted frontend user representation.
     */
    public getStoredUser(): StoredUser | null {
        return this.userStorage.getUser();
    }

    /**
     * Clear local authentication state.
     *
     * No network request is performed.
     */
    public clearLocalSession(): void {
        this.tokenStorage.clear();

        this.userStorage.clearUser();

        this.refreshPromise =
            null;
    }

    /* =========================================================================
     * API -> Storage Mapping
     * =========================================================================
     */

    /**
     * Convert the actual backend /auth/me/ response into the frontend
     * persistence representation.
     *
     * Backend representation:
     *
     *     first_name
     *     last_name
     *     is_verified
     *     optional is_active
     *     optional organization
     *
     * Frontend storage representation:
     *
     *     firstName
     *     lastName
     *     isVerified
     *     isActive
     *     organizationId
     *
     * UserStorage remains the final validation and persistence boundary.
     */
    private toStoredUser(
        user: BackendCurrentUser,
    ): StoredUser {
        return {
            id:
                user.id,

            email:
                user.email,

            firstName:
                user.first_name,

            lastName:
                user.last_name,

            phone:
                user.phone,

            isVerified:
                user.is_verified,

            /*
             * The current backend /me/ response does not expose is_active.
             *
             * The authenticated /me/ response is therefore normalized to
             * active until the backend exposes an authoritative value.
             */
            isActive:
                user.is_active ??
                true,

            organizationId:
                user.organization ??
                null,
        };
    }

    /* =========================================================================
     * API -> Domain Mapping
     * =========================================================================
     */

    /**
     * Convert the backend current-user representation into the canonical
     * frontend CurrentUser contract.
     *
     * Fields not currently exposed by the backend receive explicit defaults.
     *
     * These defaults are centralized here rather than being scattered through
     * application components.
     */
    private toCurrentUser(
        user: BackendCurrentUser,
    ): CurrentUser {
        return {
            id:
                user.id,

            email:
                user.email,

            first_name:
                user.first_name,

            last_name:
                user.last_name,

            phone:
                user.phone,

            is_verified:
                user.is_verified,

            is_active:
                user.is_active ??
                true,

            employee_id:
                user.employee_id ??
                null,

            is_staff:
                user.is_staff ??
                false,

            is_superuser:
                user.is_superuser ??
                false,

            is_internal_user:
                user.is_internal_user ??
                false,

            organization:
                user.organization ??
                null,

            last_login:
                user.last_login ??
                null,

            created_at:
                user.created_at ??
                "",

            updated_at:
                user.updated_at ??
                "",

            profile: {
                avatar:
                    null,

                timezone:
                    "UTC",

                language:
                    "en",

                theme:
                    "system",

                locale:
                    "en",
            },
        };
    }
}

/* =============================================================================
 * Factory
 * =============================================================================
 */

/**
 * Create an authentication service.
 */
export function createAuthService(
    dependencies: AuthServiceDependencies,
): AuthService {
    return new AuthService(
        dependencies,
    );
}
