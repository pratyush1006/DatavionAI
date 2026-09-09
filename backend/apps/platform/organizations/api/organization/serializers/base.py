"""
Base serializers for the Organizations application.
"""

from __future__ import annotations

from apps.common.api.serializers.base import BaseModelSerializer
from apps.platform.geography.models import (
    AdministrativeRegion,
    City,
    Country,
)
from apps.platform.organizations.models import Organization
from rest_framework import serializers


class OrganizationBaseSerializer(
    BaseModelSerializer,
):
    """
    Base serializer for Organization serializers.

    Provides common normalization and field-level validation shared
    across create, update, detail, list, and summary serializers.

    Geography references are validated here at the API boundary.
    Cross-reference hierarchy validation is delegated to the
    Organization domain service.
    """

    class Meta:
        model = Organization
        fields: tuple[str, ...] = ()

    # ==========================================================
    # Normalization helpers
    # ==========================================================

    def _normalize(
        self,
        value: str | None,
    ) -> str | None:
        """
        Strip leading and trailing whitespace.

        Returns ``None`` unchanged to support nullable fields.
        """

        if value is None:
            return None

        return value.strip()

    def _normalize_lower(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize and convert to lowercase.
        """

        value = self._normalize(value)

        if value is None:
            return None

        return value.lower()

    def _normalize_upper(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize and convert to uppercase.
        """

        value = self._normalize(value)

        if value is None:
            return None

        return value.upper()

    # ==========================================================
    # Core identity
    # ==========================================================

    def validate_name(
        self,
        value: str,
    ) -> str:
        return self._normalize(value)

    def validate_display_name(
        self,
        value: str,
    ) -> str:
        return self._normalize(value)

    def validate_code(
        self,
        value: str,
    ) -> str:
        return self._normalize_upper(value)

    def validate_slug(
        self,
        value: str,
    ) -> str:
        return self._normalize_lower(value)

    # ==========================================================
    # Contact information
    # ==========================================================

    def validate_email(
        self,
        value: str,
    ) -> str:
        return self._normalize_lower(value)

    def validate_support_email(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize_lower(value)

    def validate_website(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_phone(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    # ==========================================================
    # Address
    # ==========================================================

    def validate_address(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_city(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_state(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_country(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_postal_code(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    # ==========================================================
    # Geography master-data references
    # ==========================================================

    def validate_country_ref(
        self,
        value: Country | None,
    ) -> Country | None:
        """
        Validate the selected Geography country.

        Only active Geography records may be referenced by an
        Organization.
        """

        if value is None:
            return None

        if not value.is_active or value.is_deleted:
            raise serializers.ValidationError(
                "The selected country is inactive or archived.",
            )

        return value

    def validate_region_ref(
        self,
        value: AdministrativeRegion | None,
    ) -> AdministrativeRegion | None:
        """
        Validate the selected Geography region.
        """

        if value is None:
            return None

        if not value.is_active or value.is_deleted:
            raise serializers.ValidationError(
                "The selected region is inactive or archived.",
            )

        return value

    def validate_city_ref(
        self,
        value: City | None,
    ) -> City | None:
        """
        Validate the selected Geography city.
        """

        if value is None:
            return None

        if not value.is_active or value.is_deleted:
            raise serializers.ValidationError(
                "The selected city is inactive or archived.",
            )

        return value

    # ==========================================================
    # Registration
    # ==========================================================

    def validate_registration_number(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_tax_number(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_license_number(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    def validate_accreditation(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    # ==========================================================
    # Miscellaneous
    # ==========================================================

    def validate_description(
        self,
        value: str | None,
    ) -> str | None:
        return self._normalize(value)

    # ==========================================================
    # Geography hierarchy
    # ==========================================================

    def validate(
        self,
        attrs: dict[str, object],
    ) -> dict[str, object]:
        """
        Validate Geography reference relationships.

        Full cross-reference validation is performed in the domain
        service because update operations must also consider the
        persisted Organization state.
        """

        country_ref = attrs.get("country_ref")
        region_ref = attrs.get("region_ref")
        city_ref = attrs.get("city_ref")

        if region_ref is not None and country_ref is None:
            raise serializers.ValidationError(
                {
                    "country_ref": (
                        "Country reference is required when "
                        "a region reference is supplied."
                    ),
                },
            )

        if city_ref is not None and country_ref is None:
            raise serializers.ValidationError(
                {
                    "country_ref": (
                        "Country reference is required when "
                        "a city reference is supplied."
                    ),
                },
            )

        return attrs


__all__: tuple[str, ...] = ("OrganizationBaseSerializer",)
