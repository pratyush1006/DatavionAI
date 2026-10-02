"""
Audit logging utilities.

Provides reusable audit logging helpers for the DatavionAI
platform.

Business modules should never interact directly with the Python
logging package. They should emit audit events through
``log_audit_event()``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from apps.common.logging.constants import (
    EVENT_CATEGORY_FIELD,
    EVENT_NAME_FIELD,
    EVENT_TYPE_FIELD,
    ORGANIZATION_ID_FIELD,
    TENANT_ID_FIELD,
    USER_ID_FIELD,
)
from apps.common.logging.logger import (
    get_logger,
)

AUDIT_LOGGER_NAME = "audit"

DEFAULT_AUDIT_MESSAGE = "Audit event"


def get_audit_logger():
    """
    Return the audit logger instance.
    """

    return get_logger(
        AUDIT_LOGGER_NAME,
    )


def log_audit_event(
    *,
    action: str,
    resource: str,
    message: str = DEFAULT_AUDIT_MESSAGE,
    event_type: str = "APPLICATION",
    event_category: str = "GENERAL",
    success: bool = True,
    user_id: UUID | int | None = None,
    resource_id: UUID | int | None = None,
    organization_id: UUID | int | None = None,
    tenant_id: UUID | int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> None:
    """
    Emit a structured audit event.

    Args:
        action:
            Performed action.

        resource:
            Target resource.

        event_type:
            Audit event type.

        event_category:
            Audit category.

        success:
            Whether action succeeded.

        metadata:
            Additional structured metadata.
    """

    extra: dict[str, Any] = {
        EVENT_NAME_FIELD: action,
        EVENT_TYPE_FIELD: event_type,
        EVENT_CATEGORY_FIELD: event_category,
        "resource": resource,
        "resource_id": resource_id,
        "success": success,
        USER_ID_FIELD: user_id,
        ORGANIZATION_ID_FIELD: organization_id,
        TENANT_ID_FIELD: tenant_id,
    }

    if metadata:
        extra["metadata"] = dict(
            metadata,
        )

    get_audit_logger().info(
        message,
        extra=extra,
    )


__all__: tuple[str, ...] = (
    "AUDIT_LOGGER_NAME",
    "DEFAULT_AUDIT_MESSAGE",
    "get_audit_logger",
    "log_audit_event",
)
