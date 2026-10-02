"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useQueries } from "@tanstack/react-query";
import { AlertTriangle, CalendarDays, ClipboardList, FileText, House, Stethoscope, Syringe, Users, type LucideIcon } from "lucide-react";
import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";
import { NursingOperations, nursingSections } from "./nursing-operations";

type Row = Record<string, unknown>;
type Payload = Row[] | { results?: Row[]; rows?: Row[]; data?: Row[] };
const sources = [["assignments", "/nursing/assignments/"], ["tasks", "/nursing/tasks/"], ["medication", "/nursing/medication-administrations/"], ["care-plans", "/nursing/care-plans/"], ["alerts", "/nursing/alerts/"], ["schedules", "/nursing/schedules/"], ["handovers", "/nursing/handovers/"]] as const;
const nav: Array<[string, string, LucideIcon]> = [["Overview", "overview", House], ["My Patients", "assignments", Stethoscope], ["Tasks", "tasks", ClipboardList], ["Medication", "medication", Syringe], ["Care Plans", "care-plans", ClipboardList], ["Alerts", "alerts", AlertTriangle], ["Schedules", "schedules", CalendarDays], ["Handovers", "handovers", FileText]];
function list(payload: Payload | undefined): Row[] { return Array.isArray(payload) ? payload : payload?.results ?? payload?.rows ?? payload?.data ?? []; }
function show(value: unknown, fallback = "-"): string { return value === null || value === undefined || value === "" ? fallback : String(value); }

export function NurseDashboard() {
  const { bootstrap } = useBootstrap();
  const section = useSearchParams().get("section") ?? "overview";
  const allowed = Boolean(bootstrap?.organization?.id && (bootstrap.user.is_platform_admin || bootstrap.permissions.includes("*") || bootstrap.permissions.includes("nursing.view")));
  const queries = useQueries({ queries: sources.map(([key, path]) => ({ queryKey: ["nursing", key, bootstrap?.organization?.id], queryFn: async () => (await apiClient.get<Payload>(path, { params: { page_size: 100 } })).data, enabled: allowed, staleTime: 15_000 })) });
  const assignments = list(queries[0].data).filter((row) => row.status === "active");
  const tasks = list(queries[1].data).filter((row) => ["pending", "in_progress"].includes(String(row.status)));
  const medication = list(queries[2].data).filter((row) => row.status === "scheduled");
  const alerts = list(queries[4].data).filter((row) => row.severity === "critical" && row.status !== "resolved");
  const schedules = list(queries[5].data);
  const shift = schedules.find((row) => row.status === "active") ?? schedules.find((row) => row.status === "scheduled");
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const name = bootstrap?.user.first_name ?? bootstrap?.user.full_name?.split(" ")[0] ?? "Nurse";
  const loading = queries.some((query) => query.isPending && query.fetchStatus === "fetching");
  return <section className="container-fluid py-4"><div className="row g-4">
    <aside className="col-12 col-xl-2"><nav className="card border-0 shadow-sm p-2" aria-label="Nurse workspace">{nav.map(([label, target, Icon]) => <Link key={target} href={target === "overview" ? "/nurse" : `/nurse?section=${target}`} className={`nav-link d-flex align-items-center gap-2 rounded px-3 py-2 ${section === target ? "active" : "text-body"}`}><Icon size={18} />{label}</Link>)}</nav></aside>
    <div className="col-12 col-xl-10">{section !== "overview" && nursingSections.includes(section) ? <NursingOperations section={section} /> : <>
      <div className="mb-4"><h1 className="h2 mb-1">{greeting}, {name}</h1><p className="text-body-secondary mb-0">{show(shift?.ward_name, "No ward scheduled")} - {show(shift?.shift_type, "Off shift")}</p></div>
      {!allowed && <div className="alert alert-info">Your role does not have access to nursing records.</div>}
      {queries.some((query) => query.isError) && <div className="alert alert-warning">Some nursing data could not be loaded.</div>}
      <div className="row g-3 mb-4"><Kpi label="Patients" value={assignments.length} detail="Assigned" icon={Users} color="primary" loading={loading} /><Kpi label="Tasks" value={tasks.length} detail="Pending" icon={ClipboardList} color="info" loading={loading} /><Kpi label="Medication" value={medication.length} detail="Scheduled" icon={Syringe} color="warning" loading={loading} /><Kpi label="Alerts" value={alerts.length} detail="Critical" icon={AlertTriangle} color="danger" loading={loading} /></div>
      <div className="row g-4 mb-4"><div className="col-12 col-lg-7"><Panel title="Patient Care" href="/nurse?section=assignments"><table className="table align-middle"><thead><tr><th>Patient</th><th>Ward</th><th>Since</th></tr></thead><tbody>{assignments.map((row) => <tr key={String(row.id)}><td>{show(row.patient_name)}</td><td>{show(row.ward_name)}</td><td>{show(row.started_at)}</td></tr>)}{!assignments.length && <Empty columns={3} text="No active patient assignments." />}</tbody></table></Panel></div><div className="col-12 col-lg-5"><Panel title="Nursing Tasks" href="/nurse?section=tasks">{tasks.slice(0, 6).map((task) => <Link href="/nurse?section=tasks" className="list-group-item list-group-item-action px-0" key={String(task.id)}><strong>{show(task.title)}</strong><div className="small text-body-secondary">{show(task.patient_name)} - {show(task.due_at)}</div></Link>)}{!tasks.length && <p>No pending tasks.</p>}</Panel></div></div>
      <div className="card border-0 shadow-sm"><div className="card-body p-4"><div className="d-flex gap-2 mb-3"><Link className="btn btn-sm btn-primary" href="/nurse?section=medication">Medication Schedule ({medication.length})</Link><Link className="btn btn-sm btn-outline-danger" href="/nurse?section=alerts">Critical Alerts ({alerts.length})</Link><Link className="btn btn-sm btn-outline-secondary" href="/nurse?section=handovers">Handovers</Link></div>{alerts.map((alert) => <div className="border-top py-2 d-flex justify-content-between" key={String(alert.id)}><span>{show(alert.patient_name)} - {show(alert.title)}</span><span className="text-danger">{show(alert.status)}</span></div>)}{!alerts.length && <p className="text-body-secondary mb-0">No critical alerts.</p>}</div></div>
    </>}</div>
  </div></section>;
}

function Kpi({ label, value, detail, icon: Icon, color, loading }: { label: string; value: number; detail: string; icon: LucideIcon; color: string; loading: boolean }) { return <div className="col-12 col-sm-6 col-xl-3"><div className="card border-0 shadow-sm h-100"><div className="card-body"><div className="d-flex justify-content-between"><span>{label}</span><Icon size={20} className={`text-${color}`} /></div><div className="display-6 fw-semibold my-2">{loading ? "..." : value}</div><div className="small text-body-secondary">{detail}</div></div></div></div>; }
function Panel({ title, href, children }: { title: string; href: string; children: React.ReactNode }) { return <div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between"><h2 className="h5">{title}</h2><Link href={href}>Manage</Link></div>{children}</div></div>; }
function Empty({ columns, text }: { columns: number; text: string }) { return <tr><td colSpan={columns} className="text-center text-body-secondary py-4">{text}</td></tr>; }
