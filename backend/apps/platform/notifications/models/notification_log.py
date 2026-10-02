"""
Notification log model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.notifications.constants import (
    NotificationProvider,
    NotificationStatus,
)
from apps.platform.notifications.managers import (
    NotificationLogManager,
)
from apps.platform.notifications.models.notification import Notification


class NotificationLog(BaseModel):
    """
    Audit log for notification delivery attempts.

    Every attempt to send a notification creates
    a NotificationLog record.
    """

    objects = NotificationLogManager()

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="logs",
        help_text="Notification associated with this log entry.",
    )

    attempt = models.PositiveSmallIntegerField(
        default=1,
        help_text="Delivery attempt number.",
    )

    provider = models.CharField(
        max_length=30,
        choices=NotificationProvider.choices,
        db_index=True,
        help_text="Notification provider used.",
    )

    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        db_index=True,
        help_text="Delivery status returned by the provider.",
    )

    provider_message_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text="Provider-specific message identifier.",
    )

    response = models.JSONField(
        default=dict,
        blank=True,
        help_text="Raw provider response payload.",
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional audit metadata.",
    )

    error_message = models.TextField(
        blank=True,
        help_text="Failure reason if delivery was unsuccessful.",
    )

    duration_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Delivery duration in milliseconds.",
    )

    class Meta:
        """
        Django model metadata.
        """

        db_table = "notification_logs"

        verbose_name = "Notification Log"

        verbose_name_plural = "Notification Logs"

        ordering = ("-created_at",)

        indexes = [
            #
            # Single-column indexes
            #
            models.Index(
                fields=["notification"],
                name="notlog_notif_idx",
            ),
            models.Index(
                fields=["provider"],
                name="notlog_provider_idx",
            ),
            models.Index(
                fields=["status"],
                name="notlog_status_idx",
            ),
            models.Index(
                fields=["attempt"],
                name="notlog_attempt_idx",
            ),
            models.Index(
                fields=["provider_message_id"],
                name="notlog_provmsg_idx",
            ),
            models.Index(
                fields=["created_at"],
                name="notlog_created_idx",
            ),
            #
            # Composite indexes
            #
            models.Index(
                fields=[
                    "notification",
                    "status",
                ],
                name="notlog_notif_stat_idx",
            ),
            models.Index(
                fields=[
                    "provider",
                    "status",
                ],
                name="notlog_prov_stat_idx",
            ),
            models.Index(
                fields=[
                    "notification",
                    "created_at",
                ],
                name="notlog_notif_cre_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "notification",
                    "attempt",
                ],
                name="unique_notification_attempt",
            ),
        ]

    @property
    def successful(
        self,
    ) -> bool:
        """
        Return whether the delivery succeeded.
        """

        return self.status in (
            NotificationStatus.SENT,
            NotificationStatus.DELIVERED,
        )

    @property
    def failed(
        self,
    ) -> bool:
        """
        Return whether the delivery failed.
        """

        return self.status == NotificationStatus.FAILED

    def __str__(
        self,
    ) -> str:
        """
        Return readable representation.
        """

        return (
            f"Notification "
            f"{self.notification_id} "
            f"Attempt {self.attempt} "
            f"({self.status})"
        )


__all__ = [
    "NotificationLog",
]
