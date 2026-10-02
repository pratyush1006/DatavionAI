
"use client";

import type {
  ModuleAction,
  ModuleKpi,
  ModuleTable,
  ModuleUIComposition,
} from "./types";

type ModuleBusinessProfile = Readonly<{
  sections?: ModuleUIComposition["sections"];
  actions?: ModuleAction[];
  kpis?: ModuleKpi[];
  filters?: ModuleUIComposition["filters"];
  table?: ModuleTable;
}>;

const BUSINESS_PROFILES: Readonly<Record<string, ModuleBusinessProfile>> = {
  patients: {
    actions: [
      { id: "patients:new", label: "New patient", href: "/patients/new", variant: "primary" },
      { id: "patients:search", label: "Search patients", href: "/patients", variant: "secondary" },
    ],
    kpis: [
      { id: "patients:total", label: "Total patients", value: "—", description: "Current patient population" },
      { id: "patients:active", label: "Active patients", value: "—", description: "Patients with active care" },
      { id: "patients:new", label: "New this period", value: "—", description: "Newly registered patients" },
    ],
    filters: [
      { id: "patients:search", label: "Patient search", placeholder: "Name, patient ID, phone" },
      { id: "patients:status", label: "Status", placeholder: "All patient statuses" },
    ],
    table: {
      columns: [
        { id: "patient", label: "Patient" },
        { id: "status", label: "Status" },
        { id: "updated", label: "Updated" },
      ],
      emptyMessage: "No patient records are available for this workspace.",
    },
  },

  appointments: {
    actions: [
      { id: "appointments:new", label: "New appointment", href: "/clinical/appointments", variant: "primary" },
      { id: "appointments:schedule", label: "Open schedule", href: "/clinical/appointments", variant: "secondary" },
    ],
    kpis: [
      { id: "appointments:today", label: "Today's appointments", value: "—", description: "Appointments scheduled today" },
      { id: "appointments:upcoming", label: "Upcoming", value: "—", description: "Future scheduled appointments" },
      { id: "appointments:pending", label: "Pending", value: "—", description: "Appointments requiring attention" },
    ],
    filters: [
      { id: "appointments:date", label: "Date", placeholder: "Select appointment date" },
      { id: "appointments:status", label: "Status", placeholder: "All appointment statuses" },
    ],
    table: {
      columns: [
        { id: "patient", label: "Patient" },
        { id: "provider", label: "Provider" },
        { id: "time", label: "Time" },
        { id: "status", label: "Status" },
      ],
      emptyMessage: "No appointments are available for the selected period.",
    },
  },

  pharmacy: {
    actions: [
      { id: "pharmacy:dispense", label: "New dispensing", href: "/pharmacy/dispensing", variant: "primary" },
      { id: "pharmacy:inventory", label: "Open inventory", href: "/pharmacy/inventory", variant: "secondary" },
    ],
    kpis: [
      { id: "pharmacy:inventory", label: "Inventory items", value: "—", description: "Items currently tracked" },
      { id: "pharmacy:low-stock", label: "Low stock", value: "—", description: "Items below configured threshold" },
      { id: "pharmacy:dispensing", label: "Dispensing activity", value: "—", description: "Recent dispensing activity" },
    ],
    filters: [
      { id: "pharmacy:search", label: "Medication search", placeholder: "Medicine, SKU, batch" },
      { id: "pharmacy:stock", label: "Stock status", placeholder: "All stock statuses" },
    ],
    table: {
      columns: [
        { id: "medicine", label: "Medicine" },
        { id: "stock", label: "Stock" },
        { id: "expiry", label: "Expiry" },
        { id: "status", label: "Status" },
      ],
      emptyMessage: "No pharmacy inventory records are available.",
    },
  },

  laboratory: {
    actions: [
      { id: "laboratory:order", label: "New lab order", href: "/laboratory/orders", variant: "primary" },
      { id: "laboratory:results", label: "Review results", href: "/laboratory/results", variant: "secondary" },
    ],
    kpis: [
      { id: "laboratory:orders", label: "Open orders", value: "—", description: "Laboratory orders in progress" },
      { id: "laboratory:pending", label: "Pending results", value: "—", description: "Results awaiting completion" },
      { id: "laboratory:completed", label: "Completed", value: "—", description: "Completed laboratory work" },
    ],
    filters: [
      { id: "laboratory:search", label: "Order search", placeholder: "Order ID, patient, test" },
      { id: "laboratory:status", label: "Order status", placeholder: "All laboratory statuses" },
    ],
    table: {
      columns: [
        { id: "order", label: "Order" },
        { id: "patient", label: "Patient" },
        { id: "test", label: "Test" },
        { id: "status", label: "Status" },
      ],
      emptyMessage: "No laboratory orders are available.",
    },
  },

  documents: {
    actions: [
      { id: "documents:new", label: "New document", href: "/documents/new", variant: "primary" },
      { id: "documents:open", label: "Browse documents", href: "/documents", variant: "secondary" },
    ],
    kpis: [
      { id: "documents:total", label: "Documents", value: "—", description: "Documents available in scope" },
      { id: "documents:recent", label: "Recently updated", value: "—", description: "Documents updated recently" },
      { id: "documents:pending", label: "Pending", value: "—", description: "Documents requiring attention" },
    ],
    filters: [
      { id: "documents:search", label: "Document search", placeholder: "Name, type, identifier" },
      { id: "documents:type", label: "Document type", placeholder: "All document types" },
    ],
    table: {
      columns: [
        { id: "document", label: "Document" },
        { id: "type", label: "Type" },
        { id: "updated", label: "Updated" },
        { id: "status", label: "Status" },
      ],
      emptyMessage: "No documents are available in the current scope.",
    },
  },

  billing: {
    actions: [
      { id: "billing:charges", label: "Review charges", href: "/billing/charges", variant: "primary" },
      { id: "billing:claims", label: "Open claims", href: "/billing/claims", variant: "secondary" },
    ],
    kpis: [
      { id: "billing:charges", label: "Charges", value: "—", description: "Charges captured in scope" },
      { id: "billing:claims", label: "Claims", value: "—", description: "Claims in the current workflow" },
      { id: "billing:exceptions", label: "Exceptions", value: "—", description: "Billing exceptions requiring review" },
    ],
    filters: [
      { id: "billing:search", label: "Billing search", placeholder: "Patient, claim, charge" },
      { id: "billing:status", label: "Workflow status", placeholder: "All billing statuses" },
    ],
    table: {
      columns: [
        { id: "reference", label: "Reference" },
        { id: "patient", label: "Patient" },
        { id: "amount", label: "Amount" },
        { id: "status", label: "Status" },
      ],
      emptyMessage: "No billing records are available in the current scope.",
    },
  },
};

function buildDefaultSections(): ModuleUIComposition["sections"] {
  return [
    { id: "overview", title: "Overview", description: "Module overview and current workspace state.", kind: "overview" },
    { id: "kpis", title: "Key metrics", description: "Runtime metrics for this module.", kind: "kpis" },
    { id: "actions", title: "Actions", description: "Available workspace actions.", kind: "actions" },
    { id: "filters", title: "Filters", description: "Workspace filtering controls.", kind: "filters" },
    { id: "content", title: "Workspace data", description: "Primary module content.", kind: "content" },
    { id: "activity", title: "Activity", description: "Recent activity for this module.", kind: "activity" },
    { id: "ai", title: "AI capabilities", description: "AI experiences supplied by the module.", kind: "ai" },
  ];
}

function buildDefaultActions(moduleIdentifier: string): ModuleAction[] {
  return [
    {
      id: `${moduleIdentifier}:primary-action`,
      label: "Open workspace",
      variant: "primary",
    },
  ];
}

function buildDefaultKpis(): ModuleKpi[] {
  return [
    { id: "records", label: "Records", value: "—", description: "Current module records" },
    { id: "activity", label: "Activity", value: "—", description: "Recent module activity" },
    { id: "status", label: "Status", value: "Ready", description: "Workspace runtime status" },
  ];
}

function buildDefaultFilters(): ModuleUIComposition["filters"] {
  return [
    { id: "search", label: "Search", placeholder: "Search this workspace" },
  ];
}

export function composeModuleUI(
  module: ModuleUIComposition["module"],
): ModuleUIComposition {
  const profile = BUSINESS_PROFILES[module.identifier] ?? {};

  return {
    module,
    sections: profile.sections ?? buildDefaultSections(),
    actions: profile.actions ?? buildDefaultActions(module.identifier),
    kpis: profile.kpis ?? buildDefaultKpis(),
    filters: profile.filters ?? buildDefaultFilters(),
    table: profile.table,
  };
}
