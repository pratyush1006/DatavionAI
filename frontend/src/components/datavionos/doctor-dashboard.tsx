"use client";

import { useQuery } from "@tanstack/react-query";
import { CalendarDays, Users, Stethoscope } from "lucide-react";
import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";

type Overview = { my_patients: number; today_appointments: number; upcoming_appointments: number; schedule: Array<{ id: string; time: string; patient_name: string; status: string }> };
async function load(): Promise<Overview> { return (await apiClient.get<Overview>("/platform/doctor-overview/")).data; }

export function DoctorDashboard() {
  const { bootstrap } = useBootstrap();
  const query = useQuery({ queryKey: ["doctor-overview"], queryFn: load });
  const name = bootstrap?.user.full_name || [bootstrap?.user.first_name, bootstrap?.user.last_name].filter(Boolean).join(" ") || "Doctor";
  const data = query.data;
  const cards = [["My patients", data?.my_patients ?? "—", Users], ["Today", data?.today_appointments ?? "—", CalendarDays], ["Upcoming", data?.upcoming_appointments ?? "—", Stethoscope]] as const;
  return <main className="container-fluid py-4 py-lg-5"><header className="mb-5"><div className="small text-uppercase fw-semibold text-primary mb-2">Clinical workspace</div><h1 className="h2 fw-bold mb-2">Good morning, {name}</h1><p className="text-body-secondary mb-0">Your provider-scoped patients, schedule, and clinical workload.</p></header>{query.isError ? <div className="alert alert-warning">Your provider overview could not be loaded.</div> : null}<section className="row g-3 mb-4">{cards.map(([label, value, Icon]) => <div className="col-12 col-sm-6 col-xl-4" key={label}><article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><Icon className="text-primary mb-3" size={22}/><div className="small text-body-secondary">{label}</div><div className="fs-3 fw-bold">{value}</div></div></article></div>)}</section><section className="card border-0 shadow-sm"><div className="card-body p-4"><h2 className="h5">Today&apos;s appointments</h2><div className="vstack gap-2 mt-3">{data?.schedule.map((item) => <div className="d-flex justify-content-between border-bottom pb-2" key={item.id}><span>{new Date(item.time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} · {item.patient_name}</span><span className="text-body-secondary text-capitalize">{item.status}</span></div>)}{!data?.schedule.length ? <span className="text-body-secondary">No appointments scheduled today.</span> : null}</div></div></section></main>;
}
