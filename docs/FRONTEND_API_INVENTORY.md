# DatavionAI Frontend/API Inventory

## Source of truth

This inventory is based on Django's active runtime URL resolver (`config.urls` and its included URLConfs), not archived installer scripts or generated OpenAPI snapshots. On 2026-09-30 the resolver exposed **465 API URL patterns under 45 `/api/` prefixes**. A pattern may support multiple HTTP methods; the count is URL patterns, not operation count.

## Active API families

| Prefix | URL patterns | Frontend capability |
| --- | ---: | --- |
| `/api/ai/` | 13 | AI chat and clinical AI |
| `/api/ai-control/` | 2 | AI application controls |
| `/api/allergies/` | 2 | Allergies |
| `/api/appointments/` | 8 | Appointments |
| `/api/audit/` | 2 | Audit events |
| `/api/auth/` | 14 | Login/OTP, registration, verification, password and OAuth |
| `/api/billing/` | 3 | Finance billing alias |
| `/api/compliance/` | 3 | Consent and PHI access logs |
| `/api/configuration/` | 2 | Platform configuration |
| `/api/departments/` | 2 | Departments |
| `/api/device-platform/` | 5 | Device platform |
| `/api/diagnoses/` | 2 | Diagnoses |
| `/api/docs/` | 1 | Swagger UI |
| `/api/documents/` | 2 | Document list/detail |
| `/api/employees/` | 8 | Employee lifecycle |
| `/api/encounters/` | 3 | Encounters |
| `/api/finance/` | 3 | Canonical finance alias |
| `/api/geography/` | 9 | Countries, regions, cities, location, tracking |
| `/api/hospital-operations/` | 10 | Hospital operations |
| `/api/hr/` | 41 | HR, payroll, leave, shifts, onboarding, reviews |
| `/api/imaging/` | 2 | Imaging health and contract |
| `/api/insurance/` | 25 | Insurance resources and route resolution |
| `/api/interoperability/` | 6 | FHIR and HL7 |
| `/api/laboratories/` | 23 | Laboratory workflows |
| `/api/medications/` | 2 | Medications |
| `/api/notes/` | 5 | Clinical notes and templates |
| `/api/notifications/` | 7 | Notifications |
| `/api/onboarding/` | 8 | Registration catalogs, plans, signup, status |
| `/api/organization-access/` | 5 | Organization access control |
| `/api/organization-control/` | 3 | Effective module/feature controls |
| `/api/organizations/` | 10 | Organization catalogs, CRUD, hierarchy, branding |
| `/api/patient-management/` | 96 | Patient profiles, registration, contacts, documents, history, timeline, consent, family |
| `/api/pharmacy/` | 15 | Pharmacy and inventory workflows |
| `/api/platform/` | 2 | Runtime bootstrap and effective capability context |
| `/api/prescriptions/` | 3 | Prescriptions |
| `/api/providers/` | 2 | Providers |
| `/api/rbac/` | 14 | Roles, permissions, assignments and hierarchy |
| `/api/revenue-cycle/` | 48 | Charges, claims, billing, denials, eligibility, analytics |
| `/api/saas-billing/` | 34 | Plans, subscriptions, invoices, payments, usage, billing account |
| `/api/schema/` | 1 | OpenAPI schema |
| `/api/search/` | 1 | Search |
| `/api/teams/` | 2 | Teams |
| `/api/telemedicine/` | 9 | Sessions, participants, recordings |
| `/api/tenancy/` | 5 | Tenant memberships and selection |
| `/api/vitals/` | 2 | Vitals |

## Canonical runtime flow

- Public signup: `/api/onboarding/catalog/`, `/api/onboarding/plans/`, `/api/onboarding/signup/preflight/`, `/api/onboarding/signup/`.
- Tenant selector: `/api/tenancy/my-tenants/` and `POST /api/tenancy/select/`.
- Authenticated runtime: `/api/platform/bootstrap/` returns tenant, organization, subscription, entitlements, effective permissions, modules, navigation and dashboard cards.
- Organization controls: `/api/organization-control/` snapshot and module/feature toggles; `/api/organization-access/` access assignments.
- Shared authenticated API requests carry `Authorization`, `X-Tenant-ID`, `X-Organization-ID`, and `X-Request-ID` through the canonical frontend API client. Backend authorization remains authoritative.

## Frontend integration status

Connected shared flows include authentication, public organization registration, runtime bootstrap/dashboard/navigation, and tenant switching. Feature routes/services also exist for patients, appointments, documents, employees, and notes. The rest of the mounted APIs remain candidates for incremental module UI work; routes should consume their domain services and bootstrap authorization rather than constructing raw URLs or hardcoding module availability.

## Signup/free-tier regression

The existing seeded plan catalog is consumed through `/api/onboarding/plans/`; frontend tests must not replace its data or reduce catalog expectations. A zero-price plan with `trial_days=0` is an active, open-ended free subscription, not an immediately expired trial. Positive-duration trials retain their finite trial period.
