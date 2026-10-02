import type { ModuleRuntimeDefinition } from "../../domain/types";

export type PharmacyWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type PharmacyWorkspaceState =
  | "loading"
  | "ready"
  | "empty"
  | "error";

export type PharmacyAiBoundary = Readonly<{
  department: "pharmacy";
  owner: "pharmacy";
  enabledByOrganization: boolean;
}>;
