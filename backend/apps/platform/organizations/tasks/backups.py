"""
Organization backup tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def backup_organization(
    *,
    organization_id: UUID,
) -> None:
    """
    Create a backup for an organization.
    """
    logger.info(
        "Organization backup started.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def restore_organization_backup(
    *,
    organization_id: UUID,
) -> None:
    """
    Restore an organization backup.
    """
    logger.info(
        "Organization backup restoration started.",
        extra={
            "organization_id": str(organization_id),
        },
    )


__all__: tuple[str, ...] = (
    "backup_organization",
    "restore_organization_backup",
)
