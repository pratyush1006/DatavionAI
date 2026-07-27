"""
Recommendation model.
"""

from __future__ import annotations

from django.db import models

from apps.ai.constants import (
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
)
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Recommendation(BaseModel):
    """
    Represents an AI-generated clinical recommendation.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="Organization that owns the recommendation.",
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="Patient associated with the recommendation.",
    )

    recommendation_type = models.CharField(
        max_length=50,
        choices=RecommendationType.choices,
        help_text="Type of recommendation.",
    )

    title = models.CharField(
        max_length=255,
        help_text="Short recommendation title.",
    )

    description = models.TextField(
        help_text="Detailed recommendation description.",
    )

    confidence_score = models.FloatField(
        null=True,
        blank=True,
        help_text="AI confidence score.",
    )

    source = models.CharField(
        max_length=255,
        blank=True,
        help_text="Source of the recommendation (AI model or rule engine).",
    )

    status = models.CharField(
        max_length=20,
        choices=RecommendationStatus.choices,
        default=RecommendationStatus.PENDING,
        db_index=True,
        help_text="Recommendation status.",
    )

    priority = models.CharField(
        max_length=20,
        choices=RecommendationPriority.choices,
        default=RecommendationPriority.MEDIUM,
        help_text="Recommendation priority.",
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the recommendation expires.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the recommendation was created.",
    )

    class Meta:
        db_table = "recommendations"

        verbose_name = "Recommendation"

        verbose_name_plural = "Recommendations"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="recommendation_org_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "recommendation_type",
                ],
                name="recommendation_org_type_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "status",
                ],
                name="rec_patient_status_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "priority",
                ],
                name="rec_patient_priority_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "priority",
                ],
                name="rec_org_priority_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Return the recommendation display string.
        """

        return f"{self.title} - {self.status}"


__all__ = [
    "Recommendation",
]
