"""
Revenue Cycle Appeals API views.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.revenue_cycle.appeals.api.serializers import (
    AppealSerializer,
    AppealTransitionSerializer,
)
from apps.revenue_cycle.appeals.exceptions import (
    AppealError,
    AppealNotFoundError,
    InvalidAppealTransition,
)
from apps.revenue_cycle.appeals.models import Appeal
from apps.revenue_cycle.appeals.policies import AppealPolicy
from apps.revenue_cycle.appeals.selectors import (
    get_appeal,
    list_appeals,
)
from apps.revenue_cycle.appeals.workflows import (
    AppealCreateWorkflow,
    AppealDeletionWorkflow,
    AppealRestoreWorkflow,
    AppealTransitionWorkflow,
)


def _tenant(request: Request) -> UUID:
    """Return the explicit tenant from the request."""
    value = getattr(request, "tenant", None)
    if value is None or getattr(value, "id", None) is None:
        raise PermissionError("Explicit request.tenant is required.")
    return value.id


def _organization(request: Request) -> Any:
    """Return the explicit organization and validate its tenant."""
    organization = getattr(request, "organization", None)
    if organization is None or getattr(organization, "id", None) is None:
        raise PermissionError("Explicit request.organization is required.")

    tenant_id = _tenant(request)
    if organization.tenant_id != tenant_id:
        raise PermissionError("Organization does not belong to the active tenant.")
    return organization


def _context(request: Request) -> WorkflowContext:
    """Build a workflow context from explicit request context."""
    return WorkflowContext.create(
        actor=request.user,
        tenant_id=_tenant(request),
    )


class AppealListCreateAPIView(APIView):
    """List and create tenant-scoped appeals."""

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Return active appeals visible to the organization."""
        organization = _organization(request)
        if not AppealPolicy.can_list(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = list_appeals(
            organization_id=organization.id,
            tenant_id=_tenant(request),
        )
        return Response(
            AppealSerializer(
                queryset,
                many=True,
            ).data
        )

    def post(self, request: Request) -> Response:
        """Create an appeal through the creation workflow."""
        organization = _organization(request)
        if not AppealPolicy.can_create(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AppealSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        patient = serializer.validated_data.pop("patient")
        payload = dict(serializer.validated_data)

        result = AppealCreateWorkflow().execute(
            context=_context(request),
            organization_id=organization.id,
            patient_id=patient.id,
            data=payload,
        )
        return Response(
            AppealSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class AppealRetrieveUpdateAPIView(APIView):
    """Retrieve and update one appeal."""

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, appeal_id: UUID) -> Response:
        """Return one tenant-scoped appeal."""
        organization = _organization(request)
        appeal = get_appeal(
            organization_id=organization.id,
            tenant_id=_tenant(request),
            appeal_id=appeal_id,
        )
        if appeal is None:
            return Response(
                {"detail": "Appeal not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not AppealPolicy.can_list(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(AppealSerializer(appeal).data)

    def patch(self, request: Request, appeal_id: UUID) -> Response:
        """Update one non-terminal appeal."""
        organization = _organization(request)
        appeal = get_appeal(
            organization_id=organization.id,
            tenant_id=_tenant(request),
            appeal_id=appeal_id,
        )
        if appeal is None:
            return Response(
                {"detail": "Appeal not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not AppealPolicy.can_mutate(
            actor=request.user,
            organization=organization,
            appeal=appeal,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AppealSerializer(
            appeal,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        return Response(AppealSerializer(serializer.save()).data)


class AppealTransitionAPIView(APIView):
    """Transition an appeal through its controlled lifecycle."""

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, appeal_id: UUID) -> Response:
        """Apply a lifecycle transition."""
        organization = _organization(request)
        appeal = get_appeal(
            organization_id=organization.id,
            tenant_id=_tenant(request),
            appeal_id=appeal_id,
        )
        if appeal is None:
            return Response(
                {"detail": "Appeal not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not AppealPolicy.can_mutate(
            actor=request.user,
            organization=organization,
            appeal=appeal,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AppealTransitionSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        try:
            result = AppealTransitionWorkflow().execute(
                context=_context(request),
                organization_id=organization.id,
                appeal_id=appeal_id,
                target_status=serializer.validated_data["status"],
                reason=serializer.validated_data.get("reason", ""),
            )
        except (
            AppealNotFoundError,
            InvalidAppealTransition,
            AppealError,
        ) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(AppealSerializer(result.data).data)


class AppealDeleteAPIView(APIView):
    """Soft-delete an appeal."""

    permission_classes = (IsAuthenticated,)

    def delete(self, request: Request, appeal_id: UUID) -> Response:
        """Delete an appeal through its workflow."""
        organization = _organization(request)
        appeal = get_appeal(
            organization_id=organization.id,
            tenant_id=_tenant(request),
            appeal_id=appeal_id,
        )
        if appeal is None:
            return Response(
                {"detail": "Appeal not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not AppealPolicy.can_mutate(
            actor=request.user,
            organization=organization,
            appeal=appeal,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = AppealDeletionWorkflow().execute(
            context=_context(request),
            organization_id=organization.id,
            appeal_id=appeal_id,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class AppealRestoreAPIView(APIView):
    """Restore a deleted appeal."""

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, appeal_id: UUID) -> Response:
        """Restore an appeal through its workflow."""
        organization = _organization(request)
        if not AppealPolicy.can_create(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            result = AppealRestoreWorkflow().execute(
                context=_context(request),
                organization_id=organization.id,
                appeal_id=appeal_id,
            )
        except AppealNotFoundError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(AppealSerializer(result.data).data)


__all__ = (
    "AppealDeleteAPIView",
    "AppealListCreateAPIView",
    "AppealRestoreAPIView",
    "AppealRetrieveUpdateAPIView",
    "AppealTransitionAPIView",
)
