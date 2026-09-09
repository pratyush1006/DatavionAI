"""Prior Authorization API views."""

from __future__ import annotations

from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.revenue_cycle.prior_authorization.api.serializers import (
    PriorAuthorizationDetailSerializer,
    PriorAuthorizationLifecycleSerializer,
    PriorAuthorizationWriteSerializer,
)
from apps.revenue_cycle.prior_authorization.policies import (
    can_create,
    can_delete,
    can_restore,
    can_transition,
    can_update,
    can_view,
)
from apps.revenue_cycle.prior_authorization.rbac import (
    CanCreatePriorAuthorization,
    CanDeletePriorAuthorization,
    CanRestorePriorAuthorization,
    CanTransitionPriorAuthorization,
    CanUpdatePriorAuthorization,
    CanViewPriorAuthorization,
)
from apps.revenue_cycle.prior_authorization.selectors import (
    get_verification,
    list_verifications,
)
from apps.revenue_cycle.prior_authorization.workflows import (
    PriorAuthorizationCreateRequest,
    PriorAuthorizationCreationWorkflow,
    PriorAuthorizationDeleteRequest,
    PriorAuthorizationDeletionWorkflow,
    PriorAuthorizationLifecycleRequest,
    PriorAuthorizationLifecycleWorkflow,
    PriorAuthorizationRestoreRequest,
    PriorAuthorizationRestoreWorkflow,
    PriorAuthorizationUpdateRequest,
    PriorAuthorizationUpdateWorkflow,
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


class PriorAuthorizationListCreateAPIView(APIView):
    """List and create Prior Authorization records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return tenant-safe verification records."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            CanViewPriorAuthorization().has_permission(request, self)
        patient_id = request.query_params.get("patient_id")
        queryset = list_verifications(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            patient_id=patient_id,
        )
        return Response(PriorAuthorizationDetailSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_create(user=request.user, organization_id=organization.pk):
            CanCreatePriorAuthorization().has_permission(request, self)
        serializer = PriorAuthorizationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data.pop("patient_id", None)
        payer_id = serializer.validated_data.pop("payer_id", "")
        member_id = serializer.validated_data.pop("member_id", "")
        request_reference = request.data.get("request_reference", "")
        idempotency_key = request.headers.get(
            "Idempotency-Key", request.data.get("idempotency_key", "")
        )
        workflow = PriorAuthorizationCreationWorkflow(
            request=PriorAuthorizationCreateRequest(
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
            context=_context(request, "revenue_cycle.prior_authorization.create")
        )
        return Response(
            PriorAuthorizationDetailSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class PriorAuthorizationDetailAPIView(APIView):
    """Retrieve, update, and delete one Prior Authorization."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, verification_id):
        """Return one tenant-safe verification."""

        organization = _organization(request)
        if not can_view(user=request.user, organization_id=organization.pk):
            CanViewPriorAuthorization().has_permission(request, self)
        verification = get_verification(
            tenant_id=_tenant(request),
            organization_id=organization.pk,
            verification_id=verification_id,
        )
        return Response(PriorAuthorizationDetailSerializer(verification).data)

    def patch(self, request, verification_id):
        """Update a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_update(user=request.user, organization_id=organization.pk):
            CanUpdatePriorAuthorization().has_permission(request, self)
        serializer = PriorAuthorizationWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = PriorAuthorizationUpdateWorkflow(
            request=PriorAuthorizationUpdateRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                data=serializer.validated_data,
            )
        ).execute(context=_context(request, "revenue_cycle.prior_authorization.update"))
        return Response(PriorAuthorizationDetailSerializer(result.data).data)

    def delete(self, request, verification_id):
        """Soft-delete a verification through the workflow boundary."""

        organization = _organization(request)
        if not can_delete(user=request.user, organization_id=organization.pk):
            CanDeletePriorAuthorization().has_permission(request, self)
        result = PriorAuthorizationDeletionWorkflow(
            request=PriorAuthorizationDeleteRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                deleted_by_id=request.user.pk,
            )
        ).execute(context=_context(request, "revenue_cycle.prior_authorization.delete"))
        return Response(PriorAuthorizationDetailSerializer(result.data).data)


class PriorAuthorizationLifecycleAPIView(APIView):
    """Transition Prior Authorization lifecycle state."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Apply a strict lifecycle transition."""

        organization = _organization(request)
        if not can_transition(user=request.user, organization_id=organization.pk):
            CanTransitionPriorAuthorization().has_permission(request, self)
        serializer = PriorAuthorizationLifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PriorAuthorizationLifecycleWorkflow(
            request=PriorAuthorizationLifecycleRequest(
                organization_id=organization.pk,
                tenant_id=_tenant(request),
                verification_id=verification_id,
                actor_id=request.user.pk,
                **serializer.validated_data,
            )
        ).execute(
            context=_context(request, "revenue_cycle.prior_authorization.lifecycle")
        )
        return Response(PriorAuthorizationDetailSerializer(result.data).data)


class PriorAuthorizationRestoreAPIView(APIView):
    """Restore a deleted Prior Authorization."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, verification_id):
        """Restore through the workflow boundary."""

        organization = _organization(request)
        if not can_restore(user=request.user, organization_id=organization.pk):
            CanRestorePriorAuthorization().has_permission(request, self)
        try:
            result = PriorAuthorizationRestoreWorkflow(
                request=PriorAuthorizationRestoreRequest(
                    organization_id=organization.pk,
                    tenant_id=_tenant(request),
                    verification_id=verification_id,
                )
            ).execute(
                context=_context(request, "revenue_cycle.prior_authorization.restore")
            )
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Insurance verification record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(PriorAuthorizationDetailSerializer(result.data).data)


__all__ = (
    "PriorAuthorizationDetailAPIView",
    "PriorAuthorizationLifecycleAPIView",
    "PriorAuthorizationListCreateAPIView",
    "PriorAuthorizationRestoreAPIView",
)
