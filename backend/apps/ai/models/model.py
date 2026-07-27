"""
AI Model model.
"""

from __future__ import annotations

from django.db import models

from apps.ai.constants import DEFAULT_MODEL_STATUS, ModelStatus, ModelType
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class AIModel(BaseModel):
    """
    Represents a registered AI model within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="ai_models",
        help_text="Organization that owns the AI model.",
    )

    name = models.CharField(
        max_length=255,
        help_text="Human-readable model name.",
    )

    model_type = models.CharField(
        max_length=50,
        choices=ModelType.choices,
        help_text="Type of AI model.",
    )

    version = models.CharField(
        max_length=50,
        help_text="Model version identifier.",
    )

    status = models.CharField(
        max_length=20,
        choices=ModelStatus.choices,
        default=DEFAULT_MODEL_STATUS,
        db_index=True,
        help_text="Current deployment status.",
    )

    description = models.TextField(
        blank=True,
        help_text="Detailed model description.",
    )

    accuracy = models.FloatField(
        null=True,
        blank=True,
        help_text="Model accuracy metric.",
    )

    metadata = models.JSONField(
        default=dict,
        help_text="Arbitrary model metadata.",
    )

    class Meta:
        db_table = "ai_models"

        verbose_name = "AI Model"

        verbose_name_plural = "AI Models"

        ordering = (
            "name",
            "-version",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="ai_model_org_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "model_type",
                ],
                name="ai_model_org_type_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                    "version",
                ],
                name="unique_ai_model_per_org",
            ),
        ]

    def __str__(self) -> str:
        """
        Return the AI model display name.
        """

        return f"{self.name} v{self.version}"


__all__ = [
    "AIModel",
]
