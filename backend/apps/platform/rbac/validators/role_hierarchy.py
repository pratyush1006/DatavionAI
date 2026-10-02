"""
Role hierarchy validators.
"""

from __future__ import annotations

from collections import deque

from django.core.exceptions import ValidationError

from apps.platform.rbac.constants import (
    MAX_ROLE_HIERARCHY_DEPTH,
)
from apps.platform.rbac.models import (
    RoleHierarchy,
)


def validate_role_hierarchy(
    *,
    parent_role,
    child_role,
    instance: RoleHierarchy | None = None,
) -> None:
    """
    Validate a role hierarchy relationship.
    """

    validate_self_role_hierarchy(
        parent_role=parent_role,
        child_role=child_role,
    )

    validate_role_hierarchy_unique(
        parent_role=parent_role,
        child_role=child_role,
        instance=instance,
    )

    validate_role_hierarchy_cycle(
        parent_role=parent_role,
        child_role=child_role,
        instance=instance,
    )


def validate_self_role_hierarchy(
    *,
    parent_role,
    child_role,
) -> None:
    """
    Prevent a role from inheriting itself.
    """

    if parent_role == child_role:
        raise ValidationError(
            "A role cannot inherit from itself.",
        )


def validate_role_hierarchy_unique(
    *,
    parent_role,
    child_role,
    instance: RoleHierarchy | None = None,
) -> None:
    """
    Ensure the hierarchy relationship is unique.
    """

    queryset = RoleHierarchy.objects.filter(
        parent_role=parent_role,
        child_role=child_role,
    )

    if instance is not None:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "This role hierarchy already exists.",
        )


def validate_role_hierarchy_cycle(
    *,
    parent_role,
    child_role,
    instance: RoleHierarchy | None = None,
) -> None:
    """
    Prevent circular role inheritance.
    """

    visited: set[int] = set()

    queue: deque[tuple[int, int]] = deque(
        [
            (
                child_role.pk,
                0,
            ),
        ],
    )

    while queue:
        current_role_id, depth = queue.popleft()

        if current_role_id == parent_role.pk:
            raise ValidationError(
                "Circular role hierarchy detected.",
            )

        if depth >= MAX_ROLE_HIERARCHY_DEPTH:
            continue

        if current_role_id in visited:
            continue

        visited.add(
            current_role_id,
        )

        queryset = RoleHierarchy.objects.filter(
            parent_role_id=current_role_id,
            is_active=True,
        )

        if instance is not None:
            queryset = queryset.exclude(
                pk=instance.pk,
            )

        for hierarchy in queryset:
            queue.append(
                (
                    hierarchy.child_role_id,
                    depth + 1,
                ),
            )


__all__ = [
    "validate_role_hierarchy",
    "validate_role_hierarchy_cycle",
    "validate_role_hierarchy_unique",
    "validate_self_role_hierarchy",
]
