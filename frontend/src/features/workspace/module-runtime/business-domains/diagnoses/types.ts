import type { ModuleRuntimeDefinition } from "../../domain/types";

export type DiagnosesWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type DiagnosesWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type DiagnosesAiBoundary = Readonly<{
  department: "diagnoses";
  owner: "diagnoses";
  enabledByOrganization: boolean;
}>;
