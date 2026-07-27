"""
User tenant preference model.

Stores user's selected tenant context.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class UserTenantPreference(
    BaseModel,
):
    """
    Stores user's active tenant.

    Example:

    User:
        owner@apollo.com

    Active tenant:
        Apollo Clinic
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_preference",
    )

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="user_preferences",
    )

    class Meta:
        db_table = "platform_user_tenant_preferences"

        verbose_name = "User Tenant Preference"

        verbose_name_plural = "User Tenant Preferences"

    def __str__(
        self,
    ) -> str:

        return f"{self.user} -> {self.tenant}"


__all__ = ("UserTenantPreference",)
