"""
List serializer for the Accounts app.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.api.serializers.fields import _LIST_FIELDS
from apps.accounts.models import User


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users.
    """

    class Meta:
        model = User

        fields = _LIST_FIELDS

        read_only_fields = _LIST_FIELDS
