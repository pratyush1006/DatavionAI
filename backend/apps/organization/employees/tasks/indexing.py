"""
Employee indexing tasks.

Responsible for:

- Search indexing
- Employee discovery
- External search synchronization
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def index_employee(
    *,
    employee_id: UUID,
) -> None:
    """
    Index employee.

    Future integration:

    - Elasticsearch
    - OpenSearch
    - AI semantic search
    """

    logger.info(
        "Employee indexing requested.",
        extra={
            "employee_id": str(
                employee_id,
            ),
        },
    )


__all__ = ("index_employee",)
