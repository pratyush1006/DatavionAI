"""
Storage asset model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.storage.constants import (
    ASSET_CATEGORY_CHOICES,
    ASSET_CATEGORY_DOCUMENT,
    ASSET_STATUS_CHOICES,
    ASSET_STATUS_READY,
    ASSET_VISIBILITY_CHOICES,
    ASSET_VISIBILITY_PRIVATE,
    DEFAULT_STORAGE_PROVIDER,
    STORAGE_PROVIDER_CHOICES,
)


class Asset(BaseModel):
    """
    Represents a file stored by the platform.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="assets",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_assets",
    )

    folder = models.ForeignKey(
        "storage.Folder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets",
    )

    name = models.CharField(
        max_length=255,
    )

    original_name = models.CharField(
        max_length=255,
    )

    extension = models.CharField(
        max_length=20,
    )

    mime_type = models.CharField(
        max_length=100,
    )

    category = models.CharField(
        max_length=30,
        choices=ASSET_CATEGORY_CHOICES,
        default=ASSET_CATEGORY_DOCUMENT,
    )

    size = models.BigIntegerField()

    provider = models.CharField(
        max_length=20,
        choices=STORAGE_PROVIDER_CHOICES,
        default=DEFAULT_STORAGE_PROVIDER,
    )

    storage_key = models.CharField(
        max_length=512,
    )

    path = models.TextField()

    checksum = models.CharField(
        max_length=64,
        db_index=True,
    )

    visibility = models.CharField(
        max_length=20,
        choices=ASSET_VISIBILITY_CHOICES,
        default=ASSET_VISIBILITY_PRIVATE,
    )

    status = models.CharField(
        max_length=20,
        choices=ASSET_STATUS_CHOICES,
        default=ASSET_STATUS_READY,
    )

    class Meta:
        db_table = "storage_assets"

        verbose_name = "Asset"
        verbose_name_plural = "Assets"

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "storage_key",
                ],
                name="unique_storage_key_per_organization",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "category",
                ],
            ),
            models.Index(
                fields=[
                    "provider",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "checksum",
                ],
            ),
        ]

    def __str__(self) -> str:
        return self.original_name
