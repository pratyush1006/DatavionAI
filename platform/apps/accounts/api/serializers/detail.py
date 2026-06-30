"""
Detail serializer for the Accounts app.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.api.serializers.fields import _DETAIL_FIELDS
from apps.accounts.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """

    class Meta:
        model = User

        fields = _DETAIL_FIELDS

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
