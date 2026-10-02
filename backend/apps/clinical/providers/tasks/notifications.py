"""
Provider notification tasks.

Responsible for:

- Provider notifications
- Clinical operation notifications
- Workflow notifications
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def send_provider_created_notification(
    *,
    provider_id: UUID,
) -> None:
    """
    Notify provider creation.
    """

    logger.info(
        "Provider created notification queued.",
        extra={
            "provider_id": str(
                provider_id,
            ),
        },
    )


def send_provider_updated_notification(
    *,
    provider_id: UUID,
) -> None:
    """
    Notify provider update.
    """

    logger.info(
        "Provider updated notification queued.",
        extra={
            "provider_id": str(
                provider_id,
            ),
        },
    )


def send_provider_status_changed_notification(
    *,
    provider_id: UUID,
) -> None:
    """
    Notify provider lifecycle status change.
    """

    logger.info(
        "Provider status notification queued.",
        extra={
            "provider_id": str(
                provider_id,
            ),
        },
    )


__all__ = (
    "send_provider_created_notification",
    "send_provider_updated_notification",
    "send_provider_status_changed_notification",
)
