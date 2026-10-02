"""
User role test factory.
"""

from __future__ import annotations

import factory

from apps.platform.accounts.models import User
from apps.platform.rbac.constants import (
    DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE,
)
from apps.platform.rbac.models import (
    UserRole,
)

from .role import (
    RoleFactory,
)


class UserFactory(
    factory.django.DjangoModelFactory,
):
    """
    Temporary factory for User.

    TODO:
    Move this factory to
    apps/platform/accounts/tests/factories.py
    and import it from there.
    """

    class Meta:
        model = User

    email = factory.Sequence(
        lambda n: f"user{n}@example.com",
    )

    username = factory.Sequence(
        lambda n: f"user{n}",
    )

    first_name = factory.Faker(
        "first_name",
    )

    last_name = factory.Faker(
        "last_name",
    )

    is_active = True


class UserRoleFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for UserRole.
    """

    class Meta:
        model = UserRole

    user = factory.SubFactory(
        UserFactory,
    )

    role = factory.SubFactory(
        RoleFactory,
    )

    assignment_source = DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE

    is_active = True


__all__ = [
    "UserFactory",
    "UserRoleFactory",
]
