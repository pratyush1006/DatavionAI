"""
Module entitlement models.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel

from .plan import SubscriptionPlan


class ModuleEntitlement(BaseModel):
    """
    Controls DatavionOS module availability.
    """

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="module_entitlements",
    )

    module_identifier = models.CharField(
        max_length=100,
    )

    enabled = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "module_entitlements"

        unique_together = (
            "plan",
            "module_identifier",
        )

    def __str__(self):

        return self.module_identifier
