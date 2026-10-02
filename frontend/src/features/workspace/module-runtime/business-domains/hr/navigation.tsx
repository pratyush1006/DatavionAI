"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Home, Users, Building2, Clock, CalendarDays, Target, ClipboardList, FileText, ChartColumn, Settings, Wallet, Star, type LucideIcon } from "lucide-react";
import { useBootstrap } from "@/core/bootstrap";
import { hrLink, isHrManager } from "./persona";

const items: Array<{ title: string; section?: string; route?: string; icon: LucideIcon; permission?: string }> = [
  { title: "Overview", section: "overview", icon: Home },
  { title: "Employees", section: "employees", icon: Users, permission: "employees.view" },
  { title: "Departments", route: "/settings/access", icon: Building2, permission: "departments.view" },
  { title: "Attendance", section: "attendance", icon: Clock, permission: "attendance.view" },
  { title: "Leave", section: "requests", icon: CalendarDays, permission: "leave.view" },
  { title: "Recruitment", section: "recruitment", icon: Target, permission: "recruitment.view" },
  { title: "Onboarding", section: "processes", icon: ClipboardList, permission: "onboarding.view" },
  { title: "Payroll", section: "payslips", icon: Wallet, permission: "payroll.view" },
  { title: "Performance", section: "reviews", icon: Star, permission: "performance.view" },
  { title: "Documents", route: "/documents", icon: FileText, permission: "documents.view" },
  { title: "Reports", section: "reports", icon: ChartColumn },
  { title: "HR Settings", section: "types", icon: Settings, permission: "leave.view" },
];

export function HrNavigation() {
  const { bootstrap } = useBootstrap();
  const params = useSearchParams();
  const section = params.get("section") ?? "overview";
  const manager = isHrManager(bootstrap?.organization_roles ?? [], params.get("view"));
  const can = (permission?: string) => !permission || bootstrap?.user.is_platform_admin || bootstrap?.permissions.includes("*") || bootstrap?.permissions.includes(permission);
  return <nav className="p-3" aria-label="HR navigation">
    <div className="small text-uppercase fw-semibold text-body-secondary px-3 mb-3" style={{ letterSpacing: ".08em" }}>Human resources</div>
    <div className="nav nav-pills flex-column gap-1">{items.filter((item) => can(item.permission)).map(({ title, section: target, route, icon: Icon }) => <Link key={title} className={`nav-link d-flex align-items-center gap-3 px-3 py-2 ${target === section ? "active" : "text-body"}`} href={route ?? hrLink(target ?? "overview", manager)} aria-current={target === section ? "page" : undefined}><Icon size={18} aria-hidden="true" />{manager && title === "Reports" ? "HR Analytics" : title}</Link>)}</div>
    <div className="border-top mt-4 pt-3 px-3 small text-body-secondary">Organization workspace<div className="fw-semibold text-body mt-1">{bootstrap?.organization?.name ?? "Select an organization"}</div></div>
  </nav>;
}
