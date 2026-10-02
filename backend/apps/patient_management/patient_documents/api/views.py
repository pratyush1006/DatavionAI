"""Patient Documents API endpoints."""

from __future__ import annotations

from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.patient_documents.api.filters import (
    PatientDocumentFilter,
)
from apps.patient_management.patient_documents.api.serializers import (
    PatientDocumentAccessLogSerializer,
    PatientDocumentCreateSerializer,
    PatientDocumentDetailSerializer,
    PatientDocumentListSerializer,
    PatientDocumentUpdateSerializer,
    PatientDocumentVersionCreateSerializer,
    PatientDocumentVersionSerializer,
)
from apps.patient_management.patient_documents.permissions import (
    CanActivatePatientDocument,
    CanArchivePatientDocument,
    CanCreatePatientDocument,
    CanCreatePatientDocumentVersion,
    CanDeletePatientDocument,
    CanListPatientDocuments,
    CanRestorePatientDocument,
    CanUpdatePatientDocument,
    CanViewPatientDocument,
    CanViewPatientDocumentAccessAudit,
)
from apps.patient_management.patient_documents.policies import (
    PatientDocumentPolicy,
)
from apps.patient_management.patient_documents.selectors import (
    get_patient_document,
    list_document_access_logs,
    list_document_versions,
    patient_document_queryset,
)
from apps.patient_management.patient_documents.workflows import (
    PatientDocumentAccessRequest,
    PatientDocumentAccessWorkflow,
    PatientDocumentActivationWorkflow,
    PatientDocumentArchiveWorkflow,
    PatientDocumentCreationRequest,
    PatientDocumentCreationWorkflow,
    PatientDocumentDeletionRequest,
    PatientDocumentDeletionWorkflow,
    PatientDocumentLifecycleRequest,
    PatientDocumentRestoreWorkflow,
    PatientDocumentUpdateRequest,
    PatientDocumentUpdateWorkflow,
    PatientDocumentVersionCreationRequest,
    PatientDocumentVersionCreationWorkflow,
)


def _tenant_id(
    request,
):
    """Resolve the current tenant from authenticated organization context."""
    tenant = getattr(
        getattr(request, "tenant", None),
        "id",
        None,
    )
    if tenant is not None:
        return tenant

    role = request.user.organization_roles.select_related(
        "organization__tenant"
    ).first()
    if role is None:
        raise RuntimeError(
            "Tenant context is required.",
        )
    return role.organization.tenant_id


def _organization(
    request,
):
    """Resolve the current organization object."""
    organization = getattr(
        request,
        "organization",
        None,
    )
    if organization is not None:
        return organization

    role = request.user.organization_roles.select_related("organization").first()
    if role is None:
        raise RuntimeError(
            "Organization context is required.",
        )
    return role.organization


def _organization_id(
    request,
):
    """Resolve the current organization identifier."""
    return _organization(request).id


class PatientDocumentListCreateAPIView(
    APIView,
):
    """List and create organization-scoped patient documents."""

    def get_permissions(
        self,
    ):
        """Return the RBAC permission adapter for the current method."""
        permission_map = {
            "GET": CanListPatientDocuments,
            "POST": CanCreatePatientDocument,
        }
        permission_class = permission_map.get(
            self.request.method,
            IsAuthenticated,
        )
        return [
            permission_class(),
        ]

    def get(
        self,
        request,
    ):
        """Return filtered patient documents."""
        organization = _organization(request)
        if not PatientDocumentPolicy().can_list(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {
                    "detail": "You do not have permission to list patient documents.",
                    "code": "patient_document_list_forbidden",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = patient_document_queryset(
            tenant_id=_tenant_id(request),
            organization_id=organization.id,
        )
        filtered = PatientDocumentFilter(
            request.query_params,
            queryset=queryset,
        ).qs
        serializer = PatientDocumentListSerializer(
            filtered,
            many=True,
        )
        return Response(
            serializer.data,
        )

    def post(
        self,
        request,
    ):
        """Create a patient document through its workflow."""
        serializer = PatientDocumentCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        organization = _organization(request)
        if not PatientDocumentPolicy().can_create(
            actor=request.user,
            organization=organization,
        ):
            return Response(
                {
                    "detail": "You do not have permission to create patient documents.",
                    "code": "patient_document_create_forbidden",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.create",
        )
        result = PatientDocumentCreationWorkflow(
            request=PatientDocumentCreationRequest(
                organization_id=organization.id,
                patient_id=serializer.validated_data["patient_id"],
                data={
                    key: value
                    for key, value in serializer.validated_data.items()
                    if key
                    not in {
                        "organization_id",
                        "patient_id",
                    }
                },
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "data": asdict(result.data),
                "message": result.message,
                "code": result.code,
            },
            status=status.HTTP_201_CREATED,
        )


class PatientDocumentDetailAPIView(
    APIView,
):
    """Retrieve one tenant-scoped patient document."""

    permission_classes = (CanViewPatientDocument,)

    def get(
        self,
        request,
        document_id,
    ):
        """Return document details after object-level authorization."""
        document = get_patient_document(
            document_id=document_id,
            tenant_id=_tenant_id(request),
            organization_id=_organization_id(request),
        )
        if not PatientDocumentPolicy().can_view(
            actor=request.user,
            document=document,
        ):
            return Response(
                {
                    "detail": "You do not have permission to view patient documents.",
                    "code": "patient_document_view_forbidden",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.access",
        )
        access_result = PatientDocumentAccessWorkflow(
            request=PatientDocumentAccessRequest(
                document_id=document.id,
                action="view",
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get(
                    "HTTP_USER_AGENT",
                    "",
                ),
            ),
        ).execute(
            context=context,
        )
        if not access_result.success:
            return Response(
                {
                    "detail": access_result.message,
                    "code": access_result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PatientDocumentDetailSerializer(
            document,
        )
        return Response(
            serializer.data,
        )


class PatientDocumentUpdateAPIView(
    APIView,
):
    """Update one patient document through its workflow."""

    permission_classes = (CanUpdatePatientDocument,)

    def patch(
        self,
        request,
        document_id,
    ):
        """Update mutable document metadata."""
        serializer = PatientDocumentUpdateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.update",
        )
        result = PatientDocumentUpdateWorkflow(
            request=PatientDocumentUpdateRequest(
                document_id=document_id,
                data=serializer.validated_data,
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": result.message,
                "code": result.code,
            },
        )


class PatientDocumentDeleteAPIView(
    APIView,
):
    """Soft-delete one patient document."""

    permission_classes = (CanDeletePatientDocument,)

    def delete(
        self,
        request,
        document_id,
    ):
        """Delete through the dedicated workflow."""
        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.delete",
        )
        result = PatientDocumentDeletionWorkflow(
            request=PatientDocumentDeletionRequest(
                document_id=document_id,
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": result.message,
                "code": result.code,
            },
        )


class PatientDocumentActivationAPIView(
    APIView,
):
    """Activate a draft or archived patient document."""

    permission_classes = (CanActivatePatientDocument,)

    def post(
        self,
        request,
        document_id,
    ):
        """Activate through the lifecycle workflow."""
        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.activate",
        )
        result = PatientDocumentActivationWorkflow(
            request=PatientDocumentLifecycleRequest(
                document_id=document_id,
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": result.message,
                "code": result.code,
            },
        )


class PatientDocumentArchiveAPIView(
    APIView,
):
    """Archive a patient document."""

    permission_classes = (CanArchivePatientDocument,)

    def post(
        self,
        request,
        document_id,
    ):
        """Archive through the lifecycle workflow."""
        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.archive",
        )
        result = PatientDocumentArchiveWorkflow(
            request=PatientDocumentLifecycleRequest(
                document_id=document_id,
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": result.message,
                "code": result.code,
            },
        )


class PatientDocumentRestoreAPIView(
    APIView,
):
    """Restore a soft-deleted patient document."""

    permission_classes = (CanRestorePatientDocument,)

    def post(
        self,
        request,
        document_id,
    ):
        """Restore through the lifecycle workflow."""
        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.restore",
        )
        result = PatientDocumentRestoreWorkflow(
            request=PatientDocumentLifecycleRequest(
                document_id=document_id,
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": result.message,
                "code": result.code,
            },
        )


class PatientDocumentVersionListCreateAPIView(
    APIView,
):
    """List or create immutable patient-document versions."""

    def get_permissions(
        self,
    ):
        """Return the RBAC permission adapter for the current method."""
        permission_map = {
            "GET": CanViewPatientDocument,
            "POST": CanCreatePatientDocumentVersion,
        }
        permission_class = permission_map.get(
            self.request.method,
            IsAuthenticated,
        )
        return [
            permission_class(),
        ]

    def get(
        self,
        request,
        document_id,
    ):
        """Return version history inside the tenant boundary."""
        document = get_patient_document(
            document_id=document_id,
            tenant_id=_tenant_id(request),
            organization_id=_organization_id(request),
        )
        if not PatientDocumentPolicy().can_view(
            actor=request.user,
            document=document,
        ):
            return Response(
                {
                    "detail": "You do not have permission to view patient documents.",
                    "code": "patient_document_view_forbidden",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PatientDocumentVersionSerializer(
            list_document_versions(
                document_id=document.id,
                tenant_id=_tenant_id(request),
                organization_id=_organization_id(request),
            ),
            many=True,
        )
        return Response(
            serializer.data,
        )

    def post(
        self,
        request,
        document_id,
    ):
        """Create the next immutable version."""
        serializer = PatientDocumentVersionCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        document = get_patient_document(
            document_id=document_id,
            tenant_id=_tenant_id(request),
            organization_id=_organization_id(request),
        )
        if not PatientDocumentPolicy().can_create_version(
            actor=request.user,
            document=document,
        ):
            return Response(
                {
                    "detail": "You do not have permission to create document versions.",
                    "code": "patient_document_version_forbidden",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        context = WorkflowContext.create(
            tenant_id=_tenant_id(request),
            actor_id=request.user.pk,
            workflow_name="patient_document.version.create",
        )
        result = PatientDocumentVersionCreationWorkflow(
            request=PatientDocumentVersionCreationRequest(
                document_id=document.id,
                data=serializer.validated_data,
            ),
        ).execute(
            context=context,
        )
        if not result.success:
            return Response(
                {
                    "detail": result.message,
                    "code": result.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            PatientDocumentVersionSerializer(result.data.version).data,
            status=status.HTTP_201_CREATED,
        )


class PatientDocumentAccessAuditAPIView(
    APIView,
):
    """Return immutable patient-document access audit history."""

    permission_classes = (CanViewPatientDocumentAccessAudit,)

    def get(
        self,
        request,
        document_id,
    ):
        """Return access audit records inside the tenant boundary."""
        document = get_patient_document(
            document_id=document_id,
            tenant_id=_tenant_id(request),
            organization_id=_organization_id(request),
        )
        if not PatientDocumentPolicy().can_view_access_audit(
            actor=request.user,
            document=document,
        ):
            return Response(
                {
                    "detail": "You do not have permission to view document access audit records.",
                    "code": "patient_document_access_audit_forbidden",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PatientDocumentAccessLogSerializer(
            list_document_access_logs(
                document_id=document.id,
                tenant_id=_tenant_id(request),
                organization_id=_organization_id(request),
            ),
            many=True,
        )
        return Response(
            serializer.data,
        )


__all__ = (
    "PatientDocumentAccessAuditAPIView",
    "PatientDocumentActivationAPIView",
    "PatientDocumentArchiveAPIView",
    "PatientDocumentDeleteAPIView",
    "PatientDocumentDetailAPIView",
    "PatientDocumentListCreateAPIView",
    "PatientDocumentRestoreAPIView",
    "PatientDocumentUpdateAPIView",
    "PatientDocumentVersionListCreateAPIView",
)
