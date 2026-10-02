"""Patient Address API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.addresses.models import Address


class AddressSerializer(serializers.ModelSerializer):
    coordinates = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()

    class Meta:
        model = Address
        fields = (
            "id",
            "tenant",
            "organization",
            "patient",
            "address_type",
            "address_use",
            "status",
            "source",
            "address_line_1",
            "address_line_2",
            "landmark",
            "district",
            "postal_code",
            "country",
            "region",
            "city",
            "city_name",
            "region_name",
            "country_name",
            "country_code",
            "latitude",
            "longitude",
            "formatted_address",
            "geocoding_place_id",
            "geocoding_raw",
            "geocoded_at",
            "is_primary",
            "is_verified",
            "verification_notes",
            "verified_at",
            "verified_by",
            "created_at",
            "updated_at",
            "coordinates",
            "full_address",
        )
        read_only_fields = (
            "id",
            "formatted_address",
            "geocoding_place_id",
            "geocoding_raw",
            "geocoded_at",
            "is_verified",
            "verified_at",
            "verified_by",
            "created_at",
            "updated_at",
            "coordinates",
            "full_address",
        )

    def validate(self, attrs):
        tenant = attrs.get("tenant", getattr(self.instance, "tenant", None))
        organization = attrs.get(
            "organization",
            getattr(self.instance, "organization", None),
        )
        patient = attrs.get("patient", getattr(self.instance, "patient", None))
        if tenant and organization and organization.tenant_id != tenant.id:
            raise serializers.ValidationError(
                {"tenant": "Tenant must match organization tenant."}
            )
        if patient and organization and patient.organization_id != organization.id:
            raise serializers.ValidationError(
                {"patient": "Patient must belong to organization."}
            )
        return attrs
