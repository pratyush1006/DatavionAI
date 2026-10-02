# DatavionAI Imaging / Radiology

Canonical domain: `apps.imaging`.

## Workflow

Order: `DRAFT -> ORDERED -> READY -> SCHEDULED -> IN_PROGRESS -> COMPLETED` with cancellation from operational states.

Study: `SCHEDULED -> ARRIVED -> READY -> ACQUIRING -> ACQUIRED -> PRELIMINARY -> FINAL`, with amendment support.

Report: `DRAFT -> PRELIMINARY -> FINAL`, with amendment/finalization support.

CECT: `CT ORDER -> CONTRAST SCREENING -> CONTRAST CLEARED -> CONTRAST ADMINISTERED -> ACQUISITION`. CECT cannot enter acquisition before contrast administration.

`workflow_registry.py` is authoritative. `workflows/` implements transitions. `models/workflow.py` persists the workflow cursor and immutable transition ledger. `orchestration/` coordinates handoffs.

No migrations are executed by the rebuild installer.
