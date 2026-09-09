from __future__ import annotations

"""DatavionAI Revenue Cycle RC9 ERA complete rebuild installer."""

import ast
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
MODULE_ROOT = BACKEND_ROOT / "apps" / "revenue_cycle" / "era"
BACKUP_ROOT = BACKEND_ROOT / ".rc9_era_complete_rebuild_backup"

FILES = {
    "api/serializers/era.py": '''"""Serializers for Revenue Cycle Electronic Remittance Advice."""

from __future__ import annotations

from rest_framework import serializers

from ...models import ERA


class ERAInputSerializer(serializers.Serializer):
    """Validate ERA creation input."""

    patient_id = serializers.UUIDField(required=False, allow_null=True)
    payer_name = serializers.CharField(max_length=200)
    payer_identifier = serializers.CharField(max_length=100, required=False, allow_blank=True)
    trace_number = serializers.CharField(max_length=100)
    check_or_eft_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    source = serializers.ChoiceField(
        choices=[value for value, _label in ERA._meta.get_field("source").choices],
        required=False,
    )
    payment_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=0,
        required=False,
    )
    adjustment_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=0,
        required=False,
    )
    received_at = serializers.DateTimeField()
    external_reference = serializers.CharField(max_length=150, required=False, allow_blank=True)
    idempotency_key = serializers.CharField(max_length=150)
    raw_payload = serializers.JSONField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)


class ERAOutputSerializer(serializers.ModelSerializer):
    """Serialize an ERA aggregate for API responses."""

    class Meta:
        """Configure serialized ERA fields."""

        model = ERA
        fields = (
            "id", "patient", "payer_name", "payer_identifier", "trace_number",
            "check_or_eft_number", "source", "status", "payment_amount",
            "adjustment_amount", "received_at", "validated_at", "posted_at",
            "reversed_at", "external_reference", "idempotency_key",
            "validation_errors", "notes", "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "status", "validated_at", "posted_at", "reversed_at",
            "validation_errors", "created_at", "updated_at",
        )


__all__ = ("ERAInputSerializer", "ERAOutputSerializer")
''',
    "api/serializers/__init__.py": '''"""Public serializer exports for Revenue Cycle ERA."""

from __future__ import annotations

from .era import ERAInputSerializer, ERAOutputSerializer

__all__ = ("ERAInputSerializer", "ERAOutputSerializer")
''',
    "api/views/era.py": '''"""REST API views for Revenue Cycle Electronic Remittance Advice."""

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
        context = WorkflowContext(actor=request.user, payload=workflow_request)
        result = CreateERAWorkflow(logger_=None, payload=workflow_request).run(context)
        return Response(ERAOutputSerializer(result.data).data, status=status.HTTP_201_CREATED)


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
        context = WorkflowContext(actor=request.user, payload=workflow_request)
        result = DeleteERAWorkflow(logger_=None, payload=workflow_request).run(context)
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
        context = WorkflowContext(actor=request.user, payload=workflow_request)
        result = ValidateERAWorkflow(logger_=None, payload=workflow_request).run(context)
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
        context = WorkflowContext(actor=request.user, payload=workflow_request)
        result = PostERAWorkflow(logger_=None, payload=workflow_request).run(context)
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
        context = WorkflowContext(actor=request.user, payload=workflow_request)
        result = ReverseERAWorkflow(logger_=None, payload=workflow_request).run(context)
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
        context = WorkflowContext(actor=request.user, payload=workflow_request)
        result = RestoreERAWorkflow(logger_=None, payload=workflow_request).run(context)
        return Response(ERAOutputSerializer(result.data).data)


__all__ = (
    "ERADetailAPIView", "ERAListCreateAPIView", "ERAPostAPIView",
    "ERARestoreAPIView", "ERAReverseAPIView", "ERAValidateAPIView",
)
''',
    "api/views/__init__.py": '''"""Public API view exports for Revenue Cycle ERA."""

from __future__ import annotations

from .era import (
    ERADetailAPIView,
    ERAListCreateAPIView,
    ERAPostAPIView,
    ERARestoreAPIView,
    ERAReverseAPIView,
    ERAValidateAPIView,
)

__all__ = (
    "ERADetailAPIView", "ERAListCreateAPIView", "ERAPostAPIView",
    "ERARestoreAPIView", "ERAReverseAPIView", "ERAValidateAPIView",
)
''',
    "workflows/era.py": '''"""Workflow orchestration for Revenue Cycle Electronic Remittance Advice."""

from __future__ import annotations

from dataclasses import dataclass, field

from django.db import transaction

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult

from ..events import ERAEvent
from ..models import ERA
from ..services import delete_era, post_era, restore_era, reverse_era, validate_era


@dataclass(frozen=True)
class ERAWorkflowRequest:
    """Carry tenant, organization, actor, and ERA workflow input."""

    actor: object
    organization_id: object
    tenant_id: object
    era_id: object | None = None
    data: dict = field(default_factory=dict)


def _event(era: ERA, action: str) -> None:
    """Publish an ERA domain event after transaction commit."""
    publish_after_commit(
        ERAEvent(
            era_id=era.id,
            organization_id=era.organization_id,
            action=action,
        )
    )


class CreateERAWorkflow(BaseWorkflow):
    """Create an ERA aggregate."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create the ERA inside an atomic transaction."""
        request = context.payload
        with transaction.atomic():
            era = ERA.objects.create(
                organization_id=request.organization_id,
                patient_id=request.data.get("patient_id"),
                payer_name=request.data["payer_name"],
                payer_identifier=request.data.get("payer_identifier", ""),
                trace_number=request.data["trace_number"],
                check_or_eft_number=request.data.get("check_or_eft_number", ""),
                source=request.data.get("source", "edi_835"),
                payment_amount=request.data.get("payment_amount", "0.00"),
                adjustment_amount=request.data.get("adjustment_amount", "0.00"),
                received_at=request.data["received_at"],
                external_reference=request.data.get("external_reference", ""),
                idempotency_key=request.data["idempotency_key"],
                raw_payload=request.data.get("raw_payload", {}),
                notes=request.data.get("notes", ""),
                processed_by=request.actor,
            )
            _event(era, "created")
        return WorkflowResult.ok(data=era)


class ValidateERAWorkflow(BaseWorkflow):
    """Validate an ERA aggregate."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Validate the ERA using a row lock."""
        request = context.payload
        with transaction.atomic():
            era = ERA.objects.select_for_update().get(pk=request.era_id)
            era = validate_era(era=era)
            _event(era, "validated")
        return WorkflowResult.ok(data=era)


class PostERAWorkflow(BaseWorkflow):
    """Post a validated ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Post the ERA through the domain service."""
        request = context.payload
        with transaction.atomic():
            era = post_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
                user=request.actor,
            )
            _event(era, "posted")
        return WorkflowResult.ok(data=era)


class ReverseERAWorkflow(BaseWorkflow):
    """Reverse a posted ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Reverse the ERA through the domain service."""
        request = context.payload
        with transaction.atomic():
            era = reverse_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
                user=request.actor,
            )
            _event(era, "reversed")
        return WorkflowResult.ok(data=era)


class DeleteERAWorkflow(BaseWorkflow):
    """Soft-delete an ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Soft-delete the ERA through the domain service."""
        request = context.payload
        with transaction.atomic():
            era = delete_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
                user_id=request.actor.id,
            )
            _event(era, "deleted")
        return WorkflowResult.ok(data=era)


class RestoreERAWorkflow(BaseWorkflow):
    """Restore a deleted ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Restore the ERA through the domain service."""
        request = context.payload
        with transaction.atomic():
            era = restore_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
            )
            _event(era, "restored")
        return WorkflowResult.ok(data=era)


__all__ = (
    "CreateERAWorkflow", "DeleteERAWorkflow", "ERAWorkflowRequest",
    "PostERAWorkflow", "RestoreERAWorkflow", "ReverseERAWorkflow",
    "ValidateERAWorkflow",
)
''',
    "workflows/__init__.py": '''"""Public workflow exports for Revenue Cycle ERA."""

from __future__ import annotations

from .era import (
    CreateERAWorkflow,
    DeleteERAWorkflow,
    ERAWorkflowRequest,
    PostERAWorkflow,
    RestoreERAWorkflow,
    ReverseERAWorkflow,
    ValidateERAWorkflow,
)

__all__ = (
    "CreateERAWorkflow", "DeleteERAWorkflow", "ERAWorkflowRequest",
    "PostERAWorkflow", "RestoreERAWorkflow", "ReverseERAWorkflow",
    "ValidateERAWorkflow",
)
''',
}


def create_backup() -> Path:
    """Create a timestamped backup of files that will be replaced."""
    backup_dir = BACKUP_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=False)
    for relative_path in FILES:
        source = MODULE_ROOT / relative_path
        if source.exists():
            destination = backup_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    return backup_dir


def write_files() -> None:
    """Write all rebuilt RC9 ERA source files."""
    for relative_path, content in FILES.items():
        destination = MODULE_ROOT / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content.lstrip(), encoding="utf-8")


def validate_collisions() -> None:
    """Ensure root modules do not collide with package directories."""
    pairs = (
        ("models.py", "models"),
        ("events.py", "events"),
        ("workflows.py", "workflows"),
        ("api/views.py", "api/views"),
        ("api/serializers.py", "api/serializers"),
    )
    collisions = [
        f"{module_file} <-> {package_dir}"
        for module_file, package_dir in pairs
        if (MODULE_ROOT / module_file).exists() and (MODULE_ROOT / package_dir).is_dir()
    ]
    if collisions:
        raise RuntimeError("PACKAGE COLLISIONS DETECTED: " + ", ".join(collisions))


def validate_import_boundaries() -> None:
    """Validate nested API imports use the correct package boundary."""
    serializer = (MODULE_ROOT / "api/serializers/era.py").read_text(encoding="utf-8")
    view = (MODULE_ROOT / "api/views/era.py").read_text(encoding="utf-8")
    if "from ..models import" in serializer:
        raise RuntimeError("Invalid serializer import boundary: from ..models")
    invalid = (
        "from ..models import",
        "from ..constants import",
        "from ..services import",
        "from ..selectors import",
        "from ..policies import",
        "from ..workflows import",
        "from ..permissions import",
    )
    for fragment in invalid:
        if fragment in view:
            raise RuntimeError(f"Invalid API view import boundary: {fragment}")


def validate_ast() -> None:
    """Parse every rebuilt Python file."""
    for relative_path in FILES:
        target = MODULE_ROOT / relative_path
        ast.parse(target.read_text(encoding="utf-8"), filename=str(target))


def compile_targets() -> None:
    """Compile every rebuilt Python file."""
    for relative_path in FILES:
        py_compile.compile(str(MODULE_ROOT / relative_path), doraise=True)


def main() -> None:
    """Execute the RC9 ERA complete rebuild."""
    print("=" * 78)
    print("DatavionAI Revenue Cycle RC9 ERA Complete Rebuild Installer v2.0.0")
    print("=" * 78)
    if not MODULE_ROOT.exists():
        raise RuntimeError(f"RC9 ERA module does not exist: {MODULE_ROOT}")
    backup_dir = create_backup()
    print(f"BACKUP CREATED: {backup_dir}")
    write_files()
    validate_collisions()
    print("PACKAGE COLLISIONS: NONE")
    validate_import_boundaries()
    print("IMPORT BOUNDARIES: PASS")
    validate_ast()
    print("AST VALIDATION: PASS")
    compile_targets()
    print("PY_COMPILE TARGETS: PASS")
    print(f"FILES WRITTEN: {len(FILES)}")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("LEGACY PATIENT MODULE NOT MODIFIED")
    print("RC9 ERA COMPLETE REBUILD: PASS")


if __name__ == "__main__":
    main()
