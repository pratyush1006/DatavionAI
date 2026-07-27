"""
Subscription plan models.

Defines SaaS pricing tiers for DatavionOS.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class SubscriptionPlan(BaseModel):
    """
    SaaS subscription plan.

    Examples:
        Clinic Starter
        Clinic Professional
        Clinic Enterprise
    """

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    billing_cycle = models.CharField(
        max_length=50,
        default="monthly",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "subscription_plans"

        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
