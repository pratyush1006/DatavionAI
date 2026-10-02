import type { ModuleRuntimeDefinition } from "../../domain/types";

export type PatientsWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type PatientsWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";
