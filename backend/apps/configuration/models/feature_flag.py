"""
Feature flag model.
"""

from __future__ import annotations

from django.db import models

from apps.configuration.constants import (
    FEATURE_FLAG_CHOICES,
    FEATURE_FLAG_DISABLED,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)


class FeatureFlag(BaseModel):
    """
    Represents a platform feature flag.
    """

    objects = BaseManager()

    key = models.CharField(
        max_length=100,
        choices=FEATURE_FLAG_CHOICES,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    is_enabled = models.BooleanField(
        default=FEATURE_FLAG_DISABLED,
    )

    class Meta:
        db_table = "feature_flags"

        verbose_name = "Feature Flag"
        verbose_name_plural = "Feature Flags"

        ordering = ("name",)

        indexes = [
            models.Index(
                fields=[
                    "key",
                ],
            ),
            models.Index(
                fields=[
                    "is_enabled",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({'Enabled' if self.is_enabled else 'Disabled'})"
