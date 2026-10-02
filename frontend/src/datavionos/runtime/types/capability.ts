export type CapabilityMap = Record<string, boolean>;

export type ModuleStateMap = Record<string, boolean>;

export type PermissionSet = string[];

export type LimitMap = Record<string, unknown>;

export type EffectiveCapabilityContext = {
  userId: string | null;
  organizationId: string | null;
  tenantId: string | null;

  modules: ModuleStateMap;
  features: CapabilityMap;
  permissions: PermissionSet;
  roles: string[];
  facilities: string[];
  departments: string[];
  dataScopes: Record<string, unknown>;
  aiCapabilities: CapabilityMap;
  limits: LimitMap;

  capabilities?: CapabilityMap;
};

export type RuntimeShellState = {
  loading: boolean;
  ready: boolean;
  error: string | null;
  context: EffectiveCapabilityContext | null;
};
