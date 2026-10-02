"use client";

import Link from "next/link";
import {
  ArrowLeft,
  Box,
  ExternalLink,
} from "lucide-react";
import { useMemo } from "react";

import { useBootstrap } from "@/core/bootstrap";
import { createModuleRuntimeDefinition } from "@/features/workspace/module-runtime/registry";
import { resolveBusinessRenderer } from "@/features/workspace/module-runtime/renderers";
import {
  RevenueCycleOperationalWorkspace,
  resolveRevenueCycleOperationalModule,
} from "@/features/workspace/module-runtime/business-domains/revenue-cycle/operational";

type DynamicModuleWorkspaceProps = Readonly<{
  moduleIdentifier: string;
}>;

function normalize(value: string): string {
  return value.trim().toLowerCase();
}

export function DynamicModuleWorkspace({
  moduleIdentifier,
}: DynamicModuleWorkspaceProps) {
  const {
    bootstrap,
    isLoading,
    isFetching,
    isError,
    error,
    refetch,
  } = useBootstrap();

  const runtimeModule = useMemo(() => {
    if (!bootstrap) {
      return null;
    }

    const requested = normalize(moduleIdentifier);

    return (
      bootstrap.modules.find(
        (item) =>
          normalize(item.identifier) === requested ||
          normalize(item.route).replace(/^\/+/, "") === requested ||
          normalize(item.route)
            .replace(/^\/+/, "")
            .startsWith(`${requested}/`),
      ) ?? null
    );
  }, [bootstrap, moduleIdentifier]);

  const moduleDefinition = useMemo(
    () => runtimeModule ? createModuleRuntimeDefinition(runtimeModule) : null,
    [runtimeModule],
  );

  const BusinessWorkspace = useMemo(
    () => moduleDefinition ? resolveBusinessRenderer(moduleDefinition) : null,
    [moduleDefinition],
  );

  const operationalModule = useMemo(
    () => resolveRevenueCycleOperationalModule(moduleIdentifier),
    [moduleIdentifier],
  );

  if (isLoading && !bootstrap) {
    return (
      <section className="container-fluid py-4" aria-busy="true">
        <div className="row g-4">
          <div className="col-12">
            <div className="placeholder-glow">
              <span className="placeholder col-6 rounded" />
              <span className="placeholder col-4 rounded mt-2 d-block" />
            </div>
          </div>

          <div className="col-12 col-xl-8">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <span className="placeholder col-12 rounded" />
                <span className="placeholder col-10 rounded mt-2 d-block" />
                <span className="placeholder col-8 rounded mt-2 d-block" />
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (isError && !bootstrap) {
    return (
      <section className="container-fluid py-4">
        <div className="alert alert-danger d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
          <div>
            <h1 className="h5 mb-1">Workspace unavailable</h1>
            <p className="mb-0">
              {error?.message ??
                "The workspace bootstrap could not be loaded."}
            </p>
          </div>

          <button
            type="button"
            className="btn btn-outline-danger"
            onClick={() => void refetch()}
          >
            Try again
          </button>
        </div>
      </section>
    );
  }

  if (!runtimeModule) {
    return (
      <section className="container-fluid py-4">
        <div className="card border-0 shadow-sm">
          <div className="card-body p-4 p-lg-5">
            <div className="d-flex align-items-start gap-3">
              <div className="rounded-3 bg-body-secondary p-3">
                <Box size={24} aria-hidden="true" />
              </div>

              <div>
                <h1 className="h4 mb-2">Module unavailable</h1>
                <p className="text-body-secondary mb-0">
                  This workspace is not present in the current backend
                  bootstrap context.
                </p>
              </div>
            </div>

            <div className="mt-4">
              <Link
                href="/dashboard"
                className="btn btn-primary"
              >
                <ArrowLeft
                  size={16}
                  className="me-2"
                  aria-hidden="true"
                />
                Return to dashboard
              </Link>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (operationalModule) {
    return (
      <RevenueCycleOperationalWorkspace
        module={runtimeModule as never}
        operationalModule={operationalModule}
      />
    );
  }

  if (BusinessWorkspace && moduleDefinition) {
    return <BusinessWorkspace module={moduleDefinition} />;
  }

  return (
    <section className="container-fluid py-1">
      <div className="d-flex flex-column flex-lg-row justify-content-between align-items-lg-start gap-3 mb-4">
        <div className="min-w-0">
          <div className="d-flex align-items-center gap-2 text-body-secondary small mb-2">
            <Box size={15} aria-hidden="true" />
            <span>{runtimeModule.category || "Workspace"}</span>
            {isFetching ? <span>Updating…</span> : null}
          </div>

          <h1 className="display-6 fw-semibold mb-2">
            {runtimeModule.display_name || runtimeModule.name}
          </h1>

          <p className="lead text-body-secondary mb-0">
            {runtimeModule.description ||
              "Operational workspace provided by the active DatavionOS capability context."}
          </p>
        </div>

        <div className="d-flex gap-2 flex-shrink-0">
          <Link
            href="/dashboard"
            className="btn btn-outline-secondary"
          >
            <ArrowLeft
              size={16}
              className="me-2"
              aria-hidden="true"
            />
            Dashboard
          </Link>

          {runtimeModule.route ? (
            <Link
              href={runtimeModule.route}
              className="btn btn-primary"
            >
              Open module
              <ExternalLink
                size={16}
                className="ms-2"
                aria-hidden="true"
              />
            </Link>
          ) : null}
        </div>
      </div>

      <div className="row g-4">
        <div className="col-12 col-xl-8">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-body border-bottom py-3">
              <h2 className="h6 mb-0">
                Module workspace
              </h2>
            </div>

            <div className="card-body p-4">
              <div className="row g-3">
                <div className="col-12 col-md-6">
                  <div className="border rounded-3 p-3 h-100">
                    <div className="small text-body-secondary mb-1">
                      Module
                    </div>
                    <div className="fw-semibold">
                      {runtimeModule.identifier}
                    </div>
                  </div>
                </div>

                <div className="col-12 col-md-6">
                  <div className="border rounded-3 p-3 h-100">
                    <div className="small text-body-secondary mb-1">
                      Version
                    </div>
                    <div className="fw-semibold">
                      {runtimeModule.version || "Current"}
                    </div>
                  </div>
                </div>

                <div className="col-12 col-md-6">
                  <div className="border rounded-3 p-3 h-100">
                    <div className="small text-body-secondary mb-1">
                      API prefix
                    </div>
                    <div className="fw-semibold text-break">
                      {runtimeModule.api_prefix ||
                        "Managed by module runtime"}
                    </div>
                  </div>
                </div>

                <div className="col-12 col-md-6">
                  <div className="border rounded-3 p-3 h-100">
                    <div className="small text-body-secondary mb-1">
                      Scope
                    </div>
                    <div className="fw-semibold">
                      {runtimeModule.tenant_scoped
                        ? "Organization scoped"
                        : "Platform scoped"}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-xl-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-body border-bottom py-3">
              <h2 className="h6 mb-0">
                Module context
              </h2>
            </div>

            <div className="card-body">
              <dl className="row mb-0 small">
                <dt className="col-5 text-body-secondary">
                  Status
                </dt>
                <dd className="col-7 text-end">
                  <span className="badge text-bg-success">
                    Available
                  </span>
                </dd>

                <dt className="col-5 text-body-secondary mt-3">
                  Category
                </dt>
                <dd className="col-7 text-end mt-3">
                  {runtimeModule.category || "Workspace"}
                </dd>

                <dt className="col-5 text-body-secondary mt-3">
                  System
                </dt>
                <dd className="col-7 text-end mt-3">
                  {runtimeModule.system
                    ? "System module"
                    : "Organization module"}
                </dd>
              </dl>

              {runtimeModule.tags?.length ? (
                <div className="border-top mt-4 pt-4">
                  <div className="small text-body-secondary mb-2">
                    Tags
                  </div>

                  <div className="d-flex flex-wrap gap-2">
                    {runtimeModule.tags.map((tag) => (
                      <span
                        className="badge rounded-pill text-bg-light border"
                        key={tag}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </div>

      <div className="alert alert-light border mt-4 mb-0">
        <strong>Backend-authoritative workspace.</strong>{" "}
        This screen renders the active bootstrap context. SaaS entitlement,
        organization enablement, department scope and RBAC remain enforced
        by DatavionOS backend services.
      </div>
    </section>
  );
}
