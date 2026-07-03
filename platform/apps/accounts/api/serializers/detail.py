"""
Detail serializer for the Accounts application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import User

from .fields import DETAIL_FIELDS


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """

    class Meta:
        model = User
        fields = DETAIL_FIELDS
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "UserDetailSerializer",
]
