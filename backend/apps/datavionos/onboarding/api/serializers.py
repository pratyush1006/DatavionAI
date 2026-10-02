from __future__ import annotations

from rest_framework import serializers

from apps.platform.geography.models import (
    AdministrativeRegion,
    City,
    Country,
)
from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationSize,
    OrganizationType,
)


class OrganizationOnboardingSerializer(serializers.Serializer):
    """Canonical organization registration payload."""

    name = serializers.CharField(max_length=255)
    display_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    code = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )
    slug = serializers.SlugField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    category = serializers.ChoiceField(
        choices=OrganizationCategory.choices,
    )
    organization_type = serializers.ChoiceField(
        choices=OrganizationType.choices,
    )
    size = serializers.ChoiceField(
        choices=OrganizationSize.choices,
    )
    category_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    support_email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )
    website = serializers.URLField(
        max_length=500,
        required=False,
        allow_blank=True,
    )
    address = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    city = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    state = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    country = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    country_ref = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        required=False,
        allow_null=True,
    )
    region_ref = serializers.PrimaryKeyRelatedField(
        queryset=AdministrativeRegion.objects.all(),
        required=False,
        allow_null=True,
    )
    city_ref = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False,
        allow_null=True,
    )

    postal_code = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )
    timezone = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    registration_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    tax_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    license_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    accreditation = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    is_demo = serializers.BooleanField(
        required=False,
        default=False,
    )

    plan_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )
    plan_code = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        country = attrs.get("country_ref")
        region = attrs.get("region_ref")
        city = attrs.get("city_ref")

        for field_name, value in (
            ("country_ref", country),
            ("region_ref", region),
            ("city_ref", city),
        ):
            if value is not None and (not value.is_active or value.is_deleted):
                raise serializers.ValidationError(
                    {
                        field_name: "The selected Geography record is inactive or archived."
                    }
                )

        if region is not None and country is None:
            raise serializers.ValidationError(
                {"country_ref": "Country is required when a region is selected."}
            )

        if city is not None and region is None:
            raise serializers.ValidationError(
                {"region_ref": "State / region is required when a city is selected."}
            )

        if (
            region is not None
            and country is not None
            and region.country_id != country.pk
        ):
            raise serializers.ValidationError(
                {
                    "region_ref": "Selected region does not belong to the selected country."
                }
            )

        if city is not None and country is not None and city.country_id != country.pk:
            raise serializers.ValidationError(
                {"city_ref": "Selected city does not belong to the selected country."}
            )

        if city is not None and region is not None and city.region_id != region.pk:
            raise serializers.ValidationError(
                {"city_ref": "Selected city does not belong to the selected region."}
            )

        return attrs


class OrganizationPreflightSerializer(serializers.Serializer):
    category = serializers.ChoiceField(
        choices=OrganizationCategory.choices,
    )
    organization_type = serializers.ChoiceField(
        choices=OrganizationType.choices,
    )
    size = serializers.ChoiceField(
        choices=OrganizationSize.choices,
    )
    plan_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )
    plan_code = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )


class OrganizationTypeSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    category = serializers.CharField()
    category_name = serializers.CharField()


class SaaSPlanSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    plan_type = serializers.CharField()
    healthcare_segment = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    currency = serializers.CharField()
    billing_cycle = serializers.CharField()
    trial_days = serializers.IntegerField()
    modules = serializers.JSONField()
    features = serializers.JSONField()
    limits = serializers.JSONField()
    is_featured = serializers.BooleanField()
    is_default = serializers.BooleanField()


__all__ = [
    "OrganizationOnboardingSerializer",
    "OrganizationPreflightSerializer",
    "OrganizationTypeSerializer",
    "SaaSPlanSerializer",
]
