"""
Feature entitlement models.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel

from .plan import SubscriptionPlan


class FeatureEntitlement(BaseModel):
    """
    Controls SaaS feature flags.
    """

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="feature_entitlements",
    )

    feature_key = models.CharField(
        max_length=100,
    )

    enabled = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "feature_entitlements"

        unique_together = (
            "plan",
            "feature_key",
        )

    def __str__(self):

        return self.feature_key
