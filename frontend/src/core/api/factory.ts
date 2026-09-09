/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/factory.ts
 * =============================================================================
 *
 * Application-level API client factory.
 *
 * Responsibilities
 * ----------------
 * - Construct the DatavionOS ApiClient
 * - Provide runtime API dependencies
 * - Provide authentication refresh dependencies
 * - Expose the canonical application API client
 * - Keep construction separate from transport implementation
 *
 * This module is the composition boundary between:
 *
 *     Application Runtime
 *             |
 *             v
 *        API Factory
 *             |
 *             v
 *         ApiClient
 *             |
 *             v
 *           Axios
 *
 * Design Principles
 * -----------------
 * - Dependency Injection
 * - Explicit composition
 * - No React dependency
 * - No feature-specific logic
 * - No direct storage access
 * - Single application API client
 * - Testable
 * - SSR safe
 * - Enterprise Ready
 *
 * =============================================================================
 */

import {
  ApiClient,
} from "./client";

import {
  API_CONFIG,
} from "./config";

import type {
  ApiAuthenticationDependencies,
  ApiRuntimeDependencies,
} from "./contracts";

/* =============================================================================
 * Factory Options
 * =============================================================================
 */

/**
 * Options used when constructing an application API client.
 */
export interface ApiClientFactoryOptions {
  /**
   * Runtime dependencies such as:
   *
   * - Access-token provider
   * - Tenant provider
   * - Request-ID provider
   *
   * All dependencies are optional because ApiClient provides safe defaults
   * for unauthenticated application startup.
   */
  readonly runtime?:
    Partial<ApiRuntimeDependencies>;

  /**
   * Authentication refresh and failure handling.
   */
  readonly authentication?:
    ApiAuthenticationDependencies;
}

/* =============================================================================
 * Factory
 * =============================================================================
 */

/**
 * Create a fully configured DatavionOS API client.
 *
 * The returned client is independent and can be used in:
 *
 * - React applications
 * - Server-side utilities
 * - Tests
 * - Authentication services
 * - Feature services
 *
 * This function should be preferred when a caller requires an isolated
 * API client instance, such as in tests or specialized runtimes.
 */
export function createApplicationApiClient(
  options: ApiClientFactoryOptions = {},
): ApiClient {
  return new ApiClient(
    API_CONFIG,
    options.runtime,
    options.authentication,
  );
}

/* =============================================================================
 * Application API Client
 * =============================================================================
 */

/**
 * Canonical application-level API client.
 *
 * Feature modules should import this instance through:
 *
 *     import { apiClient } from "@/core/api";
 *
 * The client starts with the safe default runtime providers defined by
 * ApiClient and can be configured later by the application/authentication
 * composition layer.
 *
 * This is the ONLY application-level API client singleton.
 *
 * Do not create another singleton in:
 *
 *     client.ts
 *
 *     auth/
 *
 *     feature modules
 *
 *     services/
 *
 *     hooks/
 *
 *     components/
 */
export const apiClient: ApiClient =
  createApplicationApiClient();
