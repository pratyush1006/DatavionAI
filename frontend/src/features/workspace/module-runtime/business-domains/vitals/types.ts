import type { ModuleRuntimeDefinition } from "../../domain/types";

export type VitalsWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type VitalsWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type VitalsAiBoundary = Readonly<{
  department: "vitals";
  owner: "vitals";
  enabledByOrganization: boolean;
}>;
