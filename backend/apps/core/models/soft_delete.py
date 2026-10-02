"""
Reusable soft delete model.

Provides recoverable deletion support for DatavionOS
business entities.
"""

from __future__ import annotations

from typing import Any

from django.db import models, transaction
from django.utils import timezone

from .managers import (
    AllObjectsManager,
    DeletedObjectsManager,
    SoftDeleteManager,
)

type DeleteResult = tuple[int, dict[str, int]]


class SoftDeleteModel(
    models.Model,
):
    """
    Abstract soft delete model.

    Provides recoverable deletion without physical removal.

    Designed for:
        - Healthcare entities
        - SaaS resources
        - Compliance workflows
        - Historical reporting
    """

    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        db_index=True,
        verbose_name="Deleted",
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="Deleted At",
    )

    deleted_by_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="Deleted By",
    )

    objects: models.Manager[Any] = SoftDeleteManager()

    all_objects: models.Manager[Any] = AllObjectsManager()

    deleted_objects: models.Manager[Any] = DeletedObjectsManager()

    class Meta:
        abstract = True

    @transaction.atomic
    def delete(
        self,
        using: str | None = None,
        keep_parents: bool = False,
        *,
        user_id: Any | None = None,
    ) -> DeleteResult:
        del using, keep_parents

        return self.soft_delete(
            user_id=user_id,
        )

    @transaction.atomic
    def soft_delete(
        self,
        *,
        user_id: Any | None = None,
    ) -> DeleteResult:

        if self.is_deleted:
            return (
                0,
                {
                    self._meta.label: 0,
                },
            )

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by_id = user_id

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
            ],
        )

        return (
            1,
            {
                self._meta.label: 1,
            },
        )

    @transaction.atomic
    def restore(self) -> None:

        if not self.is_deleted:
            return

        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by_id = None

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
            ],
        )


__all__: tuple[str, ...] = (
    "DeleteResult",
    "SoftDeleteModel",
)
