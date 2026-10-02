/**
 * DatavionOS canonical frontend runtime contract.
 *
 * IMPORTANT:
 * The frontend consumes backend authority.
 * It does not calculate authorization independently.
 */

export type RuntimeMap = Record<string, boolean>;
export type RuntimeAnyMap = Record<string, unknown>;

export interface DatavionRuntimeUser {
  id?: string | null;
  email?: string | null;
  username?: string | null;
  name?: string | null;
  [key: string]: unknown;
}

export interface DatavionRuntimeOrganization {
  id?: string | null;
  name?: string | null;
  code?: string | null;
  organization_type?: string | null;
  [key: string]: unknown;
}

export interface DatavionRuntimeSubscription {
  id?: string | null;
  status?: string | null;
  plan?: Record<string, unknown> | null;
  [key: string]: unknown;
}

export interface DatavionEffectiveContext {
  user_id?: string | null;
  organization_id?: string | null;
  tenant_id?: string | null;

  modules: RuntimeMap;
  features: RuntimeMap;

  permissions: string[];
  roles: string[];

  facilities: string[];
  departments: string[];

  data_scopes: RuntimeAnyMap;
  ai_capabilities: RuntimeMap;
  limits: RuntimeAnyMap;

  [key: string]: unknown;
}

export interface DatavionDashboardContext {
  modules: RuntimeMap;
  features: RuntimeMap;
  roles: string[];
  permissions: string[];
  departments: string[];
  facilities: string[];
  limits: RuntimeAnyMap;

  [key: string]: unknown;
}

export interface DatavionBootstrapResponse {
  authenticated: boolean;

  user: DatavionRuntimeUser | null;
  organization: DatavionRuntimeOrganization | null;
  subscription: DatavionRuntimeSubscription | null;

  effective_context: DatavionEffectiveContext;

  dashboard: DatavionDashboardContext;

  navigation: unknown[];

  capabilities?: RuntimeAnyMap;
  metadata?: RuntimeAnyMap;

  [key: string]: unknown;
}

export interface DatavionRuntimeState {
  authenticated: boolean;
  loading: boolean;
  error: string | null;

  user: DatavionRuntimeUser | null;
  organization: DatavionRuntimeOrganization | null;
  subscription: DatavionRuntimeSubscription | null;

  effectiveContext: DatavionEffectiveContext | null;

  modules: RuntimeMap;
  features: RuntimeMap;

  roles: string[];
  permissions: string[];
  departments: string[];
  facilities: string[];

  limits: RuntimeAnyMap;

  dashboard: DatavionDashboardContext | null;
  navigation: unknown[];

  raw: DatavionBootstrapResponse | null;
}
