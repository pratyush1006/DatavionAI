"""
DatavionOS Selector Mixins.

Reusable enterprise selector components.

Supports:

- Filtering
- Searching
- Ordering
- Pagination
- Tenant isolation
- User access scope
- Query optimization
- Soft delete filtering
"""

from __future__ import annotations

from typing import Any, TypeVar

from django.db.models import Model, QuerySet

from .filters import FilterSet
from .ordering import Ordering
from .pagination import Pagination, PaginationResult
from .search import Search

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


class FilterMixin[ModelType: Model]:
    """
    Generic filtering support.
    """

    filter_fields: tuple[str, ...] = ()

    def apply_filters(
        self,
        queryset: QuerySet[ModelType],
        **filters: Any,
    ) -> QuerySet[ModelType]:

        allowed = {
            key: value for key, value in filters.items() if key in self.filter_fields
        }

        return FilterSet.apply(
            queryset,
            **allowed,
        )


class SearchMixin[ModelType: Model]:
    """
    Generic search support.
    """

    search_fields: tuple[str, ...] = ()

    def apply_search(
        self,
        queryset: QuerySet[ModelType],
        query: str | None,
    ) -> QuerySet[ModelType]:

        return Search.apply(
            queryset,
            query=query,
            fields=self.search_fields,
        )


class OrderingMixin[ModelType: Model]:
    """
    Query ordering support.
    """

    ordering_fields: tuple[str, ...] = ()

    default_ordering: tuple[str, ...] = ()

    def apply_ordering(
        self,
        queryset: QuerySet[ModelType],
        ordering: str | None,
    ) -> QuerySet[ModelType]:

        return Ordering.apply(
            queryset,
            ordering=ordering,
            allowed=self.ordering_fields,
            default=self.default_ordering,
        )


class PaginationMixin[ModelType: Model]:
    """
    Pagination support.
    """

    def paginate(
        self,
        queryset: QuerySet[ModelType],
        *,
        page: int = Pagination.DEFAULT_PAGE,
        page_size: int = Pagination.DEFAULT_PAGE_SIZE,
    ) -> PaginationResult[ModelType]:

        return Pagination.paginate(
            queryset,
            page=page,
            page_size=page_size,
        )


class TenantScopeMixin[ModelType: Model]:
    """
    DatavionOS multi tenant scope.

    Supports:

    - Tenant
    - Organization
    - Facility
    """

    tenant: Any | None = None

    organization: Any | None = None

    facility: Any | None = None

    def apply_tenant_scope(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:

        return queryset


class UserScopeMixin[ModelType: Model]:
    """
    User based access filtering.
    """

    user: Any | None = None

    def apply_user_scope(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:

        return queryset


class SoftDeleteMixin[ModelType: Model]:
    """
    Exclude deleted records.
    """

    def apply_active_scope(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:

        if hasattr(
            queryset.model,
            "deleted_at",
        ):
            return queryset.filter(
                deleted_at__isnull=True,
            )

        return queryset


class OptimizationMixin[ModelType: Model]:
    """
    Query optimization hooks.
    """

    def optimize(
        self,
        queryset: QuerySet[ModelType],
    ) -> QuerySet[ModelType]:

        return queryset


__all__: tuple[str, ...] = (
    "FilterMixin",
    "OrderingMixin",
    "OptimizationMixin",
    "PaginationMixin",
    "SearchMixin",
    "SoftDeleteMixin",
    "TenantScopeMixin",
    "UserScopeMixin",
)
