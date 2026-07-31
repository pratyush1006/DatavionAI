"""
Document notification tasks.

Responsible for:

- User notifications
- Organization notifications
- Document lifecycle notifications
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def send_document_created_notification(
    *,
    document_id: UUID,
) -> None:
    """
    Notify document creation.
    """

    logger.info(
        "Document created notification queued.",
        extra={
            "document_id": str(
                document_id,
            ),
        },
    )


def send_document_updated_notification(
    *,
    document_id: UUID,
) -> None:
    """
    Notify document update.
    """

    logger.info(
        "Document updated notification queued.",
        extra={
            "document_id": str(
                document_id,
            ),
        },
    )


def send_document_deleted_notification(
    *,
    document_id: UUID,
) -> None:
    """
    Notify document deletion.
    """

    logger.info(
        "Document deleted notification queued.",
        extra={
            "document_id": str(
                document_id,
            ),
        },
    )


__all__ = (
    "send_document_created_notification",
    "send_document_updated_notification",
    "send_document_deleted_notification",
)
