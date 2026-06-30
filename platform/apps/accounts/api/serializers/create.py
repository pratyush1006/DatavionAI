"""
Create serializer for the Accounts app.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.api.serializers.fields import _WRITE_FIELDS
from apps.accounts.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users.
    """

    class Meta:
        model = User

        fields = _WRITE_FIELDS

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

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
