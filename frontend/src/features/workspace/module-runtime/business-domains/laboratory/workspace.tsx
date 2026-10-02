"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useMutation, useQueries, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, Beaker, ClipboardList, FileText, FlaskConical, House, Microscope, Settings } from "lucide-react";
import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";
import type { ModuleRuntimeDefinition } from "../../domain/types";

type Row = Record<string, unknown>;
type Payload = Row[] | { results?: Row[]; data?: Row[] };
const nav = [["Overview", "overview", House], ["Lab", "laboratories", FlaskConical], ["Orders", "orders", ClipboardList], ["Samples", "specimens", Beaker], ["Tests", "tests", Microscope], ["Results", "results", FileText], ["Reports", "reports", FileText], ["Lab Config", "config", Settings]] as const;
const sources = [["laboratories", "/laboratories/laboratories/"], ["orders", "/laboratories/orders/"], ["specimens", "/laboratories/specimens/"], ["tests", "/laboratories/tests/"], ["results", "/laboratories/results/"], ["reports", "/laboratories/reports/"]] as const;
const rows = (data: Payload | undefined) => Array.isArray(data) ? data : data?.results ?? data?.data ?? [];
const text = (value: unknown, fallback = "-") => value === null || value === undefined || value === "" ? fallback : String(value);

export function LaboratoryBusinessWorkspace({ module }: { module: ModuleRuntimeDefinition }) {
  const { bootstrap } = useBootstrap();
  const organization = bootstrap?.organization?.id;
  const section = useSearchParams().get("section") ?? "overview";
  const queries = useQueries({ queries: sources.map(([key, path]) => ({ queryKey: ["laboratory", key, organization], queryFn: async () => (await apiClient.get<Payload>(path, { params: { organization_id: organization, limit: 100 } })).data, enabled: Boolean(organization), staleTime: 10_000 })) });
  const data = Object.fromEntries(sources.map(([key], index) => [key, rows(queries[index].data)])) as Record<string, Row[]>;
  const pending = data.orders.filter((item) => !["verified", "released", "cancelled"].includes(text(item.status)));
  const collected = data.specimens.filter((item) => item.status === "collected");
  const processing = data.specimens.filter((item) => ["received", "processing"].includes(text(item.status)));
  const critical = data.results.filter((item) => item.critical || text(item.abnormal_flag).includes("critical"));
  const greeting = new Date().getHours() < 12 ? "Good morning" : new Date().getHours() < 17 ? "Good afternoon" : "Good evening";
  return <section className="container-fluid py-4"><div className="row g-4"><aside className="col-12 col-xl-2"><nav className="card border-0 shadow-sm p-2" aria-label="Laboratory workspace">{nav.map(([label, target, Icon]) => <Link key={target} href={target === "overview" ? "/workspace/laboratory" : `/workspace/laboratory?section=${target}`} className={`nav-link d-flex align-items-center gap-2 rounded px-3 py-2 ${section === target ? "active" : "text-body"}`}><Icon size={18} />{label}</Link>)}</nav></aside><main className="col-12 col-xl-10">
    {section === "overview" ? <><header className="mb-4"><h1 className="h2 mb-1">{greeting}, Lab Technician</h1><p className="text-body-secondary mb-0">Laboratory • {data.laboratories[0]?.name ? text(data.laboratories[0].name) : bootstrap?.organization?.name ?? module.displayName}</p></header>
      {queries.some((query) => query.isError) && <div className="alert alert-warning">Some laboratory data could not be loaded.</div>}
      <div className="row g-3 mb-4"><Kpi title="Lab Orders" value={pending.length} detail="Pending" /><Kpi title="Samples" value={collected.length} detail="Collected" /><Kpi title="Processing" value={processing.length} detail="Active" /><Kpi title="Critical" value={critical.length} detail="Results" danger={critical.length > 0} /></div>
      <div className="row g-4"><div className="col-12 col-lg-7"><Card title="Laboratory Worklist" href="/workspace/laboratory?section=orders">{pending.slice(0, 8).map((order) => <div className="border-bottom py-3" key={text(order.id)}><div className="d-flex justify-content-between"><strong>{text((order.items as Row[] | undefined)?.[0]?.test_name, text(order.order_number))}</strong><span className="badge text-bg-light border">{text(order.status)}</span></div><small className="text-body-secondary">{text(order.patient_name)} • {text(order.priority)}</small></div>)}{!pending.length && <p className="text-body-secondary">No pending laboratory orders.</p>}</Card></div><div className="col-12 col-lg-5"><Card title="Critical Results" href="/workspace/laboratory?section=results">{critical.slice(0, 8).map((result) => <div className="border-bottom py-3 text-danger" key={text(result.id)}><AlertTriangle size={17} className="me-2" />{text(result.value_text, text(result.value_numeric))} <small>{text(result.unit)}</small></div>)}{!critical.length && <p className="text-body-secondary">No critical results.</p>}</Card></div></div>
    </> : <LaboratorySection section={section} organization={organization ?? ""} data={data} />}
  </main></div></section>;
}

function LaboratorySection({ section, organization, data }: { section: string; organization: string; data: Record<string, Row[]> }) {
  const client = useQueryClient();
  const config = section === "config" ? { key: "laboratories", title: "Lab Configuration", columns: ["code", "name", "status", "timezone"] } : ({ laboratories: { key: "laboratories", title: "Laboratories", columns: ["code", "name", "status", "phone"] }, orders: { key: "orders", title: "Lab Orders", columns: ["order_number", "patient_name", "priority", "status", "ordered_at"] }, specimens: { key: "specimens", title: "Samples", columns: ["specimen_id", "order_number", "specimen_type", "status", "collected_at"] }, tests: { key: "tests", title: "Test Catalogue", columns: ["code", "name", "specimen_type", "unit", "turnaround_minutes"] }, results: { key: "results", title: "Results", columns: ["status", "value_text", "value_numeric", "unit", "abnormal_flag", "critical"] }, reports: { key: "reports", title: "Reports", columns: ["report_number", "title", "status", "released_at"] } } as const)[section as "laboratories"] ?? { key: "orders", title: "Lab Orders", columns: ["order_number", "status"] };
  const workflow = useMutation({ mutationFn: async ({ row, action }: { row: Row; action: string }) => apiClient.post(`/laboratories/${config.key}/${row.id}/${action}/`, { organization_id: organization }), onSuccess: () => client.invalidateQueries({ queryKey: ["laboratory"] }) });
  const action = (row: Row) => config.key === "orders" && !["collected", "processing", "verified", "released"].includes(text(row.status)) ? ["collect-specimen", "Collect sample"] : config.key === "specimens" && row.status === "collected" ? ["receive", "Receive"] : config.key === "specimens" && row.status === "received" ? ["start-processing", "Start processing"] : config.key === "specimens" && row.status === "processing" ? ["complete-processing", "Complete"] : config.key === "results" && row.status === "preliminary" ? ["verify", "Verify"] : config.key === "reports" && row.status !== "released" ? ["release", "Release"] : null;
  return <div className="card border-0 shadow-sm"><div className="card-body p-4"><h1 className="h4 mb-1">{config.title}</h1><p className="small text-body-secondary">Persistent, organization-scoped laboratory records</p>{workflow.isError && <div className="alert alert-danger">The workflow transition could not be completed.</div>}<div className="table-responsive"><table className="table align-middle"><thead><tr>{config.columns.map((column) => <th key={column}>{column.replaceAll("_", " ")}</th>)}<th>Actions</th></tr></thead><tbody>{data[config.key].map((row) => { const next = action(row); return <tr key={text(row.id)}>{config.columns.map((column) => <td key={column}>{text(row[column])}</td>)}<td>{next && <button className="btn btn-sm btn-outline-primary" disabled={workflow.isPending} onClick={() => workflow.mutate({ row, action: next[0] })}>{next[1]}</button>}</td></tr>; })}{!data[config.key].length && <tr><td className="text-center text-body-secondary py-4" colSpan={config.columns.length + 1}>No records available.</td></tr>}</tbody></table></div></div></div>;
}

function Kpi({ title, value, detail, danger = false }: { title: string; value: number; detail: string; danger?: boolean }) { return <div className="col-12 col-sm-6 col-xl-3"><div className="card border-0 shadow-sm h-100"><div className="card-body"><span className="text-body-secondary">{title}</span><div className={`display-6 fw-semibold my-2 ${danger ? "text-danger" : ""}`}>{value}</div><small className="text-body-secondary">{detail}</small></div></div></div>; }
function Card({ title, href, children }: { title: string; href: string; children: React.ReactNode }) { return <div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between"><h2 className="h5">{title}</h2><Link href={href}>Manage</Link></div>{children}</div></div>; }
