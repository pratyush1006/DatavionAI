"""
Notification model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.platform.notifications.constants import (
    DEFAULT_CHANNEL,
    DEFAULT_PRIORITY,
    DEFAULT_PROVIDER,
    NotificationChannel,
    NotificationPriority,
    NotificationProvider,
    NotificationStatus,
)
from apps.platform.notifications.managers import (
    NotificationManager,
)


class Notification(BaseModel):
    """
    Master notification record.

    Represents a notification to be delivered through one
    of the supported notification channels.
    """

    objects = NotificationManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
        help_text="Associated platform user.",
    )

    recipient = models.CharField(
        max_length=255,
        db_index=True,
        help_text=("Destination email address, phone number, or push device token."),
    )

    recipient_name = models.CharField(
        max_length=255,
        blank=True,
    )

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
        default=DEFAULT_CHANNEL,
        db_index=True,
    )

    provider = models.CharField(
        max_length=30,
        choices=NotificationProvider.choices,
        default=DEFAULT_PROVIDER,
        db_index=True,
    )

    priority = models.IntegerField(
        choices=NotificationPriority.choices,
        default=DEFAULT_PRIORITY,
        db_index=True,
    )

    template = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Notification template identifier.",
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
    )

    context = models.JSONField(
        default=dict,
        blank=True,
        help_text="Template rendering context.",
    )

    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        db_index=True,
    )

    provider_message_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    provider_response = models.JSONField(
        default=dict,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    retry_count = models.PositiveSmallIntegerField(
        default=0,
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    queued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional provider metadata.",
    )

    class Meta:
        """
        Django model metadata.
        """

        db_table = "notifications"

        verbose_name = "Notification"

        verbose_name_plural = "Notifications"

        ordering = ("-created_at",)

        indexes = [
            #
            # Single-column indexes
            #
            models.Index(
                fields=["user"],
                name="notif_user_idx",
            ),
            models.Index(
                fields=["recipient"],
                name="notif_recipient_idx",
            ),
            models.Index(
                fields=["channel"],
                name="notif_channel_idx",
            ),
            models.Index(
                fields=["provider"],
                name="notif_provider_idx",
            ),
            models.Index(
                fields=["status"],
                name="notif_status_idx",
            ),
            models.Index(
                fields=["priority"],
                name="notif_priority_idx",
            ),
            models.Index(
                fields=["scheduled_at"],
                name="notif_scheduled_idx",
            ),
            models.Index(
                fields=["queued_at"],
                name="notif_queued_idx",
            ),
            models.Index(
                fields=["sent_at"],
                name="notif_sent_idx",
            ),
            models.Index(
                fields=["created_at"],
                name="notif_created_idx",
            ),
            #
            # Composite indexes
            #
            models.Index(
                fields=[
                    "channel",
                    "status",
                ],
                name="notif_ch_status_idx",
            ),
            models.Index(
                fields=[
                    "provider",
                    "status",
                ],
                name="notif_prv_status_idx",
            ),
            models.Index(
                fields=[
                    "user",
                    "status",
                ],
                name="notif_usr_status_idx",
            ),
            #
            # Celery / scheduled delivery
            #
            models.Index(
                fields=[
                    "status",
                    "scheduled_at",
                ],
                name="notif_stat_sched_idx",
            ),
            #
            # Priority queue
            #
            models.Index(
                fields=[
                    "status",
                    "priority",
                ],
                name="notif_stat_prio_idx",
            ),
            models.Index(
                fields=[
                    "channel",
                    "priority",
                ],
                name="notif_ch_prio_idx",
            ),
        ]

    @property
    def is_pending(
        self,
    ) -> bool:
        """
        Return whether the notification is pending.
        """

        return self.status == NotificationStatus.PENDING

    @property
    def is_sent(
        self,
    ) -> bool:
        """
        Return whether the notification has been sent.
        """

        return self.status == NotificationStatus.SENT

    @property
    def is_failed(
        self,
    ) -> bool:
        """
        Return whether the notification has failed.
        """

        return self.status == NotificationStatus.FAILED

    def mark_queued(
        self,
    ) -> None:
        """
        Mark the notification as queued.
        """

        self.status = NotificationStatus.QUEUED
        self.queued_at = timezone.now()

        self.save(
            update_fields=[
                "status",
                "queued_at",
                "updated_at",
            ],
        )

    def mark_sent(
        self,
        *,
        provider_message_id: str = "",
    ) -> None:
        """
        Mark the notification as sent.
        """

        self.status = NotificationStatus.SENT
        self.sent_at = timezone.now()

        if provider_message_id:
            self.provider_message_id = provider_message_id

        self.save(
            update_fields=[
                "status",
                "sent_at",
                "provider_message_id",
                "updated_at",
            ],
        )

    def mark_delivered(
        self,
    ) -> None:
        """
        Mark the notification as delivered.
        """

        self.status = NotificationStatus.DELIVERED
        self.delivered_at = timezone.now()

        self.save(
            update_fields=[
                "status",
                "delivered_at",
                "updated_at",
            ],
        )

    def mark_failed(
        self,
        *,
        error_message: str,
    ) -> None:
        """
        Mark the notification as failed.
        """

        self.status = NotificationStatus.FAILED
        self.failed_at = timezone.now()
        self.error_message = error_message
        self.retry_count += 1

        self.save(
            update_fields=[
                "status",
                "failed_at",
                "error_message",
                "retry_count",
                "updated_at",
            ],
        )

    def __str__(
        self,
    ) -> str:
        """
        Return a readable representation.
        """

        return f"{self.channel} → {self.recipient} ({self.status})"


__all__ = [
    "Notification",
]
