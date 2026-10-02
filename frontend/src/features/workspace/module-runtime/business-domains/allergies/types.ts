import type { ModuleRuntimeDefinition } from "../../domain/types";

export type AllergiesWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type AllergiesWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type AllergiesAiBoundary = Readonly<{
  department: "allergies";
  owner: "allergies";
  enabledByOrganization: boolean;
}>;
