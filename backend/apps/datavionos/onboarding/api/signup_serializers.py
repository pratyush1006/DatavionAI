from __future__ import annotations

from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.datavionos.onboarding.api.serializers import (
    OrganizationOnboardingSerializer,
)


class SelfServiceSignupAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        validators=[validate_password],
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )

    def validate_email(self, value: str) -> str:
        return value.strip().lower()


class SelfServiceSignupOrganizationSerializer(OrganizationOnboardingSerializer):
    pass


class SelfServiceSignupSerializer(serializers.Serializer):
    account = SelfServiceSignupAccountSerializer()
    organization = SelfServiceSignupOrganizationSerializer()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        organization = attrs["organization"]

        if not organization.get("category"):
            raise serializers.ValidationError(
                {"organization": {"category": "This field is required."}}
            )
        if not organization.get("organization_type"):
            raise serializers.ValidationError(
                {"organization": {"organization_type": "This field is required."}}
            )
        if not organization.get("size"):
            raise serializers.ValidationError(
                {"organization": {"size": "This field is required."}}
            )

        return attrs


__all__ = [
    "SelfServiceSignupAccountSerializer",
    "SelfServiceSignupOrganizationSerializer",
    "SelfServiceSignupSerializer",
]
