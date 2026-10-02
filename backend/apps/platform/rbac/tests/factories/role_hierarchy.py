"""
Role hierarchy test factories.
"""

from __future__ import annotations

import factory

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
    DEFAULT_ROLE_HIERARCHY_TYPE,
)
from apps.platform.rbac.models import (
    RoleHierarchy,
)

from .role import (
    RoleFactory,
)


class RoleHierarchyFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for RoleHierarchy.
    """

    class Meta:
        model = RoleHierarchy

    parent_role = factory.SubFactory(
        RoleFactory,
    )

    child_role = factory.SubFactory(
        RoleFactory,
    )

    hierarchy_type = DEFAULT_ROLE_HIERARCHY_TYPE

    assignment_source = DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE

    is_active = True


def create_role_hierarchy(
    **kwargs,
) -> RoleHierarchy:
    """
    Create a role hierarchy.
    """

    return RoleHierarchyFactory(
        **kwargs,
    )


__all__ = [
    "RoleHierarchyFactory",
    "create_role_hierarchy",
]
