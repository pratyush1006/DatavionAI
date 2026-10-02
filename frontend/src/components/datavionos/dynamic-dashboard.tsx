"use client";

import {
  Activity,
  Building2,
  Layers3,
  Puzzle,
  ShieldCheck,
} from "lucide-react";

import { useBootstrap } from "@/core/bootstrap";
import { DoctorDashboard } from "./doctor-dashboard";
import { OrganizationDashboard } from "./organization-dashboard";
import { NurseDashboard } from "./nurse-dashboard";

function displayName(user: {
  full_name?: string;
  first_name?: string;
  last_name?: string;
}): string {
  const name = user.full_name?.trim() || [user.first_name, user.last_name]
    .filter(Boolean)
    .join(" ")
    .trim();

  return name || "there";
}

function greetingForCurrentHour(): string {
  const hour = new Date().getHours();

  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

export function DynamicDashboard() {
  const {
    bootstrap,
    isLoading,
    isFetching,
    isError,
    error,
    refetch,
  } = useBootstrap();

  if (isLoading && !bootstrap) {
    return (
      <main className="container-fluid py-4" aria-busy="true">
        <div className="placeholder-glow mb-4">
          <span className="placeholder col-4 d-block mb-3" />
          <span className="placeholder col-7 d-block" />
        </div>
        <div className="row g-3 mb-4">
          {Array.from({ length: 4 }, (_, index) => (
            <div className="col-12 col-sm-6 col-xl-3" key={index}>
              <div className="card border-0 shadow-sm h-100">
                <div className="card-body placeholder-glow">
                  <span className="placeholder col-6 d-block mb-3" />
                  <span className="placeholder col-9 d-block" />
                </div>
              </div>
            </div>
          ))}
        </div>
        <p className="small text-body-secondary">Preparing your workspace…</p>
      </main>
    );
  }

  if (!bootstrap) {
    return (
      <main className="container-fluid py-4">
        <div className="alert alert-danger d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3" role="alert">
          <div>
            <h1 className="h5 mb-1">Workspace unavailable</h1>
            <p className="mb-0">
              {error?.message ?? "Your organization workspace could not be loaded."}
            </p>
          </div>
          <button
            type="button"
            className="btn btn-outline-danger flex-shrink-0"
            onClick={() => void refetch()}
          >
            Try again
          </button>
        </div>
      </main>
    );
  }

  if (bootstrap.organization_roles.some((role) => /doctor|consultant/i.test(role))) {
    return <DoctorDashboard />;
  }

  if (bootstrap.organization_roles.some((role) => /nurse/i.test(role))) {
    return <NurseDashboard />;
  }

  if (bootstrap.organization_roles.some((role) => /organization admin|organization_admin|organization owner|organization_owner/i.test(role))) {
    return <OrganizationDashboard />;
  }

  const organizationName =
    bootstrap.organization?.name || bootstrap.tenant?.name || "DatavionOS";
  const roles = bootstrap.organization_roles.length
    ? bootstrap.organization_roles
    : bootstrap.platform_roles;
  const planName = bootstrap.subscription?.plan.name ?? "No active plan";
  const enabledModules = bootstrap.modules
    .filter((module) => module.enabled)
    .slice()
    .sort((left, right) => left.order - right.order);
  const workspaceRoutes = bootstrap.navigation.filter(
    (item) => item.route && item.route !== "/dashboard",
  );
  const activeFeatureCount = Object.values(bootstrap.feature_flags)
    .filter(Boolean)
    .length;
  const organizationProfile = [
    bootstrap.organization?.name || bootstrap.tenant?.name,
    bootstrap.organization?.category,
    bootstrap.organization?.organization_type,
    bootstrap.organization?.size,
  ]
    .filter(Boolean)
    .map((value) => String(value).replace(/[_-]+/g, " "))
    .join(" · ");
  const kpis = [
    {
      label: "Enabled modules",
      value: enabledModules.length,
      detail: "Provisioned by your subscription",
      icon: Puzzle,
      tone: "primary",
    },
    {
      label: "Available workspaces",
      value: workspaceRoutes.length,
      detail: "Allowed by your current role",
      icon: Activity,
      tone: "success",
    },
    {
      label: "Active capabilities",
      value: activeFeatureCount,
      detail: "Resolved by the backend",
      icon: Layers3,
      tone: "info",
    },
    {
      label: "Access permissions",
      value: bootstrap.permissions.length,
      detail: "Effective permissions in this workspace",
      icon: ShieldCheck,
      tone: "secondary",
    },
  ] as const;

  return (
    <main className="container-fluid py-4 py-lg-5">
      <header className="d-flex flex-column flex-lg-row justify-content-between align-items-lg-start gap-3 mb-4 mb-lg-5">
        <div>
          <div className="small text-uppercase fw-semibold text-primary mb-2" style={{ letterSpacing: ".08em" }}>
            DatavionOS workspace
          </div>
          <h1 className="h2 fw-bold mb-2">
            {greetingForCurrentHour()}, {displayName(bootstrap.user)}
          </h1>
          <p className="text-body-secondary mb-0">
            {organizationProfile || "Your workspace is tailored to your organization, subscription, and access role."}
          </p>
        </div>
        {isFetching ? (
          <span className="badge rounded-pill text-bg-light border text-body-secondary px-3 py-2">
            Updating workspace…
          </span>
        ) : null}
      </header>

      <section className="mb-4 mb-lg-5" aria-labelledby="workspace-kpis-heading">
        <div className="d-flex flex-wrap justify-content-between align-items-end gap-2 mb-3">
          <div>
            <h2 className="h4 fw-bold mb-1" id="workspace-kpis-heading">Workspace KPIs</h2>
            <p className="small text-body-secondary mb-0">Live access and capability metrics for your enabled modules.</p>
          </div>
          <span className="small text-body-secondary">Updates when your workspace access changes</span>
        </div>
        <div className="row g-3">
          {kpis.map((kpi) => {
            const Icon = kpi.icon;
            return (
              <div className="col-12 col-sm-6 col-xl-3" key={kpi.label}>
                <article className="card border-0 shadow-sm h-100">
                  <div className="card-body p-4">
                    <div className={`rounded-3 bg-${kpi.tone}-subtle text-${kpi.tone} d-inline-flex p-2 mb-3`}>
                      <Icon size={19} aria-hidden="true" />
                    </div>
                    <div className="small text-body-secondary">{kpi.label}</div>
                    <div className="fs-3 fw-semibold mt-1">{kpi.value}</div>
                    <div className="small text-body-secondary mt-1">{kpi.detail}</div>
                  </div>
                </article>
              </div>
            );
          })}
        </div>

      </section>

      <section className="row g-3 mb-4 mb-lg-5" aria-label="Workspace summary">
        <div className="col-12 col-md-6 col-xl-4">
          <article className="card border-0 shadow-sm h-100">
            <div className="card-body d-flex align-items-start gap-3 p-4">
              <span className="rounded-3 bg-primary-subtle text-primary p-3">
                <Building2 size={20} aria-hidden="true" />
              </span>
              <div className="min-w-0">
                <div className="small text-body-secondary">Organization</div>
                <div className="fw-semibold text-truncate mt-1">{organizationName}</div>
                <div className="small text-body-secondary mt-1">
                  {bootstrap.tenant?.name ? `Tenant · ${bootstrap.tenant.name}` : "Current workspace"}
                </div>
              </div>
            </div>
          </article>
        </div>

        <div className="col-12 col-md-6 col-xl-4">
          <article className="card border-0 shadow-sm h-100">
            <div className="card-body d-flex align-items-start gap-3 p-4">
              <span className="rounded-3 bg-success-subtle text-success p-3">
                <Layers3 size={20} aria-hidden="true" />
              </span>
              <div className="min-w-0">
                <div className="small text-body-secondary">Subscription plan</div>
                <div className="fw-semibold mt-1">{planName}</div>
                <div className="small text-body-secondary mt-1">
                  {bootstrap.subscription?.status ?? "Plan status unavailable"}
                  {bootstrap.subscription?.plan.billing_cycle
                    ? ` · ${bootstrap.subscription.plan.billing_cycle}`
                    : ""}
                </div>
              </div>
            </div>
          </article>
        </div>

        <div className="col-12 col-md-6 col-xl-4">
          <article className="card border-0 shadow-sm h-100">
            <div className="card-body d-flex align-items-start gap-3 p-4">
              <span className="rounded-3 bg-info-subtle text-info-emphasis p-3">
                <ShieldCheck size={20} aria-hidden="true" />
              </span>
              <div className="min-w-0">
                <div className="small text-body-secondary">Your access</div>
                {roles.length ? (
                  <div className="d-flex flex-wrap gap-2 mt-2">
                    {roles.slice(0, 3).map((role) => (
                      <span className="badge rounded-pill text-bg-light border" key={role}>
                        {role.replace(/[_-]+/g, " ")}
                      </span>
                    ))}
                    {roles.length > 3 ? (
                      <span className="badge rounded-pill text-bg-light border">+{roles.length - 3}</span>
                    ) : null}
                  </div>
                ) : (
                  <div className="small text-body-secondary mt-1">No role assigned</div>
                )}
              </div>
            </div>
          </article>
        </div>
      </section>

      {isError ? (
        <div className="alert alert-warning" role="status">
          Workspace refresh failed. Showing the last successfully loaded access context.
        </div>
      ) : null}

    </main>
  );
}
