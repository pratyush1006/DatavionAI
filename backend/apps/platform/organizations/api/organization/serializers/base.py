"""
Base serializers for the Organizations application.
"""

from __future__ import annotations

from apps.common.api.serializers.base import BaseModelSerializer
from apps.platform.organizations.models import Organization


class OrganizationBaseSerializer(BaseModelSerializer):
    """
    Base serializer for Organization serializers.

    Provides common normalization and field-level validation shared
    across create, update, detail, list, and summary serializers.
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
        """
        Normalize organization name.
        """

        return self._normalize(value)

    def validate_display_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize display name.
        """

        return self._normalize(value)

    def validate_code(
        self,
        value: str,
    ) -> str:
        """
        Normalize organization code.
        """

        return self._normalize_upper(value)

    def validate_slug(
        self,
        value: str,
    ) -> str:
        """
        Normalize organization slug.
        """

        return self._normalize_lower(value)

    # ==========================================================
    # Contact information
    # ==========================================================

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize primary email.
        """

        return self._normalize_lower(value)

    def validate_support_email(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize support email.
        """

        return self._normalize_lower(value)

    def validate_website(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize website.
        """

        return self._normalize(value)

    def validate_phone(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize phone number.
        """

        return self._normalize(value)

    # ==========================================================
    # Address
    # ==========================================================

    def validate_address(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize address.
        """

        return self._normalize(value)

    def validate_city(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize city.
        """

        return self._normalize(value)

    def validate_state(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize state.
        """

        return self._normalize(value)

    def validate_country(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize country.
        """

        return self._normalize(value)

    def validate_postal_code(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize postal code.
        """

        return self._normalize(value)

    # ==========================================================
    # Registration
    # ==========================================================

    def validate_registration_number(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize registration number.
        """

        return self._normalize(value)

    def validate_tax_number(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize tax number.
        """

        return self._normalize(value)

    def validate_license_number(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize license number.
        """

        return self._normalize(value)

    def validate_accreditation(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize accreditation.
        """

        return self._normalize(value)

    # ==========================================================
    # Miscellaneous
    # ==========================================================

    def validate_description(
        self,
        value: str | None,
    ) -> str | None:
        """
        Normalize description.
        """

        return self._normalize(value)


__all__: tuple[str, ...] = ("OrganizationBaseSerializer",)
