"""
Department notification tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def send_department_created_notification(
    *,
    department_id: UUID,
) -> None:
    """
    Notify users when department is created.
    """

    logger.info(
        "Department created notification scheduled.",
        extra={
            "department_id": str(
                department_id,
            ),
        },
    )


def send_department_updated_notification(
    *,
    department_id: UUID,
) -> None:
    """
    Notify users when department is updated.
    """

    logger.info(
        "Department updated notification scheduled.",
        extra={
            "department_id": str(
                department_id,
            ),
        },
    )


def send_department_deleted_notification(
    *,
    department_id: UUID,
) -> None:
    """
    Notify users when department is deleted.
    """

    logger.info(
        "Department deleted notification scheduled.",
        extra={
            "department_id": str(
                department_id,
            ),
        },
    )


def send_department_member_assigned_notification(
    *,
    department_id: UUID,
    employee_id: UUID,
) -> None:
    """
    Notify employee assignment.
    """

    logger.info(
        "Department member assignment notification scheduled.",
        extra={
            "department_id": str(
                department_id,
            ),
            "employee_id": str(
                employee_id,
            ),
        },
    )


__all__ = (
    "send_department_created_notification",
    "send_department_updated_notification",
    "send_department_deleted_notification",
    "send_department_member_assigned_notification",
)
