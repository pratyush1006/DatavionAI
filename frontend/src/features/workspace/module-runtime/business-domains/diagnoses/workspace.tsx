import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";
import type { DiagnosesAiBoundary } from "./types";

export type DiagnosesBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const diagnosesAiBoundary: DiagnosesAiBoundary = {
  department: "diagnoses",
  owner: "diagnoses",
  enabledByOrganization: false,
};

export function DiagnosesBusinessWorkspace({
  module,
}: DiagnosesBusinessWorkspaceProps) {
  return (
    <section className="container-fluid py-3">
      <div className="row g-3 mb-3">
        <div className="col-12">
          <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
            <div>
              <div className="text-body-secondary small text-uppercase fw-semibold">
                Diagnoses workspace
              </div>
              <h1 className="h3 mb-1">Diagnoses</h1>
              <p className="text-body-secondary mb-0">
                Diagnosis records exposed by the canonical Diagnoses API contract.
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
              <div className="fs-5 fw-semibold">Diagnoses</div>
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
              <div className="text-body-secondary small">Diagnoses AI</div>
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
              <h2 className="h6 mb-1">Diagnoses AI</h2>
              <p className="small text-body-secondary mb-0">
                AI availability is controlled by the backend effective
                capability context and organization configuration. This
                workspace does not grant or infer access.
              </p>
            </div>
            <span className="badge text-bg-secondary">
              {diagnosesAiBoundary.department}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
