"""
Base serializers for the Organizations application.
"""

from __future__ import annotations

from apps.platform.organizations.models import Organization
from rest_framework import serializers


class OrganizationBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer for organization serializers.
    """

    class Meta:
        model = Organization
        fields: tuple[str, ...] = ()

    def _normalize(
        self,
        value: str,
    ) -> str:
        """
        Normalize string values.
        """

        return value.strip()

    def validate_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the organization name.
        """

        return self._normalize(
            value,
        )

    def validate_display_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the display name.
        """

        return self._normalize(
            value,
        )

    def validate_code(
        self,
        value: str,
    ) -> str:
        """
        Normalize the organization code.
        """

        return self._normalize(
            value,
        ).upper()

    def validate_slug(
        self,
        value: str,
    ) -> str:
        """
        Normalize the organization slug.
        """

        return self._normalize(
            value,
        ).lower()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the primary email.
        """

        return self._normalize(
            value,
        ).lower()

    def validate_support_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the support email.
        """

        return self._normalize(
            value,
        ).lower()


__all__ = [
    "OrganizationBaseSerializer",
]
