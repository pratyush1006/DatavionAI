"""
Organization reporting tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def generate_organization_report(
    *,
    organization_id: UUID,
) -> None:
    """
    Generate an organization report.

    Future report types:

    - Usage
    - Subscription
    - Operational
    - Compliance
    - Audit
    """
    logger.info(
        "Organization report generation started.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def generate_daily_reports() -> None:
    """
    Generate scheduled daily reports.
    """
    logger.info(
        "Daily organization reporting started.",
    )


__all__: tuple[str, ...] = (
    "generate_daily_reports",
    "generate_organization_report",
)
