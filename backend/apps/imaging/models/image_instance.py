"""
ImageInstance model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.imaging.models.series import Series


class ImageInstance(BaseModel):
    """
    Represents a single image instance within a series.
    """

    objects = BaseManager()

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name="image_instances",
        help_text="Parent series.",
    )

    sop_instance_uid = models.CharField(
        max_length=255,
        unique=True,
        help_text="DICOM SOP Instance UID.",
    )

    instance_number = models.PositiveIntegerField(
        help_text="Instance number within the series.",
    )

    rows = models.PositiveIntegerField(
        help_text="Number of rows in the image.",
    )

    columns = models.PositiveIntegerField(
        help_text="Number of columns in the image.",
    )

    bits_allocated = models.PositiveSmallIntegerField(
        help_text="Number of bits allocated for each pixel sample.",
    )

    storage_path = models.CharField(
        max_length=500,
        help_text="Path to the stored image file.",
    )

    thumbnail_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Path to the thumbnail image file.",
    )

    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="File size in bytes.",
    )

    class Meta:
        db_table = "imaging_image_instances"

        verbose_name = "Image Instance"

        verbose_name_plural = "Image Instances"

        ordering = (
            "series",
            "instance_number",
        )

        indexes = [
            models.Index(
                fields=[
                    "series",
                    "instance_number",
                ],
                name="img_inst_series_num_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the image instance display name.
        """

        return f"{self.series} - Instance {self.instance_number}"


__all__ = [
    "ImageInstance",
]
