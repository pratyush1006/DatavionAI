"""
Audit logging utilities for Datavion AI.

Business modules should never log directly.
Always use log_audit_event().
"""

from __future__ import annotations

import logging
from uuid import UUID

AUDIT_LOGGER_NAME = "audit"

audit_logger: logging.Logger = logging.getLogger(
    AUDIT_LOGGER_NAME,
)


def log_audit_event(
    *,
    action: str,
    resource: str,
    message: str,
    user_id: UUID | int | None = None,
    resource_id: UUID | int | None = None,
) -> None:
    """
    Log a structured audit event.
    """

    audit_logger.info(
        message,
        extra={
            "action": action,
            "resource": resource,
            "resource_id": resource_id,
            "user_id": user_id,
        },
    )


__all__ = [
    "log_audit_event",
]
