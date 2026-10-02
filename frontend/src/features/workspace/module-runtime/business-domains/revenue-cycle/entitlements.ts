import type { ModuleRuntimeDefinition } from "../../domain/types";

export type RevenueCycleModuleId =
  | "billing"
  | "charge_capture"
  | "coding"
  | "claims"
  | "eligibility"
  | "prior_authorization"
  | "denials"
  | "payment_posting"
  | "accounts_receivable"
  | "appeals"
  | "era"
  | "revenue_analytics";

export type RevenueCycleEntitlementStatus =
  | "NOT_ENTITLED"
  | "ENTITLED_DISABLED"
  | "ENTITLED_ENABLED"
  | "SUSPENDED"
  | "UPGRADE_REQUIRED"
  | "DEPRECATED";

export type RevenueCycleModuleCatalogEntry = Readonly<{
  id: RevenueCycleModuleId;
  label: string;
  department: "revenue_cycle";
  aiOwner: "revenue_cycle";
}>;

export type RevenueCycleEntitlementState = Readonly<{
  module: RevenueCycleModuleCatalogEntry;
  status: RevenueCycleEntitlementStatus;
  entitled: boolean;
  organizationEnabled: boolean;
  available: boolean;
  source: "backend_effective_context";
}>;

export type RevenueCycleEffectiveContext = Readonly<{
  revenueCycle?: Readonly<{
    entitlements?: Partial<
      Record<RevenueCycleModuleId, RevenueCycleEntitlementStatus>
    >;
    enabledModules?: readonly RevenueCycleModuleId[];
  }>;
}>;

export type RevenueCycleEntitlementRuntime = Readonly<{
  module: ModuleRuntimeDefinition;
  states: readonly RevenueCycleEntitlementState[];
  enabled: readonly RevenueCycleModuleId[];
  locked: readonly RevenueCycleModuleId[];
}>;

export const REVENUE_CYCLE_MODULE_CATALOG:
  readonly RevenueCycleModuleCatalogEntry[] = [
  {
    id: "billing",
    label: "Billing",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "charge_capture",
    label: "Charge Capture",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "coding",
    label: "Coding",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "claims",
    label: "Claims",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "eligibility",
    label: "Eligibility",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "prior_authorization",
    label: "Prior Authorization",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "denials",
    label: "Denials",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "payment_posting",
    label: "Payment Posting",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "accounts_receivable",
    label: "Accounts Receivable",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "appeals",
    label: "Appeals",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "era",
    label: "Era",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
  {
    id: "revenue_analytics",
    label: "Revenue Analytics",
    department: "revenue_cycle",
    aiOwner: "revenue_cycle",
  },
];

const DEFAULT_STATUS: RevenueCycleEntitlementStatus =
  "NOT_ENTITLED";

function isAvailableStatus(
  status: RevenueCycleEntitlementStatus,
): boolean {
  return status === "ENTITLED_ENABLED";
}

export function resolveRevenueCycleEntitlements(
  context: RevenueCycleEffectiveContext,
): readonly RevenueCycleEntitlementState[] {
  const resolved = context.revenueCycle;

  return REVENUE_CYCLE_MODULE_CATALOG.map((module) => {
    const status =
      resolved?.entitlements?.[module.id] ?? DEFAULT_STATUS;

    const organizationEnabled =
      resolved?.enabledModules?.includes(module.id) ?? false;

    return {
      module,
      status,
      entitled:
        status !== "NOT_ENTITLED" &&
        status !== "UPGRADE_REQUIRED" &&
        status !== "DEPRECATED",
      organizationEnabled,
      available:
        isAvailableStatus(status) &&
        organizationEnabled,
      source: "backend_effective_context",
    };
  });
}

export function getEnabledRevenueCycleModules(
  context: RevenueCycleEffectiveContext,
): readonly RevenueCycleModuleId[] {
  return resolveRevenueCycleEntitlements(context)
    .filter((state) => state.available)
    .map((state) => state.module.id);
}

export function getLockedRevenueCycleModules(
  context: RevenueCycleEffectiveContext,
): readonly RevenueCycleModuleId[] {
  return resolveRevenueCycleEntitlements(context)
    .filter((state) => !state.available)
    .map((state) => state.module.id);
}

export function isRevenueCycleModuleEnabled(
  context: RevenueCycleEffectiveContext,
  moduleId: RevenueCycleModuleId,
): boolean {
  return resolveRevenueCycleEntitlements(context).some(
    (state) =>
      state.module.id === moduleId &&
      state.available,
  );
}

export function resolveRevenueCycleWorkspace(
  module: ModuleRuntimeDefinition,
  context: RevenueCycleEffectiveContext,
): RevenueCycleEntitlementRuntime {
  const states = resolveRevenueCycleEntitlements(context);

  return {
    module,
    states,
    enabled: states
      .filter((state) => state.available)
      .map((state) => state.module.id),
    locked: states
      .filter((state) => !state.available)
      .map((state) => state.module.id),
  };
}
