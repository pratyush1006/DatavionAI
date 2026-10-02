import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";
import type { RevenueCycleAiBoundary } from "./types";

export type RevenueCycleBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const revenueCycleAiBoundary: RevenueCycleAiBoundary = {
  department: "revenue_cycle",
  owner: "revenue_cycle",
  enabledByOrganization: false,
};

export function RevenueCycleBusinessWorkspace({
  module,
}: RevenueCycleBusinessWorkspaceProps) {
  return (
    <section className="container-fluid py-3">
      <div className="row g-3 mb-3">
        <div className="col-12">
          <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
            <div>
              <div className="text-body-secondary small text-uppercase fw-semibold">
                Revenue cycle workspace
              </div>
              <h1 className="h3 mb-1">Revenue Cycle</h1>
              <p className="text-body-secondary mb-0">
                Revenue-cycle operations exposed through the canonical
                backend and API contracts.
              </p>
            </div>

            <span className="badge text-bg-light border">
              {module.displayName}
            </span>
          </div>
        </div>
      </div>

      <div className="row g-3 mb-3">
        <div className="col-12 col-md-3">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">
                Charge Capture
              </div>
              <div className="fs-6 fw-semibold">Operational</div>
              <div className="small text-body-secondary mt-1">
                Revenue-cycle workflow
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-3">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">
                Claims
              </div>
              <div className="fs-6 fw-semibold">Operational</div>
              <div className="small text-body-secondary mt-1">
                Canonical RCM domain
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-3">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">
                Billing
              </div>
              <div className="fs-6 fw-semibold">Operational</div>
              <div className="small text-body-secondary mt-1">
                Canonical finance boundary
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-3">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">
                RCM AI
              </div>
              <div className="fs-6 fw-semibold">Department-scoped</div>
              <div className="small text-body-secondary mt-1">
                Backend-controlled capability
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

      <div className="card shadow-sm mt-3 border-start border-4">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-start gap-3">
            <div>
              <h2 className="h6 mb-1">Revenue Cycle AI</h2>
              <p className="small text-body-secondary mb-0">
                AI availability is controlled by backend effective capability
                context and organization configuration. This workspace does
                not grant or infer access.
              </p>
            </div>

            <span className="badge text-bg-secondary">
              {revenueCycleAiBoundary.department}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
