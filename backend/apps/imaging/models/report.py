"""
Report model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.imaging.constants import DEFAULT_REPORT_STATUS, ReportStatus
from apps.imaging.models.study import Study


class Report(BaseModel):
    """
    Represents a radiologist report for an imaging study.
    """

    objects = BaseManager()

    study = models.OneToOneField(
        Study,
        on_delete=models.CASCADE,
        related_name="report",
        help_text="Associated imaging study.",
    )

    report_text = models.TextField(
        help_text="Full report text.",
    )

    findings = models.TextField(
        blank=True,
        help_text="Key findings from the imaging study.",
    )

    impression = models.TextField(
        blank=True,
        help_text="Radiologist impression.",
    )

    recommendations = models.TextField(
        blank=True,
        help_text="Recommended follow-up actions.",
    )

    reported_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imaging_reports",
        help_text="Employee who authored the report.",
    )

    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=DEFAULT_REPORT_STATUS,
        db_index=True,
        help_text="Current report status.",
    )

    class Meta:
        db_table = "imaging_reports"

        verbose_name = "Imaging Report"

        verbose_name_plural = "Imaging Reports"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "study",
                    "status",
                ],
                name="img_report_study_stat_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the report display name.
        """

        return f"Report for {self.study}"


__all__ = [
    "Report",
]
