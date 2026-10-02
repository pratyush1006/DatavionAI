"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getPlatformBootstrap, type PlatformBootstrap } from "@/lib/backend/runtime";

export function DynamicDashboard() {
  const [bootstrap, setBootstrap] = useState<PlatformBootstrap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getPlatformBootstrap()
      .then(setBootstrap)
      .catch((value) => {
        setError(value instanceof Error ? value.message : "Workspace bootstrap failed.");
      })
      .finally(() => setLoading(false));
  }, []);

  const visibleModules = useMemo(
    () =>
      (bootstrap?.modules ?? [])
        .filter((module) => module.enabled)
        .sort((a, b) => a.order - b.order),
    [bootstrap],
  );

  const dashboardCards = useMemo(
    () =>
      (bootstrap?.dashboard ?? [])
        .slice()
        .sort((a, b) => a.order - b.order),
    [bootstrap],
  );

  const metrics = useMemo(() => {
    const totalModules = visibleModules.length;
    const totalCards = dashboardCards.length;
    const operatingPlan = bootstrap?.subscription?.plan?.name ?? "no plan";
    const organizationName = bootstrap?.organization?.name ?? bootstrap?.tenant?.name ?? "DatavionOS";

    return [
      { label: "Workspace", value: organizationName, hint: "Current runtime context" },
      { label: "Plan", value: operatingPlan, hint: "Active subscription" },
      { label: "Enabled modules", value: String(totalModules), hint: "Runtime entitlements" },
      { label: "Dashboard cards", value: String(totalCards), hint: "Runtime widgets" },
    ];
  }, [bootstrap, dashboardCards.length, visibleModules.length]);

  if (loading) {
    return (
      <main className="container-fluid py-4">
        <div className="placeholder-glow">
          <div className="placeholder col-4 mb-3" />
          <div className="placeholder col-8" />
        </div>
        <div className="row g-3 mt-1">
          {Array.from({ length: 6 }).map((_, index) => (
            <div className="col-12 col-md-6 col-xl-4" key={index}>
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <div className="placeholder-glow">
                    <div className="placeholder col-6 mb-2" />
                    <div className="placeholder col-9" />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    );
  }

  if (error || !bootstrap) {
    return (
      <main className="container-fluid py-4">
        <div className="alert alert-danger shadow-sm" role="alert">
          <h1 className="h5">Workspace unavailable</h1>
          <p className="mb-0">{error || "The platform bootstrap contract returned no workspace."}</p>
        </div>
      </main>
    );
  }

  const organizationName = bootstrap.organization?.name || bootstrap.tenant?.name || "DatavionOS";
  const planName = bootstrap.subscription?.plan?.name || "No active plan";
  const roles = bootstrap.organization_roles.length
    ? bootstrap.organization_roles.join(", ")
    : bootstrap.platform_roles.join(", ") || "No role assigned";

  return (
    <main className="container-fluid py-4">
      <div className="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3 mb-4">
        <div>
          <p className="text-body-secondary mb-1">DatavionOS workspace</p>
          <h1 className="h3 mb-1">{organizationName}</h1>
          <p className="text-body-secondary mb-0">
            {bootstrap.user.name || bootstrap.user.email} · {roles}
          </p>
        </div>
        <span className="badge text-bg-primary fs-6 px-3 py-2">{planName}</span>
      </div>

      <div className="row g-3 mb-4">
        {metrics.map((metric) => (
          <div className="col-12 col-md-6 col-xl-3" key={metric.label}>
            <div className="card shadow-sm h-100 border-0">
              <div className="card-body">
                <div className="small text-body-secondary">{metric.label}</div>
                <div className="fw-semibold fs-5 mt-2">{metric.value}</div>
                <div className="small text-body-secondary mt-1">{metric.hint}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {bootstrap.organization ? (
        <div className="row g-3 mb-4">
          <div className="col-12 col-md-4">
            <div className="card shadow-sm h-100">
              <div className="card-body">
                <div className="text-body-secondary small">Tenant</div>
                <div className="fw-semibold">{bootstrap.tenant?.name || organizationName}</div>
              </div>
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="card shadow-sm h-100">
              <div className="card-body">
                <div className="text-body-secondary small">Subscription</div>
                <div className="fw-semibold">{planName}</div>
                <div className="small text-body-secondary">{bootstrap.subscription?.status || "Not available"}</div>
              </div>
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="card shadow-sm h-100">
              <div className="card-body">
                <div className="text-body-secondary small">Enabled modules</div>
                <div className="display-6 fw-semibold">{visibleModules.length}</div>
              </div>
            </div>
          </div>
        </div>
      ) : null}

      {dashboardCards.length ? (
        <section className="mb-4">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h2 className="h5 mb-0">Workspace actions</h2>
          </div>
          <div className="row g-3">
            {dashboardCards.map((card) => (
              <div className="col-12 col-md-6 col-xl-4" key={card.key}>
                <Link href={card.route || "#"} className="card shadow-sm h-100 text-decoration-none">
                  <div className="card-body">
                    <div className="fw-semibold text-body">{card.title}</div>
                    <div className="small text-body-secondary mt-1">{card.description}</div>
                    <div className="mt-3 btn btn-outline-primary btn-sm">Open</div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </section>
      ) : null}

      <section>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h2 className="h5 mb-0">Enabled modules</h2>
          <span className="text-body-secondary small">Driven by subscription and organization entitlements</span>
        </div>
        <div className="row g-3">
          {visibleModules.length ? (
            visibleModules.map((module) => (
              <div className="col-12 col-md-6 col-xl-4" key={module.identifier}>
                <div className="card shadow-sm h-100">
                  <div className="card-body d-flex flex-column">
                    <div className="d-flex justify-content-between gap-3">
                      <h3 className="h6 mb-0">{module.display_name || module.name}</h3>
                      <span className="badge text-bg-success">Enabled</span>
                    </div>
                    <p className="small text-body-secondary mt-2 mb-3">
                      {module.description || "Available in your current workspace entitlement."}
                    </p>
                    <div className="mt-auto">
                      {module.route ? (
                        <Link href={module.route} className="btn btn-outline-primary btn-sm">
                          Open module
                        </Link>
                      ) : (
                        <span className="text-body-secondary small">No route configured</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-12">
              <div className="alert alert-secondary">No modules are currently enabled for this workspace.</div>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
