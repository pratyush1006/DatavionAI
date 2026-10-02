import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";

export type AppointmentsBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

export function AppointmentsBusinessWorkspace({
  module,
}: AppointmentsBusinessWorkspaceProps) {
  return (
    <section className="container-fluid py-3">
      <div className="row g-3 mb-3">
        <div className="col-12">
          <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
            <div>
              <div className="text-body-secondary small text-uppercase fw-semibold">
                Clinical workspace
              </div>
              <h1 className="h3 mb-1">Appointments</h1>
              <p className="text-body-secondary mb-0">
                Appointment records exposed by the organization&apos;s
                canonical Appointments API contract.
              </p>
            </div>
            <span className="badge text-bg-light border">
              {module.displayName}
            </span>
          </div>
        </div>
      </div>

      <div className="row g-3 mb-3">
        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">Workspace</div>
              <div className="fs-5 fw-semibold">Appointments</div>
              <div className="small text-body-secondary mt-1">
                Dynamic Bootstrap module
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">Data source</div>
              <div className="fs-6 fw-semibold">Canonical API adapter</div>
              <div className="small text-body-secondary mt-1">
                Read-only workspace data
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">Authority</div>
              <div className="fs-6 fw-semibold">Backend + Bootstrap</div>
              <div className="small text-body-secondary mt-1">
                No frontend entitlement decisions
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <ModuleDataTable module={module} />
        </div>
      </div>
    </section>
  );
}
