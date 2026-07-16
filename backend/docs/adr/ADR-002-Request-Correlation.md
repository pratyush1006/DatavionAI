# ADR-002

## Decision

Every request receives a unique Request ID.

The Request ID is included in:

- Application Logs
- Audit Logs
- Error Logs
- HTTP Response Header

## Benefits

- Easier debugging
- Production tracing
- Future OpenTelemetry compatibility
