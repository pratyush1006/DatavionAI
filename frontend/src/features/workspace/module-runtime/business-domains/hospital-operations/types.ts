import type { ModuleRuntimeDefinition } from "../../domain/types";

export type HospitalOperationsWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type HospitalOperationsWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type HospitalOperationsRuntimeContract = Readonly<{
  department: "hospital_operations";
  authorizationAuthority: "backend_effective_context";
  dataAdapter: "listModule";
}>;
