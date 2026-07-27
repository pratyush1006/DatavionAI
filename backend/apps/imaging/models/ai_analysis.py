"""
AIAnalysis model.
"""

from __future__ import annotations

from django.db import models

from apps.ai.models import AIModel
from apps.core.models import BaseManager, BaseModel
from apps.imaging.constants import AIAnalysisType
from apps.imaging.models.study import Study


class AIAnalysis(BaseModel):
    """
    Represents an AI-assisted analysis of an imaging study.
    """

    objects = BaseManager()

    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        related_name="ai_analyses",
        help_text="Imaging study analyzed by the AI model.",
    )

    ai_model = models.ForeignKey(
        AIModel,
        on_delete=models.CASCADE,
        related_name="ai_analyses",
        help_text="AI model used for analysis.",
    )

    analysis_type = models.CharField(
        max_length=50,
        choices=AIAnalysisType.choices,
        help_text="Type of AI analysis performed.",
    )

    input_image_ids = models.JSONField(
        default=list,
        blank=True,
        help_text="List of ImageInstance IDs used as input.",
    )

    result = models.JSONField(
        default=dict,
        blank=True,
        help_text="Full analysis result payload.",
    )

    confidence_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Model confidence score.",
    )

    findings = models.JSONField(
        default=list,
        blank=True,
        help_text="List of findings detected by the AI model.",
    )

    is_reviewed = models.BooleanField(
        default=False,
        help_text="Whether the analysis has been reviewed by a radiologist.",
    )

    reviewed_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_ai_analyses",
        help_text="Employee who reviewed the analysis.",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the analysis was reviewed.",
    )

    class Meta:
        db_table = "imaging_ai_analyses"

        verbose_name = "AI Analysis"

        verbose_name_plural = "AI Analyses"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "study",
                    "analysis_type",
                ],
                name="imaging_ai_study_type_idx",
            ),
            models.Index(
                fields=[
                    "ai_model",
                    "created_at",
                ],
                name="imaging_ai_model_created_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the AI analysis display name.
        """

        return f"AI Analysis for {self.study} ({self.get_analysis_type_display()})"


__all__ = [
    "AIAnalysis",
]
