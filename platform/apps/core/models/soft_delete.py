"""
Reusable soft delete model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from .managers import (
    AllObjectsManager,
    DeletedObjectsManager,
    SoftDeleteManager,
)


class SoftDeleteModel(models.Model):
    """
    Abstract model implementing soft delete functionality.

    Instead of permanently deleting records, models inheriting
    from this class are marked as deleted and can be restored.
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deleted_%(class)ss",
    )

    objects = SoftDeleteManager()

    all_objects = AllObjectsManager()

    deleted_objects = DeletedObjectsManager()

    class Meta:
        abstract = True

    def soft_delete(
        self,
        *,
        user=None,
    ) -> None:
        """
        Soft delete this object.
        """

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by",
            ],
        )

    def restore(self) -> None:
        """
        Restore a previously deleted object.
        """

        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by",
            ],
        )

    def hard_delete(
        self,
    ) -> tuple[int, dict[str, int]]:
        """
        Permanently delete this object.
        """

        return super().delete()
