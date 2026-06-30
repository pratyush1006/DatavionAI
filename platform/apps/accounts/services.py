"""
Business services for the Accounts app.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.accounts.models import User


@transaction.atomic
def create_user(
    *,
    validated_data: Mapping[str, object],
) -> User:
    """
    Create a new user.

    Args:
        validated_data: Validated user data.

    Returns:
        The newly created user.
    """

    validated_data = dict(validated_data)

    password = validated_data.pop("password")

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
    validated_data: Mapping[str, object],
) -> User:
    """
    Update an existing user.

    Args:
        instance: User instance to update.
        validated_data: Validated fields to update.

    Returns:
        The updated user.
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

    if password:
        instance.set_password(
            password,
        )

    instance.save(
        update_fields=(
            list(validated_data.keys()) + (["password"] if password else [])
        ),
    )

    return instance


@transaction.atomic
def delete_user(
    *,
    instance: User,
) -> None:
    """
    Delete a user.

    Args:
        instance: User instance to delete.
    """

    instance.delete()
