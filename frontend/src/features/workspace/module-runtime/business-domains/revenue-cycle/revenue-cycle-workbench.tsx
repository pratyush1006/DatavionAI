"use client";

import { useEffect, useState } from "react";

import { apiClient } from "@/core/api";

type Row = Readonly<Record<string, unknown>>;

type Workstream = Readonly<{
  id: string;
  label: string;
  phase: string;
  endpoint: string;
  description: string;
}>;

const WORKSTREAMS: readonly Workstream[] = [
  { id: "eligibility", label: "Eligibility", phase: "Pre-service", endpoint: "/revenue-cycle/eligibility/", description: "Verify payer coverage before care." },
  { id: "authorization", label: "Prior authorization", phase: "Pre-service", endpoint: "/revenue-cycle/prior_authorization/", description: "Request and track payer authorization." },
  { id: "charge-capture", label: "Charge capture", phase: "Point of care", endpoint: "/revenue-cycle/charge_capture/charges/", description: "Capture and validate billable services." },
  { id: "coding", label: "Coding", phase: "Point of care", endpoint: "/revenue-cycle/coding/", description: "Assign and review clinical codes." },
  { id: "patient-billing", label: "Patient billing", phase: "Billing", endpoint: "/revenue-cycle/billing/patient-billing/patient-accounts/", description: "Patient accounts, responsibility, and statements." },
  { id: "scrubbing", label: "Claim scrubbing", phase: "Billing", endpoint: "/revenue-cycle/claim_scrubbing/scrubs/", description: "Detect claim errors before submission." },
  { id: "claims", label: "Claim submission", phase: "Billing", endpoint: "/revenue-cycle/claim_submission/", description: "Prepare, submit, and monitor claims." },
  { id: "payments", label: "Payment posting", phase: "Collections", endpoint: "/revenue-cycle/payment_posting/", description: "Post, reconcile, and reverse payments." },
  { id: "era", label: "ERA", phase: "Collections", endpoint: "/revenue-cycle/era/", description: "Process electronic remittance advice." },
  { id: "ar", label: "Accounts receivable", phase: "Collections", endpoint: "/revenue-cycle/ar/accounts/", description: "Manage balances, holds, and write-offs." },
  { id: "denials", label: "Denials", phase: "Recovery", endpoint: "/revenue-cycle/denials/", description: "Resolve payer denials and root causes." },
  { id: "appeals", label: "Appeals", phase: "Recovery", endpoint: "/revenue-cycle/appeals/", description: "Prepare and track appeal work." },
  { id: "analytics", label: "Revenue analytics", phase: "Performance", endpoint: "/revenue-cycle/analytics/snapshots/", description: "Review organization-scoped financial snapshots." },
];

function rowsFrom(payload: unknown): Row[] {
  if (Array.isArray(payload)) return payload.filter((row): row is Row => Boolean(row && typeof row === "object"));
  if (!payload || typeof payload !== "object") return [];
  const body = payload as Record<string, unknown>;
  const rows = body.results ?? body.data ?? body.items;
  return Array.isArray(rows) ? rows.filter((row): row is Row => Boolean(row && typeof row === "object")) : [];
}

function renderValue(value: unknown): string {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return String(value);
  return "Details available";
}

export function RevenueCycleWorkbench({ moduleName }: Readonly<{ moduleName: string }>) {
  const [selectedId, setSelectedId] = useState(WORKSTREAMS[0].id);
  const [search, setSearch] = useState("");
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const selected = WORKSTREAMS.find((item) => item.id === selectedId) ?? WORKSTREAMS[0];

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    apiClient.get<unknown>(selected.endpoint)
      .then((payload) => { if (active) setRows(rowsFrom(payload)); })
      .catch((reason: unknown) => {
        if (active) setError(reason instanceof Error ? reason.message : "The backend work queue could not be loaded.");
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [selected.endpoint]);

  const columns = rows.length ? Object.keys(rows[0]).slice(0, 6) : [];
  const visibleRows = rows.filter((row) => JSON.stringify(row).toLowerCase().includes(search.trim().toLowerCase()));

  return (
    <section className="container-fluid py-3">
      <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
        <div><div className="text-body-secondary small text-uppercase fw-semibold">Revenue cycle management</div><h1 className="h3 mb-1">Revenue Cycle</h1><p className="text-body-secondary mb-0">Manage financial workflows from eligibility and charges through collections, denial recovery, and performance.</p></div>
        <span className="badge text-bg-light border">{moduleName}</span>
      </div>

      <div className="card shadow-sm">
        <div className="card-header bg-body"><div className="fw-semibold">Revenue Cycle records</div></div>
        <div className="card-body">
          <div className="d-flex flex-wrap gap-2 mb-4" role="tablist" aria-label="Revenue Cycle workflows">
            {WORKSTREAMS.map((item) => <button key={item.id} type="button" role="tab" aria-selected={selected.id === item.id} className={`btn btn-sm rounded-pill ${selected.id === item.id ? "btn-primary" : "btn-outline-secondary"}`} onClick={() => { setSelectedId(item.id); setSearch(""); }}>{item.label}</button>)}
          </div>
          <div className="row g-2 mb-3"><div className="col-12 col-lg-8"><label className="visually-hidden" htmlFor="revenue-cycle-search">Search {selected.label}</label><input id="revenue-cycle-search" className="form-control" type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder={`Search ${selected.label.toLowerCase()}...`} /></div><div className="col-12 col-lg-4"><div className="form-control bg-body-tertiary text-body-secondary">{loading ? "Loading..." : `${visibleRows.length} records loaded`}</div></div></div>
          <div className="small text-body-secondary mb-3">{selected.phase} · {selected.description}</div>
          {error ? <div className="alert alert-warning mb-0"><strong>Queue unavailable.</strong> {error}</div> : null}
          {!error && loading ? <div className="text-body-secondary py-4">Loading backend work queue…</div> : null}
          {!error && !loading && visibleRows.length === 0 ? <div className="text-body-secondary text-center py-5">No {selected.label.toLowerCase()} records are available for this organization.</div> : null}
          {!error && !loading && visibleRows.length > 0 ? <div className="table-responsive"><table className="table table-hover align-middle mb-0"><thead><tr>{columns.map((column) => <th key={column} scope="col">{column.replaceAll("_", " ")}</th>)}</tr></thead><tbody>{visibleRows.slice(0, 25).map((row, index) => <tr key={String(row.id ?? row.uuid ?? index)}>{columns.map((column) => <td key={column}>{renderValue(row[column])}</td>)}</tr>)}</tbody></table></div> : null}
        </div>
      </div>
    </section>
  );
}
