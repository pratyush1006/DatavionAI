/**
 * =============================================================================
 * DatavionOS
 * File: src/core/bootstrap/types.ts
 * =============================================================================
 *
 * Frontend runtime contract for the DatavionOS platform bootstrap response.
 *
 * The backend is the authoritative source for:
 *
 * - identity
 * - tenant context
 * - organization context
 * - employee context
 * - RBAC
 * - effective permissions
 * - enabled modules
 * - navigation
 * - dashboard
 * - branding
 * - feature flags
 * - subscription
 * - preferences
 *
 * The PlatformBootstrap type represents the API `data` payload.
 *
 * The surrounding HTTP/API envelope is owned by:
 *
 *     @/core/types/api
 *
 * =============================================================================
 */

import type {
  ISODateTime,
  UUID,
} from "@/core/types";

/* =============================================================================
 * User
 * =============================================================================
 */

export interface BootstrapUser {
  readonly id: UUID;

  readonly email?: string;

  readonly username?: string;

  readonly first_name?: string;

  readonly last_name?: string;

  readonly full_name?: string;
}

/* =============================================================================
 * Tenant
 * =============================================================================
 */

export interface BootstrapTenant {
  readonly id: UUID;

  readonly name: string;

  readonly tenant_type: string;

  readonly status: string;
}

/* =============================================================================
 * Organization
 * =============================================================================
 */

export interface BootstrapOrganization {
  readonly id: UUID;

  readonly name: string;
}

/* =============================================================================
 * Employee
 * =============================================================================
 */

export interface BootstrapEmployee {
  readonly id: UUID;

  readonly employee_code: string;
}

/* =============================================================================
 * Module
 * =============================================================================
 */

export interface BootstrapModule {
  readonly identifier: string;

  readonly name: string;

  readonly display_name: string;

  readonly description: string;

  readonly version: string;

  readonly category: string;

  readonly route: string;

  readonly api_prefix: string;

  readonly icon: string;

  readonly permissions: readonly string[];

  readonly enabled: boolean;

  readonly system: boolean;

  readonly tenant_scoped: boolean;

  readonly order: number;

  readonly tags: readonly string[];

  readonly feature_flags: readonly string[];
}

/* =============================================================================
 * Navigation
 * =============================================================================
 *
 * This mirrors the backend NavigationItem runtime contract.
 *
 * Backend NavigationItem fields:
 *
 *     title
 *     route
 *     icon
 *     category
 *     permissions
 *     order
 *
 * Navigation visibility has already been resolved by the backend navigation
 * builder before the bootstrap payload is serialized.
 *
 * This type intentionally remains separate from the frontend UI
 * NavigationItem contract owned by:
 *
 *     @/core/navigation
 *
 * The navigation subsystem is responsible for adapting this backend DTO into
 * the frontend presentation contract when required.
 * =============================================================================
 */

export interface BootstrapNavigationItem {
  readonly title: string;

  readonly route: string;

  readonly icon: string;

  readonly category: string;

  readonly permissions: readonly string[];

  readonly order: number;
}

/* =============================================================================
 * Dashboard
 * =============================================================================
 */

export interface BootstrapDashboardCard {
  readonly key: string;

  readonly title: string;

  readonly description: string;

  readonly icon: string;

  readonly route: string;

  readonly category: string;

  readonly order: number;
}

/* =============================================================================
 * Branding
 * =============================================================================
 *
 * Branding is intentionally extensible because the backend serializer exposes
 * branding as a runtime object rather than a fixed frontend domain contract.
 * =============================================================================
 */

export type BootstrapBranding =
  Readonly<
    Record<
      string,
      unknown
    >
  >;

/* =============================================================================
 * Subscription
 * =============================================================================
 */

export interface BootstrapSubscriptionPlan {
  readonly name: string;

  readonly code: string;

  readonly billing_cycle: string;
}

export interface BootstrapSubscription {
  readonly status: string;

  readonly auto_renew: boolean;

  readonly plan: BootstrapSubscriptionPlan;
}

/* =============================================================================
 * Platform Bootstrap Payload
 * =============================================================================
 */

export interface PlatformBootstrap {
  /**
   * Authenticated runtime user.
   */
  readonly user: BootstrapUser;

  /**
   * Current tenant.
   */
  readonly tenant:
    | BootstrapTenant
    | null;

  /**
   * Current organization.
   */
  readonly organization:
    | BootstrapOrganization
    | null;

  /**
   * Current employee context.
   */
  readonly employee:
    | BootstrapEmployee
    | null;

  /**
   * Platform-level roles.
   */
  readonly platform_roles:
    readonly string[];

  /**
   * Organization-level roles.
   */
  readonly organization_roles:
    readonly string[];

  /**
   * Effective permissions resolved by the backend.
   */
  readonly permissions:
    readonly string[];

  /**
   * Runtime modules available to the current context.
   */
  readonly modules:
    readonly BootstrapModule[];

  /**
   * Backend-generated runtime navigation.
   */
  readonly navigation:
    readonly BootstrapNavigationItem[];

  /**
   * Runtime dashboard cards.
   */
  readonly dashboard:
    readonly BootstrapDashboardCard[];

  /**
   * Runtime branding configuration.
   */
  readonly branding:
    BootstrapBranding;

  /**
   * Runtime feature flags.
   */
  readonly feature_flags:
    Readonly<
      Record<
        string,
        boolean
      >
    >;

  /**
   * Current subscription.
   */
  readonly subscription:
    | BootstrapSubscription
    | null;

  /**
   * Runtime user/application preferences.
   */
  readonly preferences:
    | Readonly<
        Record<
          string,
          unknown
        >
      >
    | null;
}

/* =============================================================================
 * Bootstrap API Metadata
 * =============================================================================
 *
 * This type represents the standard API metadata when it is needed directly.
 *
 * The normal bootstrap API call should use:
 *
 *     ApiSuccessResponse<PlatformBootstrap>
 *
 * from:
 *
 *     @/core/types/api
 * =============================================================================
 */

export interface BootstrapMeta {
  readonly api_version: string;

  readonly timestamp: ISODateTime;

  readonly request_id?: string;

  readonly tenant_id?: string;
}

/* =============================================================================
 * Public API
 * =============================================================================
 *
 * Alias retained for callers that use the generic BootstrapPayload name.
 * =============================================================================
 */

export type {
  PlatformBootstrap as BootstrapPayload,
};
