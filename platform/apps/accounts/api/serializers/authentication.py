"""
Authentication serializers for the Accounts application.
"""

from __future__ import annotations

from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.accounts.models import User


class LoginSerializer(serializers.Serializer):
    """
    Validate user credentials.
    """

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )

    def validate(
        self,
        attrs,
    ):
        """
        Authenticate the user.
        """

        print("=" * 60)
        print("LOGIN REQUEST:", attrs)

        user = authenticate(
            username=attrs["email"],
            password=attrs["password"],
        )

        print("AUTHENTICATED USER:", user)
        print("=" * 60)

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password.",
            )

        attrs["user"] = user

        return attrs


class LoginResponseSerializer(serializers.Serializer):
    """
    JWT authentication response.
    """

    access = serializers.CharField()

    refresh = serializers.CharField()


class MeSerializer(serializers.ModelSerializer):
    """
    Serializer for the authenticated user.
    """

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_verified",
            "is_staff",
            "is_active",
            "organization",
        )

        read_only_fields = fields


__all__ = [
    "LoginSerializer",
    "LoginResponseSerializer",
    "MeSerializer",
]
