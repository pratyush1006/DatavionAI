import type { ModuleRuntimeDefinition } from "../../domain/types";

export type LaboratoryWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type LaboratoryWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type LaboratoryAiBoundary = Readonly<{
  department: "laboratory";
  owner: "laboratory";
  enabledByOrganization: boolean;
}>;
