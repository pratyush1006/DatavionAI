"use client";

import { useEffect, useMemo, useState } from "react";

import {
  findModuleApiContract,
  findModuleApiContractByPrefix,
  listModule,
} from "../api";
import type { ModuleApiContract } from "../api";
import type { ModuleTable } from "../composition/types";
import type { ModuleRuntimeDefinition } from "../domain/types";

type ModuleDataRecord = Readonly<Record<string, unknown>>;

type ModuleDataTableProps = Readonly<{
  module: ModuleRuntimeDefinition;
  table?: ModuleTable;
  route?: string;
}>;

type LoadState = Readonly<{
  rows: readonly ModuleDataRecord[];
  loading: boolean;
  error: string | null;
  status: number | null;
}>;

function displayValue(value: unknown): string {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return String(value);
  try { return JSON.stringify(value); } catch { return "—"; }
}

function resolveColumnValue(row: ModuleDataRecord, columnId: string): unknown {
  if (row[columnId] !== undefined) return row[columnId];
  const normalized = columnId.toLowerCase().replaceAll("-", "_");
  const match = Object.entries(row).find(([key]) => key.toLowerCase().replaceAll("-", "_") === normalized);
  return match?.[1];
}

function rowKey(row: ModuleDataRecord, index: number): string {
  const value = row.id ?? row.uuid ?? row.pk;
  return value === undefined || value === null || value === "" ? `row-${index}` : String(value);
}

function resolveContract(module: ModuleRuntimeDefinition): ModuleApiContract | undefined {
  const exact = findModuleApiContract(module.identifier);
  if (exact) return exact;

  // Bootstrap uses the singular product name while the backend API is mounted
  // at /laboratories/. Keep that intentional alias at this boundary.
  if (module.identifier.toLowerCase() === "laboratory") {
    return findModuleApiContract("laboratories");
  }

  return findModuleApiContractByPrefix(module.apiPrefix);
}

export function ModuleDataTable({ module, table, route }: ModuleDataTableProps) {
  const [search, setSearch] = useState("");
  const [state, setState] = useState<LoadState>({ rows: [], loading: true, error: null, status: null });
  const columns = useMemo(() => table?.columns ?? [], [table]);
  const contract = useMemo(() => resolveContract(module), [module]);

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();

    async function load() {
      if (!contract) {
        setState({ rows: [], loading: false, error: "No canonical backend API contract is registered for this module.", status: null });
        return;
      }

      setState((current) => ({ ...current, loading: true, error: null }));
      const result = await listModule<ModuleDataRecord>({
        contract,
        route,
        query: search.trim() ? { search: search.trim() } : {},
        signal: controller.signal,
      });

      if (cancelled) return;
      if (!result.ok) {
        if (result.error.status === 0 && controller.signal.aborted) return;
        setState({ rows: [], loading: false, error: result.error.message, status: result.error.status });
        return;
      }

      setState({ rows: result.response.data.results, loading: false, error: null, status: result.response.status });
    }

    const timer = window.setTimeout(load, 250);
    return () => { cancelled = true; controller.abort(); window.clearTimeout(timer); };
  }, [contract, route, search]);

  if (!table) return <div className="text-body-secondary">This module does not define a data table.</div>;

  return (
    <div className="d-flex flex-column gap-3">
      <div className="row g-2">
        <div className="col-12 col-lg-8">
          <label className="visually-hidden" htmlFor={`module-search-${module.identifier}`}>Search {module.displayName}</label>
          <input id={`module-search-${module.identifier}`} className="form-control" type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder={`Search ${module.displayName.toLowerCase()}...`} />
        </div>
        <div className="col-12 col-lg-4">
          <div className="form-control bg-body-tertiary text-body-secondary">
            {state.loading ? "Loading..." : `${state.rows.length} records loaded`}
          </div>
        </div>
      </div>

      {state.error ? <div className="alert alert-warning mb-0" role="alert">{state.error}</div> : null}

      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead><tr>{columns.map((column) => <th scope="col" key={column.id}>{column.label}</th>)}</tr></thead>
          <tbody>
            {state.rows.length > 0 ? state.rows.map((row, index) => (
              <tr key={rowKey(row, index)}>
                {columns.map((column) => <td key={column.id}>{displayValue(resolveColumnValue(row, column.id))}</td>)}
              </tr>
            )) : (
              <tr><td colSpan={Math.max(columns.length, 1)} className="text-center py-5"><span className="text-body-secondary">{state.loading ? "Loading module data..." : table.emptyMessage}</span></td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
