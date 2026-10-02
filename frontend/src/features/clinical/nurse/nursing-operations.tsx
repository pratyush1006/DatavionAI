"use client";

import { useState, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/core/api";

type Row = Record<string, unknown>;
type Payload = Row[] | { results?: Row[]; rows?: Row[]; data?: Row[] };
type Field = { name: string; label: string; type?: string; lookup?: keyof Lookups; options?: string[]; required?: boolean };
type Configuration = { title: string; path: string; fields: Field[]; columns: string[]; actions: Record<string, string[]> };
type Lookups = { patients: Row[]; providers: Row[]; wards: Row[]; prescriptions: Row[]; schedules: Row[] };

const configs: Record<string, Configuration> = {
  assignments: { title: "Patient & Ward Assignments", path: "/nursing/assignments/", columns: ["patient_name", "nurse_name", "ward_name", "started_at", "status"], actions: { active: ["end"] }, fields: [
    { name: "patient", label: "Patient", lookup: "patients", required: true }, { name: "nurse", label: "Nurse", lookup: "providers", required: true }, { name: "ward", label: "Ward", lookup: "wards", required: true }, { name: "started_at", label: "Starts at", type: "datetime-local", required: true }, { name: "notes", label: "Notes" },
  ] },
  tasks: { title: "Nursing Tasks", path: "/nursing/tasks/", columns: ["patient_name", "nurse_name", "title", "priority", "due_at", "status"], actions: { pending: ["start", "complete", "cancel"], in_progress: ["complete", "cancel"] }, fields: [
    { name: "patient", label: "Patient", lookup: "patients", required: true }, { name: "assigned_nurse", label: "Assigned nurse", lookup: "providers", required: true }, { name: "title", label: "Task", required: true }, { name: "description", label: "Description" }, { name: "task_type", label: "Type", options: ["medication", "vitals", "care", "review", "other"], required: true }, { name: "priority", label: "Priority", options: ["routine", "urgent", "critical"], required: true }, { name: "due_at", label: "Due at", type: "datetime-local", required: true },
  ] },
  medication: { title: "Medication Administration", path: "/nursing/medication-administrations/", columns: ["patient_name", "nurse_name", "dose", "scheduled_at", "status"], actions: { scheduled: ["administer", "record-outcome"] }, fields: [
    { name: "patient", label: "Patient", lookup: "patients", required: true }, { name: "prescription", label: "Prescription", lookup: "prescriptions", required: true }, { name: "nurse", label: "Nurse", lookup: "providers", required: true }, { name: "scheduled_at", label: "Scheduled at", type: "datetime-local", required: true }, { name: "dose", label: "Dose", required: true }, { name: "route", label: "Route" }, { name: "site", label: "Site" }, { name: "notes", label: "Notes" },
  ] },
  "care-plans": { title: "Structured Care Plans", path: "/nursing/care-plans/", columns: ["patient_name", "nurse_name", "title", "review_date", "status", "version"], actions: { draft: ["activate", "cancel"], active: ["complete", "cancel"] }, fields: [
    { name: "patient", label: "Patient", lookup: "patients", required: true }, { name: "primary_nurse", label: "Primary nurse", lookup: "providers", required: true }, { name: "title", label: "Plan title", required: true }, { name: "diagnosis", label: "Nursing diagnosis" }, { name: "goals", label: "Goals (one per line)", type: "lines" }, { name: "interventions", label: "Interventions (one per line)", type: "lines" }, { name: "review_date", label: "Review date", type: "date" },
  ] },
  alerts: { title: "Clinical Alerts", path: "/nursing/alerts/", columns: ["patient_name", "title", "severity", "status", "created_at"], actions: { open: ["acknowledge", "escalate", "resolve"], acknowledged: ["escalate", "resolve"], escalated: ["resolve"] }, fields: [
    { name: "patient", label: "Patient", lookup: "patients", required: true }, { name: "assigned_nurse", label: "Assigned nurse", lookup: "providers" }, { name: "title", label: "Alert title", required: true }, { name: "message", label: "Message", required: true }, { name: "severity", label: "Severity", options: ["info", "warning", "critical"], required: true }, { name: "source_type", label: "Source", required: true },
  ] },
  schedules: { title: "Nurse Schedules", path: "/nursing/schedules/", columns: ["nurse_name", "ward_name", "starts_at", "ends_at", "shift_type", "status"], actions: { scheduled: ["start", "cancel"], active: ["complete"] }, fields: [
    { name: "nurse", label: "Nurse", lookup: "providers", required: true }, { name: "ward", label: "Ward", lookup: "wards", required: true }, { name: "starts_at", label: "Starts at", type: "datetime-local", required: true }, { name: "ends_at", label: "Ends at", type: "datetime-local", required: true }, { name: "shift_type", label: "Shift", options: ["morning", "evening", "night", "custom"], required: true }, { name: "notes", label: "Notes" },
  ] },
  handovers: { title: "Shift Handovers", path: "/nursing/handovers/", columns: ["from_nurse_name", "to_nurse_name", "summary", "status", "created_at"], actions: { draft: ["submit"], submitted: ["accept"] }, fields: [
    { name: "schedule", label: "Shift", lookup: "schedules", required: true }, { name: "from_nurse", label: "Outgoing nurse", lookup: "providers", required: true }, { name: "to_nurse", label: "Incoming nurse", lookup: "providers", required: true }, { name: "ward", label: "Ward", lookup: "wards", required: true }, { name: "patients", label: "Patient", lookup: "patients", required: true }, { name: "summary", label: "Summary", required: true }, { name: "outstanding_tasks", label: "Outstanding tasks (one per line)", type: "lines" }, { name: "safety_concerns", label: "Safety concerns" },
  ] },
};

function list(payload: Payload | undefined): Row[] { return Array.isArray(payload) ? payload : payload?.results ?? payload?.rows ?? payload?.data ?? []; }
function show(value: unknown): string { return value === null || value === undefined || value === "" ? "—" : String(value); }
function label(row: Row): string { return show(row.display_name ?? row.nurse_name ?? row.name ?? row.title ?? row.mrn ?? row.prescription_number ?? row.id); }

async function loadLookups(): Promise<Lookups> {
  const paths = ["/patient-management/patients/", "/providers/", "/hospital-operations/units/", "/prescriptions/", "/nursing/schedules/"];
  const values = await Promise.all(paths.map(async (path) => list((await apiClient.get<Payload>(path, { params: { page_size: 200 } })).data)));
  return { patients: values[0], providers: values[1], wards: values[2], prescriptions: values[3], schedules: values[4] };
}

export function NursingOperations({ section }: { section: string }) {
  const config = configs[section] ?? configs.assignments;
  const client = useQueryClient();
  const [creating, setCreating] = useState(false);
  const [values, setValues] = useState<Record<string, string>>({});
  const records = useQuery({ queryKey: ["nursing", section], queryFn: async () => list((await apiClient.get<Payload>(config.path)).data) });
  const lookups = useQuery({ queryKey: ["nursing", "lookups"], queryFn: loadLookups, enabled: creating });
  const refresh = () => client.invalidateQueries({ queryKey: ["nursing"] });
  const create = useMutation({ mutationFn: async () => {
    const body: Row = {};
    for (const field of config.fields) {
      const value = values[field.name] ?? "";
      if (!value && !field.required) continue;
      body[field.name] = field.type === "datetime-local" ? new Date(value).toISOString() : field.type === "lines" ? value.split("\n").map((line) => line.trim()).filter(Boolean) : field.name === "patients" ? [value] : value;
    }
    return apiClient.post(config.path, body);
  }, onSuccess: async () => { setCreating(false); setValues({}); await refresh(); } });
  const workflow = useMutation({ mutationFn: async ({ row, action }: { row: Row; action: string }) => {
    let body: Row = {};
    if (action === "complete" && section === "tasks") body = { completion_notes: window.prompt("Completion notes") ?? "Completed" };
    if (action === "record-outcome") body = { status: window.prompt("Outcome: held, refused, or missed", "held") ?? "held", notes: window.prompt("Reason") ?? "" };
    if (action === "escalate") body = { escalated_to: window.prompt("Provider ID to escalate to") ?? "" };
    if (action === "resolve") body = { resolution_notes: window.prompt("Resolution notes") ?? "" };
    return apiClient.post(`${config.path}${row.id}/${action}/`, body);
  }, onSuccess: refresh });
  const submit = (event: FormEvent) => { event.preventDefault(); create.mutate(); };
  return <div className="card border-0 shadow-sm"><div className="card-body p-4">
    <div className="d-flex justify-content-between align-items-center mb-3"><div><h1 className="h4 mb-1">{config.title}</h1><p className="small text-body-secondary mb-0">Persistent, organization-scoped nursing workflow</p></div><button className="btn btn-primary btn-sm" onClick={() => setCreating(!creating)}>{creating ? "Close" : "Create"}</button></div>
    {(create.isError || workflow.isError) && <div className="alert alert-danger" role="alert">The workflow could not be saved. Check the record state and required fields.</div>}
    {creating && <form className="border rounded p-3 mb-4" onSubmit={submit}><div className="row g-3">{config.fields.map((field) => <div className="col-md-6" key={field.name}><label className="form-label" htmlFor={`nursing-${field.name}`}>{field.label}{field.required ? " *" : ""}</label>{field.lookup || field.options ? <select id={`nursing-${field.name}`} className="form-select" required={field.required} value={values[field.name] ?? ""} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })}><option value="">Select…</option>{field.options?.map((option) => <option key={option}>{option}</option>)}{field.lookup && lookups.data?.[field.lookup].map((row) => <option value={String(row.id ?? row.uuid)} key={String(row.id ?? row.uuid)}>{label(row)}</option>)}</select> : field.type === "lines" ? <textarea id={`nursing-${field.name}`} className="form-control" required={field.required} value={values[field.name] ?? ""} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })} /> : <input id={`nursing-${field.name}`} className="form-control" type={field.type ?? "text"} required={field.required} value={values[field.name] ?? ""} onChange={(event) => setValues({ ...values, [field.name]: event.target.value })} />}</div>)}</div><button className="btn btn-primary mt-3" disabled={create.isPending || lookups.isPending}>Save record</button></form>}
    {records.isPending ? <p role="status">Loading nursing records…</p> : <div className="table-responsive"><table className="table align-middle"><thead><tr>{config.columns.map((column) => <th key={column}>{column.replaceAll("_", " ")}</th>)}<th>Actions</th></tr></thead><tbody>{records.data?.map((row) => <tr key={String(row.id)}>{config.columns.map((column) => <td key={column}>{show(row[column])}</td>)}<td><div className="d-flex flex-wrap gap-1">{(config.actions[String(row.status)] ?? []).map((action) => <button className="btn btn-sm btn-outline-primary" disabled={workflow.isPending} key={action} onClick={() => workflow.mutate({ row, action })}>{action.replaceAll("-", " ")}</button>)}</div></td></tr>)}{!records.data?.length && <tr><td colSpan={config.columns.length + 1} className="text-center text-body-secondary py-4">No records yet.</td></tr>}</tbody></table></div>}
  </div></div>;
}

export const nursingSections = Object.keys(configs);
