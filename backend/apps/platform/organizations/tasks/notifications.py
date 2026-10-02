"""
Background notification tasks for organizations.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def send_organization_created_notification(
    *,
    organization_id: UUID,
) -> None:
    """
    Send notifications after an organization has been created.
    """

    logger.info(
        "Organization created notification scheduled.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def send_organization_verified_notification(
    *,
    organization_id: UUID,
) -> None:
    """
    Send notifications after an organization has been verified.
    """

    logger.info(
        "Organization verified notification scheduled.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def send_organization_suspended_notification(
    *,
    organization_id: UUID,
    reason: str | None = None,
) -> None:
    """
    Send notifications after an organization has been suspended.
    """

    logger.info(
        "Organization suspended notification scheduled.",
        extra={
            "organization_id": str(organization_id),
            "reason": reason,
        },
    )


def send_organization_activated_notification(
    *,
    organization_id: UUID,
) -> None:
    """
    Send notifications after an organization has been activated.
    """

    logger.info(
        "Organization activated notification scheduled.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def send_organization_deactivated_notification(
    *,
    organization_id: UUID,
) -> None:
    """
    Send notifications after an organization has been deactivated.
    """

    logger.info(
        "Organization deactivated notification scheduled.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def send_organization_restored_notification(
    *,
    organization_id: UUID,
) -> None:
    """
    Send notifications after an organization has been restored.
    """

    logger.info(
        "Organization restored notification scheduled.",
        extra={
            "organization_id": str(organization_id),
        },
    )


__all__: tuple[str, ...] = (
    "send_organization_activated_notification",
    "send_organization_created_notification",
    "send_organization_deactivated_notification",
    "send_organization_restored_notification",
    "send_organization_suspended_notification",
    "send_organization_verified_notification",
)
