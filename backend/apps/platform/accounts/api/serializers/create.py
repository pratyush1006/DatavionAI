"""
Create serializer for the Accounts application.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.password_validation import (
    validate_password,
)
from rest_framework import serializers

from apps.platform.accounts.models import User
from apps.platform.accounts.services import (
    UserService,
)

from .base import UserBaseSerializer
from .fields import CREATE_FIELDS


class UserCreateSerializer(
    UserBaseSerializer,
):
    """
    Serializer for creating users.
    """

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
        validators=[
            validate_password,
        ],
    )

    class Meta(
        UserBaseSerializer.Meta,
    ):
        model = User

        fields = CREATE_FIELDS

        extra_kwargs = {
            "email": {
                "required": True,
            },
            "first_name": {
                "required": True,
            },
            "last_name": {
                "required": True,
            },
        }

    def create(
        self,
        validated_data: dict[str, Any],
    ) -> User:
        """
        Create a user through service layer.
        """

        return UserService.create(
            **validated_data,
        )


__all__ = ("UserCreateSerializer",)
