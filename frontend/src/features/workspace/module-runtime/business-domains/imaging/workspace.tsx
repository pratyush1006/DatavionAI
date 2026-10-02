"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useMutation, useQueries, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, ClipboardList, FileCheck, House, ScanLine, Settings, Stethoscope } from "lucide-react";
import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";
import type { ModuleRuntimeDefinition } from "../../domain/types";

type Row = Record<string, unknown>;
type Payload = Row[] | { results?: Row[]; data?: Row[] };
const nav = [["Overview", "overview", House], ["Orders", "orders", ClipboardList], ["Worklist", "studies", ScanLine], ["Modalities", "modalities", Stethoscope], ["Procedures", "procedures", ScanLine], ["Reports", "reports", FileCheck], ["Imaging Config", "config", Settings]] as const;
const sources = [["orders", "/imaging/orders/"], ["studies", "/imaging/studies/"], ["modalities", "/imaging/modalities/"], ["procedures", "/imaging/procedures/"], ["reports", "/imaging/reports/"]] as const;
const rows = (data: Payload | undefined) => Array.isArray(data) ? data : data?.results ?? data?.data ?? [];
const text = (value: unknown, fallback = "-") => value === null || value === undefined || value === "" ? fallback : String(value);

export function ImagingBusinessWorkspace({ module }: { module: ModuleRuntimeDefinition }) {
  const { bootstrap } = useBootstrap();
  const organization = bootstrap?.organization?.id;
  const section = useSearchParams().get("section") ?? "overview";
  const queries = useQueries({ queries: sources.map(([key, path]) => ({ queryKey: ["imaging", key, organization], queryFn: async () => (await apiClient.get<Payload>(path, { params: { organization_id: organization, limit: 100 } })).data, enabled: Boolean(organization), staleTime: 10_000 })) });
  const data = Object.fromEntries(sources.map(([key], index) => [key, rows(queries[index].data)])) as Record<string, Row[]>;
  const pending = data.orders.filter((row) => !["completed", "cancelled"].includes(text(row.status)));
  const scheduled = data.studies.filter((row) => ["scheduled", "arrived", "ready"].includes(text(row.status)));
  const acquiring = data.studies.filter((row) => row.status === "acquiring");
  const urgent = data.orders.filter((row) => ["urgent", "stat"].includes(text(row.priority)) && row.status !== "completed");
  const greeting = new Date().getHours() < 12 ? "Good morning" : new Date().getHours() < 17 ? "Good afternoon" : "Good evening";
  return <section className="container-fluid py-4"><div className="row g-4"><aside className="col-12 col-xl-2"><nav className="card border-0 shadow-sm p-2" aria-label="Imaging workspace">{nav.map(([label, target, Icon]) => <Link key={target} href={target === "overview" ? "/workspace/imaging" : `/workspace/imaging?section=${target}`} className={`nav-link d-flex align-items-center gap-2 rounded px-3 py-2 ${section === target ? "active" : "text-body"}`}><Icon size={18} />{label}</Link>)}</nav></aside><main className="col-12 col-xl-10">
    {section === "overview" ? <><header className="mb-4"><h1 className="h2 mb-1">{greeting}, Imaging Technician</h1><p className="text-body-secondary mb-0">Radiology &amp; Imaging • {bootstrap?.organization?.name ?? module.displayName}</p></header>
      {queries.some((query) => query.isError) && <div className="alert alert-warning">Some imaging data could not be loaded.</div>}
      <div className="row g-3 mb-4"><Kpi title="Imaging Orders" value={pending.length} detail="Open" /><Kpi title="Scheduled" value={scheduled.length} detail="Studies" /><Kpi title="Acquiring" value={acquiring.length} detail="Active" /><Kpi title="Urgent" value={urgent.length} detail="STAT / urgent" danger={urgent.length > 0} /></div>
      <div className="row g-4"><div className="col-12 col-lg-7"><Card title="Imaging Worklist" href="/workspace/imaging?section=studies">{data.studies.slice(0, 8).map((study) => <div className="border-bottom py-3" key={text(study.id)}><div className="d-flex justify-content-between"><strong>{text(study.procedure_name, text(study.accession_number))}</strong><span className="badge text-bg-light border">{text(study.status)}</span></div><small className="text-body-secondary">{text(study.modality_name)} • {text(study.order_number)}</small></div>)}{!data.studies.length && <p className="text-body-secondary">No imaging studies in the worklist.</p>}</Card></div><div className="col-12 col-lg-5"><Card title="Priority Cases" href="/workspace/imaging?section=orders">{urgent.slice(0, 8).map((order) => <div className="border-bottom py-3 text-danger" key={text(order.id)}><AlertTriangle size={17} className="me-2" /><strong>{text(order.order_number)}</strong> • {text(order.clinical_indication)}</div>)}{!urgent.length && <p className="text-body-secondary">No urgent imaging orders.</p>}</Card></div></div>
    </> : <ImagingSection section={section} organization={organization ?? ""} data={data} />}
  </main></div></section>;
}

function ImagingSection({ section, organization, data }: { section: string; organization: string; data: Record<string, Row[]> }) {
  const client = useQueryClient();
  const configs: Record<string, { key: string; title: string; columns: string[] }> = {
    orders: { key: "orders", title: "Imaging Orders", columns: ["order_number", "patient_id", "priority", "status", "clinical_indication"] },
    studies: { key: "studies", title: "Imaging Worklist", columns: ["accession_number", "procedure_name", "modality_name", "status", "performed_at"] },
    modalities: { key: "modalities", title: "Modalities", columns: ["code", "name", "modality_type", "active"] },
    procedures: { key: "procedures", title: "Procedures", columns: ["procedure_code", "name", "modality_name", "body_region", "contrast_required"] },
    reports: { key: "reports", title: "Radiology Reports", columns: ["accession_number", "status", "impression", "radiologist_id", "signed_at"] },
    config: { key: "modalities", title: "Imaging Configuration", columns: ["code", "name", "modality_type", "active"] },
  };
  const config = configs[section] ?? configs.orders;
  const workflow = useMutation({ mutationFn: async ({ row, action }: { row: Row; action: string }) => apiClient.post(`/imaging/${config.key}/${row.id}/${action}/`, { organization_id: organization }), onSuccess: () => client.invalidateQueries({ queryKey: ["imaging"] }) });
  const action = (row: Row) => config.key === "orders" && row.status === "ordered" ? ["ready", "Mark ready"] : config.key === "orders" && row.status === "ready" ? ["schedule", "Schedule"] : config.key === "orders" && row.status === "scheduled" ? ["start", "Start"] : config.key === "orders" && row.status === "in_progress" ? ["complete", "Complete"] : config.key === "studies" && row.status === "scheduled" ? ["arrive", "Arrived"] : config.key === "studies" && row.status === "arrived" ? ["ready", "Ready"] : config.key === "studies" && row.status === "ready" ? ["acquire", "Start acquisition"] : config.key === "studies" && row.status === "acquiring" ? ["complete-acquisition", "Complete acquisition"] : config.key === "studies" && row.status === "acquired" ? ["interpret", "Send to radiologist"] : config.key === "reports" && row.status !== "final" ? ["finalize", "Finalize"] : null;
  return <div className="card border-0 shadow-sm"><div className="card-body p-4"><h1 className="h4 mb-1">{config.title}</h1><p className="small text-body-secondary">Tenant and organization-scoped radiology operations</p>{workflow.isError && <div className="alert alert-danger">The imaging workflow transition could not be completed.</div>}<div className="table-responsive"><table className="table align-middle"><thead><tr>{config.columns.map((column) => <th key={column}>{column.replaceAll("_", " ")}</th>)}<th>Actions</th></tr></thead><tbody>{data[config.key].map((row) => { const next = action(row); return <tr key={text(row.id)}>{config.columns.map((column) => <td key={column}>{text(row[column])}</td>)}<td>{next && <button className="btn btn-sm btn-outline-primary" disabled={workflow.isPending} onClick={() => workflow.mutate({ row, action: next[0] })}>{next[1]}</button>}</td></tr>; })}{!data[config.key].length && <tr><td className="text-center text-body-secondary py-4" colSpan={config.columns.length + 1}>No records available.</td></tr>}</tbody></table></div></div></div>;
}

function Kpi({ title, value, detail, danger = false }: { title: string; value: number; detail: string; danger?: boolean }) { return <div className="col-12 col-sm-6 col-xl-3"><div className="card border-0 shadow-sm h-100"><div className="card-body"><span className="text-body-secondary">{title}</span><div className={`display-6 fw-semibold my-2 ${danger ? "text-danger" : ""}`}>{value}</div><small className="text-body-secondary">{detail}</small></div></div></div>; }
function Card({ title, href, children }: { title: string; href: string; children: React.ReactNode }) { return <div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between"><h2 className="h5">{title}</h2><Link href={href}>Manage</Link></div>{children}</div></div>; }
