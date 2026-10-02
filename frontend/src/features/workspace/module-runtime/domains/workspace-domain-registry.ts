import type {
  BootstrapModule,
} from "@/core/bootstrap/types";
import type {
  ModuleRuntimeDefinition,
} from "../domain/types";
import type {
  DomainApiContract,
} from "../api/domain-types";
import type {
  DomainWorkspaceBinding,
  DomainWorkspaceDefinition,
  DomainWorkspaceContract,
  DomainWorkspaceResolutionInput,
} from "./workspace-domain-types";

export const DOMAIN_WORKSPACE_DEFINITIONS:
  readonly DomainWorkspaceDefinition[] = [
  {
    id: "patients",
    label: "Patients",
    aliases: ["patient", "patients"],
  },
  {
    id: "appointments",
    label: "Appointments",
    aliases: ["appointment", "appointments"],
  },
  {
    id: "pharmacy",
    label: "Pharmacy",
    aliases: ["pharmacy", "pharmacies", "prescription", "prescriptions", "medication", "medications"],
  },
  {
    id: "laboratory",
    label: "Laboratory",
    aliases: ["laboratory", "laboratories", "lab", "labs", "pathology"],
  },
  {
    id: "documents",
    label: "Documents",
    aliases: ["document", "documents", "storage"],
  },
  {
    id: "billing",
    label: "Billing",
    aliases: ["billing", "revenue-cycle", "revenue_cycle", "rcm", "charge", "charges", "claim", "claims", "payment", "payments"],
  },
];

type BoundDomainApiContract = DomainApiContract & Readonly<{
  domain:
    | "patients"
    | "appointments"
    | "pharmacy"
    | "laboratory"
    | "documents"
    | "billing";
}>;

const DOMAIN_API_CONTRACTS:
  readonly BoundDomainApiContract[] = [
    {
      domain: "patients",
      identifier: "patient-accounts",
      prefix: "/patient-accounts",
      group: "patient-accounts",
      routes: ["patient-accounts/", "patient-accounts/<uuid:account_id>/responsibilities/", "patient-accounts/<uuid:pk>/", "patient-accounts/<uuid:pk>/transition/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\billing\\\\\\\\patient_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patient-guarantors",
      prefix: "/patient-guarantors",
      group: "patient-guarantors",
      routes: ["patient-guarantors/", "patient-guarantors/<uuid:pk>/", "patient-guarantors/<uuid:pk>/restore/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\billing\\\\\\\\patient_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patient-management",
      prefix: "/patient-management",
      group: "patient-management",
      routes: ["api/patient-management/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patient-management-addresses",
      prefix: "/patient-management/addresses",
      group: "patient-management",
      routes: ["api/patient-management/addresses/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patient-responsibilities",
      prefix: "/patient-responsibilities",
      group: "patient-responsibilities",
      routes: ["patient-responsibilities/<uuid:pk>/", "patient-responsibilities/<uuid:pk>/restore/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\billing\\\\\\\\patient_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patient-statements",
      prefix: "/patient-statements",
      group: "patient-statements",
      routes: ["patient-statements/", "patient-statements/<uuid:pk>/issue/", "patient-statements/<uuid:pk>/void/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\billing\\\\\\\\patient_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patient-statements-generate",
      prefix: "/patient-statements/generate",
      group: "patient-statements",
      routes: ["patient-statements/generate/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\billing\\\\\\\\patient_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "patients",
      identifier: "patients",
      prefix: "/patients",
      group: "patients",
      routes: ["patients/", "patients/<uuid:patient_id>/devices/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\patient_management\\\\\\\\api\\\\\\\\urls.py", "backend\\\\\\\\apps\\\\\\\\patient_management\\\\\\\\urls.py", "backend\\\\\\\\apps\\\\\\\\device_platform\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 20,
    },
    {
      domain: "appointments",
      identifier: "appointments",
      prefix: "/appointments",
      group: "appointments",
      routes: ["api/appointments/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "pharmacy",
      identifier: "clinical-prescriptions-draft",
      prefix: "/clinical/prescriptions/draft",
      group: "clinical",
      routes: ["clinical/prescriptions/draft/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\ai\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "pharmacy",
      identifier: "medications",
      prefix: "/medications",
      group: "medications",
      routes: ["api/medications/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "pharmacy",
      identifier: "pharmacy",
      prefix: "/pharmacy",
      group: "pharmacy",
      routes: ["api/pharmacy/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "pharmacy",
      identifier: "prescriptions",
      prefix: "/prescriptions",
      group: "prescriptions",
      routes: ["api/prescriptions/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "laboratory",
      identifier: "clinical-lab-orders-status",
      prefix: "/clinical/lab-orders/status",
      group: "clinical",
      routes: ["clinical/lab-orders/status/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\ai\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "laboratory",
      identifier: "laboratories",
      prefix: "/laboratories",
      group: "laboratory",
      routes: ["api/laboratories/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 23,
    },
    {
      domain: "documents",
      identifier: "documents",
      prefix: "/documents",
      group: "documents",
      routes: ["api/documents/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "billing",
      identifier: "account-auto-charge",
      prefix: "/account/auto-charge",
      group: "account",
      routes: ["account/auto-charge/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\platform\\\\\\\\saas_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "account-payment-provider",
      prefix: "/account/payment-provider",
      group: "account",
      routes: ["account/payment-provider/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\platform\\\\\\\\saas_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "admissions",
      prefix: "/admissions",
      group: "admissions",
      routes: ["admissions/", "admissions/<uuid:admission_id>/discharge/", "admissions/<uuid:admission_id>/transfer/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\hospital_operations\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "medium",
      evidenceScore: 3,
    },
    {
      domain: "billing",
      identifier: "billing",
      prefix: "/billing",
      group: "billing",
      routes: ["api/billing/", "billing/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "charge_capture",
      prefix: "/charge_capture",
      group: "charge_capture",
      routes: ["charge_capture/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "charges",
      prefix: "/charges",
      group: "charges",
      routes: ["charges/", "charges/<uuid:charge_id>/", "charges/<uuid:charge_id>/transition/", "charges/<uuid:charge_id>/void/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\charge_capture\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 20,
    },
    {
      domain: "billing",
      identifier: "claim_scrubbing",
      prefix: "/claim_scrubbing",
      group: "claim_scrubbing",
      routes: ["claim_scrubbing/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "claim_submission",
      prefix: "/claim_submission",
      group: "claim_submission",
      routes: ["claim_submission/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "payment_posting",
      prefix: "/payment_posting",
      group: "payment_posting",
      routes: ["payment_posting/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\revenue_cycle\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "payments",
      prefix: "/payments",
      group: "payments",
      routes: ["payments/", "payments/<uuid:pk>/", "payments/<uuid:pk>/reconcile/", "payments/<uuid:pk>/refund/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\platform\\\\\\\\saas_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "billing",
      identifier: "payments-process",
      prefix: "/payments/process",
      group: "payments",
      routes: ["payments/process/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\platform\\\\\\\\saas_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      domain: "billing",
      identifier: "revenue-cycle",
      prefix: "/revenue-cycle",
      group: "billing",
      routes: ["api/revenue-cycle/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 20,
    },
    {
      domain: "billing",
      identifier: "saas-billing",
      prefix: "/saas-billing",
      group: "saas-billing",
      routes: ["api/saas-billing/"],
      sources: ["backend\\\\\\\\.datavionos_installer_backups\\\\\\\\20260917_121405\\\\\\\\config\\\\\\\\urls.py", "backend\\\\\\\\config\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      domain: "billing",
      identifier: "usage",
      prefix: "/usage",
      group: "usage",
      routes: ["usage/", "usage/<uuid:pk>/charge/", "usage/<uuid:pk>/evaluate/"],
      sources: ["backend\\\\\\\\apps\\\\\\\\platform\\\\\\\\saas_billing\\\\\\\\api\\\\\\\\urls.py"],
      confidence: "high",
      evidenceScore: 10,
    },
];

function normalize(value: string): string {
  return value.trim().toLowerCase();
}

function matchesAlias(
  value: string,
  alias: string,
): boolean {
  const normalizedValue = normalize(value);
  const normalizedAlias = normalize(alias);

  return (
    normalizedValue === normalizedAlias ||
    normalizedValue.includes(`-${normalizedAlias}`) ||
    normalizedValue.includes(`_${normalizedAlias}`) ||
    normalizedValue.includes(`/${normalizedAlias}`) ||
    normalizedValue.includes(`:${normalizedAlias}`) ||
    normalizedValue.includes(` ${normalizedAlias}`)
  );
}

function resolveDomain(
  module: BootstrapModule,
  runtimeDefinition: ModuleRuntimeDefinition,
): DomainWorkspaceDefinition | undefined {
  const values = [
    module.identifier,
    module.name,
    module.category,
    runtimeDefinition.identifier,
    runtimeDefinition.displayName,
    runtimeDefinition.category,
    runtimeDefinition.route,
    runtimeDefinition.apiPrefix,
    ...runtimeDefinition.tags,
  ].filter(Boolean);

  const candidates = DOMAIN_WORKSPACE_DEFINITIONS.filter(
    (definition) =>
      definition.aliases.some((alias) =>
        values.some((value) =>
          matchesAlias(String(value), alias),
        ),
      ),
  );

  return candidates.length === 1 ? candidates[0] : undefined;
}

function resolveContracts(
  runtimeDefinition: ModuleRuntimeDefinition,
): readonly DomainApiContract[] {
  const identifier = normalize(runtimeDefinition.identifier);
  const prefix = normalize(runtimeDefinition.apiPrefix);

  return DOMAIN_API_CONTRACTS.filter((contract) => {
    const contractIdentifier = normalize(contract.identifier);
    const contractPrefix = normalize(contract.prefix);

    return (
      contractIdentifier === identifier ||
      (
        prefix.length > 0 &&
        contractPrefix === prefix
      ) ||
      (
        prefix.length > 0 &&
        contractPrefix.startsWith(prefix)
      )
    );
  });
}

export function bindDomainWorkspace(
  input: DomainWorkspaceResolutionInput,
): DomainWorkspaceBinding | undefined {
  const definition = resolveDomain(
    input.module,
    input.runtimeDefinition,
  );

  if (!definition) {
    return undefined;
  }

  const contracts = resolveContracts(input.runtimeDefinition);

  if (contracts.length === 0) {
    return undefined;
  }

  const workspace: DomainWorkspaceContract = {
    domain: definition.id,
    moduleIdentifier: input.runtimeDefinition.identifier,
    displayName: input.runtimeDefinition.displayName,
    route: input.runtimeDefinition.route,
    apiPrefix: input.runtimeDefinition.apiPrefix,
    workspaceType: input.runtimeDefinition.workspaceType,
    rendererKey: input.runtimeDefinition.rendererKey,
    contractIdentifiers: contracts.map(
      (contract) => contract.identifier,
    ),
    contractPrefixes: contracts.map(
      (contract) => contract.prefix,
    ),
  };

  return {
    definition,
    workspace,
    contracts,
  };
}

export function bindDomainWorkspaces(
  modules: readonly BootstrapModule[],
  createRuntimeDefinition: (
    module: BootstrapModule,
  ) => ModuleRuntimeDefinition,
): readonly DomainWorkspaceBinding[] {
  return modules.flatMap((module) => {
    const runtimeDefinition = createRuntimeDefinition(module);
    const binding = bindDomainWorkspace({
      module,
      runtimeDefinition,
    });

    return binding ? [binding] : [];
  });
}

export function findDomainWorkspace(
  modules: readonly BootstrapModule[],
  moduleIdentifier: string,
  createRuntimeDefinition: (
    module: BootstrapModule,
  ) => ModuleRuntimeDefinition,
): DomainWorkspaceBinding | undefined {
  const runtimeModule = modules.find(
    (candidate) => candidate.identifier === moduleIdentifier,
  );

  if (!runtimeModule) {
    return undefined;
  }

  return bindDomainWorkspace({
    module: runtimeModule,
    runtimeDefinition: createRuntimeDefinition(runtimeModule),
  });
}
