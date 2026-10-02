"""
Update serializer for the Accounts application.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.password_validation import (
    validate_password,
)
from rest_framework import serializers

from apps.platform.accounts.models import User
from apps.platform.accounts.selectors import (
    get_user_by_email,
)
from apps.platform.accounts.services import (
    UserService,
)

from .base import UserBaseSerializer
from .fields import UPDATE_FIELDS


class UserUpdateSerializer(
    UserBaseSerializer,
):
    """
    Serializer for updating users.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            validate_password,
        ],
        style={
            "input_type": "password",
        },
    )

    class Meta(
        UserBaseSerializer.Meta,
    ):
        model = User

        fields = UPDATE_FIELDS

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize and validate email changes.
        """

        email = value.strip().lower()

        existing_user = get_user_by_email(
            email=email,
        )

        if existing_user is not None and existing_user.pk != self.instance.pk:
            raise serializers.ValidationError(
                "A user with this email already exists.",
            )

        return email

    def update(
        self,
        instance: User,
        validated_data: dict[str, Any],
    ) -> User:
        """
        Update user through service layer.
        """

        return UserService.update(
            user=instance,
            **validated_data,
        )


__all__ = ("UserUpdateSerializer",)
