"""API views for tenant-scoped payment posting."""

from __future__ import annotations

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext

from ...policies import can_read, can_restore, can_reverse, can_write
from ...selectors import get_payment_posting, payment_postings_for_organization
from ...workflows import (
    PaymentPostingCreateWorkflow,
    PaymentPostingPostWorkflow,
    PaymentPostingRestoreWorkflow,
    PaymentPostingReverseWorkflow,
    PaymentPostingUpdateWorkflow,
)
from ..serializers import (
    PaymentPostingCreateSerializer,
    PaymentPostingSerializer,
    PaymentPostingUpdateSerializer,
)


def _context(request):
    """Resolve explicit tenant and organization request context."""

    try:
        tenant = request.tenant
        organization = request.organization
    except AttributeError as exc:
        raise Http404("Explicit tenant and organization context is required.") from exc
    if tenant is None or organization is None:
        raise Http404("Explicit tenant and organization context is required.")
    if organization.tenant_id != tenant.id:
        raise Http404("Organization does not belong to the request tenant.")
    return tenant, organization


def _patient_for_organization(*, patient_id, organization):
    """Resolve the canonical patient within organization scope."""

    from apps.patient_management.patients.models import Patient

    return Patient.objects.get(pk=patient_id, organization=organization)


class PaymentPostingListCreateAPIView(APIView):
    """List and create payment postings."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return active payment postings in explicit tenant scope."""

        tenant, organization = _context(request)
        if not can_read(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = payment_postings_for_organization(
            organization_id=organization.id,
            tenant_id=tenant.id,
        )
        return Response(PaymentPostingSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a payment posting through its workflow."""

        _, organization = _context(request)
        if not can_write(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PaymentPostingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        patient = _patient_for_organization(
            patient_id=data.pop("patient"),
            organization=organization,
        )
        workflow = PaymentPostingCreateWorkflow()
        result = workflow.execute(
            WorkflowContext.create(
                tenant_id=organization.tenant_id,
                actor_id=request.user.id,
                workflow_name="revenue_cycle.payment_posting",
                metadata={"organization_id": organization.id},
            )
        )
        return Response(
            PaymentPostingSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class PaymentPostingDetailAPIView(APIView):
    """Retrieve or update a payment posting."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, posting_id):
        """Return one payment posting."""

        tenant, organization = _context(request)
        if not can_read(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            posting = get_payment_posting(
                organization_id=organization.id,
                tenant_id=tenant.id,
                posting_id=posting_id,
            )
        except PaymentPosting.DoesNotExist as exc:
            raise Http404 from exc
        return Response(PaymentPostingSerializer(posting).data)

    def patch(self, request, posting_id):
        """Update a pending payment posting through its workflow."""

        tenant, organization = _context(request)
        if not can_write(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PaymentPostingUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PaymentPostingUpdateWorkflow().execute(
            WorkflowContext.create(
                tenant_id=organization.tenant_id,
                actor_id=request.user.id,
                workflow_name="revenue_cycle.payment_posting",
                metadata={"organization_id": organization.id},
            )
        )
        return Response(PaymentPostingSerializer(result.data).data)


class PaymentPostingPostAPIView(APIView):
    """Post a pending payment posting."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, posting_id):
        """Execute the posting workflow."""

        _, organization = _context(request)
        if not can_write(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        result = PaymentPostingPostWorkflow().execute(
            WorkflowContext.create(
                tenant_id=organization.tenant_id,
                actor_id=request.user.id,
                workflow_name="revenue_cycle.payment_posting",
                metadata={"organization_id": organization.id},
            )
        )
        return Response(PaymentPostingSerializer(result.data).data)


class PaymentPostingReverseAPIView(APIView):
    """Reverse a posted payment posting."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, posting_id):
        """Execute the reversal workflow."""

        _, organization = _context(request)
        if not can_reverse(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        reason = str(request.data.get("reason", ""))
        result = PaymentPostingReverseWorkflow().execute(
            WorkflowContext.create(
                tenant_id=organization.tenant_id,
                actor_id=request.user.id,
                workflow_name="revenue_cycle.payment_posting",
                metadata={"organization_id": organization.id},
            )
        )
        return Response(PaymentPostingSerializer(result.data).data)


class PaymentPostingRestoreAPIView(APIView):
    """Restore a soft-deleted payment posting."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, posting_id):
        """Execute the restore workflow."""

        _, organization = _context(request)
        if not can_restore(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        result = PaymentPostingRestoreWorkflow().execute(
            WorkflowContext.create(
                tenant_id=organization.tenant_id,
                actor_id=request.user.id,
                workflow_name="revenue_cycle.payment_posting",
                metadata={"organization_id": organization.id},
            )
        )
        return Response(PaymentPostingSerializer(result.data).data)


__all__ = (
    "PaymentPostingDetailAPIView",
    "PaymentPostingListCreateAPIView",
    "PaymentPostingPostAPIView",
    "PaymentPostingRestoreAPIView",
    "PaymentPostingReverseAPIView",
)
