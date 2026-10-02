"use client";

import type {
  ModuleRenderer,
  ModuleRendererProps,
} from "./domain/types";

import { composeModuleUI } from "./composition";

import {
  ModuleActionsSection,
  ModuleActivitySection,
  ModuleAISection,
  ModuleContentSection,
  ModuleFiltersSection,
  ModuleKpiSection,
  ModuleOverviewSection,
} from "./composition";

import { ModuleDataTable } from "./data";
import type { ModuleRuntimeDefinition } from "./domain/types";
import { PatientsBusinessWorkspace } from "./business-domains/patients";
import { InsuranceBusinessWorkspace } from "./business-domains/insurance";
import { HrBusinessWorkspace } from "./business-domains/hr/workspace";
import { PharmacyBusinessWorkspace } from "./business-domains/pharmacy";
import { LaboratoryBusinessWorkspace } from "./business-domains/laboratory";
import { ImagingBusinessWorkspace } from "./business-domains/imaging";
import { HospitalOperationsBusinessWorkspace } from "./business-domains/hospital-operations";
import { InventoryBusinessWorkspace } from "./business-domains/inventory";
import { DepartmentManagerWorkspace } from "./business-domains/department-manager";

function WorkspaceFrame({
  module,
  children,
}: ModuleRendererProps & {
  children: React.ReactNode;
}) {
  return (
    <section className="container-fluid py-4">
      <div className="mb-4">
        <div className="d-flex flex-wrap align-items-center justify-content-between gap-3">
          <div>
            <span className="badge text-bg-light border mb-2">
              {module.category}
            </span>

            <h1 className="h3 mb-1">
              {module.displayName}
            </h1>

            {module.description ? (
              <p className="text-body-secondary mb-0">
                {module.description}
              </p>
            ) : null}
          </div>

          {module.department ? (
            <span className="badge text-bg-primary">
              {module.department}
            </span>
          ) : null}
        </div>
      </div>

      {children}
    </section>
  );
}

type ComposedModuleWorkspaceProps =
  ModuleRendererProps & {
    content?: React.ReactNode;
    children?: React.ReactNode;
  };

function ComposedModuleWorkspace({
  module,
  content,
  children,
}: ComposedModuleWorkspaceProps) {
  const composition = composeModuleUI(module);

  return (
    <WorkspaceFrame module={module}>
      <div className="d-flex flex-column gap-4">
        <ModuleOverviewSection
          composition={composition}
        />

        <ModuleKpiSection
          composition={composition}
        />

        <div className="card border-0 shadow-sm">
          <div className="card-body p-4">
            <h2 className="h6 mb-3">
              Workspace actions
            </h2>

            <ModuleActionsSection
              composition={composition}
            />
          </div>
        </div>

        <div>
          <h2 className="h6 mb-3">
            Filters
          </h2>

          <ModuleFiltersSection
            composition={composition}
          />
        </div>

        <div>
          <h2 className="h6 mb-3">
            Workspace data
          </h2>

          {composition.table ? (
            <div className="card border-0 shadow-sm">
              <div className="card-body p-4">
                <ModuleDataTable
                  module={module}
                  table={composition.table}
                />
              </div>
            </div>
          ) : (
            <ModuleContentSection>
              {content ?? children}
            </ModuleContentSection>
          )}
        </div>

        <ModuleActivitySection
          composition={composition}
        />

        <ModuleAISection
          composition={composition}
        />
      </div>
    </WorkspaceFrame>
  );
}

export function GenericModuleRenderer({
  module,
}: ModuleRendererProps) {
  return (
    <ComposedModuleWorkspace
      module={module}
    />
  );
}

export function DashboardModuleRenderer({
  module,
}: ModuleRendererProps) {
  return (
    <ComposedModuleWorkspace
      module={module}
    >
      <div className="row g-3">
        {[
          "Overview",
          "Activity",
          "Performance",
        ].map((title) => (
          <div
            className="col-12 col-md-6 col-xl-4"
            key={title}
          >
            <div className="border rounded-3 p-3 h-100">
              <div className="small text-body-secondary">
                {title}
              </div>

              <div className="display-6 fw-semibold mt-2">
                —
              </div>
            </div>
          </div>
        ))}
      </div>
    </ComposedModuleWorkspace>
  );
}

export function TableModuleRenderer({
  module,
}: ModuleRendererProps) {
  return (
    <ComposedModuleWorkspace
      module={module}
    >
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th scope="col">Record</th>
              <th scope="col">Status</th>
              <th scope="col">Updated</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td
                colSpan={3}
                className="text-center py-5"
              >
                <span className="text-body-secondary">
                  Module data will be supplied by the module API.
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </ComposedModuleWorkspace>
  );
}

export function DetailModuleRenderer({
  module,
}: ModuleRendererProps) {
  return (
    <ComposedModuleWorkspace
      module={module}
    >
      <div className="row g-4">
        <div className="col-12 col-md-6">
          <div className="small text-body-secondary">
            Module identifier
          </div>

          <div className="fw-semibold mt-1">
            {module.identifier}
          </div>
        </div>

        <div className="col-12 col-md-6">
          <div className="small text-body-secondary">
            API prefix
          </div>

          <div className="fw-semibold mt-1">
            {module.apiPrefix || "—"}
          </div>
        </div>
      </div>
    </ComposedModuleWorkspace>
  );
}

export function WorkflowModuleRenderer({
  module,
}: ModuleRendererProps) {
  return (
    <ComposedModuleWorkspace
      module={module}
    >
      <div className="d-flex flex-column gap-3">
        {[
          "Workspace initialized",
          "Module available",
          "Ready for workflow UI",
        ].map((step, index) => (
          <div
            className="d-flex align-items-center gap-3"
            key={step}
          >
            <div
              className="rounded-circle border d-flex align-items-center justify-content-center"
              style={{
                width: 32,
                height: 32,
              }}
            >
              {index + 1}
            </div>

            <span>{step}</span>
          </div>
        ))}
      </div>
    </ComposedModuleWorkspace>
  );
}

export const MODULE_RENDERERS: Readonly<
  Record<string, ModuleRenderer>
> = {
  generic: GenericModuleRenderer,
  dashboard: DashboardModuleRenderer,
  table: TableModuleRenderer,
  detail: DetailModuleRenderer,
  workflow: WorkflowModuleRenderer,
};

export function resolveModuleRenderer(
  rendererKey: string,
): ModuleRenderer {
  return (
    MODULE_RENDERERS[rendererKey] ??
    GenericModuleRenderer
  );
}

export function resolveBusinessRenderer(module: ModuleRuntimeDefinition) {
  const identifier = module.identifier.toLowerCase();
  const haystack = `${identifier} ${module.apiPrefix}`.toLowerCase();

  if (identifier === "hr") {
    return HrBusinessWorkspace;
  }

  if (identifier === "insurance") {
    return InsuranceBusinessWorkspace;
  }

  if (identifier === "pharmacy" || haystack.includes("pharmacy")) {
    return PharmacyBusinessWorkspace;
  }

  if (
    identifier === "laboratory" ||
    identifier === "laboratories" ||
    haystack.includes("laborator")
  ) {
    return LaboratoryBusinessWorkspace;
  }

  if (identifier === "imaging" || haystack.includes("imaging")) {
    return ImagingBusinessWorkspace;
  }

  if (identifier === "inventory" || haystack.includes("inventory")) {
    return InventoryBusinessWorkspace;
  }

  if (identifier === "departments" || identifier === "department-manager") {
    return DepartmentManagerWorkspace;
  }

  if (
    identifier === "hospital-operations" ||
    identifier === "hospital_operations" ||
    haystack.includes("hospital-operations")
  ) {
    return HospitalOperationsBusinessWorkspace;
  }

  if (haystack.includes("patient")) {
    return PatientsBusinessWorkspace;
  }

  return null;
}
