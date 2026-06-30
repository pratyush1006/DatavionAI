"""
Serializers for the Organizations app.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organizations.models import Organization

_LIST_FIELDS = (
    "id",
    "name",
    "code",
    "organization_type",
    "city",
    "country",
    "is_active",
)

_DETAIL_FIELDS = (
    "id",
    "name",
    "code",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
    "created_at",
    "updated_at",
)

_WRITE_FIELDS = (
    "name",
    "code",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
)

_UPDATE_FIELDS = (
    "name",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
)


class OrganizationBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared validation logic.
    """

    def validate_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize organization name.
        """
        return value.strip()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize organization email.
        """
        return value.strip().lower() if value else value


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing organizations.
    """

    class Meta:
        model = Organization

        fields = _LIST_FIELDS

        read_only_fields = _LIST_FIELDS


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving organization details.
    """

    class Meta:
        model = Organization

        fields = _DETAIL_FIELDS

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class OrganizationCreateSerializer(OrganizationBaseSerializer):
    """
    Serializer for creating organizations.
    """

    class Meta:
        model = Organization

        fields = _WRITE_FIELDS

    def validate_code(
        self,
        value: str,
    ) -> str:
        """
        Normalize organization code.
        """
        return value.strip().upper()


class OrganizationUpdateSerializer(OrganizationBaseSerializer):
    """
    Serializer for updating organizations.
    """

    class Meta:
        model = Organization

        fields = _UPDATE_FIELDS
