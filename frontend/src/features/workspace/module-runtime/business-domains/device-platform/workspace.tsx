import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";

export type DevicePlatformBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const DISCOVERED_DOMAINS = [
  "alerts",
  "api",
  "bluetooth",
  "consent",
  "events",
  "gateways",
  "integrations",
  "measurements",
  "models",
  "permissions",
  "selectors",
  "services",
  "telemetry",
  "workflows"
] as const;

export function DevicePlatformBusinessWorkspace({
  module,
}: DevicePlatformBusinessWorkspaceProps) {
  return (
    <section className="container-fluid py-3">
      <div className="row g-3 mb-3">
        <div className="col-12">
          <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
            <div>
              <div className="text-body-secondary small text-uppercase fw-semibold">
                Device Platform workspace
              </div>
              <h1 className="h3 mb-1">Device Platform</h1>
              <p className="text-body-secondary mb-0">
                Device capabilities exposed through the canonical Device Platform
                runtime contract.
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
              <div className="text-body-secondary small">Operational domains</div>
              <div className="fs-5 fw-semibold">{DISCOVERED_DOMAINS.length}</div>
              <div className="small text-body-secondary mt-1">
                Discovered from the audited backend boundary
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
                Workspace data remains backend-driven
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">Runtime authority</div>
              <div className="fs-6 fw-semibold">Backend Effective Context</div>
              <div className="small text-body-secondary mt-1">
                Frontend is projection-only
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
