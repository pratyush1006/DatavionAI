"""
Base serializers for the Accounts application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared validation logic.
    """

    class Meta:
        model = User
        fields = ()

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


__all__ = [
    "UserBaseSerializer",
]
