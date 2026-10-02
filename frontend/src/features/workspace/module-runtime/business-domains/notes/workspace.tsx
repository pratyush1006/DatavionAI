import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";

export type NotesWorkspaceProps = {
  module: ModuleRuntimeDefinition;
};

export function NotesWorkspace({ module }: NotesWorkspaceProps) {
  return (
    <section className="container-fluid py-3" data-domain="notes">
      <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
        <div>
          <h1 className="h4 mb-1">Notes</h1>
          <p className="text-body-secondary mb-0">
            Clinical notes, templates, versions, amendments, and finalization workflows.
          </p>
        </div>
        <span className="badge text-bg-light border">Clinical Documentation</span>
      </div>
      <ModuleDataTable module={module} />
    </section>
  );
}
