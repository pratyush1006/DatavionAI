import type { BootstrapModule } from "@/core/bootstrap/types";
import type { ModuleRuntimeDefinition } from "../domain/types";
import type { DomainApiContract } from "../api/domain-types";

export type DomainWorkspaceContract = Readonly<{
  domain:
    | "patients"
    | "appointments"
    | "pharmacy"
    | "laboratory"
    | "documents"
    | "billing";
  moduleIdentifier: string;
  displayName: string;
  route: string;
  apiPrefix: string;
  workspaceType: ModuleRuntimeDefinition["workspaceType"];
  rendererKey: ModuleRuntimeDefinition["rendererKey"];
  contractIdentifiers: readonly string[];
  contractPrefixes: readonly string[];
}>;

export type DomainWorkspaceDefinition = Readonly<{
  id:
    | "patients"
    | "appointments"
    | "pharmacy"
    | "laboratory"
    | "documents"
    | "billing";
  label: string;
  aliases: readonly string[];
}>;

export type DomainWorkspaceBinding = Readonly<{
  definition: DomainWorkspaceDefinition;
  workspace: DomainWorkspaceContract;
  contracts: readonly DomainApiContract[];
}>;

export type DomainWorkspaceResolutionInput = Readonly<{
  module: BootstrapModule;
  runtimeDefinition: ModuleRuntimeDefinition;
}>;
