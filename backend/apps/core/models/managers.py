"""
Reusable model managers.

Provides reusable database access managers shared across
the DatavionOS platform.
"""

from __future__ import annotations

from typing import TypeVar

from django.db import models

from .querysets import (
    ActiveQuerySet,
    BaseQuerySet,
    SoftDeleteQuerySet,
)

ModelType = TypeVar(
    "ModelType",
    bound=models.Model,
)


BaseManagerMixin = models.Manager.from_queryset(
    BaseQuerySet,
)


ActiveManagerMixin = models.Manager.from_queryset(
    ActiveQuerySet,
)


SoftDeleteManagerMixin = models.Manager.from_queryset(
    SoftDeleteQuerySet,
)


class BaseManager(
    BaseManagerMixin[ModelType],
):
    """
    Default manager for DatavionOS models.
    """

    use_in_migrations = True


class ActiveManager(
    ActiveManagerMixin[ModelType],
):
    """
    Manager for active-state models.

    Returns only active records by default.
    """

    use_in_migrations = True

    def get_queryset(
        self,
    ) -> ActiveQuerySet[ModelType]:
        """
        Return active records only.
        """

        return super().get_queryset().active()


class SoftDeleteManager(
    SoftDeleteManagerMixin[ModelType],
):
    """
    Default manager for soft-delete models.

    Returns only non-deleted records.
    """

    use_in_migrations = True

    def get_queryset(
        self,
    ) -> SoftDeleteQuerySet[ModelType]:
        """
        Return alive records only.
        """

        return super().get_queryset().alive()


class AllObjectsManager(
    SoftDeleteManagerMixin[ModelType],
):
    """
    Manager exposing all records.

    Includes soft-deleted records.
    """

    use_in_migrations = True


class DeletedObjectsManager(
    SoftDeleteManagerMixin[ModelType],
):
    """
    Manager exposing deleted records only.
    """

    use_in_migrations = True

    def get_queryset(
        self,
    ) -> SoftDeleteQuerySet[ModelType]:
        """
        Return deleted records only.
        """

        return super().get_queryset().deleted()


__all__: tuple[str, ...] = (
    "ActiveManager",
    "AllObjectsManager",
    "BaseManager",
    "DeletedObjectsManager",
    "SoftDeleteManager",
)
