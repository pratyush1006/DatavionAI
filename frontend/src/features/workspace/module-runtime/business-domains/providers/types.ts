import type { ModuleRuntimeDefinition } from "../../domain/types";

export type ProvidersWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type ProvidersWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type ProvidersAiBoundary = Readonly<{
  department: "providers";
  owner: "providers";
  enabledByOrganization: boolean;
}>;
