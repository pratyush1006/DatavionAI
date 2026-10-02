"""
Factory Boy factories for the Audit application.
"""

from __future__ import annotations

import factory
from django.contrib.auth import get_user_model

from apps.platform.audit.constants import AuditAction
from apps.platform.audit.models import AuditLog
from apps.platform.organizations.models import Organization

User = get_user_model()


class OrganizationFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Organization.
    """

    class Meta:
        model = Organization

    name = factory.Sequence(
        lambda n: f"Organization {n}",
    )

    code = factory.Sequence(
        lambda n: f"ORG{n:05d}",
    )

    email = factory.LazyAttribute(
        lambda obj: f"{obj.code.lower()}@example.com",
    )

    phone = "9876543210"

    address = "Test Address"

    city = "Bengaluru"

    state = "Karnataka"

    country = "India"


class UserFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for User.
    """

    class Meta:
        model = User

    username = factory.Sequence(
        lambda n: f"user{n}",
    )

    email = factory.LazyAttribute(
        lambda obj: f"{obj.username}@example.com",
    )

    password = factory.PostGenerationMethodCall(
        "set_password",
        "Password123!",
    )


class AuditLogFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for AuditLog.
    """

    class Meta:
        model = AuditLog

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    user = factory.SubFactory(
        UserFactory,
    )

    action = AuditAction.CREATE

    module = "accounts"

    object_type = "User"

    object_id = factory.Sequence(
        lambda n: str(n + 1),
    )

    old_values = {}

    new_values = {
        "status": "active",
    }

    request_id = factory.Faker(
        "uuid4",
    )

    correlation_id = factory.Faker(
        "uuid4",
    )

    session_key = factory.Faker(
        "uuid4",
    )

    ip_address = "127.0.0.1"

    user_agent = "pytest"

    http_method = "POST"

    request_path = "/api/accounts/users/"

    status_code = 201

    success = True

    error_message = ""


__all__ = [
    "AuditLogFactory",
    "OrganizationFactory",
    "UserFactory",
]
