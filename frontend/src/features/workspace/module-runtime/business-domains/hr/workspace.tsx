"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";
import type { ModuleRuntimeDefinition } from "../../domain/types";
import { HR_COLLECTIONS, label, type Collection, type HrRecord, type Action } from "./config";
import { display, errorMessage, listRecords, lookupRecords } from "./api";
import { HrExecutiveDashboard } from "./dashboard";
import { hrLink, isHrManager } from "./persona";

type Editor = { kind: "create" | "edit" | "view"; record?: HrRecord };
type Confirmation = { record: HrRecord; action?: Action };

export function HrBusinessWorkspace({ module }: { module: ModuleRuntimeDefinition }) {
  const { bootstrap } = useBootstrap();
  const can = (permission: string) => Boolean(bootstrap?.user.is_platform_admin || bootstrap?.permissions.includes("*") || bootstrap?.permissions.includes(permission));
  const collections = HR_COLLECTIONS.filter((item) => can(`${item.permission}.view`));
  const params = useSearchParams();
  const router = useRouter();
  const manager = isHrManager(bootstrap?.organization_roles ?? [], params.get("view"));
  const selected = params.get("section") ?? "overview";
  const setSelected = (section: string) => router.push(hrLink(section, manager));
  const executive = ["overview", "employees", "reports"].includes(selected);
  const active = collections.find((item) => item.id === selected);
  const organization = bootstrap?.organization?.id ?? bootstrap?.access_context.organization_id;
  return <section className="container-fluid py-4">
    <div className="d-flex justify-content-end mb-3"><label className="d-flex align-items-center gap-2 small text-body-secondary">Dashboard view<select aria-label="Dashboard view" className="form-select form-select-sm w-auto" value={manager ? "manager" : "executive"} onChange={(event) => router.push(hrLink(selected, event.target.value === "manager"))}><option value="executive">HR Executive</option><option value="manager">HR Manager</option></select></label></div>
    {executive ? <h1 className="visually-hidden">{module.displayName}</h1> : <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
      <div><h1 className="h3 mb-1">{module.displayName}</h1><p className="text-body-secondary mb-0">Manage your workforce, time off, payroll, and employee development.</p></div>
      <div className="d-flex gap-2"><Link className="btn btn-outline-primary" href="/employees">Employees</Link><Link className="btn btn-outline-secondary" href="/dashboard">Dashboard</Link></div>
    </div>}
    {!organization ? <div className="alert alert-info">Select an organization to manage human resources.</div> : <>
      {executive ? <HrExecutiveDashboard key={organization} organization={organization} can={can} section={selected} search={params.get("search") ?? ""} manager={manager} /> : <><nav aria-label="HR sections" className="d-flex flex-wrap gap-2 mb-4">
        <button type="button" className="btn btn-sm btn-outline-secondary" onClick={() => setSelected("overview")}>Overview</button>
        {collections.map((item) => <button type="button" key={item.id} className={`btn btn-sm ${active?.id === item.id ? "btn-primary" : "btn-outline-secondary"}`} aria-pressed={active?.id === item.id} onClick={() => setSelected(item.id)}>{item.label}</button>)}
      </nav>
      {active ? <CollectionWorkspace key={`${organization}:${active.id}`} collection={active} organization={organization} can={can} /> : <div className="alert alert-info">Your role does not have access to HR records. Contact your organization administrator.</div>}</>}
    </>}
  </section>;
}

function CollectionWorkspace({ collection, organization, can }: { collection: Collection; organization: string; can: (permission: string) => boolean }) {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [page, setPage] = useState(1);
  const [editor, setEditor] = useState<Editor | null>(null);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const [note, setNote] = useState("");
  const [notice, setNotice] = useState("");
  const records = useQuery({
    queryKey: ["hr", organization, collection.id, search, page],
    queryFn: () => listRecords(collection.path, { search, page, page_size: 20 }),
  });
  const refresh = async () => {
    await queryClient.invalidateQueries({ queryKey: ["hr", organization] });
    await queryClient.invalidateQueries({ queryKey: ["employees"] });
  };
  const detail = useMutation({
    mutationFn: async ({ record, kind }: { record: HrRecord; kind: "edit" | "view" }) => ({ kind, record: (await apiClient.get<HrRecord>(`${collection.path}${record.id}/`)).data }),
    onSuccess: setEditor,
  });
  const workflow = useMutation({
    mutationFn: async (value: Confirmation) => {
      const path = `${collection.path}${value.record.id}/`;
      if (!value.action) return apiClient.delete(path);
      return apiClient.post(`${path}${value.action.route}/`, value.action.note ? { [value.action.note]: note } : {});
    },
    onSuccess: async () => {
      setNotice(confirmation?.action ? `${confirmation.action.label} completed.` : "Record deleted.");
      setConfirmation(null);
      if (!confirmation?.action && records.data?.rows.length === 1 && page > 1) setPage(page - 1);
      await refresh();
    },
  });
  const busy = detail.isPending || workflow.isPending;
  return <div className="card shadow-sm border-0">
    <div className="card-body p-4">
      <div className="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-3">
        <h2 className="h5 mb-0">{collection.label}</h2>
        <div className="d-flex gap-2"><button className="btn btn-outline-secondary btn-sm" disabled={records.isFetching || busy} onClick={() => void records.refetch()}>Refresh</button>
          {can(`${collection.permission}.create`) && <button className="btn btn-primary btn-sm" disabled={busy} onClick={() => { setEditor({ kind: "create" }); setNotice(""); }}>Create record</button>}</div>
      </div>
      {notice && <div className="alert alert-success" role="status">{notice}</div>}
      {(detail.isError || workflow.isError) && <div className="alert alert-danger" role="alert">{errorMessage(detail.error ?? workflow.error)}</div>}
      {editor && <RecordEditor key={`${editor.kind}:${editor.record?.id ?? "new"}`} editor={editor} collection={collection} organization={organization} onClose={() => setEditor(null)} onSaved={async () => { setEditor(null); setNotice("Record saved."); await refresh(); }} />}
      {confirmation && <div className="border rounded p-3 mb-3" role="region" aria-label="Confirm action">
        <h3 className="h6">{confirmation.action?.label ?? "Delete record"} #{String(confirmation.record.id)}?</h3>
        <p className="small text-body-secondary">{confirmation.action?.route === "apply-to-attendance" ? "This updates attendance for all active employees in this organization on the holiday date." : !confirmation.action ? "This permanently removes the record." : "The backend will validate the workflow before applying this change."}</p>
        {confirmation.action?.note && <label className="d-block mb-3">{label(confirmation.action.note)}<textarea className="form-control mt-1" value={note} onChange={(event) => setNote(event.target.value)} /></label>}
        <div className="d-flex gap-2"><button className="btn btn-primary btn-sm" disabled={workflow.isPending} onClick={() => workflow.mutate(confirmation)}>{workflow.isPending ? "Saving…" : "Confirm"}</button><button className="btn btn-outline-secondary btn-sm" disabled={workflow.isPending} onClick={() => setConfirmation(null)}>Back</button></div>
      </div>}
      <form className="d-flex gap-2 mb-3" onSubmit={(event) => { event.preventDefault(); setSearch(searchInput.trim()); setPage(1); }}>
        <input className="form-control" aria-label={`Search ${collection.label}`} placeholder={`Search ${collection.label.toLowerCase()}…`} value={searchInput} onChange={(event) => setSearchInput(event.target.value)} />
        <button className="btn btn-outline-primary" type="submit">Search</button>
      </form>
      {records.isError ? <div role="alert" className="alert alert-danger">{errorMessage(records.error)} <button className="btn btn-sm btn-outline-danger" onClick={() => void records.refetch()}>Try again</button></div> : records.isPending ? <p role="status">Loading records…</p> : <>
        <div className="table-responsive"><table className="table table-hover align-middle">
          <thead><tr>{collection.columns.map((column) => <th key={column} scope="col">{label(column)}</th>)}<th scope="col">Actions</th></tr></thead>
          <tbody>{records.data.rows.map((record) => <tr key={String(record.id)}>
            {collection.columns.map((column) => <td key={column}>{column === "status" ? <span className="badge text-bg-light border">{label(display(record[column]))}</span> : display(record[column])}</td>)}
            <td><div className="d-flex flex-wrap gap-1">
              <button className="btn btn-sm btn-outline-secondary" disabled={busy} onClick={() => detail.mutate({ record, kind: "view" })}>Details</button>
              {can(`${collection.permission}.update`) && <button className="btn btn-sm btn-outline-primary" disabled={busy} onClick={() => detail.mutate({ record, kind: "edit" })}>Edit</button>}
              {collection.actions?.filter((action) => can(action.permission) && (!action.statuses || action.statuses.includes(String(record.status)))).map((action) => <button key={action.route} className="btn btn-sm btn-outline-primary" disabled={busy} onClick={() => { setConfirmation({ record, action }); setNote(""); workflow.reset(); }}>{action.label}</button>)}
              {can(`${collection.permission}.delete`) && <button className="btn btn-sm btn-outline-danger" disabled={busy} onClick={() => { setConfirmation({ record }); workflow.reset(); }}>Delete</button>}
            </div></td>
          </tr>)}{!records.data.rows.length && <tr><td colSpan={collection.columns.length + 1} className="text-center text-body-secondary py-5">{search ? "No matching records." : "No records yet."}</td></tr>}</tbody>
        </table></div>
        <div className="d-flex justify-content-between align-items-center"><span className="small text-body-secondary">{records.data.count} records · Page {page}</span><div className="d-flex gap-2"><button className="btn btn-sm btn-outline-secondary" disabled={page <= 1 || records.isFetching} onClick={() => setPage(page - 1)}>Previous</button><button className="btn btn-sm btn-outline-secondary" disabled={!records.data.hasNext || records.isFetching} onClick={() => setPage(page + 1)}>Next</button></div></div>
      </>}
    </div>
  </div>;
}

function RecordEditor({ editor, collection, organization, onClose, onSaved }: { editor: Editor; collection: Collection; organization: string; onClose: () => void; onSaved: () => Promise<void> }) {
  const fields = collection.fields.filter((field) => editor.kind !== "edit" || !collection.updateFields || collection.updateFields.includes(field.name));
  const [lineItems, setLineItems] = useState<Array<{ component_type: string; name: string; amount: string }>>(() => (Array.isArray(editor.record?.line_items) ? editor.record.line_items : []).map((item: HrRecord) => ({ component_type: String(item.component_type), name: String(item.name), amount: String(item.amount) })));
  const [values, setValues] = useState<Record<string, string | boolean>>(() => Object.fromEntries(fields.map((field) => {
    let value: unknown = editor.record?.[`${field.name}_id`] ?? editor.record?.[field.name] ?? field.default ?? "";
    if (value && typeof value === "object") value = (value as HrRecord).id;
    if (field.type === "datetime-local" && value) {
      const date = new Date(String(value));
      if (!Number.isNaN(date.getTime())) value = new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    }
    return [field.name, typeof value === "boolean" ? value : String(value)];
  })));
  const references = [...new Set(fields.flatMap((field) => field.lookup ? [field.lookup] : []))];
  const lookups = useQuery({
    queryKey: ["hr", organization, "lookups", ...references],
    queryFn: async () => Object.fromEntries(await Promise.all(references.map(async (id) => [id, await lookupRecords(id === "employees" ? "/employees/" : id === "departments" ? "/departments/" : HR_COLLECTIONS.find((item) => item.id === id)!.path)]))) as Record<string, HrRecord[]>,
    enabled: editor.kind !== "view" && references.length > 0,
  });
  const save = useMutation({
    mutationFn: async () => {
      const body: HrRecord = {};
      if (collection.organization) body.organization = organization;
      for (const field of fields) {
        if (field.type === "line-items") { body.line_items = lineItems; continue; }
        const value = values[field.name];
        if (value === "") { if (field.nullable) body[field.name] = null; else if (field.type === "textarea" || field.type === "text" || !field.type && !field.lookup && !field.choices) body[field.name] = ""; continue; }
        body[field.name] = field.type === "datetime-local" ? new Date(String(value)).toISOString() : field.type === "number" ? Number(value) : value;
      }
      return editor.kind === "edit" ? apiClient.patch(`${collection.path}${editor.record!.id}/`, body) : apiClient.post(collection.path, body);
    },
    onSuccess: onSaved,
  });
  const submit = (event: FormEvent) => { event.preventDefault(); save.mutate(); };
  if (editor.kind === "view") return <div className="border rounded p-3 mb-4" aria-label="Record details"><div className="d-flex justify-content-between"><h3 className="h6">Record #{String(editor.record?.id)}</h3><button className="btn btn-sm btn-outline-secondary" onClick={onClose}>Close</button></div><dl className="row mb-0">{Object.entries(editor.record ?? {}).map(([key, value]) => <div key={key} className="col-md-6 mb-2"><dt className="small text-body-secondary">{label(key)}</dt><dd className="mb-0" style={{ whiteSpace: "pre-wrap" }}>{Array.isArray(value) ? value.map((item) => typeof item === "object" ? Object.entries(item as HrRecord).map(([name, content]) => `${label(name)}: ${display(content)}`).join(" · ") : display(item)).join("\n") : display(value)}</dd></div>)}</dl></div>;
  return <form className="border rounded p-3 mb-4" aria-label="HR record form" onSubmit={submit}>
    <h3 className="h6 mb-3">{editor.kind === "edit" ? "Edit" : "Create"} · {collection.label}</h3>
    {save.isError && <div className="alert alert-danger" role="alert">{errorMessage(save.error)}</div>}
    {lookups.isError && <div className="alert alert-danger" role="alert">Could not load related records. {errorMessage(lookups.error)} <button type="button" className="btn btn-sm btn-outline-danger ms-2" onClick={() => void lookups.refetch()}>Retry</button></div>}
    <fieldset disabled={save.isPending}>
      <div className="row g-3">{fields.map((field) => {
        if (field.type === "line-items") return <div className="col-12" key={field.name}>
          <h4 className="h6">Earnings and deductions</h4>
          {lineItems.map((item, index) => <div className="row g-2 mb-2" key={index}>
            <div className="col-md-3"><label className="form-label" htmlFor={`component-${index}`}>Component</label><select id={`component-${index}`} className="form-select" value={item.component_type} onChange={(event) => setLineItems(lineItems.map((line, i) => i === index ? { ...line, component_type: event.target.value } : line))}><option value="earning">Earning</option><option value="deduction">Deduction</option></select></div>
            <div className="col-md-4"><label className="form-label" htmlFor={`line-name-${index}`}>Name</label><input id={`line-name-${index}`} className="form-control" required value={item.name} onChange={(event) => setLineItems(lineItems.map((line, i) => i === index ? { ...line, name: event.target.value } : line))} /></div>
            <div className="col-md-3"><label className="form-label" htmlFor={`amount-${index}`}>Amount</label><input id={`amount-${index}`} className="form-control" type="number" min="0" step="0.01" required value={item.amount} onChange={(event) => setLineItems(lineItems.map((line, i) => i === index ? { ...line, amount: event.target.value } : line))} /></div>
            <div className="col-md-2 d-flex align-items-end"><button className="btn btn-outline-danger" type="button" onClick={() => setLineItems(lineItems.filter((_, i) => i !== index))}>Remove</button></div>
          </div>)}
          <button type="button" className="btn btn-sm btn-outline-primary" onClick={() => setLineItems([...lineItems, { component_type: "earning", name: "", amount: "" }])}>Add component</button>
        </div>;
        const id = `hr-${field.name}`;
        const lookup = field.lookup ? lookups : undefined;
        const options = field.lookup ? lookups.data?.[field.lookup] : undefined;
        return <div className="col-md-6" key={field.name}>
          <label className="form-label" htmlFor={id}>{label(field.name)}{field.required ? " *" : ""}</label>
          {field.lookup || field.choices ? <select className="form-select" id={id} required={field.required} disabled={lookup?.isPending || lookup?.isError} value={String(values[field.name])} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })}>
            <option value="">{lookup?.isPending ? "Loading…" : "Select…"}</option>
            {field.choices?.map((value) => <option key={value} value={value}>{label(value)}</option>)}
            {options?.map((record) => <option key={String(record.id)} value={String(record.id)}>{display(record.full_name ?? record.employee_name ?? record.name ?? record.title)}{record.employee_code ? ` (${record.employee_code})` : ` #${record.id}`}</option>)}
          </select> : field.type === "textarea" ? <textarea className="form-control" id={id} value={String(values[field.name])} required={field.required} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })} /> : <input className={field.type === "checkbox" ? "form-check-input d-block" : "form-control"} id={id} type={field.type ?? "text"} step={field.type === "number" ? "any" : undefined} required={field.required} checked={field.type === "checkbox" ? Boolean(values[field.name]) : undefined} value={field.type === "checkbox" ? undefined : String(values[field.name])} onChange={(event) => setValues({ ...values, [field.name]: field.type === "checkbox" ? event.target.checked : event.target.value })} />}
        </div>;
      })}</div>
      <div className="d-flex gap-2 mt-3"><button type="submit" className="btn btn-primary" disabled={references.length > 0 && (lookups.isPending || lookups.isError)}>{save.isPending ? "Saving…" : "Save record"}</button><button type="button" className="btn btn-outline-secondary" onClick={onClose}>Cancel</button></div>
    </fieldset>
  </form>;
}
