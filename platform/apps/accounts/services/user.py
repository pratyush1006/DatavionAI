"""
User business services.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.accounts.models import User

type UserData = Mapping[str, object]


@transaction.atomic
def create_user(
    *,
    validated_data: UserData,
) -> User:
    """
    Create a new user.
    """

    validated_data = dict(validated_data)

    password = validated_data.pop(
        "password",
    )

    user = User(
        **validated_data,
    )

    user.set_password(
        password,
    )

    user.save()

    return user


@transaction.atomic
def update_user(
    *,
    instance: User,
    validated_data: UserData,
) -> User:
    """
    Update an existing user.
    """

    validated_data = dict(validated_data)

    password = validated_data.pop(
        "password",
        None,
    )

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    if password is not None:
        instance.set_password(
            password,
        )

    instance.save()

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_user(
    *,
    instance: User,
) -> None:
    """
    Delete a user.
    """

    instance.delete()


__all__ = [
    "create_user",
    "update_user",
    "delete_user",
]
