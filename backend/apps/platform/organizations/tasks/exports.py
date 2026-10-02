"""
Organization export tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def export_organization(
    *,
    organization_id: UUID,
    export_format: str = "csv",
) -> None:
    """
    Export an organization.

    Supported formats (future):

    - CSV
    - Excel
    - PDF
    - JSON
    """
    logger.info(
        "Organization export started.",
        extra={
            "organization_id": str(organization_id),
            "format": export_format,
        },
    )


def export_all_organizations(
    *,
    export_format: str = "csv",
) -> None:
    """
    Export all organizations.
    """
    logger.info(
        "Bulk organization export started.",
        extra={
            "format": export_format,
        },
    )


__all__: tuple[str, ...] = (
    "export_all_organizations",
    "export_organization",
)
