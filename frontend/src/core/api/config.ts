/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/config.ts
 * =============================================================================
 *
 * Central API configuration.
 *
 * The current DatavionOS backend exposes its API directly below:
 *
 *     /api/*
 *
 * Example:
 *
 *     /api/auth/login/
 *
 * API versioning is intentionally optional. When no API version is configured,
 * the API client must NOT inject /v1 or any other version segment.
 *
 * Design Principles
 * -----------------
 * - Single Source of Truth
 * - Environment Driven
 * - Immutable Configuration
 * - SSR Safe
 * - Type Safe
 * - No hardcoded deployment URLs
 * - Optional API versioning
 * - Enterprise Ready
 * =============================================================================
 */

/* =============================================================================
 * Types
 * =============================================================================
 */

export interface ApiConfig {
  readonly baseURL: string;

  /**
   * Optional API version.
   *
   * Empty string means that the configured base URL is already the
   * complete API root.
   */
  readonly version: string;

  readonly timeout: number;

  readonly withCredentials: boolean;
}

/* =============================================================================
 * Defaults
 * =============================================================================
 */

const DEFAULT_API_VERSION = "";

const DEFAULT_TIMEOUT = 30_000;

/**
 * Local-development API root.
 *
 * Production deployments should provide:
 *
 *     NEXT_PUBLIC_API_BASE_URL
 *
 * through the environment.
 */
const DEFAULT_BASE_URL =
  "http://127.0.0.1:8000/api";

/* =============================================================================
 * Environment
 * =============================================================================
 */

/**
 * Read an environment variable safely.
 *
 * Next.js exposes NEXT_PUBLIC_* variables to browser code.
 */
function getEnvironmentValue(
  key: string,
): string | undefined {
  if (
    typeof process === "undefined"
  ) {
    return undefined;
  }

  const value =
    process.env[key];

  if (
    typeof value !== "string"
  ) {
    return undefined;
  }

  const normalized =
    value.trim();

  return (
    normalized ||
    undefined
  );
}

/**
 * Normalize an API base URL.
 *
 * Removes trailing slashes.
 */
function normalizeBaseURL(
  value: string,
): string {
  return value.replace(
    /\/+$/,
    "",
  );
}

/**
 * Normalize an API version.
 *
 * Empty values remain empty.
 *
 * Examples:
 *
 *     "v1"   -> "v1"
 *     "/v1/" -> "v1"
 *     ""     -> ""
 */
function normalizeApiVersion(
  value: string,
): string {
  return value.replace(
    /^\/+|\/+$/g,
    "",
  );
}

/**
 * Resolve API base URL.
 */
function resolveBaseURL(): string {
  const configuredURL =
    getEnvironmentValue(
      "NEXT_PUBLIC_API_BASE_URL",
    );

  return normalizeBaseURL(
    configuredURL ??
      DEFAULT_BASE_URL,
  );
}

/**
 * Resolve API version.
 *
 * The current DatavionOS backend does not expose /api/v1.
 *
 * Therefore the default is intentionally empty.
 */
function resolveApiVersion(): string {
  const configuredVersion =
    getEnvironmentValue(
      "NEXT_PUBLIC_API_VERSION",
    );

  return normalizeApiVersion(
    configuredVersion ??
      DEFAULT_API_VERSION,
  );
}

/**
 * Resolve request timeout.
 */
function resolveTimeout(): number {
  const configuredTimeout =
    getEnvironmentValue(
      "NEXT_PUBLIC_API_TIMEOUT",
    );

  if (
    !configuredTimeout
  ) {
    return DEFAULT_TIMEOUT;
  }

  const timeout =
    Number(
      configuredTimeout,
    );

  if (
    !Number.isFinite(timeout) ||
    timeout <= 0
  ) {
    return DEFAULT_TIMEOUT;
  }

  return timeout;
}

/**
 * Resolve whether credentials should be included.
 */
function resolveWithCredentials(): boolean {
  const configuredValue =
    getEnvironmentValue(
      "NEXT_PUBLIC_API_WITH_CREDENTIALS",
    );

  if (
    configuredValue === undefined
  ) {
    return true;
  }

  return (
    configuredValue.toLowerCase() ===
    "true"
  );
}

/* =============================================================================
 * Public Configuration
 * =============================================================================
 */

/**
 * Immutable DatavionOS API configuration.
 */
export const API_CONFIG: ApiConfig =
  Object.freeze({
    baseURL:
      resolveBaseURL(),

    version:
      resolveApiVersion(),

    timeout:
      resolveTimeout(),

    withCredentials:
      resolveWithCredentials(),
  });

/**
 * API base URL.
 */
export const API_BASE_URL =
  API_CONFIG.baseURL;

/**
 * API version.
 */
export const API_VERSION =
  API_CONFIG.version;

/**
 * API request timeout.
 */
export const API_TIMEOUT =
  API_CONFIG.timeout;

/**
 * Whether browser credentials should be included.
 */
export const API_WITH_CREDENTIALS =
  API_CONFIG.withCredentials;

/* =============================================================================
 * URL Helpers
 * =============================================================================
 */

/**
 * Build an API URL.
 *
 * With the current configuration:
 *
 *     buildApiUrl("/auth/login/")
 *
 * becomes:
 *
 *     http://127.0.0.1:8000/api/auth/login/
 *
 * If an API version is explicitly configured:
 *
 *     NEXT_PUBLIC_API_VERSION=v1
 *
 * then:
 *
 *     http://127.0.0.1:8000/api/v1/auth/login/
 */
export function buildApiUrl(
  path: string,
): string {
  const normalizedPath =
    path.replace(
      /^\/+/,
      "",
    );

  const normalizedVersion =
    normalizeApiVersion(
      API_VERSION,
    );

  return [
    API_BASE_URL,
    normalizedVersion,
    normalizedPath,
  ]
    .filter(Boolean)
    .join("/");
}

/**
 * Return whether a URL belongs to the configured API.
 */
export function isApiUrl(
  url: string,
): boolean {
  const normalizedURL =
    normalizeBaseURL(
      url,
    );

  return (
    normalizedURL ===
      API_BASE_URL ||
    normalizedURL.startsWith(
      `${API_BASE_URL}/`,
    )
  );
}
