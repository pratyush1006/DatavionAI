"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useMutation, useQueries, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, Boxes, Building2, ClipboardList, House, PackageCheck, Search, Settings, ShoppingCart, Truck } from "lucide-react";
import { useState, type FormEvent } from "react";
import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";
import type { ModuleRuntimeDefinition } from "../../domain/types";

type Row = Record<string, unknown>;
type Payload = Row[] | { results?: Row[]; rows?: Row[]; data?: Row[]; count?: number };
type Summary = { low_stock_count: number; expiring_batch_count: number; low_stock: Row[]; expiring_batches: Row[] };
const sections = [
  ["Overview", "overview", House], ["Pharmacy", "pharmacies", Building2], ["Prescriptions", "dispensing", ClipboardList],
  ["Inventory", "inventory", Boxes], ["Suppliers", "suppliers", Truck], ["Purchases", "purchases", ShoppingCart],
  ["Stock", "stock", PackageCheck], ["Reports", "reports", AlertTriangle], ["Settings", "settings", Settings],
] as const;
function list(payload: Payload | undefined): Row[] { return Array.isArray(payload) ? payload : payload?.results ?? payload?.rows ?? payload?.data ?? []; }
function show(value: unknown, fallback = "-"): string { return value === null || value === undefined || value === "" ? fallback : String(value); }

export function PharmacyBusinessWorkspace({ module }: { module: ModuleRuntimeDefinition }) {
  const { bootstrap } = useBootstrap();
  const organization = bootstrap?.organization?.id;
  const section = useSearchParams().get("section") ?? "overview";
  const params = organization ? { organization_id: organization, limit: 100 } : undefined;
  const sourceQueries = useQueries({ queries: [
    ["pharmacies", "/pharmacy/pharmacies/"], ["suppliers", "/pharmacy/suppliers/"], ["products", "/pharmacy/products/"],
    ["purchases", "/pharmacy/purchase-orders/"], ["dispensing", "/pharmacy/dispensing-orders/"], ["batches", "/pharmacy/batches/"], ["prescriptions", "/prescriptions/"],
  ].map(([key, path]) => ({ queryKey: ["pharmacy", key, organization], queryFn: async () => (await apiClient.get<Payload>(path, { params })).data, enabled: Boolean(organization), staleTime: 15_000 })) });
  const pharmacies = list(sourceQueries[0].data), suppliers = list(sourceQueries[1].data), products = list(sourceQueries[2].data), purchases = list(sourceQueries[3].data), dispensing = list(sourceQueries[4].data), batches = list(sourceQueries[5].data), prescriptions = list(sourceQueries[6].data);
  const pharmacyId = String(pharmacies[0]?.id ?? "");
  const summary = useQuery({ queryKey: ["pharmacy", "summary", organization, pharmacyId], queryFn: async () => (await apiClient.get<Summary>("/pharmacy/summary/", { params: { organization_id: organization, pharmacy_id: pharmacyId } })).data, enabled: Boolean(organization && pharmacyId) });
  const inventory = useQuery({ queryKey: ["pharmacy", "inventory", pharmacyId], queryFn: async () => (await apiClient.get<Row[]>("/pharmacy/inventory/", { params: { pharmacy_id: pharmacyId } })).data, enabled: Boolean(pharmacyId) });
  const pending = dispensing.filter((row) => row.status === "pending");
  const loading = sourceQueries.some((query) => query.isPending && query.fetchStatus === "fetching");
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  return <section className="container-fluid py-4"><div className="row g-4">
    <aside className="col-12 col-xl-2"><nav className="card border-0 shadow-sm p-2" aria-label="Pharmacy workspace">{sections.map(([label, target, Icon]) => <Link key={target} href={target === "overview" ? "/workspace/pharmacy" : `/workspace/pharmacy?section=${target}`} className={`nav-link d-flex align-items-center gap-2 rounded px-3 py-2 ${section === target ? "active" : "text-body"}`}><Icon size={18} />{label}</Link>)}</nav></aside>
    <div className="col-12 col-xl-10">{section === "overview" ? <>
      <div className="d-flex flex-wrap justify-content-between gap-3 mb-4"><div><h1 className="h2 mb-1">{greeting}, Pharmacist</h1><p className="text-body-secondary mb-0">Pharmacy - {bootstrap?.organization?.name ?? module.displayName}</p></div><Link href="/workspace/pharmacy?section=dispensing" className="btn btn-outline-primary d-flex align-items-center gap-2"><Search size={17} />Search medicine or prescription</Link></div>
      {sourceQueries.some((query) => query.isError) && <div className="alert alert-warning">Some pharmacy data could not be loaded.</div>}
      <div className="row g-3 mb-4"><Kpi title="Prescriptions" value={dispensing.length} detail="Dispensing orders" loading={loading} /><Kpi title="Dispensing" value={pending.length} detail="Pending" loading={loading} /><Kpi title="Low Stock" value={summary.data?.low_stock_count ?? 0} detail="Attention" loading={summary.isPending} /><Kpi title="Expiring" value={summary.data?.expiring_batch_count ?? 0} detail="Within 30 days" loading={summary.isPending} /></div>
      <div className="row g-4"><div className="col-12 col-lg-7"><Card title="Dispensing Queue" href="/workspace/pharmacy?section=dispensing">{pending.slice(0, 8).map((order) => <div className="border-bottom py-3" key={String(order.id)}><div className="d-flex justify-content-between"><strong>{show(order.prescription_number, `Rx ${order.prescription}`)}</strong><span className="badge text-bg-warning">Pending</span></div><div className="small text-body-secondary">{show(order.patient_name)} - {show(order.pharmacy_name)}</div></div>)}{!pending.length && <p className="text-body-secondary">No pending dispensing orders.</p>}</Card></div><div className="col-12 col-lg-5"><Card title="Inventory Alerts" href="/workspace/pharmacy?section=stock">{summary.data?.low_stock.map((item) => <Alert key={String(item.id)} text={`${show(item.sku)} low stock`} danger />)}{summary.data?.expiring_batches.map((item) => <Alert key={String(item.id)} text={`Batch ${show(item.batch_number)} expires ${show(item.expiry_date)}`} />)}{!summary.data?.low_stock_count && !summary.data?.expiring_batch_count && <p className="text-body-secondary">No inventory alerts.</p>}</Card></div></div>
    </> : <PharmacySection section={section} organization={organization ?? ""} pharmacyId={pharmacyId} data={{ pharmacies, suppliers, products, purchases, dispensing, batches, prescriptions, inventory: inventory.data ?? [] }} />}</div>
  </div></section>;
}

function PharmacySection({ section, organization, pharmacyId, data }: { section: string; organization: string; pharmacyId: string; data: Record<string, Row[]> }) {
  const client = useQueryClient();
  const [creating, setCreating] = useState(false);
  const [values, setValues] = useState<Record<string, string>>({});
  const config = sectionConfig(section);
  const create = useMutation({ mutationFn: async () => {
    let body: Row = { organization_id: organization, ...values };
    if (section === "purchases") body = { organization_id: organization, pharmacy: values.pharmacy, supplier: values.supplier, order_number: values.order_number, lines: [{ product: values.product, quantity_ordered: values.quantity_ordered, unit_cost: values.unit_cost, tax_rate: 0 }] };
    if (section === "dispensing") body = { organization_id: organization, pharmacy: values.pharmacy, prescription: values.prescription, dispense_number: values.dispense_number, lines: [{ product: values.product, batch: values.batch, quantity_prescribed: values.quantity_prescribed }] };
    return apiClient.post(config.path, body);
  }, onSuccess: async () => { setCreating(false); setValues({}); await client.invalidateQueries({ queryKey: ["pharmacy"] }); } });
  const workflow = useMutation({ mutationFn: async ({ row, action }: { row: Row; action: string }) => {
    if (action === "dispense") return apiClient.post(`/pharmacy/dispensing-orders/${row.id}/dispense/`, { organization_id: organization, lines: Array.isArray(row.lines) ? row.lines.map((line) => ({ product: (line as Row).product, batch: (line as Row).batch, quantity: (line as Row).quantity_prescribed })) : [] }, { headers: { "Idempotency-Key": crypto.randomUUID() } });
    if (action === "request-approval") return apiClient.post(`/pharmacy/purchase-orders/${row.id}/request-approval/`, { organization_id: organization });
    return Promise.resolve(null);
  }, onSuccess: () => client.invalidateQueries({ queryKey: ["pharmacy"] }) });
  const rows = section === "inventory" || section === "stock" || section === "reports" ? data.inventory : data[config.dataKey] ?? [];
  const submit = (event: FormEvent) => { event.preventDefault(); create.mutate(); };
  return <div className="card border-0 shadow-sm"><div className="card-body p-4"><div className="d-flex justify-content-between mb-3"><div><h1 className="h4">{config.title}</h1><p className="text-body-secondary small">Organization-scoped pharmacy operations</p></div>{config.fields.length > 0 && <button className="btn btn-primary btn-sm" onClick={() => setCreating(!creating)}>{creating ? "Close" : "Create"}</button>}</div>
    {create.isError && <div className="alert alert-danger">Could not save the pharmacy record.</div>}
    {creating && <form className="border rounded p-3 mb-4" onSubmit={submit}><div className="row g-3">{config.fields.map((field) => <div className="col-md-6" key={field}><label className="form-label" htmlFor={`pharmacy-${field}`}>{field.replaceAll("_", " ")} *</label>{["pharmacy", "supplier", "product", "batch", "prescription"].includes(field) ? <select id={`pharmacy-${field}`} className="form-select" required onChange={(event) => setValues({ ...values, [field]: event.target.value })}><option value="">Select...</option>{(field === "pharmacy" ? data.pharmacies : field === "supplier" ? data.suppliers : field === "product" ? data.products : field === "batch" ? data.batches : data.prescriptions).map((row) => <option key={String(row.id)} value={String(row.id)}>{show(row.name ?? row.sku ?? row.batch_number ?? row.prescription_number ?? row.id)}</option>)}</select> : <input id={`pharmacy-${field}`} className="form-control" required value={values[field] ?? ""} onChange={(event) => setValues({ ...values, [field]: event.target.value })} />}</div>)}</div><button className="btn btn-primary mt-3" disabled={create.isPending}>Save record</button></form>}
    <div className="table-responsive"><table className="table align-middle"><thead><tr>{config.columns.map((column) => <th key={column}>{column.replaceAll("_", " ")}</th>)}<th>Actions</th></tr></thead><tbody>{rows.map((row) => <tr key={String(row.id ?? row.product_id)}>{config.columns.map((column) => <td key={column}>{show(row[column])}</td>)}<td>{section === "dispensing" && row.status === "pending" && <button className="btn btn-sm btn-outline-primary" onClick={() => workflow.mutate({ row, action: "dispense" })}>Dispense</button>}{section === "purchases" && row.status === "draft" && <button className="btn btn-sm btn-outline-primary" onClick={() => workflow.mutate({ row, action: "request-approval" })}>Request approval</button>}</td></tr>)}{!rows.length && <tr><td colSpan={config.columns.length + 1} className="text-center text-body-secondary py-4">No records available.</td></tr>}</tbody></table></div>
    {!pharmacyId && ["inventory", "stock", "reports"].includes(section) && <div className="alert alert-info">Create a pharmacy before managing inventory.</div>}
  </div></div>;
}

function sectionConfig(section: string) { const values: Record<string, { title: string; path: string; dataKey: string; columns: string[]; fields: string[] }> = {
  pharmacies: { title: "Pharmacies", path: "/pharmacy/pharmacies/", dataKey: "pharmacies", columns: ["code", "name", "status", "phone"], fields: ["code", "name", "address", "phone", "email"] },
  suppliers: { title: "Suppliers", path: "/pharmacy/suppliers/", dataKey: "suppliers", columns: ["code", "name", "contact_name", "phone", "email"], fields: ["code", "name", "contact_name", "phone", "email", "tax_id", "address"] },
  purchases: { title: "Purchases", path: "/pharmacy/purchase-orders/", dataKey: "purchases", columns: ["order_number", "pharmacy_name", "supplier_name", "status", "ordered_at"], fields: ["pharmacy", "supplier", "order_number", "product", "quantity_ordered", "unit_cost"] },
  dispensing: { title: "Prescription Dispensing", path: "/pharmacy/dispensing-orders/", dataKey: "dispensing", columns: ["dispense_number", "prescription_number", "patient_name", "status", "dispensed_at"], fields: ["pharmacy", "prescription", "dispense_number", "product", "batch", "quantity_prescribed"] },
  inventory: { title: "Inventory", path: "", dataKey: "inventory", columns: ["sku", "medication", "stock", "reorder_level"], fields: [] },
  stock: { title: "Stock", path: "", dataKey: "inventory", columns: ["sku", "medication", "stock", "reorder_level"], fields: [] },
  reports: { title: "Pharmacy Reports", path: "", dataKey: "inventory", columns: ["sku", "medication", "stock", "reorder_level"], fields: [] },
  settings: { title: "Pharmacy Settings", path: "", dataKey: "pharmacies", columns: ["code", "name", "status"], fields: [] },
  }; return values[section] ?? values.pharmacies; }
function Kpi({ title, value, detail, loading }: { title: string; value: number; detail: string; loading: boolean }) { return <div className="col-12 col-sm-6 col-xl-3"><div className="card border-0 shadow-sm h-100"><div className="card-body"><span className="text-body-secondary">{title}</span><div className="display-6 fw-semibold my-2">{loading ? "..." : value}</div><span className="small text-body-secondary">{detail}</span></div></div></div>; }
function Card({ title, href, children }: { title: string; href: string; children: React.ReactNode }) { return <div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between"><h2 className="h5">{title}</h2><Link href={href}>Manage</Link></div>{children}</div></div>; }
function Alert({ text, danger = false }: { text: string; danger?: boolean }) { return <div className={`border-top py-2 ${danger ? "text-danger" : "text-warning-emphasis"}`}><AlertTriangle size={16} className="me-2" />{text}</div>; }
