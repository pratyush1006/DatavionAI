"""
Base serializers for the Accounts app.
"""

from __future__ import annotations

from rest_framework import serializers


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared validation logic.
    """

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
