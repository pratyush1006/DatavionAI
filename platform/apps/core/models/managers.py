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

    def active(self) -> BaseQuerySet:
        """
        Return only active objects.
        """
        return self.get_queryset().active()

    def inactive(self) -> BaseQuerySet:
        """
        Return only inactive objects.
        """
        return self.get_queryset().inactive()

    def ordered(self) -> BaseQuerySet:
        """
        Return objects ordered by newest first.
        """
        return self.get_queryset().ordered()


class ActiveManager(models.Manager.from_queryset(ActiveQuerySet)):
    """
    Manager for models implementing ActiveMixin.
    """

    def active(self) -> ActiveQuerySet:
        return self.get_queryset().active()

    def inactive(self) -> ActiveQuerySet:
        return self.get_queryset().inactive()

    def ordered(self) -> ActiveQuerySet:
        return self.get_queryset().ordered()


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Default manager excluding soft-deleted objects.
    """

    def get_queryset(self) -> SoftDeleteQuerySet:
        return super().get_queryset().alive()

    def alive(self) -> SoftDeleteQuerySet:
        return self.get_queryset()

    def deleted(self) -> SoftDeleteQuerySet:
        return super().get_queryset().deleted()

    def restore(self) -> int:
        return self.get_queryset().restore()

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class AllObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Manager returning all objects, including deleted.
    """

    def alive(self) -> SoftDeleteQuerySet:
        return self.get_queryset().alive()

    def deleted(self) -> SoftDeleteQuerySet:
        return self.get_queryset().deleted()


class DeletedObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Manager returning only deleted objects.
    """

    def get_queryset(self) -> SoftDeleteQuerySet:
        return super().get_queryset().deleted()

    def restore(self) -> int:
        return self.get_queryset().restore()

    def hard_delete(self):
        return self.get_queryset().hard_delete()
