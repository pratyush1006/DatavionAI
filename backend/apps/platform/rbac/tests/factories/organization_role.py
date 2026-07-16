"""
Organization role factory.
"""

from __future__ import annotations

import factory

from apps.platform.organizations.tests.factories import (
    OrganizationFactory,
)
from apps.platform.rbac.constants import (
    DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE,
)
from apps.platform.rbac.models import (
    OrganizationRole,
)

from .role import (
    RoleFactory,
)
from .user_role import (
    UserFactory,
)


class OrganizationRoleFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for OrganizationRole.
    """

    class Meta:
        model = OrganizationRole

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    user = factory.SubFactory(
        UserFactory,
    )

    role = factory.SubFactory(
        RoleFactory,
    )

    assignment_source = DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE

    is_primary = False

    is_active = True


__all__ = [
    "OrganizationRoleFactory",
]
