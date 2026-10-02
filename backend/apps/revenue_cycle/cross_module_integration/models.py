"""Persistent integration records for Revenue Cycle cross-module coordination."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.models import BaseModel

from .constants import IntegrationEventType, IntegrationRecordStatus, IntegrationSource


class RevenueCycleIntegrationRecord(BaseModel):
    """Persist an organization-scoped integration message and processing state."""

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="revenue_cycle_integration_records",
    )
    event_type = models.CharField(
        max_length=30,
        choices=IntegrationEventType.choices,
    )
    source = models.CharField(
        max_length=30,
        choices=IntegrationSource.choices,
    )
    event_name = models.CharField(max_length=150)
    aggregate_id = models.UUIDField()
    idempotency_key = models.CharField(max_length=200)
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20,
        choices=IntegrationRecordStatus.choices,
        default=IntegrationRecordStatus.PENDING,
        db_index=True,
    )
    attempts = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenue_cycle_integration_records",
    )

    class Meta:
        """Configure integration uniqueness and query indexes."""

        db_table = "revenue_cycle_integration_records"
        ordering = ("-created_at",)
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="unique_rc_integration_idempotency",
            ),
            models.CheckConstraint(
                condition=Q(attempts__gte=0),
                name="rc_integration_attempts_non_negative",
            ),
        )
        indexes = (
            models.Index(
                fields=("organization", "status", "created_at"),
                name="rc_integration_status_idx",
            ),
            models.Index(
                fields=("organization", "source", "created_at"),
                name="rc_integration_source_idx",
            ),
            models.Index(
                fields=("organization", "aggregate_id"),
                name="rc_integration_aggregate_idx",
            ),
        )

    def __str__(self) -> str:
        """Return a stable integration record label."""

        return f"{self.source}:{self.event_name}:{self.idempotency_key}"


__all__ = ("RevenueCycleIntegrationRecord",)
