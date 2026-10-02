import type {
  ModuleApiContract,
  ModuleApiRegistry,
} from "./types";

export const MODULE_API_REGISTRY: ModuleApiRegistry = {
  "account": {
    identifier: "account",
    prefix: "/account",
    group: "account",
    routes: [
    "account/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "account-auto-charge": {
    identifier: "account-auto-charge",
    prefix: "/account/auto-charge",
    group: "account",
    routes: [
    "account/auto-charge/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "account-payment-provider": {
    identifier: "account-payment-provider",
    prefix: "/account/payment-provider",
    group: "account",
    routes: [
    "account/payment-provider/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "account-update": {
    identifier: "account-update",
    prefix: "/account/update",
    group: "account",
    routes: [
    "account/update/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "accounts": {
    identifier: "accounts",
    prefix: "/accounts",
    group: "accounts",
    routes: [
    "accounts/",
    "accounts/<uuid:account_id>/hold/",
    "accounts/<uuid:account_id>/release-hold/",
    "accounts/<uuid:account_id>/transactions/",
    "accounts/<uuid:account_id>/write-off/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\accounts_receivable\\urls.py"
    ],
  },
  "admissions": {
    identifier: "admissions",
    prefix: "/admissions",
    group: "admissions",
    routes: [
    "admissions/",
    "admissions/<uuid:admission_id>/discharge/",
    "admissions/<uuid:admission_id>/transfer/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "ai": {
    identifier: "ai",
    prefix: "/ai",
    group: "ai",
    routes: [
    "api/ai/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "ai-control": {
    identifier: "ai-control",
    prefix: "/ai-control",
    group: "ai-control",
    routes: [
    "api/ai-control/"
    ],
    sources: [
    "backend\\config\\urls.py"
    ],
  },
  "allergies": {
    identifier: "allergies",
    prefix: "/allergies",
    group: "allergies",
    routes: [
    "api/allergies/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "analytics": {
    identifier: "analytics",
    prefix: "/analytics",
    group: "analytics",
    routes: [
    "analytics/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "appeals": {
    identifier: "appeals",
    prefix: "/appeals",
    group: "appeals",
    routes: [
    "appeals/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "applications": {
    identifier: "applications",
    prefix: "/applications",
    group: "applications",
    routes: [
    "applications/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "appointments": {
    identifier: "appointments",
    prefix: "/appointments",
    group: "appointments",
    routes: [
    "api/appointments/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "ar": {
    identifier: "ar",
    prefix: "/ar",
    group: "ar",
    routes: [
    "ar/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "assignments": {
    identifier: "assignments",
    prefix: "/assignments",
    group: "assignments",
    routes: [
    "assignments/",
    "assignments/<int:shift_assignment_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\shifts\\api\\urls.py"
    ],
  },
  "audit": {
    identifier: "audit",
    prefix: "/audit",
    group: "audit",
    routes: [
    "api/audit/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "auth": {
    identifier: "auth",
    prefix: "/auth",
    group: "auth",
    routes: [
    "api/auth/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "authentication": {
    identifier: "authentication",
    prefix: "/authentication",
    group: "authentication",
    routes: [
    "authentication/"
    ],
    sources: [
    "backend\\apps\\platform\\accounts\\api\\urls.py"
    ],
  },
  "balances": {
    identifier: "balances",
    prefix: "/balances",
    group: "balances",
    routes: [
    "balances/",
    "balances/<int:leave_balance_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\leave\\api\\urls.py"
    ],
  },
  "beds": {
    identifier: "beds",
    prefix: "/beds",
    group: "beds",
    routes: [
    "beds/",
    "beds/<uuid:bed_id>/clean/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "beds-assignments": {
    identifier: "beds-assignments",
    prefix: "/beds/assignments",
    group: "beds",
    routes: [
    "beds/assignments/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "beds-reservations": {
    identifier: "beds-reservations",
    prefix: "/beds/reservations",
    group: "beds",
    routes: [
    "beds/reservations/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "billing": {
    identifier: "billing",
    prefix: "/billing",
    group: "billing",
    routes: [
    "api/billing/",
    "billing/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py",
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "bootstrap": {
    identifier: "bootstrap",
    prefix: "/bootstrap",
    group: "bootstrap",
    routes: [
    "bootstrap/"
    ],
    sources: [
    "backend\\apps\\datavionos\\api\\urls.py"
    ],
  },
  "branding": {
    identifier: "branding",
    prefix: "/branding",
    group: "branding",
    routes: [
    "branding/"
    ],
    sources: [
    "backend\\apps\\platform\\organizations\\api\\urls.py"
    ],
  },
  "by-organization": {
    identifier: "by-organization",
    prefix: "/by-organization",
    group: "by-organization",
    routes: [
    "by-organization/<uuid:organization_id>/"
    ],
    sources: [
    "backend\\apps\\platform\\organizations\\api\\organization_branding\\urls.py"
    ],
  },
  "charge_capture": {
    identifier: "charge_capture",
    prefix: "/charge_capture",
    group: "charge_capture",
    routes: [
    "charge_capture/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "charges": {
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
    "backend\\apps\\revenue_cycle\\charge_capture\\api\\urls.py"
    ],
  },
  "chat": {
    identifier: "chat",
    prefix: "/chat",
    group: "chat",
    routes: [
    "chat/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "chat-stream": {
    identifier: "chat-stream",
    prefix: "/chat/stream",
    group: "chat",
    routes: [
    "chat/stream/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "cities": {
    identifier: "cities",
    prefix: "/cities",
    group: "cities",
    routes: [
    "cities/"
    ],
    sources: [
    "backend\\apps\\platform\\geography\\api\\geography\\urls.py"
    ],
  },
  "claim_scrubbing": {
    identifier: "claim_scrubbing",
    prefix: "/claim_scrubbing",
    group: "claim_scrubbing",
    routes: [
    "claim_scrubbing/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "claim_submission": {
    identifier: "claim_submission",
    prefix: "/claim_submission",
    group: "claim_submission",
    routes: [
    "claim_submission/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "clinical-artifacts": {
    identifier: "clinical-artifacts",
    prefix: "/clinical/artifacts",
    group: "clinical",
    routes: [
    "clinical/artifacts/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "clinical-artifacts-versions": {
    identifier: "clinical-artifacts-versions",
    prefix: "/clinical/artifacts/versions",
    group: "clinical",
    routes: [
    "clinical/artifacts/versions/<uuid:version_id>/review/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "clinical-lab-orders-status": {
    identifier: "clinical-lab-orders-status",
    prefix: "/clinical/lab-orders/status",
    group: "clinical",
    routes: [
    "clinical/lab-orders/status/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "clinical-notes-clean": {
    identifier: "clinical-notes-clean",
    prefix: "/clinical/notes/clean",
    group: "clinical",
    routes: [
    "clinical/notes/clean/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "clinical-prescriptions-draft": {
    identifier: "clinical-prescriptions-draft",
    prefix: "/clinical/prescriptions/draft",
    group: "clinical",
    routes: [
    "clinical/prescriptions/draft/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "coding": {
    identifier: "coding",
    prefix: "/coding",
    group: "coding",
    routes: [
    "coding/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "configuration": {
    identifier: "configuration",
    prefix: "/configuration",
    group: "configuration",
    routes: [
    "api/configuration/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "contacts": {
    identifier: "contacts",
    prefix: "/contacts",
    group: "contacts",
    routes: [
    "contacts/"
    ],
    sources: [
    "backend\\apps\\patient_management\\api\\urls.py"
    ],
  },
  "contract": {
    identifier: "contract",
    prefix: "/contract",
    group: "contract",
    routes: [
    "contract/"
    ],
    sources: [
    "backend\\apps\\imaging\\api\\urls.py"
    ],
  },
  "countries": {
    identifier: "countries",
    prefix: "/countries",
    group: "countries",
    routes: [
    "countries/"
    ],
    sources: [
    "backend\\apps\\platform\\geography\\api\\geography\\urls.py"
    ],
  },
  "current-location": {
    identifier: "current-location",
    prefix: "/current-location",
    group: "current-location",
    routes: [
    "current-location/"
    ],
    sources: [
    "backend\\apps\\platform\\geography\\api\\geography\\urls.py"
    ],
  },
  "customer_invoices": {
    identifier: "customer_invoices",
    prefix: "/customer_invoices",
    group: "customer_invoices",
    routes: [
    "customer_invoices/",
    "customer_invoices/<uuid:customer_invoice_id>/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\billing\\accounts_receivable\\api\\urls.py"
    ],
  },
  "customers": {
    identifier: "customers",
    prefix: "/customers",
    group: "customers",
    routes: [
    "customers/",
    "customers/<uuid:customer_id>/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\billing\\accounts_receivable\\api\\urls.py"
    ],
  },
  "cycles": {
    identifier: "cycles",
    prefix: "/cycles",
    group: "cycles",
    routes: [
    "cycles/",
    "cycles/<int:review_cycle_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\performance\\api\\urls.py"
    ],
  },
  "denials": {
    identifier: "denials",
    prefix: "/denials",
    group: "denials",
    routes: [
    "denials/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "department-members": {
    identifier: "department-members",
    prefix: "/department-members",
    group: "department-members",
    routes: [
    "department-members/<uuid:membership_id>/lifecycle/"
    ],
    sources: [
    "backend\\apps\\datavionos\\access_control\\api\\urls.py"
    ],
  },
  "department-members-assign": {
    identifier: "department-members-assign",
    prefix: "/department-members/assign",
    group: "department-members",
    routes: [
    "department-members/assign/"
    ],
    sources: [
    "backend\\apps\\datavionos\\access_control\\api\\urls.py"
    ],
  },
  "departments": {
    identifier: "departments",
    prefix: "/departments",
    group: "departments",
    routes: [
    "api/departments/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "device-platform": {
    identifier: "device-platform",
    prefix: "/device-platform",
    group: "device-platform",
    routes: [
    "api/device-platform/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "devices": {
    identifier: "devices",
    prefix: "/devices",
    group: "devices",
    routes: [
    "devices/",
    "devices/<uuid:device_id>/",
    "devices/<uuid:device_id>/<str:action>/"
    ],
    sources: [
    "backend\\apps\\device_platform\\api\\urls.py"
    ],
  },
  "diagnoses": {
    identifier: "diagnoses",
    prefix: "/diagnoses",
    group: "diagnoses",
    routes: [
    "api/diagnoses/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "docs": {
    identifier: "docs",
    prefix: "/docs",
    group: "docs",
    routes: [
    "api/docs/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "documents": {
    identifier: "documents",
    prefix: "/documents",
    group: "documents",
    routes: [
    "api/documents/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "eligibility": {
    identifier: "eligibility",
    prefix: "/eligibility",
    group: "eligibility",
    routes: [
    "eligibility/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "employees": {
    identifier: "employees",
    prefix: "/employees",
    group: "employees",
    routes: [
    "api/employees/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "encounters": {
    identifier: "encounters",
    prefix: "/encounters",
    group: "encounters",
    routes: [
    "api/encounters/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "enrollments": {
    identifier: "enrollments",
    prefix: "/enrollments",
    group: "enrollments",
    routes: [
    "enrollments/<uuid:enrollment_id>/resolve-route/<str:service>/"
    ],
    sources: [
    "backend\\apps\\insurance\\api\\urls.py"
    ],
  },
  "era": {
    identifier: "era",
    prefix: "/era",
    group: "era",
    routes: [
    "era/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "features": {
    identifier: "features",
    prefix: "/features",
    group: "features",
    routes: [
    "features/<uuid:feature_id>/"
    ],
    sources: [
    "backend\\apps\\datavionos\\control_plane\\api\\urls.py"
    ],
  },
  "finance": {
    identifier: "finance",
    prefix: "/finance",
    group: "finance",
    routes: [
    "api/finance/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "geography": {
    identifier: "geography",
    prefix: "/geography",
    group: "geography",
    routes: [
    "api/geography/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "goals": {
    identifier: "goals",
    prefix: "/goals",
    group: "goals",
    routes: [
    "goals/",
    "goals/<int:performance_goal_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\performance\\api\\urls.py"
    ],
  },
  "health": {
    identifier: "health",
    prefix: "/health",
    group: "health",
    routes: [
    "health/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py",
    "backend\\apps\\billing\\finance\\api\\urls.py",
    "backend\\apps\\clinical\\laboratories\\api\\urls.py",
    "backend\\apps\\core\\urls.py",
    "backend\\apps\\imaging\\api\\urls.py"
    ],
  },
  "health-live": {
    identifier: "health-live",
    prefix: "/health/live",
    group: "health",
    routes: [
    "health/live/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "health-ready": {
    identifier: "health-ready",
    prefix: "/health/ready",
    group: "health",
    routes: [
    "health/ready/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "hierarchies": {
    identifier: "hierarchies",
    prefix: "/hierarchies",
    group: "hierarchies",
    routes: [
    "hierarchies/"
    ],
    sources: [
    "backend\\apps\\platform\\organizations\\api\\urls.py"
    ],
  },
  "hospital-operations": {
    identifier: "hospital-operations",
    prefix: "/hospital-operations",
    group: "hospital-operations",
    routes: [
    "api/hospital-operations/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "identifiers": {
    identifier: "identifiers",
    prefix: "/identifiers",
    group: "identifiers",
    routes: [
    "identifiers/"
    ],
    sources: [
    "backend\\apps\\patient_management\\urls.py"
    ],
  },
  "imaging": {
    identifier: "imaging",
    prefix: "/imaging",
    group: "imaging",
    routes: [
    "api/imaging/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "insurance": {
    identifier: "insurance",
    prefix: "/insurance",
    group: "insurance",
    routes: [
    "api/insurance/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "insurance_verification": {
    identifier: "insurance_verification",
    prefix: "/insurance_verification",
    group: "insurance_verification",
    routes: [
    "insurance_verification/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "invoices": {
    identifier: "invoices",
    prefix: "/invoices",
    group: "invoices",
    routes: [
    "invoices/",
    "invoices/<uuid:pk>/",
    "invoices/<uuid:pk>/cancel/",
    "invoices/<uuid:pk>/finalize/",
    "invoices/<uuid:pk>/issue/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "invoices-generate": {
    identifier: "invoices-generate",
    prefix: "/invoices/generate",
    group: "invoices",
    routes: [
    "invoices/generate/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "jobs": {
    identifier: "jobs",
    prefix: "/jobs",
    group: "jobs",
    routes: [
    "jobs/",
    "jobs/<uuid:job_id>/",
    "jobs/<uuid:job_id>/<str:action>/",
    "jobs/<uuid:job_id>/notes/generate/"
    ],
    sources: [
    "backend\\apps\\transcription\\api\\urls.py"
    ],
  },
  "laboratories": {
    identifier: "laboratories",
    prefix: "/laboratories",
    group: "laboratory",
    routes: [
    "api/laboratories/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "live": {
    identifier: "live",
    prefix: "/live",
    group: "live",
    routes: [
    "live/"
    ],
    sources: [
    "backend\\apps\\core\\health\\urls.py"
    ],
  },
  "matches": {
    identifier: "matches",
    prefix: "/matches",
    group: "matches",
    routes: [
    "matches/",
    "matches/<uuid:candidate_id>/review/"
    ],
    sources: [
    "backend\\apps\\patient_management\\mpi\\api\\urls.py"
    ],
  },
  "medications": {
    identifier: "medications",
    prefix: "/medications",
    group: "medications",
    routes: [
    "api/medications/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "merge": {
    identifier: "merge",
    prefix: "/merge",
    group: "merge",
    routes: [
    "merge/"
    ],
    sources: [
    "backend\\apps\\patient_management\\mpi\\api\\urls.py"
    ],
  },
  "modules": {
    identifier: "modules",
    prefix: "/modules",
    group: "modules",
    routes: [
    "modules/<uuid:module_id>/"
    ],
    sources: [
    "backend\\apps\\datavionos\\control_plane\\api\\urls.py"
    ],
  },
  "my-tenants": {
    identifier: "my-tenants",
    prefix: "/my-tenants",
    group: "my-tenants",
    routes: [
    "my-tenants/"
    ],
    sources: [
    "backend\\apps\\platform\\tenancy\\api\\urls.py"
    ],
  },
  "notes": {
    identifier: "notes",
    prefix: "/notes",
    group: "notes",
    routes: [
    "api/notes/",
    "notes/<uuid:note_id>/",
    "notes/<uuid:note_id>/review/",
    "notes/<uuid:note_id>/sign/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py",
    "backend\\apps\\transcription\\api\\urls.py"
    ],
  },
  "notifications": {
    identifier: "notifications",
    prefix: "/notifications",
    group: "notifications",
    routes: [
    "api/notifications/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "onboard": {
    identifier: "onboard",
    prefix: "/onboard",
    group: "onboard",
    routes: [
    "onboard/"
    ],
    sources: [
    "backend\\apps\\organization\\employees\\api\\urls.py"
    ],
  },
  "onboarding": {
    identifier: "onboarding",
    prefix: "/onboarding",
    group: "onboarding",
    routes: [
    "api/onboarding/"
    ],
    sources: [
    "backend\\config\\urls.py"
    ],
  },
  "opd-queues": {
    identifier: "opd-queues",
    prefix: "/opd/queues",
    group: "opd",
    routes: [
    "opd/queues/<uuid:queue_id>/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "opd-visits": {
    identifier: "opd-visits",
    prefix: "/opd/visits",
    group: "opd",
    routes: [
    "opd/visits/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "organization-access": {
    identifier: "organization-access",
    prefix: "/organization-access",
    group: "organization-access",
    routes: [
    "api/organization-access/"
    ],
    sources: [
    "backend\\config\\urls.py"
    ],
  },
  "organization-control": {
    identifier: "organization-control",
    prefix: "/organization-control",
    group: "organization-control",
    routes: [
    "api/organization-control/"
    ],
    sources: [
    "backend\\config\\urls.py"
    ],
  },
  "organization-roles": {
    identifier: "organization-roles",
    prefix: "/organization-roles",
    group: "organization-roles",
    routes: [
    "organization-roles/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py"
    ],
  },
  "organization-types": {
    identifier: "organization-types",
    prefix: "/organization-types",
    group: "organization-types",
    routes: [
    "organization-types/"
    ],
    sources: [
    "backend\\apps\\datavionos\\onboarding\\api\\urls.py"
    ],
  },
  "organizations": {
    identifier: "organizations",
    prefix: "/organizations",
    group: "organizations",
    routes: [
    "api/organizations/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "participants": {
    identifier: "participants",
    prefix: "/participants",
    group: "participants",
    routes: [
    "participants/<uuid:participant_id>/<str:action>/",
    "participants/<uuid:participant_id>/media-state/"
    ],
    sources: [
    "backend\\apps\\telemedicine\\api\\urls.py"
    ],
  },
  "patient-accounts": {
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
    "backend\\apps\\revenue_cycle\\billing\\patient_billing\\api\\urls.py"
    ],
  },
  "patient-guarantors": {
    identifier: "patient-guarantors",
    prefix: "/patient-guarantors",
    group: "patient-guarantors",
    routes: [
    "patient-guarantors/",
    "patient-guarantors/<uuid:pk>/",
    "patient-guarantors/<uuid:pk>/restore/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\billing\\patient_billing\\api\\urls.py"
    ],
  },
  "patient-management": {
    identifier: "patient-management",
    prefix: "/patient-management",
    group: "patient-management",
    routes: [
    "api/patient-management/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "patient-management-addresses": {
    identifier: "patient-management-addresses",
    prefix: "/patient-management/addresses",
    group: "patient-management",
    routes: [
    "api/patient-management/addresses/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "patient-responsibilities": {
    identifier: "patient-responsibilities",
    prefix: "/patient-responsibilities",
    group: "patient-responsibilities",
    routes: [
    "patient-responsibilities/<uuid:pk>/",
    "patient-responsibilities/<uuid:pk>/restore/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\billing\\patient_billing\\api\\urls.py"
    ],
  },
  "patient-statements": {
    identifier: "patient-statements",
    prefix: "/patient-statements",
    group: "patient-statements",
    routes: [
    "patient-statements/",
    "patient-statements/<uuid:pk>/issue/",
    "patient-statements/<uuid:pk>/void/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\billing\\patient_billing\\api\\urls.py"
    ],
  },
  "patient-statements-generate": {
    identifier: "patient-statements-generate",
    prefix: "/patient-statements/generate",
    group: "patient-statements",
    routes: [
    "patient-statements/generate/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\billing\\patient_billing\\api\\urls.py"
    ],
  },
  "patients": {
    identifier: "patients",
    prefix: "/patients",
    group: "patients",
    routes: [
    "patients/",
    "patients/<uuid:patient_id>/devices/"
    ],
    sources: [
    "backend\\apps\\patient_management\\api\\urls.py",
    "backend\\apps\\patient_management\\urls.py",
    "backend\\apps\\device_platform\\api\\urls.py"
    ],
  },
  "payment_posting": {
    identifier: "payment_posting",
    prefix: "/payment_posting",
    group: "payment_posting",
    routes: [
    "payment_posting/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "payments": {
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
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "payments-process": {
    identifier: "payments-process",
    prefix: "/payments/process",
    group: "payments",
    routes: [
    "payments/process/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "payslips": {
    identifier: "payslips",
    prefix: "/payslips",
    group: "payslips",
    routes: [
    "payslips/",
    "payslips/<int:payslip_id>/",
    "payslips/<int:payslip_id>/mark-paid/",
    "payslips/<int:payslip_id>/process/"
    ],
    sources: [
    "backend\\apps\\hr\\payroll\\api\\urls.py"
    ],
  },
  "permission-groups": {
    identifier: "permission-groups",
    prefix: "/permission-groups",
    group: "permission-groups",
    routes: [
    "permission-groups/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py"
    ],
  },
  "permissions": {
    identifier: "permissions",
    prefix: "/permissions",
    group: "permissions",
    routes: [
    "permissions/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py"
    ],
  },
  "pharmacy": {
    identifier: "pharmacy",
    prefix: "/pharmacy",
    group: "pharmacy",
    routes: [
    "api/pharmacy/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "plans": {
    identifier: "plans",
    prefix: "/plans",
    group: "plans",
    routes: [
    "plans/",
    "plans/<uuid:pk>/",
    "plans/<uuid:pk>/activate/",
    "plans/<uuid:pk>/archive/",
    "plans/<uuid:pk>/deactivate/",
    "plans/<uuid:pk>/update/"
    ],
    sources: [
    "backend\\apps\\datavionos\\onboarding\\api\\urls.py",
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "plans-create": {
    identifier: "plans-create",
    prefix: "/plans/create",
    group: "plans",
    routes: [
    "plans/create/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "platform": {
    identifier: "platform",
    prefix: "/platform",
    group: "platform",
    routes: [
    "api/platform/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "preferences": {
    identifier: "preferences",
    prefix: "/preferences",
    group: "preferences",
    routes: [
    "preferences/"
    ],
    sources: [
    "backend\\apps\\patient_management\\api\\urls.py"
    ],
  },
  "prescriptions": {
    identifier: "prescriptions",
    prefix: "/prescriptions",
    group: "prescriptions",
    routes: [
    "api/prescriptions/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "prior_authorization": {
    identifier: "prior_authorization",
    prefix: "/prior_authorization",
    group: "prior_authorization",
    routes: [
    "prior_authorization/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\urls.py"
    ],
  },
  "processes": {
    identifier: "processes",
    prefix: "/processes",
    group: "processes",
    routes: [
    "processes/",
    "processes/<int:lifecycle_process_id>/",
    "processes/<int:lifecycle_process_id>/cancel/",
    "processes/<int:lifecycle_process_id>/complete/"
    ],
    sources: [
    "backend\\apps\\hr\\onboarding\\api\\urls.py"
    ],
  },
  "profiles": {
    identifier: "profiles",
    prefix: "/profiles",
    group: "profiles",
    routes: [
    "profiles/"
    ],
    sources: [
    "backend\\apps\\patient_management\\urls.py"
    ],
  },
  "providers": {
    identifier: "providers",
    prefix: "/providers",
    group: "providers",
    routes: [
    "api/providers/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "rag-index": {
    identifier: "rag-index",
    prefix: "/rag/index",
    group: "rag",
    routes: [
    "rag/index/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "rag-search": {
    identifier: "rag-search",
    prefix: "/rag/search",
    group: "rag",
    routes: [
    "rag/search/"
    ],
    sources: [
    "backend\\apps\\ai\\api\\urls.py"
    ],
  },
  "rbac": {
    identifier: "rbac",
    prefix: "/rbac",
    group: "rbac",
    routes: [
    "api/rbac/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "ready": {
    identifier: "ready",
    prefix: "/ready",
    group: "ready",
    routes: [
    "ready/"
    ],
    sources: [
    "backend\\apps\\core\\health\\urls.py"
    ],
  },
  "recordings": {
    identifier: "recordings",
    prefix: "/recordings",
    group: "recordings",
    routes: [
    "recordings/<uuid:recording_id>/finalize/"
    ],
    sources: [
    "backend\\apps\\telemedicine\\api\\urls.py"
    ],
  },
  "records": {
    identifier: "records",
    prefix: "/records",
    group: "records",
    routes: [
    "records/",
    "records/<uuid:record_id>/process/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\cross_module_integration\\urls.py"
    ],
  },
  "records-ingest": {
    identifier: "records-ingest",
    prefix: "/records/ingest",
    group: "records",
    routes: [
    "records/ingest/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\cross_module_integration\\urls.py"
    ],
  },
  "regions": {
    identifier: "regions",
    prefix: "/regions",
    group: "regions",
    routes: [
    "regions/"
    ],
    sources: [
    "backend\\apps\\platform\\geography\\api\\geography\\urls.py"
    ],
  },
  "register": {
    identifier: "register",
    prefix: "/register",
    group: "register",
    routes: [
    "register/"
    ],
    sources: [
    "backend\\apps\\datavionos\\onboarding\\api\\urls.py"
    ],
  },
  "registrations": {
    identifier: "registrations",
    prefix: "/registrations",
    group: "registrations",
    routes: [
    "registrations/"
    ],
    sources: [
    "backend\\apps\\patient_management\\api\\urls.py"
    ],
  },
  "requests": {
    identifier: "requests",
    prefix: "/requests",
    group: "requests",
    routes: [
    "requests/",
    "requests/<int:leave_request_id>/",
    "requests/<int:leave_request_id>/approve/",
    "requests/<int:leave_request_id>/cancel/",
    "requests/<int:leave_request_id>/reject/"
    ],
    sources: [
    "backend\\apps\\hr\\leave\\api\\urls.py"
    ],
  },
  "revenue-cycle": {
    identifier: "revenue-cycle",
    prefix: "/revenue-cycle",
    group: "billing",
    routes: [
    "api/revenue-cycle/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "reviews": {
    identifier: "reviews",
    prefix: "/reviews",
    group: "reviews",
    routes: [
    "reviews/",
    "reviews/<int:performance_review_id>/",
    "reviews/<int:performance_review_id>/acknowledge/",
    "reviews/<int:performance_review_id>/complete/",
    "reviews/<int:performance_review_id>/submit/"
    ],
    sources: [
    "backend\\apps\\hr\\performance\\api\\urls.py"
    ],
  },
  "role-hierarchies": {
    identifier: "role-hierarchies",
    prefix: "/role-hierarchies",
    group: "role-hierarchies",
    routes: [
    "role-hierarchies/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py"
    ],
  },
  "role-permissions": {
    identifier: "role-permissions",
    prefix: "/role-permissions",
    group: "role-permissions",
    routes: [
    "role-permissions/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py"
    ],
  },
  "roles": {
    identifier: "roles",
    prefix: "/roles",
    group: "roles",
    routes: [
    "roles/",
    "roles/<uuid:assignment_id>/lifecycle/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py",
    "backend\\apps\\datavionos\\access_control\\api\\urls.py"
    ],
  },
  "roles-assign": {
    identifier: "roles-assign",
    prefix: "/roles/assign",
    group: "roles",
    routes: [
    "roles/assign/"
    ],
    sources: [
    "backend\\apps\\datavionos\\access_control\\api\\urls.py"
    ],
  },
  "rooms": {
    identifier: "rooms",
    prefix: "/rooms",
    group: "rooms",
    routes: [
    "rooms/"
    ],
    sources: [
    "backend\\apps\\hospital_operations\\api\\urls.py"
    ],
  },
  "saas-billing": {
    identifier: "saas-billing",
    prefix: "/saas-billing",
    group: "saas-billing",
    routes: [
    "api/saas-billing/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "salary-structures": {
    identifier: "salary-structures",
    prefix: "/salary-structures",
    group: "salary-structures",
    routes: [
    "salary-structures/",
    "salary-structures/<int:salary_structure_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\payroll\\api\\urls.py"
    ],
  },
  "schema": {
    identifier: "schema",
    prefix: "/schema",
    group: "schema",
    routes: [
    "api/schema/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "scrubs": {
    identifier: "scrubs",
    prefix: "/scrubs",
    group: "scrubs",
    routes: [
    "scrubs/",
    "scrubs/<uuid:scrub_id>/",
    "scrubs/<uuid:scrub_id>/override/",
    "scrubs/<uuid:scrub_id>/run/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\claim_scrubbing\\api\\urls.py"
    ],
  },
  "search": {
    identifier: "search",
    prefix: "/search",
    group: "search",
    routes: [
    "api/search/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "select": {
    identifier: "select",
    prefix: "/select",
    group: "select",
    routes: [
    "select/"
    ],
    sources: [
    "backend\\apps\\platform\\tenancy\\api\\urls.py"
    ],
  },
  "sessions": {
    identifier: "sessions",
    prefix: "/sessions",
    group: "sessions",
    routes: [
    "sessions/",
    "sessions/<uuid:session_id>/",
    "sessions/<uuid:session_id>/<str:action>/",
    "sessions/<uuid:session_id>/participants/",
    "sessions/<uuid:session_id>/recordings/",
    "sessions/<uuid:session_id>/recordings/start/"
    ],
    sources: [
    "backend\\apps\\telemedicine\\api\\urls.py"
    ],
  },
  "snapshots": {
    identifier: "snapshots",
    prefix: "/snapshots",
    group: "snapshots",
    routes: [
    "snapshots/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\revenue_analytics\\urls.py"
    ],
  },
  "snapshots-generate": {
    identifier: "snapshots-generate",
    prefix: "/snapshots/generate",
    group: "snapshots",
    routes: [
    "snapshots/generate/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\revenue_analytics\\urls.py"
    ],
  },
  "status": {
    identifier: "status",
    prefix: "/status",
    group: "status",
    routes: [
    "status/"
    ],
    sources: [
    "backend\\apps\\datavionos\\onboarding\\api\\urls.py"
    ],
  },
  "submissions": {
    identifier: "submissions",
    prefix: "/submissions",
    group: "submissions",
    routes: [
    "submissions/",
    "submissions/<uuid:submission_id>/",
    "submissions/<uuid:submission_id>/restore/",
    "submissions/<uuid:submission_id>/transition/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\claim_submission\\api\\urls.py"
    ],
  },
  "subscription": {
    identifier: "subscription",
    prefix: "/subscription",
    group: "subscription",
    routes: [
    "subscription/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "subscription-activate": {
    identifier: "subscription-activate",
    prefix: "/subscription/activate",
    group: "subscription",
    routes: [
    "subscription/activate/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "subscription-cancel": {
    identifier: "subscription-cancel",
    prefix: "/subscription/cancel",
    group: "subscription",
    routes: [
    "subscription/cancel/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "subscription-create": {
    identifier: "subscription-create",
    prefix: "/subscription/create",
    group: "subscription",
    routes: [
    "subscription/create/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "subscription-renew": {
    identifier: "subscription-renew",
    prefix: "/subscription/renew",
    group: "subscription",
    routes: [
    "subscription/renew/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "task-templates": {
    identifier: "task-templates",
    prefix: "/task-templates",
    group: "task-templates",
    routes: [
    "task-templates/",
    "task-templates/<int:task_template_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\onboarding\\api\\urls.py"
    ],
  },
  "tasks": {
    identifier: "tasks",
    prefix: "/tasks",
    group: "tasks",
    routes: [
    "tasks/",
    "tasks/<int:lifecycle_task_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\onboarding\\api\\urls.py"
    ],
  },
  "teams": {
    identifier: "teams",
    prefix: "/teams",
    group: "teams",
    routes: [
    "api/teams/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "telemedicine": {
    identifier: "telemedicine",
    prefix: "/telemedicine",
    group: "telemedicine",
    routes: [
    "api/telemedicine/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "telemetry-ingest": {
    identifier: "telemetry-ingest",
    prefix: "/telemetry/ingest",
    group: "telemetry",
    routes: [
    "telemetry/ingest/"
    ],
    sources: [
    "backend\\apps\\device_platform\\api\\urls.py"
    ],
  },
  "templates": {
    identifier: "templates",
    prefix: "/templates",
    group: "templates",
    routes: [
    "templates/"
    ],
    sources: [
    "backend\\apps\\notes\\api\\urls.py"
    ],
  },
  "tenancy": {
    identifier: "tenancy",
    prefix: "/tenancy",
    group: "tenancy",
    routes: [
    "api/tenancy/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
  "tenants": {
    identifier: "tenants",
    prefix: "/tenants",
    group: "tenants",
    routes: [
    "tenants/",
    "tenants/<uuid:tenant_id>/"
    ],
    sources: [
    "backend\\apps\\platform\\tenancy\\api\\urls.py"
    ],
  },
  "tenants-create": {
    identifier: "tenants-create",
    prefix: "/tenants/create",
    group: "tenants",
    routes: [
    "tenants/create/"
    ],
    sources: [
    "backend\\apps\\platform\\tenancy\\api\\urls.py"
    ],
  },
  "tracking-sessions": {
    identifier: "tracking-sessions",
    prefix: "/tracking/sessions",
    group: "tracking",
    routes: [
    "tracking/sessions/",
    "tracking/sessions/<uuid:session_id>/",
    "tracking/sessions/<uuid:session_id>/locations/",
    "tracking/sessions/<uuid:session_id>/participants/",
    "tracking/sessions/<uuid:session_id>/stop/"
    ],
    sources: [
    "backend\\apps\\platform\\geography\\api\\geography\\urls.py"
    ],
  },
  "transactions": {
    identifier: "transactions",
    prefix: "/transactions",
    group: "transactions",
    routes: [
    "transactions/<uuid:transaction_id>/reverse/"
    ],
    sources: [
    "backend\\apps\\revenue_cycle\\accounts_receivable\\urls.py"
    ],
  },
  "types": {
    identifier: "types",
    prefix: "/types",
    group: "types",
    routes: [
    "types/",
    "types/<int:leave_type_id>/"
    ],
    sources: [
    "backend\\apps\\hr\\leave\\api\\urls.py"
    ],
  },
  "usage": {
    identifier: "usage",
    prefix: "/usage",
    group: "usage",
    routes: [
    "usage/",
    "usage/<uuid:pk>/charge/",
    "usage/<uuid:pk>/evaluate/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "usage-collect": {
    identifier: "usage-collect",
    prefix: "/usage/collect",
    group: "usage",
    routes: [
    "usage/collect/"
    ],
    sources: [
    "backend\\apps\\platform\\saas_billing\\api\\urls.py"
    ],
  },
  "user-roles": {
    identifier: "user-roles",
    prefix: "/user-roles",
    group: "user-roles",
    routes: [
    "user-roles/"
    ],
    sources: [
    "backend\\apps\\platform\\rbac\\api\\urls.py"
    ],
  },
  "users": {
    identifier: "users",
    prefix: "/users",
    group: "users",
    routes: [
    "users/"
    ],
    sources: [
    "backend\\apps\\platform\\accounts\\api\\urls.py"
    ],
  },
  "vitals": {
    identifier: "vitals",
    prefix: "/vitals",
    group: "vitals",
    routes: [
    "api/vitals/"
    ],
    sources: [
    "backend\\.datavionos_installer_backups\\20260917_121405\\config\\urls.py",
    "backend\\config\\urls.py"
    ],
  },
};

export function findModuleApiContract(
  identifier: string,
): ModuleApiContract | undefined {
  return MODULE_API_REGISTRY[identifier];
}

export function findModuleApiContractByPrefix(
  prefix: string,
): ModuleApiContract | undefined {
  return Object.values(MODULE_API_REGISTRY).find(
    (contract) => contract.prefix === prefix,
  );
}

export function listModuleApiContracts(): readonly ModuleApiContract[] {
  return Object.values(MODULE_API_REGISTRY);
}
