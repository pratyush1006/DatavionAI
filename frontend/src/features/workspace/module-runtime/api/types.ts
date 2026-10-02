export type ModuleApiContract = Readonly<{
  identifier: string;
  prefix: string;
  group: string;
  routes: readonly string[];
  sources: readonly string[];
}>;

export type ModuleApiRegistry = Readonly<
  Record<string, ModuleApiContract>
>;
