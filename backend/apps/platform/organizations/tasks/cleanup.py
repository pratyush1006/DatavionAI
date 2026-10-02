"""
Background cleanup tasks for organizations.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

logger = logging.getLogger(__name__)

ORGANIZATION_RETENTION_DAYS = 90


def cleanup_deleted_organizations() -> None:
    """
    Permanently remove organizations that have exceeded the
    configured retention period.

    Actual deletion should be implemented once the repository/service
    layer for organization cleanup is available.
    """
    cutoff = datetime.now(UTC) - timedelta(
        days=ORGANIZATION_RETENTION_DAYS,
    )

    logger.info(
        "Organization cleanup started.",
        extra={
            "cutoff": cutoff.isoformat(),
        },
    )


def cleanup_expired_invitations() -> None:
    """
    Remove expired organization invitations.

    Invitation management belongs to the Tenancy module.
    This task remains as a placeholder until the tenancy
    cleanup service is available.
    """
    logger.info(
        "Expired organization invitation cleanup started.",
    )


def cleanup_orphaned_records() -> None:
    """
    Remove orphaned organization-related records.

    Examples include branding, settings, or profile records
    that no longer have a valid organization.
    """
    logger.info(
        "Organization orphan cleanup started.",
    )


__all__: tuple[str, ...] = (
    "cleanup_deleted_organizations",
    "cleanup_expired_invitations",
    "cleanup_orphaned_records",
)
