/* DatavionOS Revenue Cycle operational workspace presentation layer. */

"use client";

import Link from "next/link";
import { useMemo } from "react";

import { useBootstrap } from "@/core/bootstrap";
import { ModuleDataTable } from "../../data/module-data-table";
import type { ModuleRuntimeDefinition } from "../../domain/types";
import { FinanceManagerDashboard } from "./finance-manager-dashboard";

export type RevenueCycleOperationalModule =
  | "revenue_cycle"
  | "billing"
  | "charge_capture"
  | "coding"
  | "claims"
  | "eligibility"
  | "prior_authorization"
  | "denials"
  | "payment_posting"
  | "accounts_receivable"
  | "appeals"
  | "era"
  | "revenue_analytics";

export type RevenueCycleOperationalWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
  operationalModule: RevenueCycleOperationalModule;
}>;

type ModuleConfig = Readonly<{
  label: string;
  description: string;
  queue: string;
  kpis: readonly string[];
  actions: readonly string[];
}>;

const MODULE_CONFIG: Readonly<
  Record<RevenueCycleOperationalModule, ModuleConfig>
> = {
  revenue_cycle: {
    label: "Revenue Cycle",
    description:
      "Revenue-cycle operations, work queues, and financial controls for the active organization.",
    queue: "Revenue cycle work queue",
    kpis: ["Open financial work", "Claims requiring review", "Unresolved exceptions"],
    actions: ["Review revenue work queue", "Review claim exceptions"],
  },
  billing: {
    label: "Billing",
    description: "Invoice, charge and patient-balance operations.",
    queue: "Billing work queue",
    kpis: ["Open invoices", "Unbilled encounters", "Patient balance"],
    actions: ["Review billing queue", "Review invoices"],
  },
  charge_capture: {
    label: "Charge Capture",
    description: "Capture and reconcile billable clinical activity.",
    queue: "Charge capture queue",
    kpis: ["Pending charges", "Capture rate", "Exceptions"],
    actions: ["Review exceptions", "Review pending charges"],
  },
  coding: {
    label: "Coding",
    description: "Clinical and financial coding work queues.",
    queue: "Coding work queue",
    kpis: ["Pending coding", "Coding exceptions", "Ready to bill"],
    actions: ["Review coding queue", "Review exceptions"],
  },
  claims: {
    label: "Claims",
    description: "Prepare, scrub and submit claims through the canonical RCM domain.",
    queue: "Claims work queue",
    kpis: ["Draft claims", "Claims in review", "Submission exceptions"],
    actions: ["Review claims", "Review exceptions"],
  },
  eligibility: {
    label: "Eligibility",
    description: "Coverage and payer eligibility verification.",
    queue: "Eligibility queue",
    kpis: ["Pending checks", "Verified", "Exceptions"],
    actions: ["Review pending checks", "Review exceptions"],
  },
  prior_authorization: {
    label: "Prior Authorization",
    description: "Authorization request preparation and tracking.",
    queue: "Authorization queue",
    kpis: ["Pending requests", "Approved", "Expiring"],
    actions: ["Review requests", "Review expirations"],
  },
  denials: {
    label: "Denials",
    description: "Denial work queues, root causes and resolution workflows.",
    queue: "Denial queue",
    kpis: ["Open denials", "Appealable", "Resolved"],
    actions: ["Review denials", "Review root causes"],
  },
  payment_posting: {
    label: "Payment Posting",
    description: "Post and reconcile payer and patient payments.",
    queue: "Payment posting queue",
    kpis: ["Unposted payments", "Exceptions", "Posted today"],
    actions: ["Review payments", "Review exceptions"],
  },
  accounts_receivable: {
    label: "Accounts Receivable",
    description: "Organization-scoped AR work queues and aging.",
    queue: "AR work queue",
    kpis: ["Open AR", "30+ day AR", "90+ day AR"],
    actions: ["Review AR", "Review aging"],
  },
  appeals: {
    label: "Appeals",
    description: "Prepare and track payer appeal workflows.",
    queue: "Appeals queue",
    kpis: ["Open appeals", "Due soon", "Resolved"],
    actions: ["Review appeals", "Review due dates"],
  },
  era: {
    label: "ERA",
    description: "Electronic remittance advice processing and reconciliation.",
    queue: "ERA queue",
    kpis: ["Unprocessed ERA", "Exceptions", "Reconciled"],
    actions: ["Review ERA", "Review exceptions"],
  },
  revenue_analytics: {
    label: "Revenue Analytics",
    description: "Revenue-cycle performance and operational analytics.",
    queue: "Analytics workspace",
    kpis: ["Net collections", "Denial rate", "Days in AR"],
    actions: ["Open analytics", "Review trends"],
  },
};

const RCM_IDS = Object.keys(
  MODULE_CONFIG,
) as RevenueCycleOperationalModule[];

function normalize(value: string): string {
  return value.trim().toLowerCase().replace(/-/g, "_");
}

function titleCase(value: string): string {
  return value
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function moduleRoute(identifier: string): string {
  return `/workspace/${encodeURIComponent(identifier)}`;
}

export function RevenueCycleOperationalWorkspace({
  module,
  operationalModule,
}: RevenueCycleOperationalWorkspaceProps) {
  const { bootstrap } = useBootstrap();
  const config = MODULE_CONFIG[operationalModule];
  const enabledModules = useMemo(() => {
    if (!bootstrap) {
      return [];
    }

    return bootstrap.modules
      .filter((item) => {
        const id = normalize(item.identifier);
        return RCM_IDS.includes(
          id as RevenueCycleOperationalModule,
        );
      })
      .filter((item) => item.enabled)
      .sort((left, right) => left.order - right.order);
  }, [bootstrap]);

  if (operationalModule === "revenue_cycle") {
    return <FinanceManagerDashboard moduleName={module.displayName} />;
  }

  return (
    <section className="container-fluid py-3">
      <div className="d-flex flex-column flex-lg-row justify-content-between align-items-lg-start gap-3 mb-4">
        <div>
          <div className="small text-body-secondary text-uppercase fw-semibold">
            Revenue Cycle
          </div>
          <h1 className="h3 mb-1">{config.label}</h1>
          <p className="text-body-secondary mb-0">
            {config.description}
          </p>
        </div>

        <span className="badge text-bg-light border">
          {module.displayName}
        </span>
      </div>

      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body">
          <div className="d-flex flex-wrap align-items-center gap-2">
            <span className="small fw-semibold me-2">
              Revenue Cycle modules
            </span>

            {enabledModules.map((item) => (
              <Link
                key={item.identifier}
                href={moduleRoute(item.identifier)}
                className={`btn btn-sm ${
                  normalize(item.identifier) === operationalModule
                    ? "btn-primary"
                    : "btn-outline-secondary"
                }`}
              >
                {item.display_name || titleCase(item.identifier)}
              </Link>
            ))}
          </div>
        </div>
      </div>

      <div className="row g-3 mb-4">
        {config.kpis.map((kpi) => (
          <div className="col-12 col-md-4" key={kpi}>
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <div className="small text-body-secondary">
                  {kpi}
                </div>
                <div className="fs-4 fw-semibold mt-2">—</div>
                <div className="small text-body-secondary mt-1">
                  Live metric supplied by the backend domain/API.
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="row g-4">
        <div className="col-12 col-xl-8">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-body border-bottom">
              <h2 className="h6 mb-0">{config.queue}</h2>
            </div>

            <div className="card-body">
              <ModuleDataTable module={module} />
            </div>
          </div>
        </div>

        <div className="col-12 col-xl-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-body border-bottom">
              <h2 className="h6 mb-0">Quick actions</h2>
            </div>

            <div className="card-body d-flex flex-column gap-2">
              {config.actions.map((action) => (
                <button
                  type="button"
                  className="btn btn-outline-primary text-start"
                  key={action}
                  disabled
                  title="Action endpoint is owned by the backend module API."
                >
                  {action}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="alert alert-light border mt-4 mb-0">
        <strong>Backend-authoritative runtime.</strong>{" "}
        Entitlement, organization ON/OFF state, RBAC, tenant scope and
        department AI ownership are not decided by this component.
      </div>
    </section>
  );
}

export function resolveRevenueCycleOperationalModule(
  identifier: string,
): RevenueCycleOperationalModule | null {
  const normalized = normalize(identifier);

  return RCM_IDS.includes(
    normalized as RevenueCycleOperationalModule,
  )
    ? (normalized as RevenueCycleOperationalModule)
    : null;
}
