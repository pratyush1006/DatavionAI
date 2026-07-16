"""
Storage folder model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import (
    BaseManager,
    BaseModel,
)


class Folder(BaseModel):
    """
    Represents a logical folder for organizing storage assets.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="storage_folders",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "storage_folders"

        verbose_name = "Folder"
        verbose_name_plural = "Folders"

        ordering = ("name",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "parent",
                    "name",
                ],
                name="unique_folder_per_parent",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                ],
            ),
            models.Index(
                fields=[
                    "parent",
                ],
            ),
        ]

    def __str__(self) -> str:
        return self.full_path

    @property
    def full_path(self) -> str:
        """
        Return the complete folder path.
        """

        if self.parent is None:
            return self.name

        return f"{self.parent.full_path}/{self.name}"
