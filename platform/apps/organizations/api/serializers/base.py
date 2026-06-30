"""
Base serializers for the Organizations app.
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
        fields = ()

    def validate_name(self, value: str) -> str:
        """
        Normalize organization name.
        """
        return value.strip()

    def validate_email(self, value: str) -> str:
        """
        Normalize organization email.
        """
        return value.strip().lower() if value else value
