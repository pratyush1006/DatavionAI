import { API_BASE_URL } from "@/core/api/config";

export type CapabilityMap =
  Record<string, boolean>;

export interface EffectiveCapabilityContext {
  user_id: string;
  organization_id: string;
  tenant_id: string | null;

  modules: CapabilityMap;
  module_state: CapabilityMap;
  features: CapabilityMap;

  permissions: string[];
  roles: string[];

  facilities: string[];
  departments: string[];

  data_scopes:
    Record<string, unknown>;

  ai_capabilities:
    Record<string, boolean>;

  limits:
    Record<string, unknown>;
}

export interface EffectiveCapabilityResponse {
  success: boolean;
  status: string;

  user_id?: string;
  organization_id?: string;
  tenant_id?: string | null;

  modules?: CapabilityMap;
  module_state?: CapabilityMap;
  features?: CapabilityMap;

  permissions?: string[];
  roles?: string[];

  facilities?: string[];
  departments?: string[];

  data_scopes?:
    Record<string, unknown>;

  ai_capabilities?:
    Record<string, boolean>;

  limits?:
    Record<string, unknown>;

  effective_capabilities?:
    EffectiveCapabilityContext;

  capabilities?: {
    effective_capabilities?:
      EffectiveCapabilityContext;
  };

  error?: {
    code?: string;
    message?: string;
  };
}

export function getEffectiveCapabilityEndpoint(): string {
  const explicit =
    process.env
      .NEXT_PUBLIC_EFFECTIVE_CAPABILITY_ENDPOINT;

  if (explicit) {
    return explicit.replace(
      /\/+$/,
      "",
    );
  }

  return (
    `${API_BASE_URL}/datavionos/effective-context/`
  );
}

export function normalizeEffectiveCapability(
  payload: EffectiveCapabilityResponse,
): EffectiveCapabilityContext {
  const nested =
    payload.capabilities
      ?.effective_capabilities ??
    payload.effective_capabilities;

  return {
    user_id:
      nested?.user_id ??
      payload.user_id ??
      "",

    organization_id:
      nested?.organization_id ??
      payload.organization_id ??
      "",

    tenant_id:
      nested?.tenant_id ??
      payload.tenant_id ??
      null,

    modules:
      nested?.modules ??
      payload.modules ??
      {},

    module_state:
      nested?.module_state ??
      payload.module_state ??
      nested?.modules ??
      payload.modules ??
      {},

    features:
      nested?.features ??
      payload.features ??
      {},

    permissions:
      nested?.permissions ??
      payload.permissions ??
      [],

    roles:
      nested?.roles ??
      payload.roles ??
      [],

    facilities:
      nested?.facilities ??
      payload.facilities ??
      [],

    departments:
      nested?.departments ??
      payload.departments ??
      [],

    data_scopes:
      nested?.data_scopes ??
      payload.data_scopes ??
      {},

    ai_capabilities:
      nested?.ai_capabilities ??
      payload.ai_capabilities ??
      {},

    limits:
      nested?.limits ??
      payload.limits ??
      {},
  };
}

export function isModuleEnabled(
  context:
    | EffectiveCapabilityContext
    | null,
  name: string,
): boolean {
  if (!context) {
    return false;
  }

  return Boolean(
    context.modules[name] ??
      context.module_state[name],
  );
}

export function isFeatureEnabled(
  context:
    | EffectiveCapabilityContext
    | null,
  name: string,
): boolean {
  if (!context) {
    return false;
  }

  return Boolean(
    context.features[name],
  );
}

export function isAIEnabled(
  context:
    | EffectiveCapabilityContext
    | null,
  name: string,
): boolean {
  if (!context) {
    return false;
  }

  return Boolean(
    context.ai_capabilities[name],
  );
}

export function hasPermission(
  context:
    | EffectiveCapabilityContext
    | null,
  permission: string,
): boolean {
  if (!context) {
    return false;
  }

  return context.permissions.includes(
    permission,
  );
}

export function hasAnyPermission(
  context:
    | EffectiveCapabilityContext
    | null,
  permissions: string[],
): boolean {
  return permissions.some(
    (permission) =>
      hasPermission(
        context,
        permission,
      ),
  );
}
