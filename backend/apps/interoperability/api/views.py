"""FHIR and HL7 interoperability API views."""

from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.encounters.models import Encounter
from apps.clinical.providers.models import Provider
from apps.interoperability.api.serializers import (
    HL7ADTRequestSerializer,
    HL7ORURequestSerializer,
)
from apps.interoperability.serializers.fhir import (
    encounter_to_fhir,
    organization_to_fhir,
    patient_to_fhir,
    provider_to_fhir,
)
from apps.interoperability.serializers.hl7 import build_adt_a01, build_oru_r01
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class FHIRPatientDetailAPIView(APIView):
    """Return a tenant-scoped FHIR Patient resource."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=dict)
    def get(self, request: Any, patient_id: str) -> Response:
        organization = getattr(request, "organization", None)
        patient = get_object_or_404(Patient, id=patient_id, organization=organization)
        return Response(patient_to_fhir(patient))


class FHIREncounterDetailAPIView(APIView):
    """Return a tenant-scoped FHIR Encounter resource."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=dict)
    def get(self, request: Any, encounter_id: str) -> Response:
        organization = getattr(request, "organization", None)
        encounter = get_object_or_404(
            Encounter, id=encounter_id, organization=organization
        )
        return Response(encounter_to_fhir(encounter))


class FHIRProviderDetailAPIView(APIView):
    """Return a tenant-scoped FHIR Practitioner resource."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=dict)
    def get(self, request: Any, provider_id: str) -> Response:
        organization = getattr(request, "organization", None)
        provider = get_object_or_404(
            Provider, id=provider_id, organization=organization
        )
        return Response(provider_to_fhir(provider))


class FHIROrganizationDetailAPIView(APIView):
    """Return the current organization as a FHIR Organization resource."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=dict)
    def get(self, request: Any) -> Response:
        organization = getattr(request, "organization", None)
        if organization is None:
            return Response({"detail": "Organization context is required."}, status=400)
        organization = get_object_or_404(Organization, id=organization.id)
        return Response(organization_to_fhir(organization))


class HL7ADTAPIView(APIView):
    """Build an HL7 v2 ADT^A01 message."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(request=HL7ADTRequestSerializer, responses=dict)
    def post(self, request: Any) -> Response:
        serializer = HL7ADTRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        return Response(
            {
                "message_type": "ADT^A01",
                "message": build_adt_a01(**payload),
            },
            status=200,
        )


class HL7ORUAPIView(APIView):
    """Build an HL7 v2 ORU^R01 message."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(request=HL7ORURequestSerializer, responses=dict)
    def post(self, request: Any) -> Response:
        serializer = HL7ORURequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        return Response(
            {
                "message_type": "ORU^R01",
                "message": build_oru_r01(**payload),
            },
            status=200,
        )


__all__ = [
    "FHIRPatientDetailAPIView",
    "FHIREncounterDetailAPIView",
    "FHIRProviderDetailAPIView",
    "FHIROrganizationDetailAPIView",
    "HL7ADTAPIView",
    "HL7ORUAPIView",
]
