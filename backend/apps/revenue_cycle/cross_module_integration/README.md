# Revenue Cycle — RC14 Cross-Module Integration

Cross-module integration foundation for Revenue Cycle.

The bounded context provides:
- organization-scoped integration envelopes
- idempotent ingestion
- explicit processing state
- row-locked processing
- platform RBAC
- explicit tenant and organization context
- workflow and policy enforcement
- after-commit domain events
- immutable historical integration records
- API and admin access

RC14 intentionally does not own a Patient model and does not generate migrations.
