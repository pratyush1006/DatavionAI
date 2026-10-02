export type ModuleDataRecord = Readonly<Record<string, unknown>>;

export type ModuleDataResponse = Readonly<{
  rows: readonly ModuleDataRecord[];
  count?: number;
  next?: string | null;
  previous?: string | null;
}>;

export type ModuleDataQuery = Readonly<{
  search?: string;
  page?: number;
  pageSize?: number;
}>;
