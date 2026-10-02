
import type { BootstrapModule } from "@/core/bootstrap/types";

export type ModuleWorkspaceType =
  | "dashboard"
  | "table"
  | "detail"
  | "workflow"
  | "custom"
  | "generic";

export type ModuleRendererKey =
  | "generic"
  | "dashboard"
  | "table"
  | "detail"
  | "workflow"
  | "custom";

export type ModuleRuntimeDefinition = Readonly<{
  identifier: string;
  displayName: string;
  description: string;
  route: string;
  apiPrefix: string;
  category: string;
  icon: string;
  department?: string;
  version?: string;
  workspaceType: ModuleWorkspaceType;
  rendererKey: ModuleRendererKey;
  tags: readonly string[];
  tenantScoped: boolean;
  system: boolean;
}>;

export type ModuleRendererProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export type ModuleRenderer = (
  props: ModuleRendererProps,
) => React.ReactNode;

export function isBootstrapModule(
  value: unknown,
): value is BootstrapModule {
  return Boolean(
    value &&
      typeof value === "object" &&
      "identifier" in value &&
      "route" in value &&
      "display_name" in value,
  );
}
