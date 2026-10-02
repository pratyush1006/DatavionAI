"""
Department synchronization tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def synchronize_department(
    *,
    department_id: UUID,
) -> None:
    """
    Synchronize department with external systems.
    """

    logger.info(
        "Department synchronization started.",
        extra={
            "department_id": str(
                department_id,
            ),
        },
    )


__all__ = ("synchronize_department",)
