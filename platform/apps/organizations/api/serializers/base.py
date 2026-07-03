"""
Base serializers for the Organizations application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organizations.models import Organization


class OrganizationBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared validation logic.
    """

    class Meta:
        model = Organization
        fields: tuple[str, ...] = ()

    def validate_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the organization name.
        """

        return value.strip()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the organization email.
        """

        if not value:
            return value

        return value.strip().lower()


__all__ = [
    "OrganizationBaseSerializer",
]
