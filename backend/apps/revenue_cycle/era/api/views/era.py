"""REST API views for Revenue Cycle Electronic Remittance Advice."""

from __future__ import annotations

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext

from ...models import ERA
from ...policies import (
    can_delete,
    can_post,
    can_read,
    can_restore,
    can_reverse,
    can_validate,
    can_write,
)
from ...selectors import eras_for_organization, get_era
from ...tenant import resolve_context
from ...workflows import (
    CreateERAWorkflow,
    DeleteERAWorkflow,
    ERAWorkflowRequest,
    PostERAWorkflow,
    RestoreERAWorkflow,
    ReverseERAWorkflow,
    ValidateERAWorkflow,
)
from ..serializers import ERAInputSerializer, ERAOutputSerializer


class ERAListCreateAPIView(APIView):
    """List and create tenant-scoped ERAs."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return active ERAs for the request organization."""
        tenant, organization = resolve_context(request)
        if not can_read(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = eras_for_organization(
            organization_id=organization.id,
            tenant_id=tenant.id,
        )
        return Response(ERAOutputSerializer(queryset, many=True).data)

    def post(self, request):
        """Create an ERA through workflow orchestration."""
        tenant, organization = resolve_context(request)
        if not can_write(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ERAInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow_request = ERAWorkflowRequest(
            actor=request.user,
            organization_id=organization.id,
            tenant_id=tenant.id,
            data=dict(serializer.validated_data),
        )
        context = WorkflowContext.create(
            tenant_id=workflow_request.tenant_id,
            actor_id=request.user.id,
            workflow_name="revenue_cycle.era",
            metadata={"organization_id": workflow_request.organization_id},
        )
        result = CreateERAWorkflow(logger_=None, payload=workflow_request).execute(
            context
        )
        return Response(
            ERAOutputSerializer(result.data).data, status=status.HTTP_201_CREATED
        )


class ERADetailAPIView(APIView):
    """Retrieve or soft-delete a tenant-scoped ERA."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, era_id):
        """Return one active ERA."""
        tenant, organization = resolve_context(request)
        if not can_read(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            era = get_era(
                organization_id=organization.id,
                tenant_id=tenant.id,
                era_id=era_id,
            )
        except ERA.DoesNotExist as exc:
            raise Http404 from exc
        return Response(ERAOutputSerializer(era).data)

    def delete(self, request, era_id):
        """Soft-delete an ERA through workflow orchestration."""
        tenant, organization = resolve_context(request)
        if not can_delete(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        workflow_request = ERAWorkflowRequest(
            actor=request.user,
            organization_id=organization.id,
            tenant_id=tenant.id,
            era_id=era_id,
        )
        context = WorkflowContext.create(
            tenant_id=workflow_request.tenant_id,
            actor_id=request.user.id,
            workflow_name="revenue_cycle.era",
            metadata={"organization_id": workflow_request.organization_id},
        )
        result = DeleteERAWorkflow(logger_=None, payload=workflow_request).execute(
            context
        )
        return Response(ERAOutputSerializer(result.data).data)


class ERAValidateAPIView(APIView):
    """Validate a received ERA."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, era_id):
        """Validate an ERA through workflow orchestration."""
        tenant, organization = resolve_context(request)
        if not can_validate(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        workflow_request = ERAWorkflowRequest(
            actor=request.user,
            organization_id=organization.id,
            tenant_id=tenant.id,
            era_id=era_id,
        )
        context = WorkflowContext.create(
            tenant_id=workflow_request.tenant_id,
            actor_id=request.user.id,
            workflow_name="revenue_cycle.era",
            metadata={"organization_id": workflow_request.organization_id},
        )
        result = ValidateERAWorkflow(logger_=None, payload=workflow_request).execute(
            context
        )
        return Response(ERAOutputSerializer(result.data).data)


class ERAPostAPIView(APIView):
    """Post a validated ERA."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, era_id):
        """Post an ERA through workflow orchestration."""
        tenant, organization = resolve_context(request)
        if not can_post(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        workflow_request = ERAWorkflowRequest(
            actor=request.user,
            organization_id=organization.id,
            tenant_id=tenant.id,
            era_id=era_id,
        )
        context = WorkflowContext.create(
            tenant_id=workflow_request.tenant_id,
            actor_id=request.user.id,
            workflow_name="revenue_cycle.era",
            metadata={"organization_id": workflow_request.organization_id},
        )
        result = PostERAWorkflow(logger_=None, payload=workflow_request).execute(
            context
        )
        return Response(ERAOutputSerializer(result.data).data)


class ERAReverseAPIView(APIView):
    """Reverse a posted ERA."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, era_id):
        """Reverse an ERA through workflow orchestration."""
        tenant, organization = resolve_context(request)
        if not can_reverse(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        workflow_request = ERAWorkflowRequest(
            actor=request.user,
            organization_id=organization.id,
            tenant_id=tenant.id,
            era_id=era_id,
        )
        context = WorkflowContext.create(
            tenant_id=workflow_request.tenant_id,
            actor_id=request.user.id,
            workflow_name="revenue_cycle.era",
            metadata={"organization_id": workflow_request.organization_id},
        )
        result = ReverseERAWorkflow(logger_=None, payload=workflow_request).execute(
            context
        )
        return Response(ERAOutputSerializer(result.data).data)


class ERARestoreAPIView(APIView):
    """Restore a deleted ERA."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, era_id):
        """Restore an ERA through workflow orchestration."""
        tenant, organization = resolve_context(request)
        if not can_restore(user=request.user, organization_id=organization.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        workflow_request = ERAWorkflowRequest(
            actor=request.user,
            organization_id=organization.id,
            tenant_id=tenant.id,
            era_id=era_id,
        )
        context = WorkflowContext.create(
            tenant_id=workflow_request.tenant_id,
            actor_id=request.user.id,
            workflow_name="revenue_cycle.era",
            metadata={"organization_id": workflow_request.organization_id},
        )
        result = RestoreERAWorkflow(logger_=None, payload=workflow_request).execute(
            context
        )
        return Response(ERAOutputSerializer(result.data).data)


__all__ = (
    "ERADetailAPIView",
    "ERAListCreateAPIView",
    "ERAPostAPIView",
    "ERARestoreAPIView",
    "ERAReverseAPIView",
    "ERAValidateAPIView",
)
