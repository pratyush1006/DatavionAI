import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";
import type { EncountersAiBoundary } from "./types";

export type EncountersBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const encountersAiBoundary: EncountersAiBoundary = {
  department: "encounters",
  owner: "encounters",
  enabledByOrganization: false,
};

export function EncountersBusinessWorkspace({
  module,
}: EncountersBusinessWorkspaceProps) {
  return (
    <section className="container-fluid py-3">
      <div className="row g-3 mb-3">
        <div className="col-12">
          <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
            <div>
              <div className="text-body-secondary small text-uppercase fw-semibold">
                Encounters workspace
              </div>
              <h1 className="h3 mb-1">Encounters</h1>
              <p className="text-body-secondary mb-0">
                Clinical encounter records exposed through the canonical
                Encounters API contract.
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
              <div className="fs-5 fw-semibold">Encounters</div>
              <div className="small text-body-secondary mt-1">
                Dynamic Bootstrap clinical module
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
              <div className="text-body-secondary small">Encounters AI</div>
              <div className="fs-6 fw-semibold">Department-scoped</div>
              <div className="small text-body-secondary mt-1">
                Backend-controlled capability boundary
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
              <h2 className="h6 mb-1">Encounters AI</h2>
              <p className="small text-body-secondary mb-0">
                AI availability is controlled by backend effective capability
                context and organization configuration. This workspace does
                not grant or infer access.
              </p>
            </div>
            <span className="badge text-bg-secondary">
              {encountersAiBoundary.department}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
