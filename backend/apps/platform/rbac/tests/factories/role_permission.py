"""
Role permission factory.
"""

from __future__ import annotations

import factory

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_PERMISSION_SOURCE,
    DEFAULT_ROLE_PERMISSION_TYPE,
)
from apps.platform.rbac.models import (
    RolePermission,
)

from .permission import (
    PermissionFactory,
)
from .role import (
    RoleFactory,
)


class RolePermissionFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for RolePermission.
    """

    class Meta:
        model = RolePermission

    role = factory.SubFactory(
        RoleFactory,
    )

    permission = factory.SubFactory(
        PermissionFactory,
    )

    assignment_type = DEFAULT_ROLE_PERMISSION_TYPE

    assignment_source = DEFAULT_ROLE_PERMISSION_SOURCE

    is_active = True


__all__ = [
    "RolePermissionFactory",
]
