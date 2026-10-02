import { apiClient } from "@/core/api";
import type { HrRecord } from "./config";

export function rowsFrom(data: unknown): HrRecord[] {
  if (Array.isArray(data)) return data as HrRecord[];
  if (data && typeof data === "object") {
    const value = data as HrRecord;
    const rows = value.results ?? value.items ?? value.rows;
    if (Array.isArray(rows)) return rows as HrRecord[];
  }
  throw new Error("The HR API returned an unexpected collection response.");
}

export async function listRecords(path: string, params: Record<string, string | number> = {}) {
  const response = await apiClient.get<unknown>(path, { params });
  const rows = rowsFrom(response.data);
  const pagination = (response.meta as unknown as { pagination?: Record<string, unknown> } | undefined)?.pagination;
  const payload = response.data as HrRecord | null;
  return {
    rows,
    count: Number(pagination?.count ?? payload?.count ?? rows.length),
    hasNext: Boolean(pagination?.next ?? payload?.next),
  };
}

export async function lookupRecords(path: string) {
  const rows: HrRecord[] = [];
  for (let page = 1; ; page++) {
    const result = await listRecords(path, { page, page_size: 100 });
    rows.push(...result.rows);
    if (!result.hasNext) return rows;
  }
}

export function errorMessage(error: unknown): string {
  if (error && typeof error === "object" && "message" in error) {
    const value = error as { message: string; details?: unknown };
    return value.details ? `${value.message} ${JSON.stringify(value.details)}` : value.message;
  }
  return "The request could not be completed. Please try again.";
}

export function display(value: unknown): string {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (typeof value === "object") {
    if (Array.isArray(value)) return value.map(display).join(", ");
    const row = value as HrRecord;
    return String(row.full_name ?? row.name ?? row.title ?? row.id ?? "—");
  }
  return String(value);
}
