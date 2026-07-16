"""
Audit logging utilities for the Datavion AI platform.

Business modules should never log directly.
Always use ``log_audit_event()``.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any
from uuid import UUID

AUDIT_LOGGER_NAME = "audit"

DEFAULT_AUDIT_MESSAGE = "Audit event"

audit_logger = logging.getLogger(
    AUDIT_LOGGER_NAME,
)


def log_audit_event(
    *,
    action: str,
    resource: str,
    message: str = DEFAULT_AUDIT_MESSAGE,
    user_id: UUID | int | None = None,
    resource_id: UUID | int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> None:
    """
    Log a structured audit event.
    """

    extra: dict[str, Any] = {
        "action": action,
        "resource": resource,
        "resource_id": resource_id,
        "user_id": user_id,
    }

    if metadata is not None:
        extra.update(metadata)

    audit_logger.info(
        message,
        extra=extra,
    )


__all__ = [
    "log_audit_event",
]
