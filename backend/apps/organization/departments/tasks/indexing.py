"""
Department search indexing tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def index_department(
    *,
    department_id: UUID,
) -> None:
    """
    Index department in search engine.
    """

    logger.info(
        "Department indexing started.",
        extra={
            "department_id": str(
                department_id,
            ),
        },
    )


def remove_department_index(
    *,
    department_id: UUID,
) -> None:
    """
    Remove department from search index.
    """

    logger.info(
        "Department index removal started.",
        extra={
            "department_id": str(
                department_id,
            ),
        },
    )


__all__ = (
    "index_department",
    "remove_department_index",
)
