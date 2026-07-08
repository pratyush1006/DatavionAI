"""
Reusable model managers.
"""

from __future__ import annotations

from django.db import models

from .querysets import (
    ActiveQuerySet,
    BaseQuerySet,
    SoftDeleteQuerySet,
)


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    """
    Base manager shared across models.
    """

    def active(
        self,
    ) -> BaseQuerySet:
        """
        Return only active objects.
        """

        return self.get_queryset().active()

    def inactive(
        self,
    ) -> BaseQuerySet:
        """
        Return only inactive objects.
        """

        return self.get_queryset().inactive()

    def newest(
        self,
    ) -> BaseQuerySet:
        """
        Return objects ordered by newest first.
        """

        return self.get_queryset().newest()


class ActiveManager(models.Manager.from_queryset(ActiveQuerySet)):
    """
    Manager for models implementing ActiveMixin.
    """

    def active(
        self,
    ) -> ActiveQuerySet:
        """
        Return only active objects.
        """

        return self.get_queryset().active()

    def inactive(
        self,
    ) -> ActiveQuerySet:
        """
        Return only inactive objects.
        """

        return self.get_queryset().inactive()

    def newest(
        self,
    ) -> ActiveQuerySet:
        """
        Return objects ordered by newest first.
        """

        return self.get_queryset().newest()


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Default manager excluding soft-deleted objects.
    """

    def get_queryset(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only non-deleted objects.
        """

        return super().get_queryset().alive()

    def alive(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only non-deleted objects.
        """

        return self.get_queryset()

    def deleted(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only deleted objects.
        """

        return super().get_queryset().deleted()

    def restore(
        self,
    ) -> int:
        """
        Restore all soft-deleted objects.
        """

        return self.get_queryset().restore()

    def hard_delete(
        self,
    ) -> tuple[int, dict[str, int]]:
        """
        Permanently delete all objects.
        """

        return self.get_queryset().hard_delete()


class AllObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Manager returning all objects, including deleted.
    """

    def alive(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only non-deleted objects.
        """

        return self.get_queryset().alive()

    def deleted(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only deleted objects.
        """

        return self.get_queryset().deleted()

    def hard_delete(
        self,
    ) -> tuple[int, dict[str, int]]:
        """
        Permanently delete all objects.
        """

        return self.get_queryset().hard_delete()


class DeletedObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Manager returning only deleted objects.
    """

    def get_queryset(
        self,
    ) -> SoftDeleteQuerySet:
        """
        Return only deleted objects.
        """

        return super().get_queryset().deleted()

    def restore(
        self,
    ) -> int:
        """
        Restore all deleted objects.
        """

        return self.get_queryset().restore()

    def hard_delete(
        self,
    ) -> tuple[int, dict[str, int]]:
        """
        Permanently delete all objects.
        """

        return self.get_queryset().hard_delete()


__all__ = [
    "ActiveManager",
    "AllObjectsManager",
    "BaseManager",
    "DeletedObjectsManager",
    "SoftDeleteManager",
]
