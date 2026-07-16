"""
Reusable QuerySet classes.

Provides reusable QuerySet implementations shared across the
Datavion AI platform.
"""

from __future__ import annotations

from typing import Self

from django.db import models
from django.utils import timezone


class BaseQuerySet(
    models.QuerySet,
):
    """
    Base queryset shared across business models.
    """

    def newest(
        self,
    ) -> Self:
        """
        Return records ordered by newest first.
        """

        return self.order_by(
            "-created_at",
        )

    def oldest(
        self,
    ) -> Self:
        """
        Return records ordered by oldest first.
        """

        return self.order_by(
            "created_at",
        )


class ActiveQuerySet(
    BaseQuerySet,
):
    """
    QuerySet for models implementing ActiveMixin.
    """

    def active(
        self,
    ) -> Self:
        """
        Return only active records.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> Self:
        """
        Return only inactive records.
        """

        return self.filter(
            is_active=False,
        )


class SoftDeleteQuerySet(
    BaseQuerySet,
):
    """
    QuerySet for models implementing SoftDeleteMixin.
    """

    def alive(
        self,
    ) -> Self:
        """
        Return only non-deleted records.
        """

        return self.filter(
            is_deleted=False,
        )

    def deleted(
        self,
    ) -> Self:
        """
        Return only soft-deleted records.
        """

        return self.filter(
            is_deleted=True,
        )

    def restore(
        self,
    ) -> int:
        """
        Restore all soft-deleted records.
        """

        return self.update(
            is_active=True,
            is_deleted=False,
            deleted_at=None,
            deleted_by=None,
        )

    def delete(
        self,
    ) -> tuple[int, dict[str, int]]:
        """
        Soft delete all records in the queryset.
        """

        count = self.update(
            is_active=False,
            is_deleted=True,
            deleted_at=timezone.now(),
        )

        return (
            count,
            {
                self.model._meta.label: count,
            },
        )

    def hard_delete(
        self,
    ) -> tuple[int, dict[str, int]]:
        """
        Permanently delete all records.
        """

        return super().delete()


__all__ = [
    "BaseQuerySet",
    "ActiveQuerySet",
    "SoftDeleteQuerySet",
]
