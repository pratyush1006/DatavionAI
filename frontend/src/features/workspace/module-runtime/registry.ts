
import type { BootstrapModule } from "@/core/bootstrap/types";
import type {
  ModuleRendererKey,
  ModuleRuntimeDefinition,
  ModuleWorkspaceType,
} from "./domain/types";

const DEFAULT_ICON = "grid";

function inferWorkspaceType(
  bootstrapModule: BootstrapModule,
): ModuleWorkspaceType {
  const identifier = bootstrapModule.identifier.toLowerCase();
  const category = bootstrapModule.category.toLowerCase();

  if (
    identifier.includes("dashboard") ||
    category.includes("dashboard")
  ) {
    return "dashboard";
  }

  if (
    identifier.includes("detail") ||
    identifier.includes("profile")
  ) {
    return "detail";
  }

  if (
    identifier.includes("workflow") ||
    identifier.includes("process")
  ) {
    return "workflow";
  }

  if (
    identifier.includes("table") ||
    identifier.includes("list") ||
    identifier.includes("management")
  ) {
    return "table";
  }

  return "generic";
}

function inferRendererKey(
  workspaceType: ModuleWorkspaceType,
): ModuleRendererKey {
  if (workspaceType === "dashboard") {
    return "dashboard";
  }

  if (workspaceType === "table") {
    return "table";
  }

  if (workspaceType === "detail") {
    return "detail";
  }

  if (workspaceType === "workflow") {
    return "workflow";
  }

  if (workspaceType === "custom") {
    return "custom";
  }

  return "generic";
}

function deriveDepartment(
  bootstrapModule: BootstrapModule,
): string | undefined {
  const tags = bootstrapModule.tags ?? [];

  const departmentTag = tags.find((tag) =>
    tag.startsWith("department:"),
  );

  if (!departmentTag) {
    return undefined;
  }

  return departmentTag.slice("department:".length);
}

export function createModuleRuntimeDefinition(
  bootstrapModule: BootstrapModule,
): ModuleRuntimeDefinition {
  const workspaceType = inferWorkspaceType(bootstrapModule);

  return {
    identifier: bootstrapModule.identifier,
    displayName:
      bootstrapModule.display_name || bootstrapModule.name,
    description: bootstrapModule.description ?? "",
    route: bootstrapModule.route,
    apiPrefix: bootstrapModule.api_prefix ?? "",
    category: bootstrapModule.category ?? "General",
    icon: DEFAULT_ICON,
    department: deriveDepartment(bootstrapModule),
    version: bootstrapModule.version,
    workspaceType,
    rendererKey: inferRendererKey(workspaceType),
    tags: bootstrapModule.tags ?? [],
    tenantScoped: Boolean(bootstrapModule.tenant_scoped),
    system: Boolean(bootstrapModule.system),
  };
}

export function createModuleRuntimeRegistry(
  modules: readonly BootstrapModule[],
): readonly ModuleRuntimeDefinition[] {
  return modules.map(createModuleRuntimeDefinition);
}

export function findModuleRuntime(
  modules: readonly BootstrapModule[],
  identifier: string,
): ModuleRuntimeDefinition | null {
  const bootstrapModule = modules.find(
    (candidate) => candidate.identifier === identifier,
  );

  return bootstrapModule
    ? createModuleRuntimeDefinition(bootstrapModule)
    : null;
}
