"""
Tenant subscription models.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.platform.tenancy.models import (
    Tenant,
)

from .plan import (
    SubscriptionPlan,
)


class TenantSubscription(BaseModel):
    """
    Active subscription assigned to tenant.
    """

    class Status(models.TextChoices):
        ACTIVE = (
            "active",
            "Active",
        )

        CANCELLED = (
            "cancelled",
            "Cancelled",
        )

        EXPIRED = (
            "expired",
            "Expired",
        )

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    auto_renew = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "tenant_subscriptions"

    def __str__(self):

        return f"{self.tenant} - {self.plan}"
