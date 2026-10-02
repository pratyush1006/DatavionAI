"use client";

import Link from "next/link";
import { useState } from "react";
import { useQueries } from "@tanstack/react-query";
import { Users, Clock, CalendarDays, ClipboardCheck, ArrowUpRight, Download, RefreshCw, TrendingDown, Briefcase } from "lucide-react";
import { useBootstrap } from "@/core/bootstrap";
import { display, errorMessage, lookupRecords } from "./api";
import type { HrRecord } from "./config";
import { hrLink } from "./persona";
import { ManagerAnalytics, turnover, WorkforceTrend } from "./manager-analytics";

const sources = [
  { id: "employees", path: "/employees/", permission: "employees.view" },
  { id: "attendance", path: "/hr/attendance/", permission: "attendance.view" },
  { id: "requests", path: "/hr/leave/requests/", permission: "leave.view" },
  { id: "processes", path: "/hr/onboarding/processes/", permission: "onboarding.view" },
  { id: "departments", path: "/departments/", permission: "departments.view" },
  { id: "jobs", path: "/hr/recruitment/jobs/", permission: "recruitment.view" },
  { id: "interviews", path: "/hr/recruitment/interviews/", permission: "recruitment.view" },
];
const dateKey = (date: Date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
const activeEmployee = (row: HrRecord, today: string) => !["terminated", "inactive"].includes(String(row.status).toLowerCase()) && (!row.joining_date || String(row.joining_date) <= today) && (!row.termination_date || String(row.termination_date) > today);

export function HrExecutiveDashboard({ organization, can, section = "overview", search = "", manager = false }: { organization: string; can: (permission: string) => boolean; section?: string; search?: string; manager?: boolean }) {
  const { bootstrap } = useBootstrap();
  const [tab, setTab] = useState("employees");
  const [now, setNow] = useState(() => new Date());
  const today = dateKey(now);
  const queries = useQueries({ queries: sources.map((source) => ({ queryKey: ["hr", organization, "dashboard", source.id], queryFn: () => lookupRecords(source.path), enabled: can(source.permission) && (source.id !== "departments" || manager), staleTime: 30_000 })) });
  const rows = (index: number) => queries[index].data ?? [];
  const available = (index: number) => can(sources[index].permission) && queries[index].isSuccess;
  const value = (index: number, count: number) => !can(sources[index].permission) ? "—" : queries[index].isPending ? "…" : queries[index].isError ? "—" : String(count);
  const employees = rows(0).filter((row) => activeEmployee(row, today));
  const attendance = rows(1).filter((row) => row.work_date === today);
  const present = new Set(attendance.filter((row) => ["present", "late", "half_day"].includes(String(row.status))).map((row) => String(row.employee))).size;
  const onLeave = new Set(rows(2).filter((row) => row.status === "approved" && String(row.start_date) <= today && String(row.end_date) >= today).map((row) => String(row.employee))).size;
  const pending = rows(2).filter((row) => row.status === "pending");
  const joining = employees.filter((row) => row.joining_date === today);
  const joined = employees.filter((row) => String(row.joining_date ?? "").startsWith(today.slice(0, 7)));
  const openJobs = rows(5).filter((row) => row.status === "open");
  const interviewsToday = rows(6).filter((row) => row.status === "scheduled" && dateKey(new Date(String(row.scheduled_at))) === today);
  const executiveMetrics = [
    { title: "Employees", value: value(0, employees.length), note: available(0) ? `+${joined.length} joined this month` : "Active workforce", section: "employees", icon: Users, color: "primary" },
    { title: "Present", value: value(1, present), note: available(0) && available(1) && employees.length ? `${Math.round(present / employees.length * 100)}% of workforce today` : "Attendance recorded today", section: "attendance", icon: Clock, color: "success" },
    { title: "On Leave", value: value(2, onLeave), note: "Approved leave today", section: "requests", icon: CalendarDays, color: "warning" },
    { title: "Approvals", value: value(2, pending.length), note: "Leave requests pending", section: "requests", icon: ClipboardCheck, color: "danger" },
  ];
  const monthStart = dateKey(new Date(now.getFullYear(), now.getMonth(), 1));
  const previousStart = dateKey(new Date(now.getFullYear(), now.getMonth() - 1, 1));
  const previousEnd = dateKey(new Date(now.getFullYear(), now.getMonth(), 0));
  const currentTurnover = turnover(rows(0), monthStart, today);
  const previousTurnover = turnover(rows(0), previousStart, previousEnd);
  const delta = (current: number | null, previous: number | null) => current === null || previous === null ? "Comparison unavailable" : `${current >= previous ? "\u2191" : "\u2193"} ${Math.abs(current - previous).toFixed(1)} percentage points vs last month`;
  const attendanceRate = (month: string) => {
    const records = rows(1).filter((row) => String(row.work_date).startsWith(month) && !["holiday", "week_off"].includes(String(row.status)));
    return records.length ? records.filter((row) => ["present", "late", "half_day"].includes(String(row.status))).length / records.length * 100 : null;
  };
  const metrics = manager ? [
    { ...executiveMetrics[0], title: "Headcount" },
    { ...executiveMetrics[1], title: "Attendance", value: available(0) && available(1) && employees.length ? `${Math.round(present / employees.length * 100)}%` : "—", note: available(1) ? delta(attendanceRate(today.slice(0, 7)), attendanceRate(previousStart.slice(0, 7))) : "Attendance data unavailable" },
    { title: "Turnover", value: available(0) && currentTurnover !== null ? `${currentTurnover.toFixed(1)}%` : "—", note: available(0) ? delta(currentTurnover, previousTurnover) : "Employee data unavailable", section: "reports", icon: TrendingDown, color: "warning" },
    { title: "Open Jobs", value: value(5, openJobs.length), note: available(5) ? `${openJobs.filter((row) => row.priority === "urgent").length} urgent` : "Recruitment data unavailable", section: "recruitment", icon: Briefcase, color: "danger" },
  ] : executiveMetrics;
  const chart = Array.from({ length: 6 }, (_, index) => {
    const end = new Date(now.getFullYear(), now.getMonth() - 4 + index, 0);
    const cutoff = end > now ? today : dateKey(end);
    return { month: end.toLocaleDateString(undefined, { month: "short" }), count: rows(0).filter((row) => row.joining_date && String(row.joining_date) <= cutoff && (!row.termination_date || String(row.termination_date) > cutoff) && (row.termination_date || !["terminated", "inactive"].includes(String(row.status).toLowerCase()))).length };
  });
  const max = Math.max(1, ...chart.map((item) => item.count));
  const visibleTab = section === "employees" ? "employees" : tab;
  const tableSources: Record<string, { index: number; columns: string[]; rows: HrRecord[] }> = {
    employees: { index: 0, columns: ["full_name", "employee_code", "designation", "joining_date", "status"], rows: employees.filter((row) => !search || [row.full_name, row.employee_code, row.designation, row.work_email].some((field) => String(field ?? "").toLowerCase().includes(search.toLowerCase()))) },
    attendance: { index: 1, columns: ["employee_name", "check_in", "check_out", "hours_worked", "status"], rows: attendance },
    recruitment: { index: 5, columns: ["title", "department_name", "vacancies", "priority", "status"], rows: openJobs },
    requests: { index: 2, columns: ["employee_name", "leave_type", "start_date", "end_date", "status"], rows: pending },
  };
  const table = tableSources[visibleTab];
  function exportReport() {
    const data = [["Month", "Headcount"], ...chart.map((item) => [item.month, String(item.count)])];
    const url = URL.createObjectURL(new Blob([data.map((row) => row.join(",")).join("\r\n")], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a"); link.href = url; link.download = `hr-headcount-${today}.csv`; link.click(); URL.revokeObjectURL(url);
  }
  return <>
    <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
      <div><div className="small text-primary fw-semibold mb-2">{section === "reports" ? "WORKFORCE REPORTS" : (manager ? "HR MANAGER DASHBOARD" : "HR EXECUTIVE DASHBOARD")}</div><h2 className="h3 fw-semibold mb-2">Good {now.getHours() < 12 ? "morning" : now.getHours() < 17 ? "afternoon" : "evening"}, {manager ? "HR Manager" : "HR Executive"} <span aria-hidden="true">👋</span></h2><p className="text-body-secondary mb-0">{manager ? "Workforce Management" : "Human Resources"} · {bootstrap?.organization?.name}</p></div>
      <div className="d-flex align-items-center gap-2"><span className="small text-body-secondary me-2">{now.toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short", year: "numeric" })}</span><button type="button" className="btn btn-outline-secondary btn-sm" aria-label="Refresh HR dashboard" disabled={queries.some((query) => query.isFetching)} onClick={() => { setNow(new Date()); queries.forEach((query, index) => { if (can(sources[index].permission) && (sources[index].id !== "departments" || manager)) void query.refetch(); }); }}><RefreshCw size={16} /></button></div>
    </div>
    {queries.map((query, index) => query.isError && can(sources[index].permission) ? <div key={sources[index].id} className="alert alert-danger small" role="alert">Could not load {sources[index].id}: {errorMessage(query.error)} <button className="btn btn-sm btn-outline-danger ms-2" onClick={() => void query.refetch()}>Retry</button></div> : null)}
    <div className="row g-3 mb-4">{metrics.map(({ title, value: count, note, section: target, icon: Icon, color }) => <div className="col-6 col-xl-3" key={title}><Link href={hrLink(target, manager)} className="card border-0 shadow-sm h-100 text-decoration-none text-body"><div className="card-body p-4"><div className="d-flex justify-content-between align-items-center mb-3"><span className="text-body-secondary small fw-medium">{title}</span><span className={`rounded-3 p-2 bg-${color}-subtle text-${color}`}><Icon size={20} aria-hidden="true" /></span></div><div className="display-6 fw-semibold mb-1" data-testid={`hr-metric-${title.toLowerCase().replaceAll(" ", "-")}`}>{count}</div><span className="small text-body-secondary">{note}</span></div></Link></div>)}</div>
    <div className="row g-4 mb-4">
      <div className="col-12 col-xl-8"><div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between align-items-start gap-2 mb-4"><div><h3 className="h5 mb-1">{manager ? "Workforce Analytics" : "Workforce Overview"}</h3><p className="small text-body-secondary mb-0">Headcount over the last six months</p></div><button type="button" className="btn btn-sm btn-outline-secondary" disabled={!available(0)} onClick={exportReport}><Download size={14} className="me-2" />Export</button></div>
        {available(0) ? <>{manager ? <WorkforceTrend chart={chart} /> : <div className="d-flex align-items-end gap-3 px-2" style={{ height: 210 }} role="img" aria-label={`Headcount chart: ${chart.map((item) => `${item.month}: ${item.count}`).join(", ")}`}>{chart.map((item, index) => <div key={index} className="d-flex flex-column align-items-center justify-content-end flex-fill h-100"><span className="small fw-semibold mb-2">{item.count}</span><div className={`w-100 rounded-top ${index === chart.length - 1 ? "bg-primary" : "bg-primary-subtle"}`} style={{ height: `${Math.max(2, item.count / max * 155)}px`, maxWidth: 62 }} /><span className="small text-body-secondary mt-2">{item.month}</span></div>)}</div>}<p className="small text-body-secondary mt-3 mb-0">Derived from employee joining and termination dates.</p></> : <div className="text-body-secondary d-flex align-items-center justify-content-center" style={{ height: 210 }}>{can("employees.view") ? queries[0].isError ? "Workforce data unavailable" : "Loading workforce…" : "Employee access is required to view headcount."}</div>}
      </div></div></div>
      <div className="col-12 col-xl-4"><div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><h3 className="h5 mb-4">{manager ? "Manager Actions" : "HR Actions"}</h3><div className="d-flex flex-column gap-3">
        {(manager ? [{ name: "Leave Approvals", count: value(2, pending.length), target: "requests", detail: "Review pending leave requests" }, { name: "Recruitment", count: value(5, openJobs.length), target: "recruitment", detail: "Manage jobs and candidates" }, { name: "Performance Reviews", count: "\u2192", target: "reviews", detail: "Open employee review workflows" }] : [{ name: "Leave requests", count: value(2, pending.length), target: "requests", detail: "Review pending approvals" }, { name: "Joining today", count: value(0, joining.length), target: "employees", detail: "Welcome your new employees" }, { name: "Interviews today", count: value(6, interviewsToday.length), target: "interviews", detail: "Review scheduled interviews" }]).map((action) => <Link key={action.name} href={hrLink(action.target, manager)} className="d-flex align-items-center gap-3 border rounded-3 p-3 text-decoration-none text-body"><span className="fs-4 fw-semibold text-primary">{action.count}</span><div className="flex-grow-1"><div className="fw-medium">{action.name}</div><div className="small text-body-secondary">{action.detail}</div></div><ArrowUpRight size={17} className="text-body-secondary" /></Link>)}
        <div className="small text-body-secondary border-top pt-3"><Link href={hrLink("processes", manager)}>View onboarding</Link> · <Link href={hrLink("interviews", manager)}>View interviews</Link></div>
      </div></div></div></div>
    </div>
    {manager && search && section === "employees" && <div className="card border-0 shadow-sm mb-4"><div className="card-body p-4"><h3 className="h5">Department search results</h3>{available(4) ? rows(4).filter((row) => [row.name, row.code].some((field) => String(field ?? "").toLowerCase().includes(search.toLowerCase()))).map((row) => <Link key={String(row.id)} className="d-block py-2" href="/settings/access">{display(row.name)} · {display(row.code)}</Link>) : <p className="text-body-secondary small">Department data unavailable or loading.</p>}</div></div>}
    {manager && <><p className="small text-body-secondary">Attendance: employees present today / active headcount. Turnover: departures this month / average opening and current headcount. Attendance comparisons use recorded working days.</p><ManagerAnalytics today={today} employees={employees} leave={rows(2)} processes={rows(3)} ready={[available(0), available(2)]} /></>}
    <div className="card border-0 shadow-sm"><div className="card-body p-4"><div className="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-3"><nav className="nav nav-pills gap-1" aria-label="Dashboard records">{[{ id: "employees", name: "Employees" }, { id: "attendance", name: "Attendance" }, { id: "requests", name: "Leave" }, { id: "recruitment", name: "Recruitment" }].map((item) => <button type="button" key={item.id} className={`nav-link ${visibleTab === item.id ? "active" : "text-body-secondary"}`} aria-pressed={visibleTab === item.id} onClick={() => setTab(item.id)} disabled={section === "employees" && item.id !== "employees"}>{item.name}</button>)}</nav><Link className="small text-decoration-none" href={visibleTab === "employees" ? "/employees" : hrLink(visibleTab, manager)}>View all <ArrowUpRight size={14} /></Link></div>
      {table ? <div className="table-responsive"><table className="table align-middle mb-0"><thead><tr>{table.columns.map((column) => <th scope="col" className="small text-body-secondary fw-medium" key={column}>{column === "full_name" ? "Employee" : column.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase())}</th>)}</tr></thead><tbody>{table.rows.slice(0, section === "employees" ? 100 : 5).map((row) => <tr key={String(row.id)}>{table.columns.map((column, index) => <td key={column}>{index === 0 && visibleTab === "employees" ? <Link href={`/employees/${row.id}`} className="fw-medium text-decoration-none">{display(row[column])}</Link> : display(row[column])}</td>)}</tr>)}{!table.rows.length && <tr><td colSpan={table.columns.length} className="text-center text-body-secondary py-4">{!can(sources[table.index].permission) ? "You do not have access to these records." : queries[table.index].isPending ? "Loading records…" : queries[table.index].isError ? "Records unavailable. Retry above." : "No records to show."}</td></tr>}</tbody></table></div> : <p className="text-body-secondary mb-0">Choose a records tab above.</p>}
    </div></div>
  </>;
}
