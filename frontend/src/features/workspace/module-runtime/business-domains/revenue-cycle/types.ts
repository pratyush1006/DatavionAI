import type { ModuleRuntimeDefinition } from "../../domain/types";

export type RevenueCycleWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type RevenueCycleWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type RevenueCycleAiBoundary = Readonly<{
  department: "revenue_cycle";
  owner: "revenue_cycle";
  enabledByOrganization: boolean;
}>;
