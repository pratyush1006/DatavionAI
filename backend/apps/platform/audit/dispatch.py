"""
Audit dispatch utilities.

This module provides a centralized dispatch layer for audit events.

Currently audit events are written synchronously through
AuditService. In the future this module can be extended to:

- Dispatch Celery tasks
- Publish domain events
- Push audit events to Kafka
- Stream events to SIEM systems
- Forward events to OpenTelemetry
"""

from __future__ import annotations

from apps.platform.audit.services import AuditService


def dispatch_audit_event(
    **kwargs,
):
    """
    Dispatch an audit event.

    Currently delegates directly to AuditService.
    """

    return AuditService.log_event(
        **kwargs,
    )


__all__ = [
    "dispatch_audit_event",
]
