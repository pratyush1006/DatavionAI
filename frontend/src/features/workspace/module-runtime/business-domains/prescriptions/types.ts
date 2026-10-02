import type { ModuleRuntimeDefinition } from "../../domain/types";

export type PrescriptionsWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type PrescriptionsWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type PrescriptionsAiBoundary = Readonly<{
  department: "prescriptions";
  owner: "prescriptions";
  enabledByOrganization: boolean;
}>;
