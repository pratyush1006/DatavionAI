"""
Role hierarchy resolution helpers.
"""

from __future__ import annotations

from collections import deque

from django.db.models import QuerySet

from apps.platform.rbac.constants import (
    MAX_ROLE_HIERARCHY_DEPTH,
)
from apps.platform.rbac.models import (
    Role,
    RoleHierarchy,
)


def resolve_inherited_roles(
    *,
    roles: QuerySet[Role],
) -> QuerySet[Role]:
    """
    Resolve all inherited roles for the supplied roles.

    Traverses the role hierarchy and returns the original
    roles together with all inherited roles.
    """

    role_ids = set(
        roles.values_list(
            "id",
            flat=True,
        ),
    )

    visited = set(
        role_ids,
    )

    queue = deque(
        (
            role_id,
            0,
        )
        for role_id in role_ids
    )

    while queue:
        current_role_id, depth = queue.popleft()

        if depth >= MAX_ROLE_HIERARCHY_DEPTH:
            continue

        child_role_ids = (
            RoleHierarchy.objects.active()
            .filter(
                parent_role_id=current_role_id,
            )
            .values_list(
                "child_role_id",
                flat=True,
            )
        )

        for child_role_id in child_role_ids:
            if child_role_id in visited:
                continue

            visited.add(
                child_role_id,
            )

            queue.append(
                (
                    child_role_id,
                    depth + 1,
                ),
            )

    return (
        Role.objects.active()
        .filter(
            id__in=visited,
        )
        .distinct()
    )


__all__ = [
    "resolve_inherited_roles",
]
