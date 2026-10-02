"""Patient financial responsibility serializers."""

from __future__ import annotations

from apps.revenue_cycle.billing.patient_billing.models import (
    PatientFinancialResponsibility,
)
from rest_framework import serializers


class PatientResponsibilitySerializer(serializers.ModelSerializer):
    """Serialize financial responsibility records."""

    class Meta:
        """Serializer metadata."""

        model = PatientFinancialResponsibility
        fields = (
            "id",
            "account",
            "party_type",
            "guarantor",
            "percentage",
            "priority",
            "effective_from",
            "effective_to",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "account",
            "is_active",
            "created_at",
            "updated_at",
        )


class PatientResponsibilityCreateSerializer(serializers.ModelSerializer):
    """Validate financial responsibility creation."""

    class Meta:
        """Serializer metadata."""

        model = PatientFinancialResponsibility
        fields = (
            "party_type",
            "guarantor",
            "percentage",
            "priority",
            "effective_from",
            "effective_to",
            "notes",
        )


class PatientResponsibilityUpdateSerializer(serializers.ModelSerializer):
    """Validate financial responsibility updates."""

    class Meta:
        """Serializer metadata."""

        model = PatientFinancialResponsibility
        fields = (
            "party_type",
            "guarantor",
            "percentage",
            "priority",
            "effective_from",
            "effective_to",
            "notes",
        )


__all__ = (
    "PatientResponsibilityCreateSerializer",
    "PatientResponsibilitySerializer",
    "PatientResponsibilityUpdateSerializer",
)
