/**
 * =============================================================================
 * DatavionOS
 * File: src/core/bootstrap/service.ts
 * =============================================================================
 *
 * Platform bootstrap API service.
 *
 * The backend is the authoritative source for runtime platform state.
 *
 * The frontend must not independently calculate:
 *
 * - enabled modules
 * - SaaS entitlements
 * - tenant eligibility
 * - RBAC permissions
 * - navigation visibility
 * - dashboard availability
 *
 * All of those are resolved by the backend bootstrap pipeline.
 * =============================================================================
 */

import {
  apiClient,
} from "@/core/api";

import type {
  PlatformBootstrap,
} from "./types";

/* =============================================================================
 * Endpoints
 * =============================================================================
 */

const BOOTSTRAP_ENDPOINT =
  "/bootstrap/";

/* =============================================================================
 * Service
 * =============================================================================
 */

export class BootstrapService {
  /**
   * Fetch the complete runtime bootstrap payload.
   *
   * ApiClient unwraps the DatavionOS API envelope and returns the success
   * response directly.
   */
  public async getBootstrap(): Promise<PlatformBootstrap> {
    const response =
      await apiClient.get<PlatformBootstrap>(
        BOOTSTRAP_ENDPOINT,
      );

    return response.data;
  }
}

/* =============================================================================
 * Singleton
 * =============================================================================
 *
 * Bootstrap is infrastructure-level functionality, so feature components
 * should use this canonical service rather than constructing their own client.
 * =============================================================================
 */

export const bootstrapService =
  new BootstrapService();

/* =============================================================================
 * Exports
 * =============================================================================
 */

export {
  BOOTSTRAP_ENDPOINT,
};
