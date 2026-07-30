"""
Reusable QuerySet classes.

Provides reusable database query abstractions shared across
the DatavionOS platform.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from typing import TypeVar

from django.db import models, transaction
from django.utils import timezone

ModelType = TypeVar(
    "ModelType",
    bound=models.Model,
)


type DeleteResult = tuple[
    int,
    dict[str, int],
]


class BaseQuerySet(
    models.QuerySet[ModelType],
):
    """
    Base queryset for DatavionOS models.
    """

    def newest(self):
        return self.order_by(
            "-created_at",
        )

    def oldest(self):
        return self.order_by(
            "created_at",
        )

    def recent(
        self,
        *,
        days: int,
    ):
        since = timezone.now() - timezone.timedelta(
            days=days,
        )

        return self.filter(
            created_at__gte=since,
        )

    def created_between(
        self,
        *,
        start: datetime,
        end: datetime,
    ):
        return self.filter(
            created_at__range=(
                start,
                end,
            ),
        )

    def updated_between(
        self,
        *,
        start: datetime,
        end: datetime,
    ):
        return self.filter(
            updated_at__range=(
                start,
                end,
            ),
        )

    def exists_by_pk(
        self,
        pk: object,
    ) -> bool:
        return self.filter(
            pk=pk,
        ).exists()

    def chunked(
        self,
        *,
        size: int = 1000,
    ) -> Iterator[list[ModelType]]:

        if size <= 0:
            raise ValueError(
                "Chunk size must be greater than zero.",
            )

        batch = []

        for obj in self.iterator(
            chunk_size=size,
        ):
            batch.append(obj)

            if len(batch) >= size:
                yield batch
                batch = []

        if batch:
            yield batch


class ActiveQuerySet(
    BaseQuerySet[ModelType],
):
    def active(self):
        return self.filter(
            is_active=True,
        )

    def inactive(self):
        return self.filter(
            is_active=False,
        )


class SoftDeleteQuerySet(
    BaseQuerySet[ModelType],
):
    def alive(self):
        return self.filter(
            is_deleted=False,
        )

    def deleted(self):
        return self.filter(
            is_deleted=True,
        )

    @transaction.atomic
    def restore(self) -> int:

        return self.update(
            is_deleted=False,
            deleted_at=None,
            deleted_by_id=None,
        )

    @transaction.atomic
    def delete(
        self,
        *,
        user_id=None,
    ) -> DeleteResult:

        count = self.update(
            is_deleted=True,
            deleted_at=timezone.now(),
            deleted_by_id=user_id,
        )

        return (
            count,
            {
                self.model._meta.label: count,
            },
        )

    def alive_count(self):
        return self.alive().count()

    def deleted_count(self):
        return self.deleted().count()


__all__: tuple[str, ...] = (
    "ActiveQuerySet",
    "BaseQuerySet",
    "DeleteResult",
    "SoftDeleteQuerySet",
)
