"""
Factory Boy factories for RBAC tests.
"""

from __future__ import annotations

import factory
from django.contrib.auth import get_user_model

from apps.organizations.models import Organization
from apps.rbac.models import (
    Permission,
    Role,
    RolePermission,
    UserRole,
)

User = get_user_model()


class OrganizationFactory(factory.django.DjangoModelFactory):
    """
    Organization factory.
    """

    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Organization {n}")
    code = factory.Sequence(lambda n: f"ORG{n:03}")


class UserFactory(factory.django.DjangoModelFactory):
    """
    User factory.
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.username}@datavion.ai",
    )

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    is_active = True


class RoleFactory(factory.django.DjangoModelFactory):
    """
    Role factory.
    """

    class Meta:
        model = Role

    name = factory.Sequence(
        lambda n: f"Role {n}",
    )

    code = factory.Sequence(
        lambda n: f"ROLE_{n}",
    )

    description = factory.Faker("sentence")

    is_active = True


class PermissionFactory(factory.django.DjangoModelFactory):
    """
    Permission factory.
    """

    class Meta:
        model = Permission

    name = factory.Sequence(
        lambda n: f"Permission {n}",
    )

    code = factory.Sequence(
        lambda n: f"permission.{n}",
    )

    description = factory.Faker("sentence")

    is_active = True


class UserRoleFactory(factory.django.DjangoModelFactory):
    """
    UserRole factory.
    """

    class Meta:
        model = UserRole

    user = factory.SubFactory(
        UserFactory,
    )

    role = factory.SubFactory(
        RoleFactory,
    )


class RolePermissionFactory(factory.django.DjangoModelFactory):
    """
    RolePermission factory.
    """

    class Meta:
        model = RolePermission

    role = factory.SubFactory(
        RoleFactory,
    )

    permission = factory.SubFactory(
        PermissionFactory,
    )
