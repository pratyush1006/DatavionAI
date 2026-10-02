
import type { ModuleRuntimeDefinition } from "../domain/types";

export type ModuleAction = Readonly<{
  id: string;
  label: string;
  href?: string;
  variant?:
    | "primary"
    | "secondary"
    | "success"
    | "danger"
    | "warning"
    | "light";
}>;

export type ModuleKpi = Readonly<{
  id: string;
  label: string;
  value: string;
  description?: string;
  trend?: string;
}>;

export type ModuleFilter = Readonly<{
  id: string;
  label: string;
  placeholder?: string;
}>;

export type ModuleTableColumn = Readonly<{
  id: string;
  label: string;
}>;

export type ModuleTable = Readonly<{
  columns: readonly ModuleTableColumn[];
  emptyMessage: string;
}>;

export type ModuleSectionKind =
  | "overview"
  | "kpis"
  | "actions"
  | "filters"
  | "content"
  | "activity"
  | "ai";

export type ModuleSection = Readonly<{
  id: string;
  title: string;
  description?: string;
  kind: ModuleSectionKind;
}>;

export type ModuleUIComposition = Readonly<{
  module: ModuleRuntimeDefinition;
  sections: readonly ModuleSection[];
  actions: readonly ModuleAction[];
  kpis: readonly ModuleKpi[];
  filters: readonly ModuleFilter[];
  table?: ModuleTable;
}>;

export type ModuleCompositionProps = Readonly<{
  composition: ModuleUIComposition;
}>;
