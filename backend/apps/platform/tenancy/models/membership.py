"""
Tenant membership model.

Connects users with tenants.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class TenantMembership(
    BaseModel,
):
    """
    User membership inside a tenant.

    Represents the relationship between:

    User <----> Tenant
    """

    class Status(
        models.TextChoices,
    ):
        """
        Membership lifecycle.
        """

        ACTIVE = (
            "active",
            "Active",
        )

        INVITED = (
            "invited",
            "Invited",
        )

        SUSPENDED = (
            "suspended",
            "Suspended",
        )

        REMOVED = (
            "removed",
            "Removed",
        )

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_memberships",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    is_owner = models.BooleanField(
        default=False,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "platform_tenant_memberships"

        unique_together = (
            "tenant",
            "user",
        )

        ordering = ("-joined_at",)

    def __str__(
        self,
    ) -> str:

        return f"{self.user} @ {self.tenant}"
