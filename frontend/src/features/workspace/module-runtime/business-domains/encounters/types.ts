import type { ModuleRuntimeDefinition } from "../../domain/types";

export type EncountersWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type EncountersWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type EncountersAiBoundary = Readonly<{
  department: "encounters";
  owner: "encounters";
  enabledByOrganization: boolean;
}>;
