"""
User business services.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction
from django.utils import timezone

from apps.platform.accounts.models import User

type UserData = Mapping[str, object]


class UserService:
    """
    Business services for user lifecycle management.
    """

    @staticmethod
    @transaction.atomic
    def create(
        **validated_data: object,
    ) -> User:
        """
        Create a new user.
        """

        validated_data = dict(validated_data)

        password = validated_data.pop("password")

        return User.objects.create_user(
            password=password,
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        **validated_data: object,
    ) -> User:
        """
        Update a user.
        """

        validated_data = dict(validated_data)

        password = validated_data.pop(
            "password",
            None,
        )

        update_fields: list[str] = []

        for field, value in validated_data.items():
            setattr(user, field, value)
            update_fields.append(field)

        if password:
            user.set_password(password)
            update_fields.append("password")

        if update_fields:
            update_fields.append("updated_at")
            user.save(update_fields=update_fields)

        return user

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        user: User,
    ) -> User:
        """
        Deactivate a user.
        """

        user.is_active = False

        user.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return user

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        user: User,
    ) -> User:
        """
        Activate a user.
        """

        user.is_active = True

        user.save(
            update_fields=[
                "is_active",
                "updated_at",
            ],
        )

        return user

    @staticmethod
    @transaction.atomic
    def record_login(
        *,
        user: User,
    ) -> None:
        """
        Record a successful login.
        """

        user.last_login = timezone.now()

        user.save(
            update_fields=[
                "last_login",
            ],
        )

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        user: User,
    ) -> None:
        """
        Permanently delete a user.

        Reserved for administrative cleanup only.
        """

        user.delete()


__all__ = [
    "UserService",
]
