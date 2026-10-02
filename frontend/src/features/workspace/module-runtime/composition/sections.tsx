
"use client";

import type { ReactNode } from "react";
import type {
  ModuleAction,
  ModuleFilter,
  ModuleKpi,
  ModuleUIComposition,
} from "./types";

type SectionProps = Readonly<{
  composition: ModuleUIComposition;
}>;

export function ModuleOverviewSection({
  composition,
}: SectionProps) {
  const { module } = composition;

  return (
    <div className="card border-0 shadow-sm">
      <div className="card-body p-4">
        <div className="d-flex flex-wrap justify-content-between gap-3">
          <div>
            <div className="small text-body-secondary">
              Module
            </div>

            <div className="fw-semibold mt-1">
              {module.displayName}
            </div>
          </div>

          <div>
            <div className="small text-body-secondary">
              Category
            </div>

            <div className="fw-semibold mt-1">
              {module.category}
            </div>
          </div>

          <div>
            <div className="small text-body-secondary">
              Workspace
            </div>

            <div className="fw-semibold mt-1 text-capitalize">
              {module.workspaceType}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function ModuleKpiSection({
  composition,
}: SectionProps) {
  return (
    <div className="row g-3">
      {composition.kpis.map((kpi: ModuleKpi) => (
        <div
          className="col-12 col-md-6 col-xl-4"
          key={kpi.id}
        >
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body p-4">
              <div className="small text-body-secondary">
                {kpi.label}
              </div>

              <div className="display-6 fw-semibold mt-2">
                {kpi.value}
              </div>

              {kpi.description ? (
                <div className="small text-body-secondary mt-2">
                  {kpi.description}
                </div>
              ) : null}

              {kpi.trend ? (
                <div className="small mt-2">
                  {kpi.trend}
                </div>
              ) : null}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export function ModuleActionsSection({
  composition,
}: SectionProps) {
  return (
    <div className="d-flex flex-wrap gap-2">
      {composition.actions.map((action: ModuleAction) => (
        <button
          className={`btn btn-${action.variant ?? "primary"}`}
          key={action.id}
          type="button"
        >
          {action.label}
        </button>
      ))}
    </div>
  );
}

export function ModuleFiltersSection({
  composition,
}: SectionProps) {
  return (
    <div className="card border-0 shadow-sm">
      <div className="card-body p-4">
        <div className="row g-3">
          {composition.filters.map(
            (filter: ModuleFilter) => (
              <div
                className="col-12 col-lg-6"
                key={filter.id}
              >
                <label
                  className="form-label"
                  htmlFor={`module-filter-${filter.id}`}
                >
                  {filter.label}
                </label>

                <input
                  className="form-control"
                  id={`module-filter-${filter.id}`}
                  placeholder={filter.placeholder}
                  type="search"
                />
              </div>
            ),
          )}
        </div>
      </div>
    </div>
  );
}

export function ModuleBusinessTableSection({
  composition,
}: SectionProps) {
  const table = composition.table;

  if (!table) {
    return null;
  }

  return (
    <div className="table-responsive">
      <table className="table table-hover align-middle mb-0">
        <thead>
          <tr>
            {table.columns.map((column) => (
              <th scope="col" key={column.id}>
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td
              colSpan={table.columns.length}
              className="text-center py-5"
            >
              <span className="text-body-secondary">
                {table.emptyMessage}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export function ModuleContentSection({
  children,
}: Readonly<{
  children?: ReactNode;
}>) {
  return (
    <div className="card border-0 shadow-sm">
      <div className="card-body p-4">
        {children ?? (
          <div className="text-body-secondary">
            Module content will be supplied by the module runtime.
          </div>
        )}
      </div>
    </div>
  );
}

export function ModuleActivitySection({
  composition,
}: SectionProps) {
  return (
    <div className="card border-0 shadow-sm">
      <div className="card-body p-4">
        <h2 className="h6 mb-3">
          {composition.sections.find(
            (section) => section.kind === "activity",
          )?.title ?? "Activity"}
        </h2>

        <div className="text-body-secondary">
          No activity has been supplied by this module yet.
        </div>
      </div>
    </div>
  );
}

export function ModuleAISection({
  composition,
}: SectionProps) {
  return (
    <div className="card border-0 shadow-sm">
      <div className="card-body p-4">
        <div className="d-flex align-items-start gap-3">
          <div
            className="rounded-circle border d-flex align-items-center justify-content-center"
            style={{
              width: 40,
              height: 40,
              flexShrink: 0,
            }}
          >
            AI
          </div>

          <div>
            <h2 className="h6 mb-1">
              AI capabilities
            </h2>

            <p className="text-body-secondary mb-0">
              AI experiences for this workspace are supplied
              by the backend module capability contract.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
