"use client";

import type {
  ModuleDataQuery,
  ModuleDataRecord,
  ModuleDataResponse,
} from "./types";

function isRecord(value: unknown): value is ModuleDataRecord {
  return Boolean(
    value &&
      typeof value === "object" &&
      !Array.isArray(value),
  );
}

function normalizeRows(payload: unknown): ModuleDataResponse {
  if (Array.isArray(payload)) {
    return { rows: payload.filter(isRecord) };
  }

  if (!isRecord(payload)) {
    return { rows: [] };
  }

  const rawRows =
    payload.results ??
    payload.data ??
    payload.items ??
    payload.rows;

  return {
    rows: Array.isArray(rawRows)
      ? rawRows.filter(isRecord)
      : [],
    count:
      typeof payload.count === "number"
        ? payload.count
        : undefined,
    next:
      typeof payload.next === "string"
        ? payload.next
        : null,
    previous:
      typeof payload.previous === "string"
        ? payload.previous
        : null,
  };
}

function buildUrl(
  apiPrefix: string,
  query: ModuleDataQuery,
): string | null {
  const trimmed = apiPrefix.trim();

  if (!trimmed || !trimmed.startsWith("/")) {
    return null;
  }

  const params = new URLSearchParams();

  if (query.search?.trim()) {
    params.set("search", query.search.trim());
  }

  if (query.page && query.page > 1) {
    params.set("page", String(query.page));
  }

  if (query.pageSize) {
    params.set("page_size", String(query.pageSize));
  }

  const queryString = params.toString();

  if (!queryString) {
    return trimmed;
  }

  return `${trimmed}${trimmed.includes("?") ? "&" : "?"}${queryString}`;
}

export async function fetchModuleData(
  apiPrefix: string,
  query: ModuleDataQuery = {},
): Promise<ModuleDataResponse> {
  const url = buildUrl(apiPrefix, query);

  if (!url) {
    return { rows: [] };
  }

  const response = await fetch(url, {
    method: "GET",
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(
      `Module data request failed with status ${response.status}.`,
    );
  }

  return normalizeRows(await response.json());
}
