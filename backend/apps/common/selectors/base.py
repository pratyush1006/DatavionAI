"""
DatavionOS Base Selector.

Foundation for all read-only selectors.

Design Principles
-----------------
- Read-only
- Multi-tenant aware
- Permission aware
- QuerySet oriented
- Type-safe
- Optimization friendly
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from django.db.models import Model, QuerySet

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


class BaseSelector(
    ABC,
    Generic[ModelType],
):
    """
    Base selector for DatavionOS applications.

    Selectors only perform reads.

    They must never:

    - create
    - update
    - delete
    """

    model: type[ModelType]

    def __init__(
        self,
        *,
        tenant: Any | None = None,
        organization: Any | None = None,
        user: Any | None = None,
    ) -> None:

        self.tenant = tenant
        self.organization = organization
        self.user = user

    def queryset(
        self,
    ) -> QuerySet[ModelType]:
        """
        Return base queryset.
        """

        return self.model.objects.all()

    def get_queryset(
        self,
    ) -> QuerySet[ModelType]:
        """
        Build contextual queryset.
        """

        queryset = self.queryset()

        queryset = self.apply_tenant_filter(
            queryset,
        )

        queryset = self.apply_permissions(
            queryset,
        )

        queryset = self.optimize(
            queryset,
        )

        return queryset

    def apply_tenant_filter(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:
        """
        Apply tenant isolation.

        Override when required.
        """

        return queryset

    def apply_permissions(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:
        """
        Apply user permission filtering.

        Override when required.
        """

        return queryset

    def all(
        self,
    ) -> QuerySet[ModelType]:
        """
        Return all accessible objects.
        """

        return self.get_queryset()

    def get(
        self,
        **filters: Any,
    ) -> ModelType:
        """
        Return one object.
        """

        return self.get_queryset().get(
            **filters,
        )

    def get_or_none(
        self,
        **filters: Any,
    ) -> ModelType | None:
        """
        Return object or None.
        """

        return self.get_queryset().filter(**filters).first()

    def filter(
        self,
        **filters: Any,
    ) -> QuerySet[ModelType]:
        """
        Filter objects.
        """

        return self.get_queryset().filter(
            **filters,
        )

    def exists(
        self,
        **filters: Any,
    ) -> bool:
        """
        Check existence.
        """

        return self.filter(
            **filters,
        ).exists()

    def count(
        self,
        **filters: Any,
    ) -> int:
        """
        Count records.
        """

        return self.filter(
            **filters,
        ).count()

    def first(
        self,
        **filters: Any,
    ) -> ModelType | None:
        """
        Return first object.
        """

        return self.filter(
            **filters,
        ).first()

    def values(
        self,
        *fields: str,
    ):
        """
        Return values queryset.
        """

        return self.get_queryset().values(
            *fields,
        )

    def values_list(
        self,
        *fields: str,
        flat: bool = False,
    ):
        """
        Return values list queryset.
        """

        return self.get_queryset().values_list(
            *fields,
            flat=flat,
        )

    @abstractmethod
    def optimize(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:
        """
        Optimize queryset.

        Add:

        - select_related
        - prefetch_related
        - annotations
        """

        raise NotImplementedError


__all__: tuple[str, ...] = ("BaseSelector",)
