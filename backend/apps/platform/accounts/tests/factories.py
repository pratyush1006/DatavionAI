"""
User test factories.
"""

from __future__ import annotations

import factory

from apps.platform.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for the custom User model.
    """

    class Meta:
        model = User

    email = factory.Sequence(
        lambda n: f"user{n}@example.com",
    )

    first_name = "Test"

    last_name = "User"

    phone = ""

    is_verified = False

    is_internal_user = True


__all__ = [
    "UserFactory",
]
