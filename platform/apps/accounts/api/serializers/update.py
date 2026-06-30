"""
Update serializer for the Accounts app.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.api.serializers.fields import _UPDATE_FIELDS
from apps.accounts.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating users.
    """

    class Meta:
        model = User

        fields = _UPDATE_FIELDS

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
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
