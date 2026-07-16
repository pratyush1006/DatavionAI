"""
Reusable model managers.

Provides reusable manager implementations shared across the
Datavion AI platform.
"""

from __future__ import annotations

from django.db import models

from .querysets import (
    ActiveQuerySet,
    BaseQuerySet,
    SoftDeleteQuerySet,
)


class BaseManager(
    models.Manager.from_queryset(
        BaseQuerySet,
    ),
):
    """
    Base manager shared across models.
    """


class ActiveManager(
    models.Manager.from_queryset(
        ActiveQuerySet,
    ),
):
    """
    Manager for models implementing ActiveMixin.
    """


class SoftDeleteManager(
    models.Manager.from_queryset(
        SoftDeleteQuerySet,
    ),
):
    """
    Default manager excluding soft-deleted records.
    """

    def get_queryset(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only non-deleted records.
        """

        return super().get_queryset().alive()


class AllObjectsManager(
    models.Manager.from_queryset(
        SoftDeleteQuerySet,
    ),
):
    """
    Manager returning all records, including soft-deleted ones.
    """


class DeletedObjectsManager(
    models.Manager.from_queryset(
        SoftDeleteQuerySet,
    ),
):
    """
    Manager returning only soft-deleted records.
    """

    def get_queryset(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only soft-deleted records.
        """

        return super().get_queryset().deleted()


__all__ = [
    "ActiveManager",
    "AllObjectsManager",
    "BaseManager",
    "DeletedObjectsManager",
    "SoftDeleteManager",
]
