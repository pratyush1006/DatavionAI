"""
Summary serializer for the Accounts application.
"""

from __future__ import annotations

from apps.platform.accounts.models import User

from .base import UserBaseSerializer
from .fields import SUMMARY_FIELDS


class UserSummarySerializer(
    UserBaseSerializer,
):
    """
    Serializer for user summary responses.
    """

    class Meta(
        UserBaseSerializer.Meta,
    ):
        model = User

        fields = SUMMARY_FIELDS

        read_only_fields = SUMMARY_FIELDS


__all__ = ("UserSummarySerializer",)
