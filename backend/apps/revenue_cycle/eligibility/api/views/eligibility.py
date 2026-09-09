"""API views for Revenue Cycle Eligibility."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.revenue_cycle.eligibility.api.serializers import (
    EligibilityCreateSerializer,
    EligibilityDetailSerializer,
    EligibilityLifecycleSerializer,
    EligibilityListSerializer,
    EligibilityUpdateSerializer,
)
from apps.revenue_cycle.eligibility.policies import EligibilityPolicy
from apps.revenue_cycle.eligibility.rbac import (
    CanCreateEligibility,
    CanDeleteEligibility,
    CanRestoreEligibility,
    CanTransitionEligibility,
    CanUpdateEligibility,
    CanViewEligibility,
)
from apps.revenue_cycle.eligibility.selectors import get_eligibility, list_eligibility
from apps.revenue_cycle.eligibility.workflows import (
    EligibilityCreationRequest,
    EligibilityCreationWorkflow,
    EligibilityDeleteRequest,
    EligibilityDeletionWorkflow,
    EligibilityLifecycleRequest,
    EligibilityLifecycleWorkflow,
    EligibilityRestoreRequest,
    EligibilityRestoreWorkflow,
    EligibilityUpdateRequest,
    EligibilityUpdateWorkflow,
)


def _organization(request):
    """Require explicit tenant and organization context."""
    organization = getattr(request, "organization", None)
    tenant = getattr(request, "tenant", None)
    if organization is None or tenant is None:
        raise PermissionError("Explicit tenant and organization context is required.")
    if organization.tenant_id != tenant.pk:
        raise PermissionError("Organization does not belong to the active tenant.")
    return organization


def _context(request, name):
    """Build a workflow context from explicit request tenant context."""
    if getattr(request, "tenant", None) is None:
        raise PermissionError("Explicit tenant context is required.")
    return WorkflowContext.create(
        tenant_id=request.tenant.pk, actor_id=request.user.pk, workflow_name=name
    )


class EligibilityListCreateAPIView(APIView):
    """List and create Eligibility records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """List scoped records."""
        organization = _organization(request)
        if not EligibilityPolicy.can_list(
            actor=request.user, organization=organization
        ):
            raise PermissionError("You cannot list eligibility records.")
        return Response(
            EligibilityListSerializer(
                list_eligibility(
                    tenant_id=request.tenant.pk,
                    organization_id=organization.pk,
                    patient_id=request.query_params.get("patient_id"),
                ),
                many=True,
            ).data
        )

    def post(self, request):
        """Create through the workflow boundary."""
        organization = _organization(request)
        CanCreateEligibility().has_permission(request, self)
        serializer = EligibilityCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data.pop("patient_id")
        result = EligibilityCreationWorkflow(
            request=EligibilityCreationRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                data=serializer.validated_data,
            )
        ).execute(context=_context(request, "revenue_cycle.eligibility.create"))
        return Response(EligibilityDetailSerializer(result.data).data, status=201)


class EligibilityDetailAPIView(APIView):
    """Retrieve, update, and delete one Eligibility record."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, eligibility_id):
        """Retrieve one record."""
        organization = _organization(request)
        obj = get_eligibility(
            tenant_id=request.tenant.pk,
            organization_id=organization.pk,
            eligibility_id=eligibility_id,
        )
        CanViewEligibility().has_permission(request, self)
        if not EligibilityPolicy.can_view(actor=request.user, eligibility=obj):
            raise PermissionError("You cannot view this eligibility record.")
        return Response(EligibilityDetailSerializer(obj).data)

    def patch(self, request, eligibility_id):
        """Update mutable metadata through the workflow."""
        organization = _organization(request)
        CanUpdateEligibility().has_permission(request, self)
        serializer = EligibilityUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = EligibilityUpdateWorkflow(
            request=EligibilityUpdateRequest(
                organization_id=organization.pk,
                eligibility_id=eligibility_id,
                data=serializer.validated_data,
            )
        ).execute(context=_context(request, "revenue_cycle.eligibility.update"))
        return Response(EligibilityDetailSerializer(result.data).data)

    def delete(self, request, eligibility_id):
        """Soft-delete through the workflow."""
        organization = _organization(request)
        CanDeleteEligibility().has_permission(request, self)
        result = EligibilityDeletionWorkflow(
            request=EligibilityDeleteRequest(
                organization_id=organization.pk, eligibility_id=eligibility_id
            )
        ).execute(context=_context(request, "revenue_cycle.eligibility.delete"))
        return Response(EligibilityDetailSerializer(result.data).data)


class EligibilityLifecycleAPIView(APIView):
    """Transition Eligibility lifecycle."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, eligibility_id):
        """Apply a strict lifecycle transition."""
        organization = _organization(request)
        CanTransitionEligibility().has_permission(request, self)
        serializer = EligibilityLifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = EligibilityLifecycleWorkflow(
            request=EligibilityLifecycleRequest(
                organization_id=organization.pk,
                eligibility_id=eligibility_id,
                status=serializer.validated_data["status"],
            )
        ).execute(context=_context(request, "revenue_cycle.eligibility.lifecycle"))
        return Response(EligibilityDetailSerializer(result.data).data)


class EligibilityRestoreAPIView(APIView):
    """Restore a deleted Eligibility record."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, eligibility_id):
        """Restore through the workflow boundary."""
        organization = _organization(request)
        CanRestoreEligibility().has_permission(request, self)
        result = EligibilityRestoreWorkflow(
            request=EligibilityRestoreRequest(
                organization_id=organization.pk, eligibility_id=eligibility_id
            )
        ).execute(context=_context(request, "revenue_cycle.eligibility.restore"))
        return Response(EligibilityDetailSerializer(result.data).data)


__all__ = (
    "EligibilityDetailAPIView",
    "EligibilityLifecycleAPIView",
    "EligibilityListCreateAPIView",
    "EligibilityRestoreAPIView",
)
