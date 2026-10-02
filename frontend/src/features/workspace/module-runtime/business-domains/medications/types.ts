import type { ModuleRuntimeDefinition } from "../../domain/types";

export type MedicationsWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type MedicationsWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type MedicationsAiBoundary = Readonly<{
  department: "medications";
  owner: "medications";
  enabledByOrganization: boolean;
}>;
