/**
 * =============================================================================
 * DatavionOS
 * File: src/core/bootstrap/api.ts
 * =============================================================================
 *
 * Platform bootstrap API.
 *
 * Bootstrap is retrieved exclusively through the canonical DatavionOS
 * ApiClient.
 *
 * The backend exposes:
 *
 *     /api/platform/bootstrap/
 *
 * The canonical ApiClient validates the DatavionOS response envelope and
 * returns an ApiSuccessResponse<T>.
 *
 * This module unwraps only the bootstrap business payload.
 *
 * Architecture:
 *
 *     Bootstrap API
 *          |
 *          v
 *     @/core/api
 *          |
 *          v
 *     ApiClient
 *          |
 *          v
 *     ApiSuccessResponse<PlatformBootstrap>
 *          |
 *          v
 *     PlatformBootstrap
 *
 * =============================================================================
 */

import {
  apiClient,
} from "@/core/api";

import type {
  ApiSuccessResponse,
} from "@/core/types";

import type {
  PlatformBootstrap,
} from "./types";

/* =============================================================================
 * Constants
 * =============================================================================
 */

/**
 * Platform bootstrap endpoint relative to the canonical API base URL.
 *
 * ApiClient base URL:
 *
 *     /api
 *
 * Final request URL:
 *
 *     /api/platform/bootstrap/
 */
export const PLATFORM_BOOTSTRAP_ENDPOINT =
  "/platform/bootstrap/";

/* =============================================================================
 * API
 * =============================================================================
 */

/**
 * Fetch the authenticated platform bootstrap payload.
 *
 * The backend is authoritative for:
 *
 * - identity
 * - tenant context
 * - organization context
 * - employee context
 * - roles
 * - permissions
 * - enabled modules
 * - navigation
 * - dashboard
 * - branding
 * - feature flags
 * - subscription
 * - preferences
 *
 * ApiClient validates the HTTP/API envelope.
 *
 * This function returns only the business payload so callers such as
 * TanStack Query and BootstrapProvider do not need to know about the
 * transport envelope.
 */
export async function fetchPlatformBootstrap(): Promise<PlatformBootstrap> {
  const response: ApiSuccessResponse<PlatformBootstrap> =
    await apiClient.get<PlatformBootstrap>(
      PLATFORM_BOOTSTRAP_ENDPOINT,
    );

  const bootstrap = response.data;
  // Auth identity responses may omit scope IDs. Install the backend-resolved
  // context before consumers start organization-scoped queries.
  apiClient.setOrganizationProvider({
    getOrganizationId: () => bootstrap.organization?.id ?? bootstrap.access_context.organization_id ?? null,
  });
  apiClient.setTenantProvider({
    getTenantId: () => bootstrap.tenant?.id ?? null,
  });
  return bootstrap;
}

/* =============================================================================
 * Public API
 * =============================================================================
 */

export default fetchPlatformBootstrap;
