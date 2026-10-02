"""Insurance Verification API views."""

from __future__ import annotations

from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.revenue_cycle.insurance_verification.api.serializers import (
    InsuranceVerificationDetailSerializer,
    InsuranceVerificationLifecycleSerializer,
    InsuranceVerificationWriteSerializer,
)
from apps.revenue_cycle.insurance_verification.policies import (
    can_create,
    can_delete,
    can_restore,
    can_transition,
    can_update,
    can_view,
)
from apps.revenue_cycle.insurance_verification.selectors import (
    get_verification,
    list_verifications,
)
from apps.revenue_cycle.insurance_verification.workflows import (
    InsuranceVerificationCreateRequest,
    InsuranceVerificationCreationWorkflow,
    InsuranceVerificationDeleteRequest,
    InsuranceVerificationDeletionWorkflow,
    InsuranceVerificationLifecycleRequest,
    InsuranceVerificationLifecycleWorkflow,
    InsuranceVerificationRestoreRequest,
    InsuranceVerificationRestoreWorkflow,
    InsuranceVerificationUpdateRequest,
    InsuranceVerificationUpdateWorkflow,
)


def _tenant(request) -> UUID:
    """Resolve the explicit tenant context or reject the request."""

    tenant = getattr(request, "tenant", None)
    if tenant is None or getattr(tenant, "pk", None) is None:
        raise ValueError("Explicit request.tenant is required.")
    return tenant.pk


def _organization(request):
    """Resolve explicit organization context and validate its tenant."""

    organization = getattr(request, "organization", None)
    if organization is None or getattr(organization, "pk", None) is None:
        raise ValueError("Explicit request.organization is required.")
    tenant = getattr(request, "tenant", None)
    if tenant is None or organization.tenant_id != tenant.pk:
        raise ValueError("Organization does not belong to the active tenant.")
    return organization


def _context(request, operation: str) -> WorkflowContext:
    """Build the standard Revenue Cycle workflow context."""

    return WorkflowContext.create(
        actor=request.user,
        organization_id=_organization(request).pk,
        tenant_id=_tenant(request),
        operation=operation,
    )


def _permission_denied(action: str) -> Response:
    """Build the same explicit denial response for each operation."""
    return Response(
        {
            "detail": (
                f"You do not have permission to {action} "
                "insurance verification records."
            )
        },
        status=status.HTTP_403_FORBIDDEN,
    )


class InsuranceVerificationListCreateAPIView(APIView):
    """List and create Insurance Verification records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return tenant-safe verification records."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            return _permission_denied("view")
        patient_id = request.query_params.get("patient_id")
        request_reference = request.query_params.get("request_reference")
        queryset = list_verifications(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            patient_id=patient_id,
            request_reference=request_reference,
        )
        return Response(InsuranceVerificationDetailSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_create(user=request.user, organization_id=organization.pk):
            return _permission_denied("create")
        serializer = InsuranceVerificationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data.pop("patient_id", None)
        payer_id = serializer.validated_data.pop("payer_id", "")
        member_id = serializer.validated_data.pop("member_id", "")
        request_reference = request.data.get("request_reference", "")
        idempotency_key = request.headers.get(
            "Idempotency-Key", request.data.get("idempotency_key", "")
        )
        workflow = InsuranceVerificationCreationWorkflow(
            request=InsuranceVerificationCreateRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                payer_id=payer_id,
                member_id=member_id,
                request_reference=request_reference,
                idempotency_key=idempotency_key,
                data=serializer.validated_data,
            )
        )
        result = workflow.execute(
            context=_context(request, "revenue_cycle.insurance_verification.create")
        )
        return Response(
            InsuranceVerificationDetailSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class InsuranceVerificationDetailAPIView(APIView):
    """Retrieve, update, and delete one Insurance Verification."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, verification_id):
        """Return one tenant-safe verification."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            return _permission_denied("view")
        verification = get_verification(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            verification_id=verification_id,
        )
        return Response(InsuranceVerificationDetailSerializer(verification).data)

    def patch(self, request, verification_id):
        """Update a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_update(user=request.user, organization_id=organization.pk):
            return _permission_denied("update")
        serializer = InsuranceVerificationWriteSerializer(
            data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        result = InsuranceVerificationUpdateWorkflow(
            request=InsuranceVerificationUpdateRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                data=serializer.validated_data,
            )
        ).execute(
            context=_context(request, "revenue_cycle.insurance_verification.update")
        )
        return Response(InsuranceVerificationDetailSerializer(result.data).data)

    def delete(self, request, verification_id):
        """Soft-delete a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_delete(user=request.user, organization_id=organization.pk):
            return _permission_denied("delete")
        result = InsuranceVerificationDeletionWorkflow(
            request=InsuranceVerificationDeleteRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                deleted_by_id=request.user.pk,
            )
        ).execute(
            context=_context(request, "revenue_cycle.insurance_verification.delete")
        )
        return Response(InsuranceVerificationDetailSerializer(result.data).data)


class InsuranceVerificationLifecycleAPIView(APIView):
    """Transition Insurance Verification lifecycle state."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Apply a strict lifecycle transition."""

        organization = _organization(request)
        if not can_transition(user=request.user, organization_id=organization.pk):
            return _permission_denied("change the lifecycle of")
        serializer = InsuranceVerificationLifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = InsuranceVerificationLifecycleWorkflow(
            request=InsuranceVerificationLifecycleRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                actor_id=request.user.pk,
                **serializer.validated_data,
            )
        ).execute(
            context=_context(request, "revenue_cycle.insurance_verification.lifecycle")
        )
        return Response(InsuranceVerificationDetailSerializer(result.data).data)


class InsuranceVerificationRestoreAPIView(APIView):
    """Restore a deleted Insurance Verification."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Restore through the workflow boundary."""

        organization = _organization(request)
        if not can_restore(user=request.user, organization_id=organization.pk):
            return _permission_denied("restore")
        try:
            result = InsuranceVerificationRestoreWorkflow(
                request=InsuranceVerificationRestoreRequest(
                    organization_id=organization.pk,
                    tenant_id=_tenant(request),
                    verification_id=verification_id,
                )
            ).execute(
                context=_context(
                    request, "revenue_cycle.insurance_verification.restore"
                )
            )
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Insurance verification record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(InsuranceVerificationDetailSerializer(result.data).data)


__all__ = (
    "InsuranceVerificationDetailAPIView",
    "InsuranceVerificationLifecycleAPIView",
    "InsuranceVerificationListCreateAPIView",
    "InsuranceVerificationRestoreAPIView",
)
