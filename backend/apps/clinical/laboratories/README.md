# DatavionAI Clinical Laboratories

Canonical laboratory/diagnostics domain: `apps.clinical.laboratories`.

Lifecycle: Canonical Appointment -> Laboratory Order -> Specimen -> Processing -> Result -> Verification -> Report Release.

Laboratories owns laboratory catalog, orders, specimens, processing, results, verification, reports and laboratory workflow. Appointments owns appointments and scheduling. Revenue Cycle owns charge capture, billing, claims, payments and AR. Documents owns document lifecycle. Storage owns durable object storage.

Order: ORDERED -> SCHEDULED -> COLLECTED -> PROCESSING -> VERIFIED -> RELEASED. Specimen: EXPECTED -> COLLECTED -> RECEIVED -> PROCESSING -> COMPLETED, with rejection. Result: PENDING -> PRELIMINARY -> FINAL, with correction.

`workflow_registry.py` is authoritative and `models/workflow.py` persists the workflow cursor and transition ledger.

The fresh rebuild installer never executes production migrations and never performs destructive production database operations.
