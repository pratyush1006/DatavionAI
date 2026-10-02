"""Charge Capture API views."""

from __future__ import annotations

from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.patients.models import Patient

from ...models import Charge
from ...policies import ChargeCapturePolicy
from ...selectors import ChargeSelector
from ...workflows import (
    ChargeCreateWorkflow,
    ChargeTransitionWorkflow,
    ChargeVoidWorkflow,
)
from ..serializers import (
    ChargeCreateSerializer,
    ChargeSerializer,
    ChargeTransitionSerializer,
    ChargeVoidSerializer,
)

__all__ = (
    "ChargeListCreateView",
    "ChargeDetailView",
    "ChargeTransitionView",
    "ChargeVoidView",
)


def _tenant_id(request):
    """Return the explicitly supplied request tenant identifier."""

    tenant = getattr(request, "tenant", None)
    if tenant is None:
        raise PermissionError("Explicit request.tenant is required.")
    return tenant.id


def _organization(request):
    """Return the explicitly supplied request organization."""

    organization = getattr(request, "organization", None)
    if organization is None:
        raise PermissionError("Explicit request.organization is required.")
    return organization


class ChargeListCreateView(APIView):
    """List and create Charge Capture records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return tenant-scoped charges."""

        organization = _organization(request)
        tenant_id = _tenant_id(request)

        if not ChargeCapturePolicy.can_read(
            actor=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        charges = ChargeSelector.list(
            tenant_id=tenant_id,
            organization_id=organization.id,
        )
        return Response(ChargeSerializer(charges, many=True).data)

    def post(self, request):
        """Create a tenant-scoped charge."""

        organization = _organization(request)
        tenant_id = _tenant_id(request)

        if not ChargeCapturePolicy.can_create(
            actor=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ChargeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = Patient.objects.get(
            id=serializer.validated_data["patient_id"],
        )

        charge = ChargeCreateWorkflow().execute(
            actor=request.user,
            tenant_id=tenant_id,
            organization=organization,
            patient=patient,
            **{
                key: value
                for key, value in serializer.validated_data.items()
                if key != "patient_id"
            },
        )
        return Response(
            ChargeSerializer(charge).data,
            status=status.HTTP_201_CREATED,
        )


class ChargeDetailView(APIView):
    """Retrieve one Charge Capture record."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, charge_id: UUID):
        """Return one tenant-scoped charge."""

        organization = _organization(request)
        tenant_id = _tenant_id(request)

        if not ChargeCapturePolicy.can_read(
            actor=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        charge = ChargeSelector.get(
            charge_id=charge_id,
            tenant_id=tenant_id,
            organization_id=organization.id,
        )
        return Response(ChargeSerializer(charge).data)


class ChargeTransitionView(APIView):
    """Transition a Charge Capture record."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, charge_id: UUID):
        """Apply a permitted charge lifecycle transition."""

        organization = _organization(request)
        tenant_id = _tenant_id(request)

        if not ChargeCapturePolicy.can_update(
            actor=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ChargeTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        charge = ChargeTransitionWorkflow().execute(
            actor=request.user,
            tenant_id=tenant_id,
            organization=organization,
            charge_id=charge_id,
            **serializer.validated_data,
        )
        return Response(ChargeSerializer(charge).data)


class ChargeVoidView(APIView):
    """Void a Charge Capture record."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, charge_id: UUID):
        """Void a charge when policy permits."""

        organization = _organization(request)
        tenant_id = _tenant_id(request)

        if not ChargeCapturePolicy.can_void(
            actor=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ChargeVoidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        charge = ChargeVoidWorkflow().execute(
            actor=request.user,
            tenant_id=tenant_id,
            organization=organization,
            charge_id=charge_id,
            **serializer.validated_data,
        )
        return Response(ChargeSerializer(charge).data)
