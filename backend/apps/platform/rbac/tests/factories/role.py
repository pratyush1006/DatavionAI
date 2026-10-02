"""
Role test factory.
"""

from __future__ import annotations

import factory

from apps.platform.rbac.builders import (
    RoleBuilder,
)
from apps.platform.rbac.constants import (
    DEFAULT_DISPLAY_ORDER,
    DEFAULT_ROLE_CATEGORY,
    DEFAULT_ROLE_PRIORITY,
    DEFAULT_ROLE_SCOPE,
    DEFAULT_ROLE_TYPE,
    ROLE_PRIORITIES,
)
from apps.platform.rbac.models import (
    Role,
)


class RoleFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Role.
    """

    class Meta:
        model = Role

    name = factory.Sequence(
        lambda n: f"Role {n}",
    )

    description = factory.Faker(
        "sentence",
    )

    role_type = DEFAULT_ROLE_TYPE

    scope = DEFAULT_ROLE_SCOPE

    category = DEFAULT_ROLE_CATEGORY

    parent = None

    display_order = DEFAULT_DISPLAY_ORDER

    is_system = False

    is_default = False

    is_assignable = True

    is_editable = True

    is_deletable = True

    is_active = True

    @factory.lazy_attribute
    def code(
        self,
    ) -> str:
        return RoleBuilder.build(
            name=self.name,
        )

    @factory.lazy_attribute
    def priority(
        self,
    ) -> int:
        return ROLE_PRIORITIES.get(
            self.code,
            DEFAULT_ROLE_PRIORITY,
        )


# ============================================================================
# Backward compatibility
# ============================================================================


def create_role(
    **kwargs,
) -> Role:
    """
    Backward-compatible helper.
    """

    return RoleFactory(
        **kwargs,
    )


def create_system_role(
    **kwargs,
) -> Role:
    """
    Create a system role.
    """

    kwargs.setdefault(
        "is_system",
        True,
    )

    if "name" not in kwargs:
        kwargs["name"] = "Platform Admin"

    return RoleFactory(
        **kwargs,
    )


__all__ = [
    "RoleFactory",
    "create_role",
    "create_system_role",
]
