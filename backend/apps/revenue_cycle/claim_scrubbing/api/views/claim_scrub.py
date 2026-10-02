"""Claim scrubbing API views."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.claim_scrubbing.api.serializers import (
    ClaimScrubSerializer,
    CreateClaimScrubSerializer,
)
from apps.revenue_cycle.claim_scrubbing.models import ClaimScrub
from apps.revenue_cycle.claim_scrubbing.permissions import (
    ClaimScrubbingPermission,
    ClaimScrubbingViewPermission,
)
from apps.revenue_cycle.claim_scrubbing.policies import (
    can_manage_scrubs,
    can_view_scrubs,
)
from apps.revenue_cycle.claim_scrubbing.services import create_scrub
from apps.revenue_cycle.claim_scrubbing.tenant import resolve_context
from apps.revenue_cycle.claim_scrubbing.workflows.requests import ScrubLifecycleRequest
from apps.revenue_cycle.claim_scrubbing.workflows.workflows import (
    OverrideClaimScrubWorkflow,
    RunClaimScrubWorkflow,
)


class ClaimScrubListCreateAPIView(APIView):
    """List and create claim scrubs."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """List tenant-scoped scrubs."""

        _, organization = resolve_context(request)
        if not ClaimScrubbingViewPermission().has_permission(
            request, self
        ) or not can_view_scrubs(user=request.user, organization=organization):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        rows = ClaimScrub.objects.filter(organization=organization).prefetch_related(
            "findings"
        )
        return Response(ClaimScrubSerializer(rows, many=True).data)

    def post(self, request):
        """Create an idempotent claim scrub."""

        _, organization = resolve_context(request)
        if not ClaimScrubbingPermission().has_permission(
            request, self
        ) or not can_manage_scrubs(user=request.user, organization=organization):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateClaimScrubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = get_object_or_404(
            Patient.objects,
            id=serializer.validated_data["patient_id"],
            organization=organization,
        )
        scrub, _ = create_scrub(
            organization=organization,
            patient=patient,
            user=request.user,
            **serializer.validated_data,
        )
        return Response(
            ClaimScrubSerializer(scrub).data, status=status.HTTP_201_CREATED
        )


class ClaimScrubDetailAPIView(APIView):
    """Retrieve one tenant-scoped claim scrub."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, scrub_id):
        """Return one scrub."""

        _, organization = resolve_context(request)
        if not ClaimScrubbingViewPermission().has_permission(
            request, self
        ) or not can_view_scrubs(user=request.user, organization=organization):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        scrub = get_object_or_404(
            ClaimScrub.objects.prefetch_related("findings"),
            id=scrub_id,
            organization=organization,
        )
        return Response(ClaimScrubSerializer(scrub).data)


class ClaimScrubRunAPIView(APIView):
    """Execute a claim scrub."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, scrub_id):
        """Run the scrub workflow."""

        tenant, organization = resolve_context(request)
        if not ClaimScrubbingPermission().has_permission(
            request, self
        ) or not can_manage_scrubs(user=request.user, organization=organization):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        request_data = ScrubLifecycleRequest(
            organization_id=str(organization.id),
            tenant_id=str(tenant.id),
            scrub_id=str(scrub_id),
        )
        result = RunClaimScrubWorkflow(payload=request_data).run(
            WorkflowContext(payload=request_data)
        )
        return Response(ClaimScrubSerializer(result.data).data)


class ClaimScrubOverrideAPIView(APIView):
    """Override a failed claim scrub."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, scrub_id):
        """Run the override workflow."""

        tenant, organization = resolve_context(request)
        if not ClaimScrubbingPermission().has_permission(
            request, self
        ) or not can_manage_scrubs(user=request.user, organization=organization):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        reason = str(request.data.get("reason", "")).strip()
        if not reason:
            return Response(
                {"detail": "Override reason is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request_data = ScrubLifecycleRequest(
            organization_id=str(organization.id),
            tenant_id=str(tenant.id),
            scrub_id=str(scrub_id),
            reason=reason,
        )
        result = OverrideClaimScrubWorkflow(payload=request_data).run(
            WorkflowContext(payload=request_data)
        )
        return Response(ClaimScrubSerializer(result.data).data)


__all__ = (
    "ClaimScrubListCreateAPIView",
    "ClaimScrubDetailAPIView",
    "ClaimScrubRunAPIView",
    "ClaimScrubOverrideAPIView",
)
