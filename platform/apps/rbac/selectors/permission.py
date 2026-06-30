"""
Read-only selectors for Permission.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.rbac.models import Permission

_PERMISSION_LIST_FIELDS = (
    "id",
    "name",
    "code",
    "description",
    "is_active",
)


def get_permissions(
    *,
    include_inactive: bool = False,
) -> QuerySet[Permission]:
    """
    Return all permissions ordered by name.
    """

    queryset = Permission.objects.only(
        *_PERMISSION_LIST_FIELDS,
    ).order_by(
        "name",
    )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset


def get_permission_by_id(
    *,
    permission_id: int,
) -> Permission:
    """
    Return a permission by its primary key.
    """

    return get_object_or_404(
        get_permissions(
            include_inactive=True,
        ),
        pk=permission_id,
    )


def get_permission_by_code(
    *,
    code: str,
) -> Permission:
    """
    Return a permission by its unique code.
    """

    return get_object_or_404(
        get_permissions(
            include_inactive=True,
        ),
        code=code,
    )
