"use client";

import type React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Bell, CircleHelp, Search } from "lucide-react";

interface DashboardShellProps {
  children: React.ReactNode;
}

import { useAuth } from "@/core/auth";

import {
  DynamicNavigation,
} from "./dynamic-navigation";
import { TenantSwitcher } from "./tenant-switcher";
import { useBootstrap } from "@/core/bootstrap";
import { HrNavigation } from "@/features/workspace/module-runtime/business-domains/hr/navigation";

export function DashboardShell({
  children,
}: DashboardShellProps) {
  const { user, logout } = useAuth();
  const { bootstrap } = useBootstrap();
  const isHrWorkspace = usePathname() === "/workspace/hr";
  const router = useRouter();

  const displayName =
    bootstrap?.user.full_name?.trim() ||
    [
      bootstrap?.user.first_name ?? user?.first_name,
      bootstrap?.user.last_name ?? user?.last_name,
    ]
      .filter(Boolean)
      .join(" ")
      .trim() ||
    "User";

  return (
    <div className="min-vh-100 bg-body-tertiary">
      <header className="navbar bg-body border-bottom shadow-sm sticky-top">
        <div className="container-fluid px-3 px-lg-4 gap-3">
          <Link
            className="navbar-brand fw-bold"
            href="/dashboard"
          >
            DatavionOS
          </Link>

          <div className="d-none d-lg-flex flex-grow-1 justify-content-center">
            <form className="position-relative w-100" style={{ maxWidth: "34rem" }} onSubmit={(event) => {
              event.preventDefault();
              if (isHrWorkspace) {
                const search = new FormData(event.currentTarget).get("search");
                const view = new URLSearchParams(window.location.search).get("view");
                router.push(`/workspace/hr?section=employees&search=${encodeURIComponent(String(search ?? ""))}${view ? `&view=${encodeURIComponent(view)}` : ""}`);
              }
            }}>
              <label className="visually-hidden" htmlFor="workspace-search">{isHrWorkspace ? "Search employees" : "Global search"}</label>
              <Search className="position-absolute top-50 translate-middle-y text-body-secondary" style={{ left: ".75rem" }} size={17} aria-hidden="true" />
              <input id="workspace-search" name="search" className="form-control ps-5" type="search" placeholder={isHrWorkspace ? "Search employees, departments…" : "Global search…"} />
            </form>
          </div>

          <div className="d-flex align-items-center gap-2 gap-lg-3">
            <TenantSwitcher />
            {bootstrap?.organization?.name ? (
              <span className="d-none d-md-inline text-body-secondary">
                {bootstrap.organization.name}
              </span>
            ) : null}
            <button type="button" className="btn btn-light btn-sm d-none d-md-inline-flex align-items-center gap-1" title="Alerts are delivered through the notification service.">
              <Bell size={17} aria-hidden="true" /> <span className="d-none d-xl-inline">Alerts</span>
            </button>
            <button type="button" className="btn btn-light btn-sm d-none d-xl-inline-flex align-items-center gap-1" title="Help center integration is not configured.">
              <CircleHelp size={17} aria-hidden="true" /> Help
            </button>
            <span className="text-body-secondary text-truncate" style={{ maxWidth: "10rem" }}>
              {displayName}
            </span>

            <button
              type="button"
              className="btn btn-outline-secondary btn-sm"
              onClick={() => void logout()}
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="container-fluid">
        <div className="row">
          <aside className="col-12 col-lg-2 border-end bg-body min-vh-100 p-0">
            {isHrWorkspace ? <HrNavigation /> : <DynamicNavigation />}
          </aside>

          <main className="col-12 col-lg-10 p-4">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
