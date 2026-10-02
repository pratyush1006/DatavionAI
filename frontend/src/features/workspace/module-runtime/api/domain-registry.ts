import type {
  DomainApiDefinition,
  DomainApiMap,
  DomainApiContract,
} from "./domain-types";

export const DOMAIN_API_DEFINITIONS: readonly DomainApiDefinition[] = [
  {
    id: "patients",
    label: "Patients",
    contracts: [
    {
      identifier: "patient-accounts",
      prefix: "/patient-accounts",
      group: "patient-accounts",
      routes: [
      "patient-accounts/",
      "patient-accounts/<uuid:account_id>/responsibilities/",
      "patient-accounts/<uuid:pk>/",
      "patient-accounts/<uuid:pk>/transition/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\billing\\\\patient_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patient-guarantors",
      prefix: "/patient-guarantors",
      group: "patient-guarantors",
      routes: [
      "patient-guarantors/",
      "patient-guarantors/<uuid:pk>/",
      "patient-guarantors/<uuid:pk>/restore/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\billing\\\\patient_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patient-management",
      prefix: "/patient-management",
      group: "patient-management",
      routes: [
      "api/patient-management/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patient-management-addresses",
      prefix: "/patient-management/addresses",
      group: "patient-management",
      routes: [
      "api/patient-management/addresses/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patient-responsibilities",
      prefix: "/patient-responsibilities",
      group: "patient-responsibilities",
      routes: [
      "patient-responsibilities/<uuid:pk>/",
      "patient-responsibilities/<uuid:pk>/restore/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\billing\\\\patient_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patient-statements",
      prefix: "/patient-statements",
      group: "patient-statements",
      routes: [
      "patient-statements/",
      "patient-statements/<uuid:pk>/issue/",
      "patient-statements/<uuid:pk>/void/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\billing\\\\patient_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patient-statements-generate",
      prefix: "/patient-statements/generate",
      group: "patient-statements",
      routes: [
      "patient-statements/generate/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\billing\\\\patient_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "patients",
      prefix: "/patients",
      group: "patients",
      routes: [
      "patients/",
      "patients/<uuid:patient_id>/devices/"
      ],
      sources: [
      "backend\\\\apps\\\\patient_management\\\\api\\\\urls.py",
      "backend\\\\apps\\\\patient_management\\\\urls.py",
      "backend\\\\apps\\\\device_platform\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 20,
    },
    ],
  },
  {
    id: "appointments",
    label: "Appointments",
    contracts: [
    {
      identifier: "appointments",
      prefix: "/appointments",
      group: "appointments",
      routes: [
      "api/appointments/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    ],
  },
  {
    id: "pharmacy",
    label: "Pharmacy",
    contracts: [
    {
      identifier: "clinical-prescriptions-draft",
      prefix: "/clinical/prescriptions/draft",
      group: "clinical",
      routes: [
      "clinical/prescriptions/draft/"
      ],
      sources: [
      "backend\\\\apps\\\\ai\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      identifier: "medications",
      prefix: "/medications",
      group: "medications",
      routes: [
      "api/medications/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      identifier: "pharmacy",
      prefix: "/pharmacy",
      group: "pharmacy",
      routes: [
      "api/pharmacy/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "prescriptions",
      prefix: "/prescriptions",
      group: "prescriptions",
      routes: [
      "api/prescriptions/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    ],
  },
  {
    id: "laboratory",
    label: "Laboratory",
    contracts: [
    {
      identifier: "clinical-lab-orders-status",
      prefix: "/clinical/lab-orders/status",
      group: "clinical",
      routes: [
      "clinical/lab-orders/status/"
      ],
      sources: [
      "backend\\\\apps\\\\ai\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "laboratories",
      prefix: "/laboratories",
      group: "laboratory",
      routes: [
      "api/laboratories/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 23,
    },
    ],
  },
  {
    id: "documents",
    label: "Documents",
    contracts: [
    {
      identifier: "documents",
      prefix: "/documents",
      group: "documents",
      routes: [
      "api/documents/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    ],
  },
  {
    id: "billing",
    label: "Billing",
    contracts: [
    {
      identifier: "account-auto-charge",
      prefix: "/account/auto-charge",
      group: "account",
      routes: [
      "account/auto-charge/"
      ],
      sources: [
      "backend\\\\apps\\\\platform\\\\saas_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "account-payment-provider",
      prefix: "/account/payment-provider",
      group: "account",
      routes: [
      "account/payment-provider/"
      ],
      sources: [
      "backend\\\\apps\\\\platform\\\\saas_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "admissions",
      prefix: "/admissions",
      group: "admissions",
      routes: [
      "admissions/",
      "admissions/<uuid:admission_id>/discharge/",
      "admissions/<uuid:admission_id>/transfer/"
      ],
      sources: [
      "backend\\\\apps\\\\hospital_operations\\\\api\\\\urls.py"
      ],
      confidence: "medium",
      evidenceScore: 3,
    },
    {
      identifier: "billing",
      prefix: "/billing",
      group: "billing",
      routes: [
      "api/billing/",
      "billing/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py",
      "backend\\\\apps\\\\revenue_cycle\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "charge_capture",
      prefix: "/charge_capture",
      group: "charge_capture",
      routes: [
      "charge_capture/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "charges",
      prefix: "/charges",
      group: "charges",
      routes: [
      "charges/",
      "charges/<uuid:charge_id>/",
      "charges/<uuid:charge_id>/transition/",
      "charges/<uuid:charge_id>/void/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\charge_capture\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 20,
    },
    {
      identifier: "claim_scrubbing",
      prefix: "/claim_scrubbing",
      group: "claim_scrubbing",
      routes: [
      "claim_scrubbing/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "claim_submission",
      prefix: "/claim_submission",
      group: "claim_submission",
      routes: [
      "claim_submission/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "payment_posting",
      prefix: "/payment_posting",
      group: "payment_posting",
      routes: [
      "payment_posting/"
      ],
      sources: [
      "backend\\\\apps\\\\revenue_cycle\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "payments",
      prefix: "/payments",
      group: "payments",
      routes: [
      "payments/",
      "payments/<uuid:pk>/",
      "payments/<uuid:pk>/reconcile/",
      "payments/<uuid:pk>/refund/"
      ],
      sources: [
      "backend\\\\apps\\\\platform\\\\saas_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      identifier: "payments-process",
      prefix: "/payments/process",
      group: "payments",
      routes: [
      "payments/process/"
      ],
      sources: [
      "backend\\\\apps\\\\platform\\\\saas_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 13,
    },
    {
      identifier: "revenue-cycle",
      prefix: "/revenue-cycle",
      group: "billing",
      routes: [
      "api/revenue-cycle/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 20,
    },
    {
      identifier: "saas-billing",
      prefix: "/saas-billing",
      group: "saas-billing",
      routes: [
      "api/saas-billing/"
      ],
      sources: [
      "backend\\\\.datavionos_installer_backups\\\\20260917_121405\\\\config\\\\urls.py",
      "backend\\\\config\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    {
      identifier: "usage",
      prefix: "/usage",
      group: "usage",
      routes: [
      "usage/",
      "usage/<uuid:pk>/charge/",
      "usage/<uuid:pk>/evaluate/"
      ],
      sources: [
      "backend\\\\apps\\\\platform\\\\saas_billing\\\\api\\\\urls.py"
      ],
      confidence: "high",
      evidenceScore: 10,
    },
    ],
  },
];

export const DOMAIN_API_MAP: DomainApiMap = Object.fromEntries(
  DOMAIN_API_DEFINITIONS.map((definition) => [
    definition.id,
    definition.contracts,
  ]),
) as DomainApiMap;

export function findDomainApiContracts(
  domain: DomainApiDefinition["id"],
): readonly DomainApiContract[] {
  return DOMAIN_API_MAP[domain] ?? [];
}

export function findPrimaryDomainApiContract(
  domain: DomainApiDefinition["id"],
): DomainApiContract | undefined {
  return findDomainApiContracts(domain)[0];
}

export function findDomainForModule(
  moduleIdentifier: string,
  apiPrefix: string,
): DomainApiDefinition["id"] | undefined {
  for (const definition of DOMAIN_API_DEFINITIONS) {
    if (
      definition.contracts.some(
        (contract) =>
          contract.identifier === moduleIdentifier ||
          contract.prefix === apiPrefix,
      )
    ) {
      return definition.id;
    }
  }

  return undefined;
}
