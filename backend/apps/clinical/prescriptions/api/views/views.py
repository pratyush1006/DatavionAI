"""Thin workflow-only API adapter for Prescription."""

from __future__ import annotations

from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.prescriptions.models import Prescription
from apps.clinical.prescriptions.permissions.api import PrescriptionAPIPermission
from apps.core.workflows import WorkflowContext

from ...workflows.workflow import (
    PrescriptionCreateWorkflow,
    PrescriptionDeleteWorkflow,
    PrescriptionLifecycleWorkflow,
    PrescriptionUpdateWorkflow,
    PrescriptionWorkflowRequest,
)


def _org(request):
    organization = getattr(request, "organization", None) or getattr(
        request.user, "organization", None
    )
    if organization is None:
        raise PermissionError("Organization context is required.")
    if getattr(organization, "tenant_id", None) is None:
        raise PermissionError("Tenant context is required.")
    return organization


def _ctx(request, workflow_name):
    organization = _org(request)
    return WorkflowContext.create(
        tenant_id=organization.tenant_id,
        actor_id=request.user.pk,
        workflow_name=workflow_name,
        request_id=request.headers.get("X-Request-ID"),
    )


def _json(obj):
    out = {}
    for field in obj._meta.fields:
        value = getattr(obj, field.name)
        out[field.name] = str(value.pk) if hasattr(value, "pk") else value
    return out


class PrescriptionListCreateAPIView(APIView):
    def get_permissions(self):
        action = "view" if self.request.method in {"GET", "HEAD"} else "create"
        return [IsAuthenticated(), PrescriptionAPIPermission(action=action)]

    def get(self, request):
        qs = Prescription.objects.filter(organization_id=_org(request).pk)
        return Response([_json(value) for value in qs])

    def post(self, request):
        organization = _org(request)
        result = PrescriptionCreateWorkflow(
            request=PrescriptionWorkflowRequest(
                organization_id=organization.pk,
                data=dict(request.data),
            ),
        ).run(context=_ctx(request, "prescription.create"))
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(_json(result.data), status=201)


class PrescriptionDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, PrescriptionAPIPermission)

    def get(self, request, prescription_id: UUID):
        obj = Prescription.objects.get(
            pk=prescription_id,
            organization_id=_org(request).pk,
        )
        return Response(_json(obj))

    def patch(self, request, prescription_id: UUID):
        organization = _org(request)
        result = PrescriptionUpdateWorkflow(
            request=PrescriptionWorkflowRequest(
                organization_id=organization.pk,
                record_id=prescription_id,
                data=dict(request.data),
            ),
        ).run(context=_ctx(request, "prescription.update"))
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(_json(result.data))

    def delete(self, request, prescription_id: UUID):
        organization = _org(request)
        result = PrescriptionDeleteWorkflow(
            request=PrescriptionWorkflowRequest(
                organization_id=organization.pk,
                record_id=prescription_id,
            ),
        ).run(context=_ctx(request, "prescription.delete"))
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(status=204)

    def put(self, request, prescription_id):
        """Handle full update through the existing update workflow."""
        return self.patch(request, prescription_id)


class PrescriptionLifecycleAPIView(APIView):
    permission_classes = (IsAuthenticated, PrescriptionAPIPermission)

    def get_permissions(self):
        return [IsAuthenticated(), PrescriptionAPIPermission(action="transition")]

    def post(self, request, prescription_id: UUID):
        organization = _org(request)
        result = PrescriptionLifecycleWorkflow(
            request=PrescriptionWorkflowRequest(
                organization_id=organization.pk,
                record_id=prescription_id,
                data=dict(request.data),
            ),
        ).run(context=_ctx(request, "prescription.lifecycle"))
        if not result.success:
            return Response({"detail": result.message}, status=400)
        return Response(_json(result.data))
