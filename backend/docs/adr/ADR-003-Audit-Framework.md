# ADR-003

## Decision

All audit events are written through:

log_audit_event()

Business modules never log audit events directly.

## Benefits

- Centralized auditing
- Easier maintenance
- Future database-backed audit trail
