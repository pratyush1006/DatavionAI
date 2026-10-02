"use client";

import Link from "next/link";

import { useDatavionRuntime } from "../../core/runtime/runtime-provider";
import { DATAVION_RUNTIME_MODULES } from "../../core/runtime/runtime-module-registry";

export function BackendDrivenDashboard() {
  const runtime = useDatavionRuntime();
  const effective = runtime.effective;

  if (runtime.loading) {
    return (
      <div className="container py-4">
        <div className="alert alert-secondary">
          Loading DatavionOS runtime context...
        </div>
      </div>
    );
  }

  if (!runtime.authenticated || !effective) {
    return (
      <div className="container py-4">
        <div className="alert alert-warning">
          Runtime context is not available.
        </div>
      </div>
    );
  }

  const visibleModules = DATAVION_RUNTIME_MODULES.filter(
    (module) => effective.modules[module.key] === true,
  );

  const visibleRoles = effective.roles;
  const visiblePermissions = effective.permissions;
  const visibleDepartments = effective.departments;

  return (
    <main className="container py-4">
      <div className="mb-4">
        <h1 className="h3 mb-1">DatavionOS Dashboard</h1>
        <p className="text-muted mb-0">
          Dashboard capabilities are supplied by the backend effective context.
        </p>
      </div>

      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card h-100">
            <div className="card-body">
              <div className="text-muted small">Modules</div>
              <div className="display-6">
                {visibleModules.length}
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card h-100">
            <div className="card-body">
              <div className="text-muted small">Roles</div>
              <div className="display-6">
                {visibleRoles.length}
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card h-100">
            <div className="card-body">
              <div className="text-muted small">Permissions</div>
              <div className="display-6">
                {visiblePermissions.length}
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card h-100">
            <div className="card-body">
              <div className="text-muted small">Departments</div>
              <div className="display-6">
                {visibleDepartments.length}
              </div>
            </div>
          </div>
        </div>
      </div>

      <section>
        <h2 className="h5 mb-3">Available Modules</h2>

        <div className="row g-3">
          {visibleModules.map((module) => (
            <div
              className="col-md-4 col-lg-3"
              key={module.key}
            >
              <div className="card h-100">
                <div className="card-body d-flex flex-column">
                  <h3 className="h6">{module.label}</h3>

                  <p className="small text-muted flex-grow-1">
                    Enabled by the backend effective capability context.
                  </p>

                  <Link
                    href={module.path}
                    className="btn btn-primary btn-sm"
                  >
                    Open
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
