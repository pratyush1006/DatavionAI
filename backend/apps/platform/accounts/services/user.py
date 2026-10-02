"""
User business services.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.platform.accounts.models import User


class UserService:
    """
    Business services for user lifecycle management.

    Handles:

    - User creation
    - User updates
    - Activation/deactivation
    - Login tracking
    - Account lifecycle operations
    """

    @staticmethod
    def _extract_platform_context(
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Remove platform context injected by API layer.

        These fields belong to request context,
        not the User model.
        """

        return {
            "request_user": validated_data.pop(
                "request_user",
                None,
            ),
            "tenant": validated_data.pop(
                "tenant",
                None,
            ),
            "organization": validated_data.pop(
                "organization",
                None,
            ),
        }

    @staticmethod
    @transaction.atomic
    def create(
        **validated_data: Any,
    ) -> User:
        """
        Create a new user.

        Platform context is accepted from
        DatavionOS service layer but is not
        passed directly to the model.
        """

        validated_data = dict(
            validated_data,
        )

        UserService._extract_platform_context(
            validated_data,
        )

        password = validated_data.pop(
            "password",
            None,
        )

        return User.objects.create_user(
            password=password,
            **validated_data,
        )

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        **validated_data: Any,
    ) -> User:
        """
        Update an existing user.
        """

        validated_data = dict(
            validated_data,
        )

        UserService._extract_platform_context(
            validated_data,
        )

        password = validated_data.pop(
            "password",
            None,
        )

        update_fields: list[str] = []

        for field, value in validated_data.items():
            setattr(
                user,
                field,
                value,
            )

            update_fields.append(
                field,
            )

        if password:
            user.set_password(
                password,
            )

            update_fields.append(
                "password",
            )

        if update_fields:
            update_fields.append(
                "updated_at",
            )

            user.save(
                update_fields=update_fields,
            )

        return user

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        user: User,
        **kwargs: Any,
    ) -> User:
        """
        Soft deactivate a user.

        Preserves audit history.
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
        **kwargs: Any,
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
        Record successful login.
        """

        user.last_login = timezone.now()

        user.save(
            update_fields=[
                "last_login",
                "updated_at",
            ],
        )

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        user: User,
        **kwargs: Any,
    ) -> None:
        """
        Permanently delete a user.

        Reserved for platform cleanup only.
        """

        user.delete()


__all__ = ("UserService",)
