"""
Configuration model.
"""

from __future__ import annotations

from django.db import models

from apps.configuration.constants import (
    CONFIGURATION_CATEGORY_CHOICES,
    CONFIGURATION_CATEGORY_GENERAL,
    CONFIGURATION_TYPE_CHOICES,
    CONFIGURATION_TYPE_STRING,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)


class Configuration(BaseModel):
    """
    Represents a configurable platform setting.
    """

    objects = BaseManager()

    key = models.CharField(
        max_length=100,
        unique=True,
    )

    category = models.CharField(
        max_length=30,
        choices=CONFIGURATION_CATEGORY_CHOICES,
        default=CONFIGURATION_CATEGORY_GENERAL,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    value = models.TextField()

    value_type = models.CharField(
        max_length=20,
        choices=CONFIGURATION_TYPE_CHOICES,
        default=CONFIGURATION_TYPE_STRING,
    )

    is_editable = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "configurations"

        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"

        ordering = (
            "category",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "category",
                ],
            ),
            models.Index(
                fields=[
                    "key",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"
