import Link from "next/link";
import { display } from "./api";
import type { HrRecord } from "./config";

export function ManagerAnalytics({ employees, leave, processes, ready, today }: { employees: HrRecord[]; leave: HrRecord[]; processes: HrRecord[]; ready: boolean[]; today: string }) {
  const groups = new Map<string, number>();
  for (const employee of employees) {
    const type = String(employee.employment_type ?? "Unspecified").replaceAll("_", " ");
    groups.set(type, (groups.get(type) ?? 0) + 1);
  }
  const leaveGroups = new Map<string, number>();
  for (const request of leave) {
    const status = String(request.status ?? "Unknown");
    leaveGroups.set(status, (leaveGroups.get(status) ?? 0) + 1);
  }
  const activity = [
    ...employees.filter((row) => row.joining_date).map((row) => ({ id: `employee-${row.id}`, date: String(row.joining_date), text: `${display(row.full_name)} joined`, href: `/employees/${row.id}` })),
    ...leave.filter((row) => row.start_date).map((row) => ({ id: `leave-${row.id}`, date: String(row.start_date), text: `${display(row.employee_name)} · ${display(row.status)} leave`, href: "/workspace/hr?section=requests&view=manager" })),
    ...processes.filter((row) => row.start_date).map((row) => ({ id: `process-${row.id}`, date: String(row.start_date), text: `${display(row.employee_name)} · ${display(row.process_type)}`, href: "/workspace/hr?section=processes&view=manager" })),
  ].filter((item) => item.date.slice(0, 10) <= today).sort((a, b) => b.date.localeCompare(a.date)).slice(0, 5);
  return <div className="row g-4 mb-4">
    <div className="col-12 col-xl-4"><div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><h3 className="h5">Employee Distribution</h3><p className="small text-body-secondary">By employment type</p>{ready[0] ? groups.size ? [...groups].map(([name, count]) => <div key={name} className="mb-3"><div className="d-flex justify-content-between small mb-1"><span>{name}</span><span>{count}</span></div><div className="progress" style={{ height: 8 }} role="progressbar" aria-label={name} aria-valuenow={count} aria-valuemin={0} aria-valuemax={employees.length}><div className="progress-bar" style={{ width: `${count / Math.max(1, employees.length) * 100}%` }} /></div></div>) : <p className="small text-body-secondary">No employees to show.</p> : <p className="small text-body-secondary">Employee data unavailable or loading.</p>}</div></div></div>
    <div className="col-12 col-xl-4"><div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><h3 className="h5">Leave Trends</h3><p className="small text-body-secondary">Requests by approval status</p>{ready[1] ? leaveGroups.size ? [...leaveGroups].map(([status, count]) => <div className="d-flex justify-content-between border-bottom py-2" key={status}><span className="text-capitalize">{status}</span><strong>{count}</strong></div>) : <p className="small text-body-secondary">No leave requests yet.</p> : <p className="small text-body-secondary">Leave data unavailable or loading.</p>}</div></div></div>
    <div className="col-12 col-xl-4"><div className="card border-0 shadow-sm h-100"><div className="card-body p-4"><h3 className="h5">Recent Activity</h3><p className="small text-body-secondary">Joining, leave start, and lifecycle dates</p>{activity.length ? activity.map((item) => <div className="border-bottom py-2" key={item.id}><Link href={item.href} className="small text-decoration-none">{item.text}</Link><div className="small text-body-secondary">{item.date}</div></div>) : <p className="small text-body-secondary">No accessible activity to show.</p>}</div></div></div>
  </div>;
}

export function turnover(employees: HrRecord[], start: string, end: string): number | null {
  const headcount = (date: string) => employees.filter((row) => row.joining_date && String(row.joining_date) <= date && (!row.termination_date || String(row.termination_date) > date)).length;
  const opening = employees.filter((row) => row.joining_date && String(row.joining_date) < start && (!row.termination_date || String(row.termination_date) >= start)).length;
  const average = (opening + headcount(end)) / 2;
  if (!average) return null;
  const departures = employees.filter((row) => row.termination_date && String(row.termination_date) >= start && String(row.termination_date) <= end).length;
  return departures / average * 100;
}

export function WorkforceTrend({ chart }: { chart: Array<{ month: string; count: number }> }) {
  const max = Math.max(1, ...chart.map((item) => item.count));
  const points = chart.map((item, index) => ({ ...item, x: 45 + index * 98, y: 160 - item.count / max * 125 }));
  return <svg viewBox="0 0 580 210" className="w-100" style={{ height: 210 }} role="img" aria-label={`Headcount chart: ${chart.map((item) => `${item.month}: ${item.count}`).join(", ")}`}>
    {[35, 97, 160].map((y) => <line key={y} x1="25" x2="560" y1={y} y2={y} stroke="var(--bs-border-color)" strokeDasharray="4 4" />)}
    <polyline points={points.map((point) => `${point.x},${point.y}`).join(" ")} fill="none" stroke="var(--bs-primary)" strokeWidth="3" />
    {points.map((point) => <g key={point.month}><circle cx={point.x} cy={point.y} r="5" fill="var(--bs-primary)" /><text x={point.x} y={point.y - 12} textAnchor="middle" fill="currentColor" fontSize="12">{point.count}</text><text x={point.x} y="193" textAnchor="middle" fill="currentColor" fontSize="12">{point.month}</text></g>)}
  </svg>;
}
