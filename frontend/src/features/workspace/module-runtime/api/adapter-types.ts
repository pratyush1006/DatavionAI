import type { ModuleApiContract } from "./types";

export type ModuleApiRequest = Readonly<{
  contract: ModuleApiContract;
  route?: string;
  query?: Readonly<Record<string, string | number | boolean | undefined>>;
  signal?: AbortSignal;
}>;

export type ModuleApiResponse<T> = Readonly<{
  data: T;
  status: number;
  headers: Headers;
}>;

export type ModuleApiError = Readonly<{
  status: number;
  message: string;
  body?: unknown;
}>;

export type ModuleApiResult<T> =
  | Readonly<{
      ok: true;
      response: ModuleApiResponse<T>;
    }>
  | Readonly<{
      ok: false;
      error: ModuleApiError;
    }>;

export type ModuleListResponse<T> = Readonly<{
  results: readonly T[];
  count?: number;
  next?: string | null;
  previous?: string | null;
}>;
