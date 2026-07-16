"""
Base serializers for the Accounts application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.accounts.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for user serializers.

    Provides shared normalization and validation logic.
    """

    class Meta:
        model = User
        fields: tuple[str, ...] = ()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the email address.
        """

        return value.strip().lower()

    def validate_username(
        self,
        value: str,
    ) -> str:
        """
        Normalize the username.
        """

        return value.strip()

    def validate_phone(
        self,
        value: str,
    ) -> str:
        """
        Normalize the phone number.
        """

        return value.strip()


__all__ = [
    "UserBaseSerializer",
]
