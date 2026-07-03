"""
List serializer for the Accounts application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import User

from .fields import LIST_FIELDS


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users.
    """

    class Meta:
        model = User
        fields = LIST_FIELDS
        read_only_fields = LIST_FIELDS


__all__ = [
    "UserListSerializer",
]
