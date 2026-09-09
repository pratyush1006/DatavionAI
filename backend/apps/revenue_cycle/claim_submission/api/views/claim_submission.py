"""API views for claim submission."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.patients.models import Patient
from apps.revenue_cycle.claim_submission.api.serializers import (
    ClaimSubmissionSerializer,
    CreateClaimSubmissionSerializer,
    TransitionClaimSubmissionSerializer,
    UpdateClaimSubmissionSerializer,
)
from apps.revenue_cycle.claim_submission.models import ClaimSubmission
from apps.revenue_cycle.claim_submission.permissions import (
    ClaimSubmissionManagePermission,
    ClaimSubmissionViewPermission,
)
from apps.revenue_cycle.claim_submission.policies import (
    can_manage_submissions,
    can_view_submissions,
)
from apps.revenue_cycle.claim_submission.tenant import resolve_context
from apps.revenue_cycle.claim_submission.workflows.requests import (
    ClaimSubmissionRequest,
)
from apps.revenue_cycle.claim_submission.workflows.workflows import (
    CreateClaimSubmissionWorkflow,
    RestoreClaimSubmissionWorkflow,
    TransitionClaimSubmissionWorkflow,
    UpdateClaimSubmissionWorkflow,
)


def _allowed(request, permission_class, policy, organization):
    """Evaluate API permission and organization policy."""

    return permission_class().has_permission(request, None) and policy(
        user=request.user, organization=organization
    )


class ClaimSubmissionListCreateAPIView(APIView):
    """List and create claim submissions."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """List submissions in the explicit organization context."""

        _, organization = resolve_context(request)
        if not _allowed(
            request, ClaimSubmissionViewPermission, can_view_submissions, organization
        ):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        rows = ClaimSubmission.objects.filter(organization=organization).select_related(
            "patient", "created_by"
        )
        return Response(ClaimSubmissionSerializer(rows, many=True).data)

    def post(self, request):
        """Create a submission through its workflow."""

        tenant, organization = resolve_context(request)
        if not _allowed(
            request,
            ClaimSubmissionManagePermission,
            can_manage_submissions,
            organization,
        ):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateClaimSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = get_object_or_404(
            Patient.objects,
            id=serializer.validated_data["patient_id"],
            organization=organization,
        )
        command = ClaimSubmissionRequest(
            organization_id=str(organization.id),
            tenant_id=str(tenant.id),
            user_id=str(request.user.id),
            patient_id=str(patient.id),
            claim_reference=serializer.validated_data["claim_reference"],
            payer_id=serializer.validated_data["payer_id"],
            payer_name=serializer.validated_data.get("payer_name", ""),
            submission_method=serializer.validated_data.get("submission_method", "edi"),
            idempotency_key=serializer.validated_data["idempotency_key"],
            payload=serializer.validated_data.get("payload", {}),
        )
        result = CreateClaimSubmissionWorkflow(payload=command).execute(
            WorkflowContext(payload=command)
        )
        return Response(
            ClaimSubmissionSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class ClaimSubmissionDetailAPIView(APIView):
    """Retrieve or update one claim submission."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, submission_id):
        """Retrieve a submission."""

        _, organization = resolve_context(request)
        if not _allowed(
            request, ClaimSubmissionViewPermission, can_view_submissions, organization
        ):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        submission = get_object_or_404(
            ClaimSubmission.objects, organization=organization, id=submission_id
        )
        return Response(ClaimSubmissionSerializer(submission).data)

    def patch(self, request, submission_id):
        """Update a submission through its workflow."""

        tenant, organization = resolve_context(request)
        if not _allowed(
            request,
            ClaimSubmissionManagePermission,
            can_manage_submissions,
            organization,
        ):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UpdateClaimSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = ClaimSubmissionRequest(
            organization_id=str(organization.id),
            tenant_id=str(tenant.id),
            user_id=str(request.user.id),
            submission_id=str(submission_id),
            changes=serializer.validated_data,
        )
        result = UpdateClaimSubmissionWorkflow(payload=command).execute(
            WorkflowContext(payload=command)
        )
        return Response(ClaimSubmissionSerializer(result.data).data)


class ClaimSubmissionTransitionAPIView(APIView):
    """Transition a claim submission lifecycle state."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, submission_id):
        """Execute a lifecycle transition."""

        tenant, organization = resolve_context(request)
        if not _allowed(
            request,
            ClaimSubmissionManagePermission,
            can_manage_submissions,
            organization,
        ):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TransitionClaimSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = ClaimSubmissionRequest(
            organization_id=str(organization.id),
            tenant_id=str(tenant.id),
            user_id=str(request.user.id),
            submission_id=str(submission_id),
            target_status=serializer.validated_data["target_status"],
            response_data=serializer.validated_data.get("response_data", {}),
            external_submission_id=serializer.validated_data.get(
                "external_submission_id", ""
            ),
            rejection_code=serializer.validated_data.get("rejection_code", ""),
            rejection_reason=serializer.validated_data.get("rejection_reason", ""),
        )
        result = TransitionClaimSubmissionWorkflow(payload=command).execute(
            WorkflowContext(payload=command)
        )
        return Response(ClaimSubmissionSerializer(result.data).data)


class ClaimSubmissionRestoreAPIView(APIView):
    """Restore a deleted claim submission."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, submission_id):
        """Restore a submission through its workflow."""

        tenant, organization = resolve_context(request)
        if not _allowed(
            request,
            ClaimSubmissionManagePermission,
            can_manage_submissions,
            organization,
        ):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        command = ClaimSubmissionRequest(
            organization_id=str(organization.id),
            tenant_id=str(tenant.id),
            user_id=str(request.user.id),
            submission_id=str(submission_id),
        )
        result = RestoreClaimSubmissionWorkflow(payload=command).execute(
            WorkflowContext(payload=command)
        )
        return Response(ClaimSubmissionSerializer(result.data).data)


__all__ = (
    "ClaimSubmissionListCreateAPIView",
    "ClaimSubmissionDetailAPIView",
    "ClaimSubmissionTransitionAPIView",
    "ClaimSubmissionRestoreAPIView",
)
