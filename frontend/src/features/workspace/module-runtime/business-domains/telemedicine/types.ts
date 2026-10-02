import type { ModuleRuntimeDefinition } from "../../domain/types";

export type TelemedicineWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type TelemedicineWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type TelemedicineAiBoundary = Readonly<{
  department: "telemedicine";
  owner: "telemedicine";
  enabledByOrganization: boolean;
}>;
