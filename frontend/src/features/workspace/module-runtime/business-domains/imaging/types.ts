import type { ModuleRuntimeDefinition } from "../../domain/types";

export type ImagingWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type ImagingWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type ImagingAiBoundary = Readonly<{
  department: "imaging";
  owner: "imaging";
  enabledByOrganization: boolean;
}>;
