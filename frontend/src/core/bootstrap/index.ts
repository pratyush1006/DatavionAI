/**
 * =============================================================================
 * DatavionOS
 * File: src/core/bootstrap/index.ts
 * =============================================================================
 *
 * Public bootstrap boundary.
 * =============================================================================
 */

/* =============================================================================
 * API
 * =============================================================================
 */

export {
  fetchPlatformBootstrap,
  PLATFORM_BOOTSTRAP_ENDPOINT,
} from "./api";

/* =============================================================================
 * Query
 * =============================================================================
 */

export {
  BOOTSTRAP_QUERY_KEY,
} from "./keys";

export {
  platformBootstrapQuery,
} from "./queries";

/* =============================================================================
 * Provider
 * =============================================================================
 */

export {
  BootstrapProvider,
  useBootstrap,
  useRequiredBootstrap,
} from "./provider";

export type {
  BootstrapContextValue,
  BootstrapProviderProps,
} from "./provider";

/* =============================================================================
 * Runtime Types
 * =============================================================================
 */

export type {
  BootstrapBranding,
  BootstrapDashboardCard,
  BootstrapEmployee,
  BootstrapMeta,
  BootstrapModule,
  BootstrapNavigationItem,
  BootstrapOrganization,
  BootstrapSubscription,
  BootstrapSubscriptionPlan,
  BootstrapTenant,
  BootstrapUser,
  PlatformBootstrap,
  BootstrapPayload,
} from "./types";
