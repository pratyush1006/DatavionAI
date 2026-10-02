"""Interoperability API request serializers."""

from __future__ import annotations

from rest_framework import serializers


class HL7ADTRequestSerializer(serializers.Serializer):
    """Request payload for ADT^A01 generation."""

    sending_app = serializers.CharField(max_length=100)
    sending_facility = serializers.CharField(max_length=100)
    patient_id = serializers.CharField(max_length=100)
    patient_name = serializers.CharField(max_length=200)
    gender = serializers.CharField(max_length=20)


class HL7ORURequestSerializer(serializers.Serializer):
    """Request payload for ORU^R01 generation."""

    sending_app = serializers.CharField(max_length=100)
    sending_facility = serializers.CharField(max_length=100)
    patient_id = serializers.CharField(max_length=100)
    observation_id = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=1000)


__all__ = ["HL7ADTRequestSerializer", "HL7ORURequestSerializer"]
