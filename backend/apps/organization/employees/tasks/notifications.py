"""
Employee notification tasks.

Responsible for:

- Employee notifications
- HR notifications
- Workflow notifications
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def send_employee_created_notification(
    *,
    employee_id: UUID,
) -> None:
    """
    Notify employee creation.
    """

    logger.info(
        "Employee created notification queued.",
        extra={
            "employee_id": str(
                employee_id,
            ),
        },
    )


def send_employee_updated_notification(
    *,
    employee_id: UUID,
) -> None:
    """
    Notify employee update.
    """

    logger.info(
        "Employee updated notification queued.",
        extra={
            "employee_id": str(
                employee_id,
            ),
        },
    )


def send_employee_status_changed_notification(
    *,
    employee_id: UUID,
) -> None:
    """
    Notify employee status change.
    """

    logger.info(
        "Employee status notification queued.",
        extra={
            "employee_id": str(
                employee_id,
            ),
        },
    )


__all__ = (
    "send_employee_created_notification",
    "send_employee_updated_notification",
    "send_employee_status_changed_notification",
)
