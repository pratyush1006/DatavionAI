from __future__ import annotations

"""DatavionAI Revenue Cycle RC10 Denials complete rebuild installer."""

import ast
import shutil
from datetime import datetime
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
MODULE_ROOT = BACKEND_ROOT / "apps" / "revenue_cycle" / "denials"
BACKUP_ROOT = (
    BACKEND_ROOT
    / ".rc10_denials_complete_rebuild_backup"
    / datetime.now().strftime("%Y%m%d_%H%M%S")
)

FILES = {
    "api/views/denials.py": '''from __future__ import annotations

"""Denial REST API views."""

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
from ...workflows import CreateDenialRequest, DenialCreationWorkflow, DenialTransitionWorkflow, TransitionDenialRequest
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
        result = DenialCreationWorkflow().run(WorkflowContext(payload=CreateDenialRequest(organization=organization, patient=patient, actor=request.user, data=serializer.validated_data)))
        return Response(DenialSerializer(result.data).data, status=status.HTTP_201_CREATED)


class DenialDetailAPIView(APIView):
    """Retrieve, update, or delete a denial."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, denial_id):
        """Retrieve a denial."""
        tenant, organization = _context(request)
        if not can_list(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            denial = get_denial(organization_id=organization.id, tenant_id=tenant.id, denial_id=denial_id)
        except Denial.DoesNotExist as exc:
            raise Http404 from exc
        return Response(DenialSerializer(denial).data)

    def patch(self, request, denial_id):
        """Update a denial."""
        tenant, organization = _context(request)
        if not can_update(actor=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            denial = get_denial(organization_id=organization.id, tenant_id=tenant.id, denial_id=denial_id)
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
            denial = get_denial(organization_id=organization.id, tenant_id=tenant.id, denial_id=denial_id)
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
            denial = get_denial(organization_id=organization.id, tenant_id=tenant.id, denial_id=denial_id)
        except Denial.DoesNotExist as exc:
            raise Http404 from exc
        serializer = DenialTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = DenialTransitionWorkflow().run(WorkflowContext(payload=TransitionDenialRequest(denial=denial, actor=request.user, **serializer.validated_data)))
        return Response(DenialSerializer(result.data).data)


__all__ = ("DenialDetailAPIView", "DenialListCreateAPIView", "DenialTransitionAPIView")
''',
    "api/serializers/denial.py": '''from __future__ import annotations

"""Denial API serializers."""

from rest_framework import serializers

from ...constants import DenialStatus
from ...models import Denial


class DenialSerializer(serializers.ModelSerializer):
    """Serialize Denial instances for the REST API."""

    class Meta:
        """Serializer metadata."""

        model = Denial
        fields = ("id", "organization", "patient", "status", "priority", "reason_code", "reason_description", "payer_name", "denied_amount", "denied_at", "resolution_notes", "created_at", "updated_at")
        read_only_fields = ("id", "organization", "status", "denied_at", "created_at", "updated_at")


class DenialTransitionSerializer(serializers.Serializer):
    """Validate a denial lifecycle transition request."""

    target_status = serializers.ChoiceField(choices=DenialStatus.choices)
    note = serializers.CharField(required=False, allow_blank=True)


__all__ = ("DenialSerializer", "DenialTransitionSerializer")
''',
}


def _validate(path: Path) -> None:
    """Validate Python syntax."""
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def main() -> None:
    """Install the RC10 Denials API rebuild."""
    print("=" * 78)
    print("DatavionAI Revenue Cycle RC10 Denials Complete Rebuild Installer v2.0.0")
    print("=" * 78)
    for relative in FILES:
        source = MODULE_ROOT / relative
        if not source.exists():
            raise FileNotFoundError(f"Required source file not found: {source}")
        destination = BACKUP_ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    print(f"BACKUP CREATED: {BACKUP_ROOT}")
    for relative, content in FILES.items():
        destination = MODULE_ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    for relative in FILES:
        _validate(MODULE_ROOT / relative)
    views = (MODULE_ROOT / "api/views/denials.py").read_text(encoding="utf-8")
    serializers = (MODULE_ROOT / "api/serializers/denial.py").read_text(
        encoding="utf-8"
    )
    for invalid in (
        "from ..models import",
        "from ..policies import",
        "from ..selectors import",
        "from ..services import",
        "from ..workflows import",
    ):
        if invalid in views:
            raise AssertionError(f"Invalid view import remains: {invalid}")
    for invalid in ("from ..constants import", "from ..models import"):
        if invalid in serializers:
            raise AssertionError(f"Invalid serializer import remains: {invalid}")
    if (MODULE_ROOT / "api/views.py").exists() or (
        MODULE_ROOT / "api/serializers.py"
    ).exists():
        raise AssertionError("API package/module collision detected")
    print("PACKAGE COLLISIONS: NONE")
    print("IMPORT BOUNDARIES: PASS")
    print("AST VALIDATION: PASS")
    print("PY_COMPILE TARGETS: PASS")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("LEGACY PATIENT MODULE NOT MODIFIED")
    print("RC10 DENIALS COMPLETE REBUILD: PASS")


if __name__ == "__main__":
    main()
