"use client";

import { useState } from "react";

import { ModuleDataTable } from "../../data/module-data-table";
import type { ModuleTable } from "../../composition/types";
import type { ModuleRuntimeDefinition } from "../../domain/types";

type InsuranceWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const INSURANCE_COLLECTIONS = [
  {
    id: "payers",
    label: "Payers",
    route: "/insurance/payers/",
    columns: [
      { id: "payer_code", label: "Payer code" },
      { id: "display_name", label: "Payer" },
      { id: "payer_type", label: "Type" },
      { id: "active", label: "Active" },
    ],
  },
  {
    id: "tpas",
    label: "TPAs",
    route: "/insurance/tpas/",
    columns: [
      { id: "tpa_code", label: "TPA code" },
      { id: "display_name", label: "Administrator" },
      { id: "tpa_type", label: "Type" },
      { id: "active", label: "Active" },
    ],
  },
  {
    id: "plans",
    label: "Plans",
    route: "/insurance/plans/",
    columns: [
      { id: "plan_code", label: "Plan code" },
      { id: "name", label: "Plan" },
      { id: "insurance_type", label: "Insurance type" },
      { id: "is_active", label: "Active" },
    ],
  },
  {
    id: "products",
    label: "Products",
    route: "/insurance/products/",
    columns: [
      { id: "product_code", label: "Product code" },
      { id: "name", label: "Product" },
      { id: "plan", label: "Plan" },
      { id: "is_active", label: "Active" },
    ],
  },
  {
    id: "networks",
    label: "Networks",
    route: "/insurance/networks/",
    columns: [
      { id: "network_code", label: "Network code" },
      { id: "name", label: "Network" },
      { id: "network_type", label: "Type" },
      { id: "is_active", label: "Active" },
    ],
  },
  {
    id: "subscribers",
    label: "Subscribers",
    route: "/insurance/subscribers/",
    columns: [
      { id: "subscriber_identifier", label: "Subscriber ID" },
      { id: "patient", label: "Patient" },
      { id: "relationship_to_patient", label: "Relationship" },
      { id: "employer_name", label: "Employer" },
    ],
  },
  {
    id: "enrollments",
    label: "Enrollments",
    route: "/insurance/enrollments/",
    columns: [
      { id: "member_id", label: "Member ID" },
      { id: "policy_number", label: "Policy number" },
      { id: "status", label: "Coverage status" },
      { id: "effective_date", label: "Effective date" },
    ],
  },
  {
    id: "benefits",
    label: "Benefits",
    route: "/insurance/benefits/",
    columns: [
      { id: "category", label: "Category" },
      { id: "service_type", label: "Service" },
      { id: "coverage_percent", label: "Coverage %" },
      { id: "authorization_required", label: "Authorization required" },
    ],
  },
  {
    id: "cob",
    label: "Coordination of benefits",
    route: "/insurance/cob/",
    columns: [
      { id: "enrollment", label: "Enrollment" },
      { id: "coordination_order", label: "Order" },
      { id: "responsibility", label: "Responsibility" },
      { id: "verification_status", label: "Verification" },
    ],
  },
  {
    id: "verification-requests",
    label: "Verification requests",
    route: "/revenue-cycle/insurance_verification/",
    columns: [
      { id: "request_reference", label: "Encounter / request" },
      { id: "payer_name", label: "Payer" },
      { id: "member_id", label: "Member ID" },
      { id: "status", label: "Workflow status" },
      { id: "outcome", label: "Coverage outcome" },
      { id: "response_message", label: "Latest note" },
    ],
  },
  {
    id: "coding-queue",
    label: "Coding queue",
    route: "/revenue-cycle/coding/",
    columns: [
      { id: "source_reference", label: "Encounter" },
      { id: "coding_type", label: "Coding type" },
      { id: "service_date", label: "Service date" },
      { id: "status", label: "Coding status" },
      { id: "clinical_summary", label: "Clinical summary" },
    ],
  },
  {
    id: "claim-submissions",
    label: "Claim submissions",
    route: "/revenue-cycle/claim_submission/submissions/",
    columns: [
      { id: "claim_reference", label: "Claim reference" },
      { id: "payer_name", label: "Payer" },
      { id: "status", label: "Submission status" },
      { id: "external_submission_id", label: "Payer reference" },
      { id: "rejection_reason", label: "Latest issue" },
    ],
  },
] as const;

function tableForCollection(
  collection: (typeof INSURANCE_COLLECTIONS)[number],
): ModuleTable {
  return {
    columns: collection.columns,
    emptyMessage: `No ${collection.label.toLowerCase()} records are available for this organization.`,
  };
}

export function InsuranceBusinessWorkspace({
  module,
}: InsuranceWorkspaceProps) {
  const [activeCollectionId, setActiveCollectionId] = useState("payers");
  const activeCollection = INSURANCE_COLLECTIONS.find(
    (collection) => collection.id === activeCollectionId,
  ) ?? INSURANCE_COLLECTIONS[0];

  return (
    <section className="container-fluid py-3">
      <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
        <div>
          <div className="text-body-secondary small text-uppercase fw-semibold">
            Insurance operations
          </div>
          <h1 className="h3 mb-1">Insurance</h1>
          <p className="text-body-secondary mb-0">
            Browse payer, plan, member and benefit records for your organization.
          </p>
        </div>
        <span className="badge text-bg-light border">{module.displayName}</span>
      </div>

      <div className="card shadow-sm">
        <div className="card-header bg-body">
          <div className="fw-semibold">Insurance records</div>
        </div>
        <div className="card-body">
          <div className="d-flex flex-wrap gap-2 mb-4" role="tablist" aria-label="Insurance record types">
            {INSURANCE_COLLECTIONS.map((collection) => (
              <button
                key={collection.id}
                type="button"
                role="tab"
                aria-selected={activeCollection.id === collection.id}
                className={`btn btn-sm rounded-pill ${activeCollection.id === collection.id ? "btn-primary" : "btn-outline-secondary"}`}
                onClick={() => setActiveCollectionId(collection.id)}
              >
                {collection.label}
              </button>
            ))}
          </div>
          <ModuleDataTable
            key={activeCollection.id}
            module={module}
            route={activeCollection.route}
            table={tableForCollection(activeCollection)}
          />
        </div>
      </div>
    </section>
  );
}
