import type { ModuleRuntimeDefinition } from "../../domain/types";

export type AppointmentsWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type AppointmentsWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";
