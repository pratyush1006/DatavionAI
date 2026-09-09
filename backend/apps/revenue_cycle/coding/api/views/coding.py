from __future__ import annotations

"""DRF views for Revenue Cycle Coding."""

from uuid import UUID

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext, workflow_registry
from apps.patient_management.patients.models import Patient

from ...constants import CodingStatus
from ...models import CodingRecord
from ...permissions import CodingPermissions
from ...policies import CodingPolicy
from ...selectors import (
    get_coding_record,
    list_coding_records,
)
from ...tenant import require_context
from ..serializers import (
    CodeAssignmentCreateSerializer,
    CodeAssignmentSerializer,
    CodingCreateSerializer,
    CodingRecordSerializer,
    CodingTransitionSerializer,
    CodingUpdateSerializer,
)


def _run_workflow(
    *,
    request: object,
    organization: object,
    payload: dict,
) -> object:
    """Execute the registered Coding workflow."""

    workflow_class = workflow_registry.get(
        "revenue_cycle.coding",
    )
    workflow = workflow_class(
        payload=payload,
    )

    return workflow.run(
        WorkflowContext(
            actor=request.user,
            organization=organization,
            payload=payload,
        ),
    )


def _get_record(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    record_id: UUID,
) -> CodingRecord:
    """Retrieve a tenant-scoped active Coding record or raise 404."""

    try:
        return get_coding_record(
            organization_id=organization_id,
            record_id=record_id,
            tenant_id=tenant_id,
        )
    except CodingRecord.DoesNotExist as exc:
        raise Http404 from exc


def _transition_permission(status_value: str) -> str:
    """Map a target lifecycle state to its RBAC permission."""

    mapping = {
        CodingStatus.ASSIGNED: CodingPermissions.ASSIGN,
        CodingStatus.IN_REVIEW: CodingPermissions.REVIEW,
        CodingStatus.CODED: CodingPermissions.CODE,
        CodingStatus.VALIDATED: CodingPermissions.VALIDATE,
        CodingStatus.RELEASED: CodingPermissions.RELEASE,
        CodingStatus.VOIDED: CodingPermissions.VOID,
        CodingStatus.REJECTED: CodingPermissions.UPDATE,
    }

    return mapping.get(
        status_value,
        CodingPermissions.UPDATE,
    )


class CodingListCreateAPIView(APIView):
    """List and create tenant-scoped Coding records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return active Coding records visible to the caller."""

        tenant, organization = require_context(request)

        if not CodingPolicy.can_list(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        records = list_coding_records(
            organization_id=organization.id,
            tenant_id=tenant.id,
        )

        return Response(
            CodingRecordSerializer(
                records,
                many=True,
            ).data,
        )

    def post(self, request):
        """Create a Coding record through the workflow boundary."""

        tenant, organization = require_context(request)

        if not CodingPolicy.can_create(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CodingCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        patient = Patient.objects.filter(
            id=serializer.validated_data["patient_id"],
            organization_id=organization.id,
        ).first()

        if patient is None:
            return Response(
                {"detail": "Patient not found in the organization."},
                status=status.HTTP_404_NOT_FOUND,
            )

        payload = dict(serializer.validated_data)
        payload["operation"] = "create"
        payload["tenant_id"] = str(tenant.id)
        payload["patient"] = patient

        result = _run_workflow(
            request=request,
            organization=organization,
            payload=payload,
        )

        if not result.success:
            return Response(
                {"detail": result.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CodingRecordSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class CodingDetailAPIView(APIView):
    """Retrieve, update, or soft-delete a Coding record."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, record_id: UUID):
        """Return one tenant-scoped Coding record."""

        tenant, organization = require_context(request)
        record = _get_record(
            organization_id=organization.id,
            tenant_id=tenant.id,
            record_id=record_id,
        )

        if not CodingPolicy.can_view(
            actor=request.user,
            organization=organization,
            record=record,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            CodingRecordSerializer(record).data,
        )

    def patch(self, request, record_id: UUID):
        """Update mutable Coding fields through the workflow."""

        tenant, organization = require_context(request)
        record = _get_record(
            organization_id=organization.id,
            tenant_id=tenant.id,
            record_id=record_id,
        )

        if not CodingPolicy.can_update(
            actor=request.user,
            organization=organization,
            record=record,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CodingUpdateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = _run_workflow(
            request=request,
            organization=organization,
            payload={
                "operation": "update",
                "tenant_id": str(tenant.id),
                "record_id": str(record_id),
                "changes": serializer.validated_data,
            },
        )

        if not result.success:
            return Response(
                {"detail": result.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CodingRecordSerializer(result.data).data,
        )

    def delete(self, request, record_id: UUID):
        """Soft-delete a Coding record through the workflow."""

        tenant, organization = require_context(request)
        record = _get_record(
            organization_id=organization.id,
            tenant_id=tenant.id,
            record_id=record_id,
        )

        if not CodingPolicy.can_delete(
            actor=request.user,
            organization=organization,
            record=record,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = _run_workflow(
            request=request,
            organization=organization,
            payload={
                "operation": "delete",
                "tenant_id": str(tenant.id),
                "record_id": str(record_id),
            },
        )

        if not result.success:
            return Response(
                {"detail": result.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class CodingTransitionAPIView(APIView):
    """Transition a Coding record through its controlled lifecycle."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, record_id: UUID):
        """Apply a validated lifecycle transition."""

        tenant, organization = require_context(request)
        record = _get_record(
            organization_id=organization.id,
            tenant_id=tenant.id,
            record_id=record_id,
        )

        serializer = CodingTransitionSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        target_status = serializer.validated_data["target_status"]
        permission = _transition_permission(target_status)

        if not CodingPolicy.can_transition(
            actor=request.user,
            organization=organization,
            record=record,
            permission=permission,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = _run_workflow(
            request=request,
            organization=organization,
            payload={
                "operation": "transition",
                "tenant_id": str(tenant.id),
                "record_id": str(record_id),
                "target_status": target_status,
                "note": serializer.validated_data.get(
                    "note",
                    "",
                ),
            },
        )

        if not result.success:
            return Response(
                {"detail": result.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CodingRecordSerializer(result.data).data,
        )


class CodeAssignmentAPIView(APIView):
    """Add and list code assignments for a Coding record."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, record_id: UUID):
        """Return active code assignments for a Coding record."""

        tenant, organization = require_context(request)
        record = _get_record(
            organization_id=organization.id,
            tenant_id=tenant.id,
            record_id=record_id,
        )

        if not CodingPolicy.can_view(
            actor=request.user,
            organization=organization,
            record=record,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            CodeAssignmentSerializer(
                record.code_assignments.filter(
                    is_deleted=False,
                ),
                many=True,
            ).data,
        )

    def post(self, request, record_id: UUID):
        """Add a code assignment through the workflow boundary."""

        tenant, organization = require_context(request)
        record = _get_record(
            organization_id=organization.id,
            tenant_id=tenant.id,
            record_id=record_id,
        )

        if not CodingPolicy.can_transition(
            actor=request.user,
            organization=organization,
            record=record,
            permission=CodingPermissions.CODE,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CodeAssignmentCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = _run_workflow(
            request=request,
            organization=organization,
            payload={
                "operation": "add_code",
                "tenant_id": str(tenant.id),
                "record_id": str(record_id),
                **serializer.validated_data,
            },
        )

        if not result.success:
            return Response(
                {"detail": result.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CodeAssignmentSerializer(result.data).data,
            status=status.HTTP_201_CREATED,
        )


class CodingRestoreAPIView(APIView):
    """Restore a soft-deleted Coding record."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, record_id: UUID):
        """Restore a Coding record through the workflow boundary."""

        tenant, organization = require_context(request)

        if not CodingPolicy.can_restore(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Forbidden."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = _run_workflow(
            request=request,
            organization=organization,
            payload={
                "operation": "restore",
                "tenant_id": str(tenant.id),
                "record_id": str(record_id),
            },
        )

        if not result.success:
            return Response(
                {"detail": result.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CodingRecordSerializer(result.data).data,
        )


__all__ = (
    "CodeAssignmentAPIView",
    "CodingDetailAPIView",
    "CodingListCreateAPIView",
    "CodingRestoreAPIView",
    "CodingTransitionAPIView",
)
