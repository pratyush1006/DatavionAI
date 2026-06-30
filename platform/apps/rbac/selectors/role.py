"""
Read-only selectors for Role.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.rbac.models import Role

_ROLE_LIST_FIELDS = (
    "id",
    "name",
    "code",
    "description",
    "is_active",
)


def get_roles(
    *,
    include_inactive: bool = False,
) -> QuerySet[Role]:
    """
    Return all roles ordered by name.
    """

    queryset = Role.objects.only(
        *_ROLE_LIST_FIELDS,
    ).order_by(
        "name",
    )

    if not include_inactive:
        queryset = queryset.filter(
            is_active=True,
        )

    return queryset


def get_role_by_id(
    *,
    role_id: int,
) -> Role:
    """
    Return a role by its primary key.
    """

    return get_object_or_404(
        get_roles(
            include_inactive=True,
        ),
        pk=role_id,
    )


def get_role_by_code(
    *,
    code: str,
) -> Role:
    """
    Return a role by its unique code.
    """

    return get_object_or_404(
        get_roles(
            include_inactive=True,
        ),
        code=code,
    )
