"""
Series model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.imaging.models.study import Study


class Series(BaseModel):
    """
    Represents a series within an imaging study.
    """

    objects = BaseManager()

    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        related_name="series",
        help_text="Parent imaging study.",
    )

    series_instance_uid = models.CharField(
        max_length=255,
        unique=True,
        help_text="DICOM Series Instance UID.",
    )

    series_number = models.PositiveIntegerField(
        help_text="Series number within the study.",
    )

    modality = models.CharField(
        max_length=10,
        help_text="DICOM modality.",
    )

    series_description = models.TextField(
        blank=True,
        help_text="Description of the series.",
    )

    number_of_instances = models.PositiveIntegerField(
        default=0,
        help_text="Number of image instances in this series.",
    )

    class Meta:
        db_table = "imaging_series"

        verbose_name = "Imaging Series"

        verbose_name_plural = "Imaging Series"

        ordering = (
            "study",
            "series_number",
        )

        indexes = [
            models.Index(
                fields=[
                    "study",
                    "series_number",
                ],
                name="img_series_study_num_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the series display name.
        """

        return f"{self.study} - Series {self.series_number}"


__all__ = [
    "Series",
]
