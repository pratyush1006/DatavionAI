"use client";

import { Activity, BellRing, ClipboardList, HeartPulse, Users } from "lucide-react";
import { useBootstrap } from "@/core/bootstrap";

function greeting(): string {
  const hour = new Date().getHours();
  return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
}

export function NurseDashboard() {
  const { bootstrap } = useBootstrap();
  const name = bootstrap?.user.full_name || [bootstrap?.user.first_name, bootstrap?.user.last_name].filter(Boolean).join(" ") || "Nurse";
  const scope = bootstrap?.access_context;
  const cards = [
    ["Assigned departments", scope?.department_ids.length ?? 0, "Current nursing scope", Users],
    ["Teams", scope?.team_ids.length ?? 0, "Active team memberships", Activity],
    ["Care tasks", "—", "Task queue integration pending", ClipboardList],
    ["Clinical alerts", "—", "Alerts appear when assigned", BellRing],
  ] as const;

  return <main className="container-fluid py-4 py-lg-5">
    <header className="mb-4 mb-lg-5">
      <div className="small text-uppercase fw-semibold text-primary mb-2">Nursing workspace</div>
      <h1 className="h2 fw-bold mb-2">{greeting()}, {name}</h1>
      <p className="text-body-secondary mb-0">Your department and team-scoped patient-care workspace.</p>
    </header>
    <section className="row g-3 mb-4" aria-label="Nursing workload summary">
      {cards.map(([label, value, detail, Icon]) => <div className="col-12 col-sm-6 col-xl-3" key={label}><article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><Icon className="text-primary mb-3" size={22} aria-hidden="true"/><div className="small text-body-secondary">{label}</div><div className="fs-3 fw-bold mt-1">{value}</div><div className="small text-body-secondary mt-1">{detail}</div></div></article></div>)}
    </section>
    <section className="row g-3">
      <div className="col-12 col-xl-7"><article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex align-items-center gap-2"><HeartPulse className="text-danger" size={20}/><h2 className="h5 mb-0">Patient care</h2></div><p className="text-body-secondary mt-3 mb-0">No patient-care workload is currently assigned to this nurse. Assigned patients, vitals, medication administration, and care-plan tasks will appear here when their backend workflows are enabled.</p></div></article></div>
      <div className="col-12 col-xl-5"><article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><h2 className="h5">Nursing tasks</h2><p className="text-body-secondary mt-3 mb-0">No scheduled nursing tasks are available. This panel only displays backend-assigned work; it does not fabricate clinical tasks.</p></div></article></div>
    </section>
  </main>;
}
