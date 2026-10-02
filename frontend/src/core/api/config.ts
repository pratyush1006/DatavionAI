/**
 * DatavionOS Canonical Browser API Configuration
 *
 * SINGLE API ENVIRONMENT AUTHORITY
 *
 * Runtime source:
 *   NEXT_PUBLIC_API_BASE_URL
 *
 * All browser API consumers must import their API authority
 * from this module.
 */

export type ApiConfig = {
  baseUrl: string;
  baseURL: string;
  timeout: number;
  version: string;
  withCredentials: boolean;
};

function normalizeApiBaseUrl(value: string): string {
  return value
    .trim()
    .replace(/\/+$/, "");
}

const resolvedApiBaseUrl = normalizeApiBaseUrl(
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "",
);

if (!resolvedApiBaseUrl) {
  throw new Error(
    "NEXT_PUBLIC_API_BASE_URL is required for the DatavionOS browser API runtime.",
  );
}

export const API_BASE_URL = resolvedApiBaseUrl;

export const API_TIMEOUT = 30_000;

// The backend mounts routes directly beneath /api/. Its v1 designation is
// response metadata, not an extra /v1 path segment.
export const API_VERSION = "";

export const API_WITH_CREDENTIALS = true;

export const API_CONFIG: ApiConfig = {
  baseUrl: API_BASE_URL,
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  version: API_VERSION,
  withCredentials: API_WITH_CREDENTIALS,
};

export function buildApiUrl(path: string): string {
  const normalizedPath = path.trim();

  if (!normalizedPath) {
    return API_BASE_URL;
  }

  if (/^https?:\/\//i.test(normalizedPath)) {
    return normalizedPath;
  }

  return `${API_BASE_URL}/${normalizedPath.replace(/^\/+/, "")}`;
}

export const buildApiURL = buildApiUrl;

export function isApiUrl(value: string): boolean {
  const normalizedValue = value.trim();

  if (!normalizedValue) {
    return false;
  }

  return (
    normalizedValue === API_BASE_URL ||
    normalizedValue.startsWith(`${API_BASE_URL}/`)
  );
}
