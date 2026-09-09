"""Denial REST API views."""

from __future__ import annotations

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext

from ...models import Denial
from ...policies import can_create, can_delete, can_list, can_transition, can_update
from ...selectors import get_denial, list_denials
from ...services import delete_denial, update_denial
from ...workflows import (
    CreateDenialRequest,
    DenialCreationWorkflow,
    DenialTransitionWorkflow,
    TransitionDenialRequest,
)
from ..serializers import DenialSerializer, DenialTransitionSerializer


def _context(request):
    """Require explicit tenant and organization context."""
    try:
        tenant = request.tenant
        organization = request.organization
    except AttributeError as exc:
        raise Http404("Explicit tenant and organization context is required.") from exc
    if organization.tenant_id != tenant.id:
        raise Http404("Tenant and organization context mismatch.")
    return tenant, organization


class DenialListCreateAPIView(APIView):
    """List and create denials."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """List active denials."""
        tenant, organization = _context(request)
        if not can_list(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        denials = list_denials(organization_id=organization.id, tenant_id=tenant.id)
        return Response(DenialSerializer(denials, many=True).data)

    def post(self, request):
        """Create a denial through a workflow."""
        _, organization = _context(request)
        if not can_create(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = DenialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.validated_data.pop("patient")
        result = DenialCreationWorkflow().execute(
            WorkflowContext(
                payload=CreateDenialRequest(
                    organization=organization,
                    patient=patient,
                    actor=request.user,
                    data=serializer.validated_data,
                )
            )
        )
        return Response(
            DenialSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class DenialDetailAPIView(APIView):
    """Retrieve, update, or delete a denial."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, denial_id):
        """Retrieve a denial."""
        tenant, organization = _context(request)
        if not can_list(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            denial = get_denial(
                organization_id=organization.id,
                tenant_id=tenant.id,
                denial_id=denial_id,
            )
        except Denial.DoesNotExist as exc:
            raise Http404 from exc
        return Response(DenialSerializer(denial).data)

    def patch(self, request, denial_id):
        """Update a denial."""
        tenant, organization = _context(request)
        if not can_update(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            denial = get_denial(
                organization_id=organization.id,
                tenant_id=tenant.id,
                denial_id=denial_id,
            )
        except Denial.DoesNotExist as exc:
            raise Http404 from exc
        serializer = DenialSerializer(denial, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = update_denial(denial=denial, data=serializer.validated_data)
        return Response(DenialSerializer(updated).data)

    def delete(self, request, denial_id):
        """Soft-delete a denial."""
        tenant, organization = _context(request)
        if not can_delete(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            denial = get_denial(
                organization_id=organization.id,
                tenant_id=tenant.id,
                denial_id=denial_id,
            )
        except Denial.DoesNotExist as exc:
            raise Http404 from exc
        delete_denial(denial=denial, actor_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DenialTransitionAPIView(APIView):
    """Transition a denial through its governed lifecycle."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, denial_id):
        """Execute a lifecycle transition."""
        tenant, organization = _context(request)
        if not can_transition(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            denial = get_denial(
                organization_id=organization.id,
                tenant_id=tenant.id,
                denial_id=denial_id,
            )
        except Denial.DoesNotExist as exc:
            raise Http404 from exc
        serializer = DenialTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = DenialTransitionWorkflow().execute(
            WorkflowContext(
                payload=TransitionDenialRequest(
                    denial=denial, actor=request.user, **serializer.validated_data
                )
            )
        )
        return Response(DenialSerializer(result.data).data)


__all__ = ("DenialDetailAPIView", "DenialListCreateAPIView", "DenialTransitionAPIView")
