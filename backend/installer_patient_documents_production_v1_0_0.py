"""
DatavionOS Patient Documents production installer.

Creates a fresh Patient Documents bounded context under:
    apps/patient_management/patient_documents

Design:
    API -> RBAC -> Workflow -> Policy -> Service -> Model -> Domain Event

The installer intentionally generates no Django migrations.
"""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

MODULE_NAME = "Patient Documents"
VERSION = "1.0.4"
TARGET = Path(
    r"D:\Datavion-Payment\DatavionAI\backend\apps\patient_management\patient_documents"
)

FILES = {
    ".installer_manifest.json": "{\n"
    '  "module": "patient_documents",\n'
    '  "version": "1.0.4",\n'
    '  "canonical_path": "apps.patient_management.patient_documents",\n'
    '  "canonical_patient": "apps.patient_management.patients.models.Patient",\n'
    '  "migration_policy": "no_migrations"\n'
    "}\n",
    "__init__.py": '"""Patient Documents bounded context for DatavionOS."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__: tuple[str, ...] = ()\n",
    "admin.py": '"""Django admin configuration for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.contrib import admin\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    "    PatientDocumentAccessLog,\n"
    "    PatientDocumentVersion,\n"
    ")\n"
    "\n"
    "\n"
    "@admin.register(PatientDocument)\n"
    "class PatientDocumentAdmin(admin.ModelAdmin):\n"
    '    """Admin configuration for patient documents."""\n'
    "\n"
    "    list_display = (\n"
    '        "title",\n'
    '        "patient",\n'
    '        "organization",\n'
    '        "category",\n'
    '        "status",\n'
    '        "is_confidential",\n'
    '        "created_at",\n'
    "    )\n"
    "    list_filter = (\n"
    '        "category",\n'
    '        "status",\n'
    '        "is_confidential",\n'
    '        "is_deleted",\n'
    "    )\n"
    "    search_fields = (\n"
    '        "title",\n'
    '        "original_filename",\n'
    '        "checksum",\n'
    "    )\n"
    "    readonly_fields = (\n"
    '        "id",\n'
    '        "created_at",\n'
    '        "updated_at",\n'
    '        "uploaded_at",\n'
    '        "archived_at",\n'
    "    )\n"
    "\n"
    "\n"
    "@admin.register(PatientDocumentVersion)\n"
    "class PatientDocumentVersionAdmin(admin.ModelAdmin):\n"
    '    """Admin configuration for document versions."""\n'
    "\n"
    "    list_display = (\n"
    '        "patient_document",\n'
    '        "version_number",\n'
    '        "status",\n'
    '        "created_at",\n'
    "    )\n"
    "    list_filter = (\n"
    '        "status",\n'
    "    )\n"
    "    search_fields = (\n"
    '        "patient_document__title",\n'
    '        "checksum",\n'
    "    )\n"
    "    readonly_fields = (\n"
    '        "id",\n'
    '        "created_at",\n'
    '        "updated_at",\n'
    "    )\n"
    "\n"
    "\n"
    "@admin.register(PatientDocumentAccessLog)\n"
    "class PatientDocumentAccessLogAdmin(admin.ModelAdmin):\n"
    '    """Admin configuration for document access audit records."""\n'
    "\n"
    "    list_display = (\n"
    '        "patient_document",\n'
    '        "user",\n'
    '        "action",\n'
    '        "accessed_at",\n'
    "    )\n"
    "    list_filter = (\n"
    '        "action",\n'
    "    )\n"
    "    search_fields = (\n"
    '        "patient_document__title",\n'
    '        "user__email",\n'
    "    )\n"
    "    readonly_fields = (\n"
    '        "id",\n'
    '        "accessed_at",\n'
    '        "created_at",\n'
    '        "updated_at",\n'
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessLogAdmin",\n'
    '    "PatientDocumentAdmin",\n'
    '    "PatientDocumentVersionAdmin",\n'
    ")\n",
    "api/__init__.py": '"""Patient Documents API package."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__: tuple[str, ...] = ()\n",
    "api/filters.py": '"""Filters for Patient Documents API."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "import django_filters\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentFilter(\n"
    "    django_filters.FilterSet,\n"
    "):\n"
    '    """Filter patient documents by patient, category, and status."""\n'
    "\n"
    "    patient = django_filters.UUIDFilter(\n"
    '        field_name="patient_id",\n'
    "    )\n"
    "\n"
    "    category = django_filters.CharFilter(\n"
    '        field_name="category",\n'
    "    )\n"
    "\n"
    "    status = django_filters.CharFilter(\n"
    '        field_name="status",\n'
    "    )\n"
    "\n"
    "    confidential = django_filters.BooleanFilter(\n"
    '        field_name="is_confidential",\n'
    "    )\n"
    "\n"
    "    class Meta:\n"
    '        """FilterSet metadata."""\n'
    "\n"
    "        model = PatientDocument\n"
    "        fields = (\n"
    '            "patient",\n'
    '            "category",\n'
    '            "status",\n'
    '            "confidential",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentFilter",\n'
    ")\n",
    "api/serializers/__init__.py": '"""Patient Documents serializer exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .access_log import PatientDocumentAccessLogSerializer\n"
    "from .create import PatientDocumentCreateSerializer\n"
    "from .detail import PatientDocumentDetailSerializer\n"
    "from .list import PatientDocumentListSerializer\n"
    "from .update import PatientDocumentUpdateSerializer\n"
    "from .version import (\n"
    "    PatientDocumentVersionCreateSerializer,\n"
    "    PatientDocumentVersionSerializer,\n"
    ")\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessLogSerializer",\n'
    '    "PatientDocumentCreateSerializer",\n'
    '    "PatientDocumentDetailSerializer",\n'
    '    "PatientDocumentListSerializer",\n'
    '    "PatientDocumentUpdateSerializer",\n'
    '    "PatientDocumentVersionCreateSerializer",\n'
    '    "PatientDocumentVersionSerializer",\n'
    ")\n",
    "api/serializers/create.py": '"""Patient Document creation serializer."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from rest_framework import serializers\n"
    "\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    PatientDocumentCategory,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentCreateSerializer(\n"
    "    serializers.Serializer,\n"
    "):\n"
    '    """Validate Patient Document creation input."""\n'
    "\n"
    "    patient_id = serializers.UUIDField()\n"
    "    title = serializers.CharField(\n"
    "        max_length=255,\n"
    "    )\n"
    "    storage_key = serializers.CharField(\n"
    "        max_length=500,\n"
    "    )\n"
    "    category = serializers.ChoiceField(\n"
    "        choices=PatientDocumentCategory.choices,\n"
    "    )\n"
    "    description = serializers.CharField(\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    original_filename = serializers.CharField(\n"
    "        max_length=255,\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    mime_type = serializers.CharField(\n"
    "        max_length=150,\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    file_size = serializers.IntegerField(\n"
    "        min_value=0,\n"
    "        required=False,\n"
    "        default=0,\n"
    "    )\n"
    "    checksum = serializers.CharField(\n"
    "        max_length=255,\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    is_confidential = serializers.BooleanField(\n"
    "        required=False,\n"
    "        default=False,\n"
    "    )\n"
    "    metadata = serializers.JSONField(\n"
    "        required=False,\n"
    "        default=dict,\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentCreateSerializer",\n'
    ")\n",
    "api/serializers/detail.py": '"""Patient Document detail serializer."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from rest_framework import serializers\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentDetailSerializer(\n"
    "    serializers.ModelSerializer,\n"
    "):\n"
    '    """Serialize Patient Document detail without exposing storage internals."""\n'
    "\n"
    "    class Meta:\n"
    '        """Serializer metadata."""\n'
    "\n"
    "        model = PatientDocument\n"
    "        fields = (\n"
    '            "id",\n'
    '            "organization",\n'
    '            "patient",\n'
    '            "title",\n'
    '            "category",\n'
    '            "status",\n'
    '            "description",\n'
    '            "original_filename",\n'
    '            "mime_type",\n'
    '            "file_size",\n'
    '            "checksum",\n'
    '            "is_confidential",\n'
    '            "metadata",\n'
    '            "uploaded_at",\n'
    '            "archived_at",\n'
    '            "created_by",\n'
    '            "created_at",\n'
    '            "updated_at",\n'
    "        )\n"
    "        read_only_fields = fields\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentDetailSerializer",\n'
    ")\n",
    "api/serializers/list.py": '"""Patient Document list serializer."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from rest_framework import serializers\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentListSerializer(\n"
    "    serializers.ModelSerializer,\n"
    "):\n"
    '    """Serialize safe list metadata for patient documents."""\n'
    "\n"
    "    class Meta:\n"
    '        """Serializer metadata."""\n'
    "\n"
    "        model = PatientDocument\n"
    "        fields = (\n"
    '            "id",\n'
    '            "patient",\n'
    '            "title",\n'
    '            "category",\n'
    '            "status",\n'
    '            "original_filename",\n'
    '            "mime_type",\n'
    '            "file_size",\n'
    '            "checksum",\n'
    '            "is_confidential",\n'
    '            "uploaded_at",\n'
    '            "archived_at",\n'
    '            "created_at",\n'
    '            "updated_at",\n'
    "        )\n"
    "        read_only_fields = fields\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentListSerializer",\n'
    ")\n",
    "api/serializers/update.py": '"""Patient Document update serializer."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from rest_framework import serializers\n"
    "\n"
    "\n"
    "class PatientDocumentUpdateSerializer(\n"
    "    serializers.Serializer,\n"
    "):\n"
    '    """Validate mutable Patient Document fields."""\n'
    "\n"
    "    title = serializers.CharField(\n"
    "        max_length=255,\n"
    "        required=False,\n"
    "    )\n"
    "    category = serializers.CharField(\n"
    "        max_length=40,\n"
    "        required=False,\n"
    "    )\n"
    "    description = serializers.CharField(\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    is_confidential = serializers.BooleanField(\n"
    "        required=False,\n"
    "    )\n"
    "    metadata = serializers.JSONField(\n"
    "        required=False,\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentUpdateSerializer",\n'
    ")\n",
    "api/urls.py": '"""URL routes for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.urls import path\n"
    "\n"
    "from apps.patient_management.patient_documents.api.views import (\n"
    "    PatientDocumentAccessAuditAPIView,\n"
    "    PatientDocumentActivationAPIView,\n"
    "    PatientDocumentArchiveAPIView,\n"
    "    PatientDocumentDeleteAPIView,\n"
    "    PatientDocumentDetailAPIView,\n"
    "    PatientDocumentListCreateAPIView,\n"
    "    PatientDocumentRestoreAPIView,\n"
    "    PatientDocumentUpdateAPIView,\n"
    "    PatientDocumentVersionListCreateAPIView,\n"
    ")\n"
    "\n"
    "\n"
    'app_name = "patient_documents"\n'
    "\n"
    "urlpatterns = [\n"
    "    path(\n"
    '        "<uuid:document_id>/versions/",\n'
    "        PatientDocumentVersionListCreateAPIView.as_view(),\n"
    '        name="versions",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/access-audit/",\n'
    "        PatientDocumentAccessAuditAPIView.as_view(),\n"
    '        name="access-audit",\n'
    "    ),\n"
    "    path(\n"
    '        "",\n'
    "        PatientDocumentListCreateAPIView.as_view(),\n"
    '        name="list-create",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/",\n'
    "        PatientDocumentDetailAPIView.as_view(),\n"
    '        name="detail",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/update/",\n'
    "        PatientDocumentUpdateAPIView.as_view(),\n"
    '        name="update",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/delete/",\n'
    "        PatientDocumentDeleteAPIView.as_view(),\n"
    '        name="delete",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/activate/",\n'
    "        PatientDocumentActivationAPIView.as_view(),\n"
    '        name="activate",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/archive/",\n'
    "        PatientDocumentArchiveAPIView.as_view(),\n"
    '        name="archive",\n'
    "    ),\n"
    "    path(\n"
    '        "<uuid:document_id>/restore/",\n'
    "        PatientDocumentRestoreAPIView.as_view(),\n"
    '        name="restore",\n'
    "    ),\n"
    "]\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "app_name",\n'
    '    "urlpatterns",\n'
    ")\n",
    "api/views.py": '"""Patient Documents API endpoints."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from dataclasses import asdict\n"
    "\n"
    "from rest_framework import status\n"
    "from rest_framework.permissions import IsAuthenticated\n"
    "from rest_framework.response import Response\n"
    "from rest_framework.views import APIView\n"
    "\n"
    "from apps.core.workflows import WorkflowContext\n"
    "from apps.patient_management.patient_documents.api.filters import (\n"
    "    PatientDocumentFilter,\n"
    ")\n"
    "from apps.patient_management.patient_documents.api.serializers import (\n"
    "    PatientDocumentAccessLogSerializer,\n"
    "    PatientDocumentCreateSerializer,\n"
    "    PatientDocumentDetailSerializer,\n"
    "    PatientDocumentListSerializer,\n"
    "    PatientDocumentUpdateSerializer,\n"
    "    PatientDocumentVersionCreateSerializer,\n"
    "    PatientDocumentVersionSerializer,\n"
    ")\n"
    "from apps.patient_management.patient_documents.permissions import (\n"
    "    CanActivatePatientDocument,\n"
    "    CanArchivePatientDocument,\n"
    "    CanCreatePatientDocument,\n"
    "    CanCreatePatientDocumentVersion,\n"
    "    CanDeletePatientDocument,\n"
    "    CanListPatientDocuments,\n"
    "    CanRestorePatientDocument,\n"
    "    CanUpdatePatientDocument,\n"
    "    CanViewPatientDocument,\n"
    "    CanViewPatientDocumentAccessAudit,\n"
    ")\n"
    "from apps.patient_management.patient_documents.policies import (\n"
    "    PatientDocumentPolicy,\n"
    ")\n"
    "from apps.patient_management.patient_documents.selectors import (\n"
    "    get_patient_document,\n"
    "    list_document_access_logs,\n"
    "    list_document_versions,\n"
    "    patient_document_queryset,\n"
    ")\n"
    "from apps.patient_management.patient_documents.workflows import (\n"
    "    PatientDocumentAccessRequest,\n"
    "    PatientDocumentAccessWorkflow,\n"
    "    PatientDocumentActivationWorkflow,\n"
    "    PatientDocumentArchiveWorkflow,\n"
    "    PatientDocumentCreationRequest,\n"
    "    PatientDocumentCreationWorkflow,\n"
    "    PatientDocumentDeletionRequest,\n"
    "    PatientDocumentDeletionWorkflow,\n"
    "    PatientDocumentLifecycleRequest,\n"
    "    PatientDocumentRestoreWorkflow,\n"
    "    PatientDocumentUpdateRequest,\n"
    "    PatientDocumentUpdateWorkflow,\n"
    "    PatientDocumentVersionCreationRequest,\n"
    "    PatientDocumentVersionCreationWorkflow,\n"
    ")\n"
    "\n"
    "\n"
    "def _tenant_id(\n"
    "    request,\n"
    "):\n"
    '    """Resolve the current tenant from authenticated organization context."""\n'
    "    tenant = getattr(\n"
    '        getattr(request, "tenant", None),\n'
    '        "id",\n'
    "        None,\n"
    "    )\n"
    "    if tenant is not None:\n"
    "        return tenant\n"
    "\n"
    "    role = (\n"
    "        request.user.organization_roles\n"
    '        .select_related("organization__tenant")\n'
    "        .first()\n"
    "    )\n"
    "    if role is None:\n"
    "        raise RuntimeError(\n"
    '            "Tenant context is required.",\n'
    "        )\n"
    "    return role.organization.tenant_id\n"
    "\n"
    "\n"
    "def _organization(\n"
    "    request,\n"
    "):\n"
    '    """Resolve the current organization object."""\n'
    "    organization = getattr(\n"
    "        request,\n"
    '        "organization",\n'
    "        None,\n"
    "    )\n"
    "    if organization is not None:\n"
    "        return organization\n"
    "\n"
    "    role = (\n"
    "        request.user.organization_roles\n"
    '        .select_related("organization")\n'
    "        .first()\n"
    "    )\n"
    "    if role is None:\n"
    "        raise RuntimeError(\n"
    '            "Organization context is required.",\n'
    "        )\n"
    "    return role.organization\n"
    "\n"
    "\n"
    "def _organization_id(\n"
    "    request,\n"
    "):\n"
    '    """Resolve the current organization identifier."""\n'
    "    return _organization(request).id\n"
    "\n"
    "\n"
    "class PatientDocumentListCreateAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """List and create organization-scoped patient documents."""\n'
    "\n"
    "    def get_permissions(\n"
    "        self,\n"
    "    ):\n"
    '        """Return the RBAC permission adapter for the current method."""\n'
    "        permission_map = {\n"
    '            "GET": CanListPatientDocuments,\n'
    '            "POST": CanCreatePatientDocument,\n'
    "        }\n"
    "        permission_class = permission_map.get(\n"
    "            self.request.method,\n"
    "            IsAuthenticated,\n"
    "        )\n"
    "        return [\n"
    "            permission_class(),\n"
    "        ]\n"
    "\n"
    "    def get(\n"
    "        self,\n"
    "        request,\n"
    "    ):\n"
    '        """Return filtered patient documents."""\n'
    "        organization = _organization(request)\n"
    "        if not PatientDocumentPolicy().can_list(\n"
    "            actor=request.user,\n"
    "            organization=organization,\n"
    "        ):\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": "You do not have permission to list patient documents.",\n'
    '                    "code": "patient_document_list_forbidden",\n'
    "                },\n"
    "                status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "\n"
    "        queryset = patient_document_queryset(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            organization_id=organization.id,\n"
    "        )\n"
    "        filtered = PatientDocumentFilter(\n"
    "            request.query_params,\n"
    "            queryset=queryset,\n"
    "        ).qs\n"
    "        serializer = PatientDocumentListSerializer(\n"
    "            filtered,\n"
    "            many=True,\n"
    "        )\n"
    "        return Response(\n"
    "            serializer.data,\n"
    "        )\n"
    "\n"
    "    def post(\n"
    "        self,\n"
    "        request,\n"
    "    ):\n"
    '        """Create a patient document through its workflow."""\n'
    "        serializer = PatientDocumentCreateSerializer(\n"
    "            data=request.data,\n"
    "        )\n"
    "        serializer.is_valid(\n"
    "            raise_exception=True,\n"
    "        )\n"
    "\n"
    "        organization = _organization(request)\n"
    "        if not PatientDocumentPolicy().can_create(\n"
    "            actor=request.user,\n"
    "            organization=organization,\n"
    "        ):\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": "You do not have permission to create patient documents.",\n'
    '                    "code": "patient_document_create_forbidden",\n'
    "                },\n"
    "                status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "\n"
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.create",\n'
    "        )\n"
    "        result = PatientDocumentCreationWorkflow(\n"
    "            request=PatientDocumentCreationRequest(\n"
    "                organization_id=organization.id,\n"
    "                patient_id=serializer.validated_data[\n"
    '                    "patient_id"\n'
    "                ],\n"
    "                data={\n"
    "                    key: value\n"
    "                    for key, value in serializer.validated_data.items()\n"
    "                    if key not in {\n"
    '                        "organization_id",\n'
    '                        "patient_id",\n'
    "                    }\n"
    "                },\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        return Response(\n"
    "            {\n"
    '                "data": asdict(result.data),\n'
    '                "message": result.message,\n'
    '                "code": result.code,\n'
    "            },\n"
    "            status=status.HTTP_201_CREATED,\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentDetailAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Retrieve one tenant-scoped patient document."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanViewPatientDocument,\n"
    "    )\n"
    "\n"
    "    def get(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Return document details after object-level authorization."""\n'
    "        document = get_patient_document(\n"
    "            document_id=document_id,\n"
    "            tenant_id=_tenant_id(request),\n"
    "            organization_id=_organization_id(request),\n"
    "        )\n"
    "        if not PatientDocumentPolicy().can_view(\n"
    "            actor=request.user,\n"
    "            document=document,\n"
    "        ):\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": "You do not have permission to view patient documents.",\n'
    '                    "code": "patient_document_view_forbidden",\n'
    "                },\n"
    "                status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "\n"
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.access",\n'
    "        )\n"
    "        access_result = PatientDocumentAccessWorkflow(\n"
    "            request=PatientDocumentAccessRequest(\n"
    "                document_id=document.id,\n"
    '                action="view",\n'
    '                ip_address=request.META.get("REMOTE_ADDR"),\n'
    "                user_agent=request.META.get(\n"
    '                    "HTTP_USER_AGENT",\n'
    '                    "",\n'
    "                ),\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not access_result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": access_result.message,\n'
    '                    "code": access_result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        serializer = PatientDocumentDetailSerializer(\n"
    "            document,\n"
    "        )\n"
    "        return Response(\n"
    "            serializer.data,\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentUpdateAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Update one patient document through its workflow."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanUpdatePatientDocument,\n"
    "    )\n"
    "\n"
    "    def patch(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Update mutable document metadata."""\n'
    "        serializer = PatientDocumentUpdateSerializer(\n"
    "            data=request.data,\n"
    "        )\n"
    "        serializer.is_valid(\n"
    "            raise_exception=True,\n"
    "        )\n"
    "\n"
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.update",\n'
    "        )\n"
    "        result = PatientDocumentUpdateWorkflow(\n"
    "            request=PatientDocumentUpdateRequest(\n"
    "                document_id=document_id,\n"
    "                data=serializer.validated_data,\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        return Response(\n"
    "            {\n"
    '                "message": result.message,\n'
    '                "code": result.code,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentDeleteAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Soft-delete one patient document."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanDeletePatientDocument,\n"
    "    )\n"
    "\n"
    "    def delete(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Delete through the dedicated workflow."""\n'
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.delete",\n'
    "        )\n"
    "        result = PatientDocumentDeletionWorkflow(\n"
    "            request=PatientDocumentDeletionRequest(\n"
    "                document_id=document_id,\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        return Response(\n"
    "            {\n"
    '                "message": result.message,\n'
    '                "code": result.code,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentActivationAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Activate a draft or archived patient document."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanActivatePatientDocument,\n"
    "    )\n"
    "\n"
    "    def post(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Activate through the lifecycle workflow."""\n'
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.activate",\n'
    "        )\n"
    "        result = PatientDocumentActivationWorkflow(\n"
    "            request=PatientDocumentLifecycleRequest(\n"
    "                document_id=document_id,\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        return Response(\n"
    "            {\n"
    '                "message": result.message,\n'
    '                "code": result.code,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentArchiveAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Archive a patient document."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanArchivePatientDocument,\n"
    "    )\n"
    "\n"
    "    def post(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Archive through the lifecycle workflow."""\n'
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.archive",\n'
    "        )\n"
    "        result = PatientDocumentArchiveWorkflow(\n"
    "            request=PatientDocumentLifecycleRequest(\n"
    "                document_id=document_id,\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        return Response(\n"
    "            {\n"
    '                "message": result.message,\n'
    '                "code": result.code,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentRestoreAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Restore a soft-deleted patient document."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanRestorePatientDocument,\n"
    "    )\n"
    "\n"
    "    def post(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Restore through the lifecycle workflow."""\n'
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.restore",\n'
    "        )\n"
    "        result = PatientDocumentRestoreWorkflow(\n"
    "            request=PatientDocumentLifecycleRequest(\n"
    "                document_id=document_id,\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "        return Response(\n"
    "            {\n"
    '                "message": result.message,\n'
    '                "code": result.code,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentVersionListCreateAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """List or create immutable patient-document versions."""\n'
    "\n"
    "    def get_permissions(\n"
    "        self,\n"
    "    ):\n"
    '        """Return the RBAC permission adapter for the current method."""\n'
    "        permission_map = {\n"
    '            "GET": CanViewPatientDocument,\n'
    '            "POST": CanCreatePatientDocumentVersion,\n'
    "        }\n"
    "        permission_class = permission_map.get(\n"
    "            self.request.method,\n"
    "            IsAuthenticated,\n"
    "        )\n"
    "        return [\n"
    "            permission_class(),\n"
    "        ]\n"
    "\n"
    "    def get(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Return version history inside the tenant boundary."""\n'
    "        document = get_patient_document(\n"
    "            document_id=document_id,\n"
    "            tenant_id=_tenant_id(request),\n"
    "            organization_id=_organization_id(request),\n"
    "        )\n"
    "        if not PatientDocumentPolicy().can_view(\n"
    "            actor=request.user,\n"
    "            document=document,\n"
    "        ):\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": "You do not have permission to view patient documents.",\n'
    '                    "code": "patient_document_view_forbidden",\n'
    "                },\n"
    "                status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "\n"
    "        serializer = PatientDocumentVersionSerializer(\n"
    "            list_document_versions(\n"
    "                document_id=document.id,\n"
    "                tenant_id=_tenant_id(request),\n"
    "                organization_id=_organization_id(request),\n"
    "            ),\n"
    "            many=True,\n"
    "        )\n"
    "        return Response(\n"
    "            serializer.data,\n"
    "        )\n"
    "\n"
    "    def post(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Create the next immutable version."""\n'
    "        serializer = PatientDocumentVersionCreateSerializer(\n"
    "            data=request.data,\n"
    "        )\n"
    "        serializer.is_valid(\n"
    "            raise_exception=True,\n"
    "        )\n"
    "\n"
    "        document = get_patient_document(\n"
    "            document_id=document_id,\n"
    "            tenant_id=_tenant_id(request),\n"
    "            organization_id=_organization_id(request),\n"
    "        )\n"
    "        if not PatientDocumentPolicy().can_create_version(\n"
    "            actor=request.user,\n"
    "            document=document,\n"
    "        ):\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": "You do not have permission to create document versions.",\n'
    '                    "code": "patient_document_version_forbidden",\n'
    "                },\n"
    "                status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "\n"
    "        context = WorkflowContext.create(\n"
    "            tenant_id=_tenant_id(request),\n"
    "            actor_id=request.user.pk,\n"
    '            workflow_name="patient_document.version.create",\n'
    "        )\n"
    "        result = PatientDocumentVersionCreationWorkflow(\n"
    "            request=PatientDocumentVersionCreationRequest(\n"
    "                document_id=document.id,\n"
    "                data=serializer.validated_data,\n"
    "            ),\n"
    "        ).execute(\n"
    "            context=context,\n"
    "        )\n"
    "        if not result.success:\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": result.message,\n'
    '                    "code": result.code,\n'
    "                },\n"
    "                status=status.HTTP_400_BAD_REQUEST,\n"
    "            )\n"
    "\n"
    "        return Response(\n"
    "            PatientDocumentVersionSerializer(result.data.version).data,\n"
    "            status=status.HTTP_201_CREATED,\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentAccessAuditAPIView(\n"
    "    APIView,\n"
    "):\n"
    '    """Return immutable patient-document access audit history."""\n'
    "\n"
    "    permission_classes = (\n"
    "        CanViewPatientDocumentAccessAudit,\n"
    "    )\n"
    "\n"
    "    def get(\n"
    "        self,\n"
    "        request,\n"
    "        document_id,\n"
    "    ):\n"
    '        """Return access audit records inside the tenant boundary."""\n'
    "        document = get_patient_document(\n"
    "            document_id=document_id,\n"
    "            tenant_id=_tenant_id(request),\n"
    "            organization_id=_organization_id(request),\n"
    "        )\n"
    "        if not PatientDocumentPolicy().can_view_access_audit(\n"
    "            actor=request.user,\n"
    "            document=document,\n"
    "        ):\n"
    "            return Response(\n"
    "                {\n"
    '                    "detail": "You do not have permission to view document access audit records.",\n'
    '                    "code": "patient_document_access_audit_forbidden",\n'
    "                },\n"
    "                status=status.HTTP_403_FORBIDDEN,\n"
    "            )\n"
    "\n"
    "        serializer = PatientDocumentAccessLogSerializer(\n"
    "            list_document_access_logs(\n"
    "                document_id=document.id,\n"
    "                tenant_id=_tenant_id(request),\n"
    "                organization_id=_organization_id(request),\n"
    "            ),\n"
    "            many=True,\n"
    "        )\n"
    "        return Response(\n"
    "            serializer.data,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessAuditAPIView",\n'
    '    "PatientDocumentActivationAPIView",\n'
    '    "PatientDocumentArchiveAPIView",\n'
    '    "PatientDocumentDeleteAPIView",\n'
    '    "PatientDocumentDetailAPIView",\n'
    '    "PatientDocumentListCreateAPIView",\n'
    '    "PatientDocumentRestoreAPIView",\n'
    '    "PatientDocumentUpdateAPIView",\n'
    '    "PatientDocumentVersionListCreateAPIView",\n'
    ")\n",
    "apps.py": '"""Django application configuration for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.apps import AppConfig\n"
    "from django.utils.translation import gettext_lazy as _\n"
    "\n"
    "\n"
    "class PatientDocumentsConfig(AppConfig):\n"
    '    """Configure the Patient Documents bounded context."""\n'
    "\n"
    '    default_auto_field = "django.db.models.BigAutoField"\n'
    '    name = "apps.patient_management.patient_documents"\n'
    '    label = "patient_documents"\n'
    '    verbose_name = _("Patient Documents")\n'
    "\n"
    "    def ready(self) -> None:\n"
    '        """Import workflow registrations when Django initializes the app."""\n'
    "        from apps.patient_management.patient_documents import workflow_registry  # noqa: F401\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentsConfig",\n'
    ")\n",
    "constants.py": '"""Constants and lifecycle choices for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import models\n"
    "\n"
    "\n"
    "class PatientDocumentStatus(models.TextChoices):\n"
    '    """Lifecycle states for a patient document."""\n'
    "\n"
    '    DRAFT = "draft", "Draft"\n'
    '    ACTIVE = "active", "Active"\n'
    '    ARCHIVED = "archived", "Archived"\n'
    "\n"
    "\n"
    "class PatientDocumentCategory(models.TextChoices):\n"
    '    """Clinical and administrative categories for patient documents."""\n'
    "\n"
    '    MEDICAL_RECORD = "medical_record", "Medical Record"\n'
    '    LAB_RESULT = "lab_result", "Laboratory Result"\n'
    '    IMAGING = "imaging", "Imaging"\n'
    '    PRESCRIPTION = "prescription", "Prescription"\n'
    '    INSURANCE = "insurance", "Insurance"\n'
    '    CONSENT = "consent", "Consent"\n'
    '    REFERRAL = "referral", "Referral"\n'
    '    IDENTIFICATION = "identification", "Identification"\n'
    '    ADMINISTRATIVE = "administrative", "Administrative"\n'
    '    OTHER = "other", "Other"\n'
    "\n"
    "\n"
    "class DocumentVersionStatus(models.TextChoices):\n"
    '    """Lifecycle states for a document version."""\n'
    "\n"
    '    ACTIVE = "active", "Active"\n'
    '    SUPERSEDED = "superseded", "Superseded"\n'
    "\n"
    "\n"
    "DOCUMENT_STATUS_TRANSITIONS = {\n"
    '    "draft": frozenset({\n'
    '        "active",\n'
    "    }),\n"
    '    "active": frozenset({\n'
    '        "archived",\n'
    "    }),\n"
    '    "archived": frozenset({\n'
    '        "active",\n'
    "    }),\n"
    "}\n"
    "\n"
    "\n"
    "class DocumentAccessAction(models.TextChoices):\n"
    '    """Audited access operations against patient documents."""\n'
    "\n"
    '    VIEW = "view", "View"\n'
    '    DOWNLOAD = "download", "Download"\n'
    '    PREVIEW = "preview", "Preview"\n'
    '    SHARE = "share", "Share"\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "DocumentAccessAction",\n'
    '    "DocumentVersionStatus",\n'
    '    "PatientDocumentCategory",\n'
    '    "PatientDocumentStatus",\n'
    ")\n",
    "events/__init__.py": '"""Patient Documents domain event exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .document_created import PatientDocumentCreatedEvent\n"
    "from .document_deleted import PatientDocumentDeletedEvent\n"
    "from .document_restored import PatientDocumentRestoredEvent\n"
    "from .document_status_changed import PatientDocumentStatusChangedEvent\n"
    "from .document_updated import PatientDocumentUpdatedEvent\n"
    "from .document_version_created import PatientDocumentVersionCreatedEvent\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessedEvent",\n'
    '    "PatientDocumentCreatedEvent",\n'
    '    "PatientDocumentDeletedEvent",\n'
    '    "PatientDocumentRestoredEvent",\n'
    '    "PatientDocumentStatusChangedEvent",\n'
    '    "PatientDocumentUpdatedEvent",\n'
    '    "PatientDocumentVersionCreatedEvent",\n'
    ")\n",
    "events/document_created.py": '"""Patient Document created domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentCreatedEvent(DomainEvent):\n"
    '    """Describe creation of a patient document."""\n'
    "\n"
    '    event_type = "patient_document.created"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentCreatedEvent",\n'
    ")\n",
    "events/document_deleted.py": '"""Patient Document deleted domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentDeletedEvent(DomainEvent):\n"
    '    """Describe soft deletion of a patient document."""\n'
    "\n"
    '    event_type = "patient_document.deleted"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentDeletedEvent",\n'
    ")\n",
    "events/document_restored.py": '"""Patient Document restored domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentRestoredEvent(DomainEvent):\n"
    '    """Describe restoration of a patient document."""\n'
    "\n"
    '    event_type = "patient_document.restored"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentRestoredEvent",\n'
    ")\n",
    "events/document_status_changed.py": '"""Patient Document lifecycle domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentStatusChangedEvent(DomainEvent):\n"
    '    """Describe a patient document lifecycle transition."""\n'
    "\n"
    '    event_type = "patient_document.status_changed"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "        previous_status: str,\n"
    "        new_status: str,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    '                "previous_status": previous_status,\n'
    '                "new_status": new_status,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentStatusChangedEvent",\n'
    ")\n",
    "events/document_updated.py": '"""Patient Document updated domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentUpdatedEvent(DomainEvent):\n"
    '    """Describe metadata mutation of a patient document."""\n'
    "\n"
    '    event_type = "patient_document.updated"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentUpdatedEvent",\n'
    ")\n",
    "exceptions.py": '"""Exceptions for the Patient Documents bounded context."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "\n"
    "class PatientDocumentError(Exception):\n"
    '    """Base exception for Patient Documents."""\n'
    "\n"
    "\n"
    "class PatientDocumentNotFoundError(PatientDocumentError):\n"
    '    """Raised when a patient document cannot be resolved."""\n'
    "\n"
    "\n"
    "class PatientDocumentValidationError(PatientDocumentError):\n"
    '    """Raised when a patient document violates a domain rule."""\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentError",\n'
    '    "PatientDocumentNotFoundError",\n'
    '    "PatientDocumentValidationError",\n'
    ")\n",
    "managers.py": '"""Managers and querysets for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import models\n"
    "\n"
    "from apps.core.models import (\n"
    "    SoftDeleteManager,\n"
    "    SoftDeleteQuerySet,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentQuerySet(\n"
    '    SoftDeleteQuerySet["PatientDocument"],\n'
    "):\n"
    '    """Query helpers for tenant-scoped patient documents."""\n'
    "\n"
    "    def for_organization(\n"
    "        self,\n"
    "        organization_id,\n"
    "    ) -> PatientDocumentQuerySet:\n"
    '        """Return documents belonging to one organization."""\n'
    "        return self.filter(\n"
    "            organization_id=organization_id,\n"
    "        )\n"
    "\n"
    "    def for_patient(\n"
    "        self,\n"
    "        patient_id,\n"
    "    ) -> PatientDocumentQuerySet:\n"
    '        """Return documents belonging to one patient."""\n'
    "        return self.filter(\n"
    "            patient_id=patient_id,\n"
    "        )\n"
    "\n"
    "    def active(\n"
    "        self,\n"
    "    ) -> PatientDocumentQuerySet:\n"
    '        """Return active documents."""\n'
    "        return self.filter(\n"
    '            status="active",\n'
    "            is_active=True,\n"
    "        )\n"
    "\n"
    "    def archived(\n"
    "        self,\n"
    "    ) -> PatientDocumentQuerySet:\n"
    '        """Return archived documents."""\n'
    "        return self.filter(\n"
    '            status="archived",\n'
    "        )\n"
    "\n"
    "    def by_category(\n"
    "        self,\n"
    "        category: str,\n"
    "    ) -> PatientDocumentQuerySet:\n"
    '        """Filter documents by category."""\n'
    "        return self.filter(\n"
    "            category=category,\n"
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentManager(\n"
    "    SoftDeleteManager.from_queryset(\n"
    "        PatientDocumentQuerySet,\n"
    "    ),\n"
    "):\n"
    '    """Default manager that hides soft-deleted documents."""\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentManager",\n'
    '    "PatientDocumentQuerySet",\n'
    ")\n",
    "migrations/__init__.py": '"""Migration package intentionally contains no generated migrations."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "__all__: tuple[str, ...] = ()\n",
    "models/__init__.py": '"""Patient Documents model exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .document_access_log import PatientDocumentAccessLog\n"
    "from .document_version import PatientDocumentVersion\n"
    "from .patient_document import PatientDocument\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocument",\n'
    '    "PatientDocumentAccessLog",\n'
    '    "PatientDocumentVersion",\n'
    ")\n",
    "models/document_access_log.py": '"""Audit log for patient-document access."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.core.exceptions import ValidationError\n"
    "from django.db import models\n"
    "\n"
    "from apps.core.models import BaseModel\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    DocumentAccessAction,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models.patient_document import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "class PatientDocumentAccessLog(BaseModel):\n"
    '    """Record an auditable access operation against a patient document."""\n'
    "\n"
    "    patient_document = models.ForeignKey(\n"
    "        PatientDocument,\n"
    "        on_delete=models.CASCADE,\n"
    '        related_name="access_logs",\n'
    "    )\n"
    "\n"
    "    user = models.ForeignKey(\n"
    "        User,\n"
    "        on_delete=models.SET_NULL,\n"
    "        null=True,\n"
    "        blank=True,\n"
    '        related_name="patient_document_access_logs",\n'
    "    )\n"
    "\n"
    "    action = models.CharField(\n"
    "        max_length=20,\n"
    "        choices=DocumentAccessAction.choices,\n"
    "    )\n"
    "\n"
    "    accessed_at = models.DateTimeField(\n"
    "        auto_now_add=True,\n"
    "        db_index=True,\n"
    "    )\n"
    "\n"
    "    ip_address = models.GenericIPAddressField(\n"
    "        null=True,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    user_agent = models.CharField(\n"
    "        max_length=1000,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    metadata = models.JSONField(\n"
    "        default=dict,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    def save(\n"
    "        self,\n"
    "        *args,\n"
    "        **kwargs,\n"
    "    ):\n"
    '        """Prevent modification of an existing access audit record."""\n'
    "        if not self._state.adding:\n"
    "            raise ValidationError(\n"
    '                "Document access audit records are immutable.",\n'
    "            )\n"
    "        return super().save(\n"
    "            *args,\n"
    "            **kwargs,\n"
    "        )\n"
    "\n"
    "    def delete(\n"
    "        self,\n"
    "        *args,\n"
    "        **kwargs,\n"
    "    ):\n"
    '        """Reject deletion of document access audit history."""\n'
    "        raise ValidationError(\n"
    '            "Document access audit records cannot be deleted.",\n'
    "        )\n"
    "\n"
    "    def restore(\n"
    "        self,\n"
    "    ):\n"
    '        """Reject restoration of document access audit history."""\n'
    "        raise ValidationError(\n"
    '            "Document access audit records cannot be restored.",\n'
    "        )\n"
    "\n"
    "    class Meta:\n"
    '        """Database metadata for document access audit records."""\n'
    "\n"
    '        db_table = "patient_document_access_logs"\n'
    "\n"
    "        ordering = (\n"
    '            "-accessed_at",\n'
    "        )\n"
    "\n"
    "        indexes = [\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "patient_document",\n'
    '                    "accessed_at",\n'
    "                ),\n"
    '                name="pdal_document_access_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "user",\n'
    '                    "accessed_at",\n'
    "                ),\n"
    '                name="pdal_user_access_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "action",\n'
    '                    "accessed_at",\n'
    "                ),\n"
    '                name="pdal_action_access_idx",\n'
    "            ),\n"
    "        ]\n"
    "\n"
    "    def __str__(\n"
    "        self,\n"
    "    ) -> str:\n"
    '        """Return an audit-log label."""\n'
    '        return f"{self.action} - {self.patient_document_id}"\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessLog",\n'
    ")\n",
    "models/document_version.py": '"""Version history for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.core.exceptions import ValidationError\n"
    "from django.db import models\n"
    "\n"
    "from apps.core.models import BaseModel\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    DocumentVersionStatus,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models.patient_document import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "class PatientDocumentVersion(BaseModel):\n"
    '    """Immutable metadata record for one patient-document version."""\n'
    "\n"
    "    patient_document = models.ForeignKey(\n"
    "        PatientDocument,\n"
    "        on_delete=models.CASCADE,\n"
    '        related_name="versions",\n'
    "    )\n"
    "\n"
    "    version_number = models.PositiveIntegerField()\n"
    "\n"
    "    storage_key = models.CharField(\n"
    "        max_length=500,\n"
    "    )\n"
    "\n"
    "    original_filename = models.CharField(\n"
    "        max_length=255,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    mime_type = models.CharField(\n"
    "        max_length=150,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    file_size = models.PositiveBigIntegerField(\n"
    "        default=0,\n"
    "    )\n"
    "\n"
    "    checksum = models.CharField(\n"
    "        max_length=255,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    status = models.CharField(\n"
    "        max_length=20,\n"
    "        choices=DocumentVersionStatus.choices,\n"
    "        default=DocumentVersionStatus.ACTIVE,\n"
    "    )\n"
    "\n"
    "    notes = models.TextField(\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    created_by = models.ForeignKey(\n"
    "        User,\n"
    "        on_delete=models.SET_NULL,\n"
    "        null=True,\n"
    "        blank=True,\n"
    '        related_name="created_patient_document_versions",\n'
    "    )\n"
    "\n"
    "    class Meta:\n"
    '        """Database metadata for document versions."""\n'
    "\n"
    '        db_table = "patient_document_versions"\n'
    "\n"
    "        ordering = (\n"
    '            "-version_number",\n'
    "        )\n"
    "\n"
    "        constraints = [\n"
    "            models.UniqueConstraint(\n"
    "                fields=(\n"
    '                    "patient_document",\n'
    '                    "version_number",\n'
    "                ),\n"
    '                name="uq_patient_document_version_number",\n'
    "            ),\n"
    "            models.CheckConstraint(\n"
    "                condition=models.Q(\n"
    "                    version_number__gt=0,\n"
    "                ),\n"
    '                name="ck_patient_document_version_positive",\n'
    "            ),\n"
    "        ]\n"
    "\n"
    "        indexes = [\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "patient_document",\n'
    '                    "version_number",\n'
    "                ),\n"
    '                name="pdv_document_version_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "patient_document",\n'
    '                    "status",\n'
    "                ),\n"
    '                name="pdv_document_status_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "checksum",\n'
    "                ),\n"
    '                name="pdv_checksum_idx",\n'
    "            ),\n"
    "        ]\n"
    "\n"
    "    IMMUTABLE_FIELDS = frozenset({\n"
    '        "patient_document_id",\n'
    '        "version_number",\n'
    '        "storage_key",\n'
    '        "original_filename",\n'
    '        "mime_type",\n'
    '        "file_size",\n'
    '        "checksum",\n'
    '        "notes",\n'
    '        "created_by_id",\n'
    "    })\n"
    "\n"
    "    def save(\n"
    "        self,\n"
    "        *args,\n"
    "        **kwargs,\n"
    "    ):\n"
    '        """Prevent modification of immutable version metadata."""\n'
    "        if not self._state.adding:\n"
    "            existing = type(self).objects.get(\n"
    "                pk=self.pk,\n"
    "            )\n"
    "            changed = {\n"
    "                field\n"
    "                for field in self.IMMUTABLE_FIELDS\n"
    "                if getattr(existing, field) != getattr(self, field)\n"
    "            }\n"
    "            if changed:\n"
    "                raise ValidationError(\n"
    '                    "Document version metadata is immutable: "\n'
    '                    + ", ".join(sorted(changed)),\n'
    "                )\n"
    "        return super().save(\n"
    "            *args,\n"
    "            **kwargs,\n"
    "        )\n"
    "\n"
    "    def delete(\n"
    "        self,\n"
    "        *args,\n"
    "        **kwargs,\n"
    "    ):\n"
    '        """Reject deletion of document-version history."""\n'
    "        raise ValidationError(\n"
    '            "Document versions are immutable and cannot be deleted.",\n'
    "        )\n"
    "\n"
    "    def restore(\n"
    "        self,\n"
    "    ):\n"
    '        """Reject restoration of document-version history."""\n'
    "        raise ValidationError(\n"
    '            "Document versions are immutable and cannot be restored.",\n'
    "        )\n"
    "\n"
    "    def clean(\n"
    "        self,\n"
    "    ) -> None:\n"
    '        """Validate version metadata."""\n'
    "        super().clean()\n"
    "        if self.version_number < 1:\n"
    "            raise ValidationError(\n"
    '                "Document version number must be positive.",\n'
    "            )\n"
    "\n"
    "    def __str__(\n"
    "        self,\n"
    "    ) -> str:\n"
    '        """Return a version label."""\n'
    '        return f"{self.patient_document_id} v{self.version_number}"\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentVersion",\n'
    ")\n",
    "models/patient_document.py": '"""Patient document aggregate."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import models\n"
    "from django.utils.translation import gettext_lazy as _\n"
    "\n"
    "from apps.core.models import AllObjectsManager, BaseModel\n"
    "from apps.patient_management.patients.models import Patient\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    PatientDocumentCategory,\n"
    "    PatientDocumentStatus,\n"
    ")\n"
    "from apps.patient_management.patient_documents.managers import (\n"
    "    PatientDocumentManager,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "from apps.platform.organizations.models import Organization\n"
    "\n"
    "\n"
    "class PatientDocument(BaseModel):\n"
    '    """Represent a document associated with a canonical patient record."""\n'
    "\n"
    "    objects = PatientDocumentManager()\n"
    "    all_objects = AllObjectsManager()\n"
    "\n"
    "    organization = models.ForeignKey(\n"
    "        Organization,\n"
    "        on_delete=models.CASCADE,\n"
    '        related_name="patient_documents",\n'
    '        help_text=_("Organization owning the patient document."),\n'
    "    )\n"
    "\n"
    "    patient = models.ForeignKey(\n"
    "        Patient,\n"
    "        on_delete=models.CASCADE,\n"
    '        related_name="patient_documents",\n'
    '        help_text=_("Canonical patient owning the document."),\n'
    "    )\n"
    "\n"
    "    title = models.CharField(\n"
    '        _("Title"),\n'
    "        max_length=255,\n"
    "    )\n"
    "\n"
    "    category = models.CharField(\n"
    '        _("Category"),\n'
    "        max_length=40,\n"
    "        choices=PatientDocumentCategory.choices,\n"
    "        default=PatientDocumentCategory.OTHER,\n"
    "        db_index=True,\n"
    "    )\n"
    "\n"
    "    status = models.CharField(\n"
    '        _("Status"),\n'
    "        max_length=20,\n"
    "        choices=PatientDocumentStatus.choices,\n"
    "        default=PatientDocumentStatus.DRAFT,\n"
    "        db_index=True,\n"
    "    )\n"
    "\n"
    "    description = models.TextField(\n"
    '        _("Description"),\n'
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    original_filename = models.CharField(\n"
    '        _("Original Filename"),\n'
    "        max_length=255,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    storage_key = models.CharField(\n"
    '        _("Storage Key"),\n'
    "        max_length=500,\n"
    "    )\n"
    "\n"
    "    mime_type = models.CharField(\n"
    '        _("MIME Type"),\n'
    "        max_length=150,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    file_size = models.PositiveBigIntegerField(\n"
    '        _("File Size"),\n'
    "        default=0,\n"
    "    )\n"
    "\n"
    "    checksum = models.CharField(\n"
    '        _("Checksum"),\n'
    "        max_length=255,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    is_confidential = models.BooleanField(\n"
    '        _("Confidential"),\n'
    "        default=False,\n"
    "        db_index=True,\n"
    "    )\n"
    "\n"
    "    metadata = models.JSONField(\n"
    '        _("Metadata"),\n'
    "        default=dict,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    uploaded_at = models.DateTimeField(\n"
    '        _("Uploaded At"),\n'
    "        null=True,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    archived_at = models.DateTimeField(\n"
    '        _("Archived At"),\n'
    "        null=True,\n"
    "        blank=True,\n"
    "    )\n"
    "\n"
    "    created_by = models.ForeignKey(\n"
    "        User,\n"
    "        on_delete=models.SET_NULL,\n"
    "        null=True,\n"
    "        blank=True,\n"
    '        related_name="created_patient_documents",\n'
    "    )\n"
    "\n"
    "    class Meta:\n"
    '        """Database metadata for the patient document aggregate."""\n'
    "\n"
    '        db_table = "patient_documents"\n'
    "\n"
    "        ordering = (\n"
    '            "-created_at",\n'
    "        )\n"
    "\n"
    "        constraints = [\n"
    "            models.UniqueConstraint(\n"
    "                fields=(\n"
    '                    "organization",\n'
    '                    "storage_key",\n'
    "                ),\n"
    '                name="uq_patient_document_org_storage_key",\n'
    "            ),\n"
    "        ]\n"
    "\n"
    "        indexes = [\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "organization",\n'
    '                    "patient",\n'
    '                    "status",\n'
    "                ),\n"
    '                name="pd_org_patient_status_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "organization",\n'
    '                    "category",\n'
    '                    "created_at",\n'
    "                ),\n"
    '                name="pd_org_category_created_idx",\n'
    "            ),\n"
    "            models.Index(\n"
    "                fields=(\n"
    '                    "patient",\n'
    '                    "created_at",\n'
    "                ),\n"
    '                name="pd_patient_created_idx",\n'
    "            ),\n"
    "        ]\n"
    "\n"
    "    def __str__(\n"
    "        self,\n"
    "    ) -> str:\n"
    '        """Return a human-readable document label."""\n'
    '        return f"{self.title} - {self.patient_id}"\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocument",\n'
    ")\n",
    "permissions.py": '"""RBAC permission identifiers and API adapters for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from apps.platform.rbac.permissions.base import (\n"
    "    RBACPermissionBase,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentPermission:\n"
    '    """Stable permission codes for the bounded context."""\n'
    "\n"
    '    LIST = "patient_document.list"\n'
    '    VIEW = "patient_document.view"\n'
    '    CREATE = "patient_document.create"\n'
    '    UPDATE = "patient_document.update"\n'
    '    ACTIVATE = "patient_document.activate"\n'
    '    DELETE = "patient_document.delete"\n'
    '    RESTORE = "patient_document.restore"\n'
    '    ARCHIVE = "patient_document.archive"\n'
    '    VERSION_CREATE = "patient_document.version_create"\n'
    '    ACCESS_AUDIT = "patient_document.access_audit"\n'
    "\n"
    "\n"
    "class CanListPatientDocuments(RBACPermissionBase):\n"
    '    """Allow listing patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.LIST\n"
    '    message = "You do not have permission to list patient documents."\n'
    "\n"
    "\n"
    "class CanViewPatientDocument(RBACPermissionBase):\n"
    '    """Allow viewing patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.VIEW\n"
    '    message = "You do not have permission to view patient documents."\n'
    "\n"
    "\n"
    "class CanCreatePatientDocument(RBACPermissionBase):\n"
    '    """Allow creating patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.CREATE\n"
    '    message = "You do not have permission to create patient documents."\n'
    "\n"
    "\n"
    "class CanUpdatePatientDocument(RBACPermissionBase):\n"
    '    """Allow updating patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.UPDATE\n"
    '    message = "You do not have permission to update patient documents."\n'
    "\n"
    "\n"
    "class CanDeletePatientDocument(RBACPermissionBase):\n"
    '    """Allow deleting patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.DELETE\n"
    '    message = "You do not have permission to delete patient documents."\n'
    "\n"
    "\n"
    "class CanRestorePatientDocument(RBACPermissionBase):\n"
    '    """Allow restoring patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.RESTORE\n"
    '    message = "You do not have permission to restore patient documents."\n'
    "\n"
    "\n"
    "class CanActivatePatientDocument(RBACPermissionBase):\n"
    '    """Allow activating patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.ACTIVATE\n"
    '    message = "You do not have permission to activate patient documents."\n'
    "\n"
    "\n"
    "class CanArchivePatientDocument(RBACPermissionBase):\n"
    '    """Allow archiving patient documents."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.ARCHIVE\n"
    '    message = "You do not have permission to archive patient documents."\n'
    "\n"
    "\n"
    "class CanCreatePatientDocumentVersion(RBACPermissionBase):\n"
    '    """Allow creating document versions."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.VERSION_CREATE\n"
    '    message = "You do not have permission to create document versions."\n'
    "\n"
    "\n"
    "class CanViewPatientDocumentAccessAudit(RBACPermissionBase):\n"
    '    """Allow viewing document access audit records."""\n'
    "\n"
    "    permission_code = PatientDocumentPermission.ACCESS_AUDIT\n"
    '    message = "You do not have permission to view document access audit records."\n'
    "\n"
    "\n"
    "__all__ = (\n"
    '    "CanActivatePatientDocument",\n'
    '    "CanArchivePatientDocument",\n'
    '    "CanCreatePatientDocument",\n'
    '    "CanCreatePatientDocumentVersion",\n'
    '    "CanDeletePatientDocument",\n'
    '    "CanListPatientDocuments",\n'
    '    "CanRestorePatientDocument",\n'
    '    "CanUpdatePatientDocument",\n'
    '    "CanViewPatientDocument",\n'
    '    "CanViewPatientDocumentAccessAudit",\n'
    '    "PatientDocumentPermission",\n'
    ")\n",
    "policies/__init__.py": '"""Patient Documents policy exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .patient_document import PatientDocumentPolicy\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentPolicy",\n'
    ")\n",
    "policies/patient_document.py": '"""Authorization policy for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from apps.patient_management.patient_documents.permissions import (\n"
    "    PatientDocumentPermission,\n"
    ")\n"
    "from apps.platform.rbac.services import (\n"
    "    user_has_permission,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentPolicy:\n"
    '    """Evaluate organization-scoped Patient Document permissions."""\n'
    "\n"
    "    def can_list(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        organization,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can list patient documents."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.LIST,\n"
    "            organization=organization,\n"
    "        )\n"
    "\n"
    "    def can_view(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can view a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.VIEW,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_create(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        organization,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can create a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.CREATE,\n"
    "            organization=organization,\n"
    "        )\n"
    "\n"
    "    def can_update(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can update a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.UPDATE,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_delete(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can delete a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.DELETE,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_restore(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can restore a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.RESTORE,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_activate(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can activate a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.ACTIVATE,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_archive(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can archive a patient document."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.ARCHIVE,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_create_version(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can create a document version."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.VERSION_CREATE,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "    def can_view_access_audit(\n"
    "        self,\n"
    "        *,\n"
    "        actor,\n"
    "        document,\n"
    "    ) -> bool:\n"
    '        """Return whether the actor can view access audit records."""\n'
    "        return user_has_permission(\n"
    "            user=actor,\n"
    "            permission=PatientDocumentPermission.ACCESS_AUDIT,\n"
    "            organization=document.organization,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentPolicy",\n'
    ")\n",
    "selectors/__init__.py": '"""Patient Documents selector exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .document_access_log import list_document_access_logs\n"
    "from .document_version import list_document_versions\n"
    "from .patient_document import (\n"
    "    get_patient_document,\n"
    "    patient_document_queryset,\n"
    ")\n"
    "\n"
    "__all__ = (\n"
    '    "get_patient_document",\n'
    '    "list_document_access_logs",\n'
    '    "list_document_versions",\n'
    '    "patient_document_queryset",\n'
    ")\n",
    "selectors/document_access_log.py": '"""Selectors for Patient Document access audit records."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from django.db.models import QuerySet\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocumentAccessLog,\n"
    ")\n"
    "\n"
    "\n"
    "def list_document_access_logs(\n"
    "    *,\n"
    "    document_id: UUID,\n"
    "    tenant_id: UUID,\n"
    "    organization_id: UUID,\n"
    ") -> QuerySet[PatientDocumentAccessLog]:\n"
    '    """Return access logs inside the tenant boundary."""\n'
    "    return (\n"
    "        PatientDocumentAccessLog.objects\n"
    "        .filter(\n"
    "            patient_document_id=document_id,\n"
    "            patient_document__organization_id=organization_id,\n"
    "            patient_document__organization__tenant_id=tenant_id,\n"
    "        )\n"
    "        .select_related(\n"
    '            "user",\n'
    '            "patient_document",\n'
    "        )\n"
    "        .order_by(\n"
    '            "-accessed_at",\n'
    "        )\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "list_document_access_logs",\n'
    ")\n",
    "selectors/document_version.py": '"""Selectors for patient document versions."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from django.db.models import QuerySet\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocumentVersion,\n"
    ")\n"
    "\n"
    "\n"
    "def list_document_versions(\n"
    "    *,\n"
    "    document_id: UUID,\n"
    "    tenant_id: UUID,\n"
    "    organization_id: UUID,\n"
    ") -> QuerySet[PatientDocumentVersion]:\n"
    '    """Return versions for an organization-scoped patient document."""\n'
    "    return (\n"
    "        PatientDocumentVersion.objects\n"
    "        .filter(\n"
    "            patient_document_id=document_id,\n"
    "            patient_document__organization_id=organization_id,\n"
    "            patient_document__organization__tenant_id=tenant_id,\n"
    "        )\n"
    "        .select_related(\n"
    '            "patient_document",\n'
    '            "created_by",\n'
    "        )\n"
    "        .order_by(\n"
    '            "-version_number",\n'
    "        )\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "list_document_versions",\n'
    ")\n",
    "selectors/patient_document.py": '"""Read-side selectors for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from django.db.models import QuerySet\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "\n"
    "\n"
    "def patient_document_queryset(\n"
    "    *,\n"
    "    tenant_id: UUID,\n"
    "    organization_id: UUID,\n"
    "    patient_id=None,\n"
    "    include_deleted: bool = False,\n"
    ") -> QuerySet[PatientDocument]:\n"
    '    """Return an optimized organization and tenant scoped queryset."""\n'
    "    manager = (\n"
    "        PatientDocument.all_objects\n"
    "        if include_deleted\n"
    "        else PatientDocument.objects\n"
    "    )\n"
    "\n"
    "    queryset = (\n"
    "        manager\n"
    "        .filter(\n"
    "            organization_id=organization_id,\n"
    "            organization__tenant_id=tenant_id,\n"
    "        )\n"
    "        .select_related(\n"
    '            "organization",\n'
    '            "patient",\n'
    '            "created_by",\n'
    "        )\n"
    "        .prefetch_related(\n"
    '            "versions",\n'
    "        )\n"
    "    )\n"
    "\n"
    "    if patient_id is not None:\n"
    "        queryset = queryset.filter(\n"
    "            patient_id=patient_id,\n"
    "        )\n"
    "\n"
    "    return queryset\n"
    "\n"
    "\n"
    "def get_patient_document(\n"
    "    *,\n"
    "    document_id: UUID,\n"
    "    tenant_id: UUID,\n"
    "    organization_id: UUID,\n"
    "    include_deleted: bool = False,\n"
    ") -> PatientDocument:\n"
    '    """Resolve one patient document inside the tenant boundary."""\n'
    "    return patient_document_queryset(\n"
    "        tenant_id=tenant_id,\n"
    "        organization_id=organization_id,\n"
    "        include_deleted=include_deleted,\n"
    "    ).get(\n"
    "        pk=document_id,\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "get_patient_document",\n'
    '    "patient_document_queryset",\n'
    ")\n",
    "services/__init__.py": '"""Patient Documents service exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .document_access_log import PatientDocumentAccessLogService\n"
    "from .document_version import PatientDocumentVersionService\n"
    "from .patient_document import PatientDocumentService\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessLogService",\n'
    '    "PatientDocumentService",\n'
    '    "PatientDocumentVersionService",\n'
    ")\n",
    "services/document_access_log.py": '"""Domain service for Patient Document access auditing."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocumentAccessLog,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentAccessLogService:\n"
    '    """Persist auditable document-access records."""\n'
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def record(\n"
    "        *,\n"
    "        patient_document,\n"
    "        user,\n"
    "        action: str,\n"
    "        ip_address: str | None = None,\n"
    '        user_agent: str = "",\n'
    "        metadata: dict | None = None,\n"
    "    ) -> PatientDocumentAccessLog:\n"
    '        """Record one document access event."""\n'
    "        return PatientDocumentAccessLog.objects.create(\n"
    "            patient_document=patient_document,\n"
    "            user=user,\n"
    "            action=action,\n"
    "            ip_address=ip_address,\n"
    "            user_agent=user_agent[:1000],\n"
    "            metadata=metadata or {},\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessLogService",\n'
    ")\n",
    "services/document_version.py": '"""Domain services for patient document versions."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    DocumentVersionStatus,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    "    PatientDocumentVersion,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentVersionService:\n"
    '    """Create immutable version metadata records."""\n'
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def create(\n"
    "        *,\n"
    "        patient_document,\n"
    "        storage_key: str,\n"
    "        performed_by,\n"
    '        original_filename: str = "",\n'
    '        mime_type: str = "",\n'
    "        file_size: int = 0,\n"
    '        checksum: str = "",\n'
    '        notes: str = "",\n'
    "    ) -> PatientDocumentVersion:\n"
    '        """Create the next sequential version."""\n'
    "        parent_document = (\n"
    "            PatientDocument.objects\n"
    "            .select_for_update()\n"
    "            .get(\n"
    "                pk=patient_document.pk,\n"
    "            )\n"
    "        )\n"
    "\n"
    "        latest = (\n"
    "            PatientDocumentVersion.objects\n"
    "            .select_for_update()\n"
    "            .filter(\n"
    "                patient_document=patient_document,\n"
    "            )\n"
    "            .order_by(\n"
    '                "-version_number",\n'
    "            )\n"
    "            .first()\n"
    "        )\n"
    "\n"
    "        next_number = (\n"
    "            latest.version_number + 1\n"
    "            if latest is not None\n"
    "            else 1\n"
    "        )\n"
    "\n"
    "        PatientDocumentVersion.objects.filter(\n"
    "            patient_document=patient_document,\n"
    "            status=DocumentVersionStatus.ACTIVE,\n"
    "        ).update(\n"
    "            status=DocumentVersionStatus.SUPERSEDED,\n"
    "        )\n"
    "\n"
    "        return PatientDocumentVersion.objects.create(\n"
    "            patient_document=patient_document,\n"
    "            version_number=next_number,\n"
    "            storage_key=storage_key,\n"
    "            original_filename=original_filename,\n"
    "            mime_type=mime_type,\n"
    "            file_size=file_size,\n"
    "            checksum=checksum,\n"
    "            status=DocumentVersionStatus.ACTIVE,\n"
    "            notes=notes,\n"
    "            created_by=performed_by,\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentVersionService",\n'
    ")\n",
    "services/patient_document.py": '"""Domain services for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from collections.abc import Mapping\n"
    "from typing import Any\n"
    "\n"
    "from django.core.exceptions import ValidationError\n"
    "from django.db import transaction\n"
    "from django.utils import timezone\n"
    "\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    DOCUMENT_STATUS_TRANSITIONS,\n"
    "    PatientDocumentStatus,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.patient_management.patient_documents.validators import (\n"
    "    validate_document_data,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentService:\n"
    '    """Perform transactional Patient Document mutations."""\n'
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def create(\n"
    "        *,\n"
    "        organization,\n"
    "        patient,\n"
    "        title: str,\n"
    "        storage_key: str,\n"
    "        performed_by,\n"
    "        category: str,\n"
    '        description: str = "",\n'
    '        original_filename: str = "",\n'
    '        mime_type: str = "",\n'
    "        file_size: int = 0,\n"
    '        checksum: str = "",\n'
    "        is_confidential: bool = False,\n"
    "        metadata: dict[str, Any] | None = None,\n"
    "    ) -> PatientDocument:\n"
    '        """Create a new patient document."""\n'
    "        if organization.tenant_id != patient.organization.tenant_id:\n"
    "            raise ValidationError(\n"
    '                "Patient and organization must belong to the same tenant.",\n'
    "            )\n"
    "\n"
    "        if patient.organization_id != organization.id:\n"
    "            raise ValidationError(\n"
    '                "Patient and organization must match.",\n'
    "            )\n"
    "\n"
    "        if not title.strip():\n"
    "            raise ValidationError(\n"
    '                "Document title is required.",\n'
    "            )\n"
    "\n"
    "        if not storage_key.strip():\n"
    "            raise ValidationError(\n"
    '                "Storage key is required.",\n'
    "            )\n"
    "\n"
    "        return PatientDocument.objects.create(\n"
    "            organization=organization,\n"
    "            patient=patient,\n"
    "            title=title.strip(),\n"
    "            category=category,\n"
    "            status=PatientDocumentStatus.DRAFT,\n"
    "            description=description.strip(),\n"
    "            original_filename=original_filename.strip(),\n"
    "            storage_key=storage_key.strip(),\n"
    "            mime_type=mime_type.strip(),\n"
    "            file_size=file_size,\n"
    "            checksum=checksum.strip(),\n"
    "            is_confidential=is_confidential,\n"
    "            metadata=metadata or {},\n"
    "            created_by=performed_by,\n"
    "        )\n"
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def update(\n"
    "        *,\n"
    "        instance: PatientDocument,\n"
    "        validated_data: Mapping[str, Any],\n"
    "        performed_by,\n"
    "    ) -> PatientDocument:\n"
    '        """Update mutable document metadata."""\n'
    "        validate_document_data(\n"
    "            validated_data,\n"
    "        )\n"
    "\n"
    "        data = dict(validated_data)\n"
    "        data.pop(\n"
    '            "organization",\n'
    "            None,\n"
    "        )\n"
    "        data.pop(\n"
    '            "patient",\n'
    "            None,\n"
    "        )\n"
    "\n"
    "        for field_name, value in data.items():\n"
    "            if isinstance(value, str):\n"
    "                value = value.strip()\n"
    "            setattr(\n"
    "                instance,\n"
    "                field_name,\n"
    "                value,\n"
    "            )\n"
    "\n"
    "        instance.save()\n"
    "        return instance\n"
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def activate(\n"
    "        *,\n"
    "        instance: PatientDocument,\n"
    "        performed_by,\n"
    "    ) -> PatientDocument:\n"
    '        """Activate a draft or archived patient document."""\n'
    "        if instance.is_deleted:\n"
    "            raise ValidationError(\n"
    '                "A deleted document cannot be activated.",\n'
    "            )\n"
    "\n"
    "        allowed = DOCUMENT_STATUS_TRANSITIONS.get(\n"
    "            instance.status,\n"
    "            frozenset(),\n"
    "        )\n"
    "        if PatientDocumentStatus.ACTIVE not in allowed:\n"
    "            raise ValidationError(\n"
    "                f\"Document cannot transition from '{instance.status}' to \"\n"
    "                f\"'{PatientDocumentStatus.ACTIVE}'.\",\n"
    "            )\n"
    "\n"
    "        instance.status = PatientDocumentStatus.ACTIVE\n"
    "        instance.is_active = True\n"
    "        if instance.uploaded_at is None:\n"
    "            instance.uploaded_at = timezone.now()\n"
    "        instance.save(\n"
    "            update_fields=[\n"
    '                "status",\n'
    '                "is_active",\n'
    '                "uploaded_at",\n'
    '                "updated_at",\n'
    "            ],\n"
    "        )\n"
    "        return instance\n"
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def archive(\n"
    "        *,\n"
    "        instance: PatientDocument,\n"
    "        performed_by,\n"
    "    ) -> PatientDocument:\n"
    '        """Archive an active patient document."""\n'
    "        if instance.is_deleted:\n"
    "            raise ValidationError(\n"
    '                "A deleted document cannot be archived.",\n'
    "            )\n"
    "\n"
    "        allowed = DOCUMENT_STATUS_TRANSITIONS.get(\n"
    "            instance.status,\n"
    "            frozenset(),\n"
    "        )\n"
    "        if PatientDocumentStatus.ARCHIVED not in allowed:\n"
    "            raise ValidationError(\n"
    "                f\"Document cannot transition from '{instance.status}' to \"\n"
    "                f\"'{PatientDocumentStatus.ARCHIVED}'.\",\n"
    "            )\n"
    "\n"
    "        instance.status = PatientDocumentStatus.ARCHIVED\n"
    "        instance.is_active = False\n"
    "        instance.archived_at = timezone.now()\n"
    "        instance.save(\n"
    "            update_fields=[\n"
    '                "status",\n'
    '                "is_active",\n'
    '                "archived_at",\n'
    '                "updated_at",\n'
    "            ],\n"
    "        )\n"
    "        return instance\n"
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def delete(\n"
    "        *,\n"
    "        instance: PatientDocument,\n"
    "        performed_by,\n"
    "    ) -> PatientDocument:\n"
    '        """Soft-delete a patient document."""\n'
    "        instance.delete(\n"
    "            user_id=performed_by.pk,\n"
    "        )\n"
    "        return instance\n"
    "\n"
    "    @staticmethod\n"
    "    @transaction.atomic\n"
    "    def restore(\n"
    "        *,\n"
    "        instance: PatientDocument,\n"
    "        performed_by,\n"
    "    ) -> PatientDocument:\n"
    '        """Restore a soft-deleted patient document."""\n'
    "        instance.restore()\n"
    "        instance.status = PatientDocumentStatus.ACTIVE\n"
    "        instance.is_active = True\n"
    "        instance.save(\n"
    "            update_fields=[\n"
    '                "is_deleted",\n'
    '                "deleted_at",\n'
    '                "deleted_by_id",\n'
    '                "status",\n'
    '                "is_active",\n'
    '                "updated_at",\n'
    "            ],\n"
    "        )\n"
    "        return instance\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentService",\n'
    ")\n",
    "tests/test_architecture.py": '"""Architecture tests for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from pathlib import Path\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "\n"
    "\n"
    "def test_canonical_patient_model_is_used() -> None:\n"
    '    """Ensure PatientDocument points to the canonical Patient model."""\n'
    "    from apps.patient_management.patients.models import Patient\n"
    "\n"
    "    assert (\n"
    "        PatientDocument._meta.get_field(\n"
    '            "patient",\n'
    "        ).remote_field.model\n"
    "        is Patient\n"
    "    )\n"
    "\n"
    "\n"
    "def test_patient_document_does_not_define_a_duplicate_patient_model() -> None:\n"
    '    """Ensure the bounded context uses the canonical Patient module."""\n'
    "    assert (\n"
    "        PatientDocument._meta.get_field(\n"
    '            "patient",\n'
    "        ).remote_field.model.__module__\n"
    '        == "apps.patient_management.patients.models"\n'
    "    )\n"
    "\n"
    "\n"
    "def test_access_audit_is_workflow_orchestrated() -> None:\n"
    '    """Ensure the API does not directly invoke the access-log service."""\n'
    '    views_source = Path(__file__).resolve().parents[1] / "api" / "views.py"\n'
    '    source = views_source.read_text(encoding="utf-8")\n'
    '    assert "PatientDocumentAccessLogService.record(" not in source\n'
    '    assert "PatientDocumentAccessWorkflow(" in source\n'
    "\n"
    "\n"
    "def test_version_creation_is_workflow_orchestrated() -> None:\n"
    '    """Ensure the API does not directly invoke the version service."""\n'
    '    views_source = Path(__file__).resolve().parents[1] / "api" / "views.py"\n'
    '    source = views_source.read_text(encoding="utf-8")\n'
    '    assert "PatientDocumentVersionService.create(" not in source\n'
    '    assert "PatientDocumentVersionCreationWorkflow(" in source\n'
    "\n"
    "\n"
    "def test_lifecycle_and_access_routes_exist() -> None:\n"
    '    """Ensure lifecycle and access operations expose explicit API routes."""\n'
    '    urls_source = Path(__file__).resolve().parents[1] / "api" / "urls.py"\n'
    '    source = urls_source.read_text(encoding="utf-8")\n'
    "    assert 'name=\"activate\"' in source\n"
    "    assert 'name=\"access-audit\"' in source\n"
    "\n"
    "\n"
    "__all__: tuple[str, ...] = ()\n",
    "urls.py": '"""Compatibility URL export for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from apps.patient_management.patient_documents.api.urls import (\n"
    "    urlpatterns,\n"
    ")\n"
    "\n"
    "__all__ = (\n"
    '    "urlpatterns",\n'
    ")\n",
    "validators.py": '"""Validation helpers for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from collections.abc import Mapping\n"
    "from typing import Any\n"
    "\n"
    "from django.core.exceptions import ValidationError\n"
    "\n"
    "\n"
    "PROTECTED_FIELDS = frozenset({\n"
    '    "id",\n'
    '    "organization",\n'
    '    "organization_id",\n'
    '    "patient",\n'
    '    "patient_id",\n'
    '    "created_at",\n'
    '    "updated_at",\n'
    '    "created_by",\n'
    '    "created_by_id",\n'
    '    "is_deleted",\n'
    '    "deleted_at",\n'
    '    "deleted_by_id",\n'
    "})\n"
    "\n"
    "\n"
    "def validate_document_data(\n"
    "    data: Mapping[str, Any],\n"
    ") -> None:\n"
    '    """Validate mutable document metadata supplied to the service."""\n'
    "    forbidden = PROTECTED_FIELDS.intersection(data.keys())\n"
    "    if forbidden:\n"
    "        raise ValidationError(\n"
    '            "Protected fields cannot be modified: "\n'
    '            + ", ".join(sorted(forbidden)),\n'
    "        )\n"
    "\n"
    '    title = data.get("title")\n'
    "    if title is not None and not str(title).strip():\n"
    "        raise ValidationError(\n"
    '            "Document title cannot be empty.",\n'
    "        )\n"
    "\n"
    '    file_size = data.get("file_size")\n'
    "    if file_size is not None and int(file_size) < 0:\n"
    "        raise ValidationError(\n"
    '            "File size cannot be negative.",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PROTECTED_FIELDS",\n'
    '    "validate_document_data",\n'
    ")\n",
    "workflow_registry.py": '"""Workflow registrations for Patient Documents."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from apps.core.workflows import workflow_registry\n"
    "from apps.patient_management.patient_documents.workflows import (\n"
    "    PatientDocumentAccessWorkflow,\n"
    "    PatientDocumentActivationWorkflow,\n"
    "    PatientDocumentArchiveWorkflow,\n"
    "    PatientDocumentCreationWorkflow,\n"
    "    PatientDocumentDeletionWorkflow,\n"
    "    PatientDocumentRestoreWorkflow,\n"
    "    PatientDocumentUpdateWorkflow,\n"
    "    PatientDocumentVersionCreationWorkflow,\n"
    ")\n"
    "\n"
    "\n"
    "workflow_registry.register(\n"
    '    name="patient_document.access",\n'
    "    workflow=PatientDocumentAccessWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.create",\n'
    "    workflow=PatientDocumentCreationWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.update",\n'
    "    workflow=PatientDocumentUpdateWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.delete",\n'
    "    workflow=PatientDocumentDeletionWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.activate",\n'
    "    workflow=PatientDocumentActivationWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.archive",\n'
    "    workflow=PatientDocumentArchiveWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.restore",\n'
    "    workflow=PatientDocumentRestoreWorkflow,\n"
    ")\n"
    "workflow_registry.register(\n"
    '    name="patient_document.version.create",\n'
    "    workflow=PatientDocumentVersionCreationWorkflow,\n"
    ")\n"
    "\n"
    "\n"
    "__all__: tuple[str, ...] = ()\n",
    "workflows/__init__.py": '"""Patient Documents workflow exports."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from .creation import (\n"
    "    PatientDocumentCreationData,\n"
    "    PatientDocumentCreationRequest,\n"
    "    PatientDocumentCreationWorkflow,\n"
    ")\n"
    "from .deletion import (\n"
    "    PatientDocumentDeletionData,\n"
    "    PatientDocumentDeletionRequest,\n"
    "    PatientDocumentDeletionWorkflow,\n"
    ")\n"
    "from .lifecycle import (\n"
    "    PatientDocumentActivationWorkflow,\n"
    "    PatientDocumentArchiveWorkflow,\n"
    "    PatientDocumentLifecycleData,\n"
    "    PatientDocumentLifecycleRequest,\n"
    "    PatientDocumentRestoreWorkflow,\n"
    ")\n"
    "from .version_creation import (\n"
    "    PatientDocumentVersionCreationData,\n"
    "    PatientDocumentVersionCreationRequest,\n"
    "    PatientDocumentVersionCreationWorkflow,\n"
    ")\n"
    "from .update import (\n"
    "    PatientDocumentUpdateData,\n"
    "    PatientDocumentUpdateRequest,\n"
    "    PatientDocumentUpdateWorkflow,\n"
    ")\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessData",\n'
    '    "PatientDocumentAccessRequest",\n'
    '    "PatientDocumentAccessWorkflow",\n'
    '    "PatientDocumentActivationWorkflow",\n'
    '    "PatientDocumentArchiveWorkflow",\n'
    '    "PatientDocumentCreationData",\n'
    '    "PatientDocumentCreationRequest",\n'
    '    "PatientDocumentCreationWorkflow",\n'
    '    "PatientDocumentDeletionData",\n'
    '    "PatientDocumentDeletionRequest",\n'
    '    "PatientDocumentDeletionWorkflow",\n'
    '    "PatientDocumentLifecycleData",\n'
    '    "PatientDocumentLifecycleRequest",\n'
    '    "PatientDocumentRestoreWorkflow",\n'
    '    "PatientDocumentUpdateData",\n'
    '    "PatientDocumentUpdateRequest",\n'
    '    "PatientDocumentUpdateWorkflow",\n'
    '    "PatientDocumentVersionCreationData",\n'
    '    "PatientDocumentVersionCreationRequest",\n'
    '    "PatientDocumentVersionCreationWorkflow",\n'
    ")\n",
    "workflows/creation.py": '"""Patient Document creation workflow."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from dataclasses import dataclass\n"
    "from uuid import UUID\n"
    "\n"
    "from django.core.exceptions import ObjectDoesNotExist\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.core.workflows import (\n"
    "    BaseWorkflow,\n"
    "    WorkflowContext,\n"
    "    WorkflowResult,\n"
    ")\n"
    "from apps.patient_management.patient_documents.events import (\n"
    "    PatientDocumentCreatedEvent,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.patient_management.patient_documents.policies import (\n"
    "    PatientDocumentPolicy,\n"
    ")\n"
    "from apps.patient_management.patient_documents.services import (\n"
    "    PatientDocumentService,\n"
    ")\n"
    "from apps.patient_management.patients.models import Patient\n"
    "from apps.platform.accounts.models import User\n"
    "from apps.platform.organizations.models import Organization\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentCreationRequest:\n"
    '    """Input for Patient Document creation."""\n'
    "\n"
    "    organization_id: UUID\n"
    "    patient_id: UUID\n"
    "    data: dict\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentCreationData:\n"
    '    """Successful Patient Document creation result."""\n'
    "\n"
    "    document_id: UUID\n"
    "    patient_id: UUID\n"
    "    event_id: UUID\n"
    "\n"
    "\n"
    "class PatientDocumentCreationWorkflow(\n"
    "    BaseWorkflow[PatientDocumentCreationData],\n"
    "):\n"
    '    """Authorize and create a tenant-scoped Patient Document."""\n'
    "\n"
    '    workflow_name = "patient_document.create"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentCreationRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentCreationData]:\n"
    "        try:\n"
    "            actor = User.objects.get(\n"
    "                pk=context.actor_id,\n"
    "            )\n"
    "            organization = (\n"
    "                Organization.objects\n"
    '                .select_related("tenant")\n'
    "                .get(\n"
    "                    pk=self._request.organization_id,\n"
    "                    tenant_id=context.tenant_id,\n"
    "                )\n"
    "            )\n"
    "            patient = (\n"
    "                Patient.objects\n"
    '                .select_related("organization")\n'
    "                .get(\n"
    "                    pk=self._request.patient_id,\n"
    "                    organization_id=organization.id,\n"
    "                    organization__tenant_id=context.tenant_id,\n"
    "                )\n"
    "            )\n"
    "        except ObjectDoesNotExist as exc:\n"
    "            raise ValueError(\n"
    '                "Organization or patient was not found.",\n'
    "            ) from exc\n"
    "\n"
    "        if not self._policy.can_create(\n"
    "            actor=actor,\n"
    "            organization=organization,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to create patient documents.",\n'
    "            )\n"
    "\n"
    "        document = PatientDocumentService.create(\n"
    "            organization=organization,\n"
    "            patient=patient,\n"
    "            performed_by=actor,\n"
    "            **self._request.data,\n"
    "        )\n"
    "\n"
    "        event = PatientDocumentCreatedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=document.id,\n"
    "            patient_id=document.patient_id,\n"
    "            organization_id=document.organization_id,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentCreationData(\n"
    "                document_id=document.id,\n"
    "                patient_id=document.patient_id,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document created successfully.",\n'
    '            code="patient_document_created",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentCreationData",\n'
    '    "PatientDocumentCreationRequest",\n'
    '    "PatientDocumentCreationWorkflow",\n'
    ")\n",
    "workflows/deletion.py": '"""Patient Document deletion workflow."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from dataclasses import dataclass\n"
    "from uuid import UUID\n"
    "\n"
    "from django.core.exceptions import ObjectDoesNotExist\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.core.workflows import (\n"
    "    BaseWorkflow,\n"
    "    WorkflowContext,\n"
    "    WorkflowResult,\n"
    ")\n"
    "from apps.patient_management.patient_documents.events import (\n"
    "    PatientDocumentDeletedEvent,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.patient_management.patient_documents.policies import (\n"
    "    PatientDocumentPolicy,\n"
    ")\n"
    "from apps.patient_management.patient_documents.services import (\n"
    "    PatientDocumentService,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentDeletionRequest:\n"
    '    """Input for Patient Document deletion."""\n'
    "\n"
    "    document_id: UUID\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentDeletionData:\n"
    '    """Successful Patient Document deletion result."""\n'
    "\n"
    "    document_id: UUID\n"
    "    deleted: bool\n"
    "    event_id: UUID\n"
    "\n"
    "\n"
    "class PatientDocumentDeletionWorkflow(\n"
    "    BaseWorkflow[PatientDocumentDeletionData],\n"
    "):\n"
    '    """Soft-delete a tenant-scoped patient document."""\n'
    "\n"
    '    workflow_name = "patient_document.delete"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentDeletionRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentDeletionData]:\n"
    "        try:\n"
    "            actor = User.objects.get(\n"
    "                pk=context.actor_id,\n"
    "            )\n"
    "            document = (\n"
    "                PatientDocument.objects\n"
    "                .select_related(\n"
    '                    "organization",\n'
    '                    "patient",\n'
    "                )\n"
    "                .get(\n"
    "                    pk=self._request.document_id,\n"
    "                    organization__tenant_id=context.tenant_id,\n"
    "                )\n"
    "            )\n"
    "        except ObjectDoesNotExist as exc:\n"
    "            raise ValueError(\n"
    '                "Patient document was not found.",\n'
    "            ) from exc\n"
    "\n"
    "        if not self._policy.can_delete(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to delete this patient document.",\n'
    "            )\n"
    "\n"
    "        PatientDocumentService.delete(\n"
    "            instance=document,\n"
    "            performed_by=actor,\n"
    "        )\n"
    "\n"
    "        event = PatientDocumentDeletedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=document.id,\n"
    "            patient_id=document.patient_id,\n"
    "            organization_id=document.organization_id,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentDeletionData(\n"
    "                document_id=document.id,\n"
    "                deleted=True,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document deleted successfully.",\n'
    '            code="patient_document_deleted",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentDeletionData",\n'
    '    "PatientDocumentDeletionRequest",\n'
    '    "PatientDocumentDeletionWorkflow",\n'
    ")\n",
    "workflows/lifecycle.py": '"""Patient Document lifecycle workflows."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from dataclasses import dataclass\n"
    "from uuid import UUID\n"
    "\n"
    "from django.core.exceptions import ObjectDoesNotExist\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.core.workflows import (\n"
    "    BaseWorkflow,\n"
    "    WorkflowContext,\n"
    "    WorkflowResult,\n"
    ")\n"
    "from apps.patient_management.patient_documents.constants import (\n"
    "    PatientDocumentStatus,\n"
    ")\n"
    "from apps.patient_management.patient_documents.events import (\n"
    "    PatientDocumentRestoredEvent,\n"
    "    PatientDocumentStatusChangedEvent,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.patient_management.patient_documents.policies import (\n"
    "    PatientDocumentPolicy,\n"
    ")\n"
    "from apps.patient_management.patient_documents.services import (\n"
    "    PatientDocumentService,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentLifecycleRequest:\n"
    '    """Input for a lifecycle transition."""\n'
    "\n"
    "    document_id: UUID\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentLifecycleData:\n"
    '    """Lifecycle workflow result."""\n'
    "\n"
    "    document_id: UUID\n"
    "    previous_status: str\n"
    "    new_status: str\n"
    "    event_id: UUID | None = None\n"
    "\n"
    "\n"
    "class PatientDocumentActivationWorkflow(\n"
    "    BaseWorkflow[PatientDocumentLifecycleData],\n"
    "):\n"
    '    """Activate a patient document."""\n'
    "\n"
    '    workflow_name = "patient_document.activate"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentLifecycleRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentLifecycleData]:\n"
    "        actor, document = _resolve(\n"
    "            context,\n"
    "            self._request.document_id,\n"
    "        )\n"
    "        if not self._policy.can_activate(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to activate this patient document.",\n'
    "            )\n"
    "\n"
    "        previous = document.status\n"
    "        updated = PatientDocumentService.activate(\n"
    "            instance=document,\n"
    "            performed_by=actor,\n"
    "        )\n"
    "        event = PatientDocumentStatusChangedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=updated.id,\n"
    "            patient_id=updated.patient_id,\n"
    "            organization_id=updated.organization_id,\n"
    "            previous_status=previous,\n"
    "            new_status=updated.status,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentLifecycleData(\n"
    "                document_id=updated.id,\n"
    "                previous_status=previous,\n"
    "                new_status=updated.status,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document activated successfully.",\n'
    '            code="patient_document_activated",\n'
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentArchiveWorkflow(\n"
    "    BaseWorkflow[PatientDocumentLifecycleData],\n"
    "):\n"
    '    """Archive a patient document."""\n'
    "\n"
    '    workflow_name = "patient_document.archive"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentLifecycleRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentLifecycleData]:\n"
    "        actor, document = _resolve(\n"
    "            context,\n"
    "            self._request.document_id,\n"
    "        )\n"
    "        if not self._policy.can_archive(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to archive this patient document.",\n'
    "            )\n"
    "\n"
    "        previous = document.status\n"
    "        updated = PatientDocumentService.archive(\n"
    "            instance=document,\n"
    "            performed_by=actor,\n"
    "        )\n"
    "        event = PatientDocumentStatusChangedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=updated.id,\n"
    "            patient_id=updated.patient_id,\n"
    "            organization_id=updated.organization_id,\n"
    "            previous_status=previous,\n"
    "            new_status=updated.status,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentLifecycleData(\n"
    "                document_id=updated.id,\n"
    "                previous_status=previous,\n"
    "                new_status=updated.status,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document archived successfully.",\n'
    '            code="patient_document_archived",\n'
    "        )\n"
    "\n"
    "\n"
    "class PatientDocumentRestoreWorkflow(\n"
    "    BaseWorkflow[PatientDocumentLifecycleData],\n"
    "):\n"
    '    """Restore a soft-deleted patient document."""\n'
    "\n"
    '    workflow_name = "patient_document.restore"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentLifecycleRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentLifecycleData]:\n"
    "        try:\n"
    "            actor = User.objects.get(\n"
    "                pk=context.actor_id,\n"
    "            )\n"
    "            document = (\n"
    "                PatientDocument.all_objects\n"
    "                .select_related(\n"
    '                    "organization",\n'
    '                    "patient",\n'
    "                )\n"
    "                .get(\n"
    "                    pk=self._request.document_id,\n"
    "                    organization__tenant_id=context.tenant_id,\n"
    "                    is_deleted=True,\n"
    "                )\n"
    "            )\n"
    "        except ObjectDoesNotExist as exc:\n"
    "            raise ValueError(\n"
    '                "Deleted patient document was not found.",\n'
    "            ) from exc\n"
    "\n"
    "        if not self._policy.can_restore(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to restore this patient document.",\n'
    "            )\n"
    "\n"
    "        previous = document.status\n"
    "        restored = PatientDocumentService.restore(\n"
    "            instance=document,\n"
    "            performed_by=actor,\n"
    "        )\n"
    "        event = PatientDocumentRestoredEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=restored.id,\n"
    "            patient_id=restored.patient_id,\n"
    "            organization_id=restored.organization_id,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentLifecycleData(\n"
    "                document_id=restored.id,\n"
    "                previous_status=previous,\n"
    "                new_status=restored.status,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document restored successfully.",\n'
    '            code="patient_document_restored",\n'
    "        )\n"
    "\n"
    "\n"
    "def _resolve(\n"
    "    context: WorkflowContext,\n"
    "    document_id: UUID,\n"
    "):\n"
    '    """Resolve actor and active document within the tenant boundary."""\n'
    "    try:\n"
    "        actor = User.objects.get(\n"
    "            pk=context.actor_id,\n"
    "        )\n"
    "        document = (\n"
    "            PatientDocument.objects\n"
    "            .select_related(\n"
    '                "organization",\n'
    '                "patient",\n'
    "            )\n"
    "            .get(\n"
    "                pk=document_id,\n"
    "                organization__tenant_id=context.tenant_id,\n"
    "            )\n"
    "        )\n"
    "    except ObjectDoesNotExist as exc:\n"
    "        raise ValueError(\n"
    '            "Patient document was not found.",\n'
    "        ) from exc\n"
    "    return actor, document\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentActivationWorkflow",\n'
    '    "PatientDocumentArchiveWorkflow",\n'
    '    "PatientDocumentLifecycleData",\n'
    '    "PatientDocumentLifecycleRequest",\n'
    '    "PatientDocumentRestoreWorkflow",\n'
    ")\n",
    "workflows/update.py": '"""Patient Document update workflow."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from collections.abc import Mapping\n"
    "from dataclasses import dataclass\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from django.core.exceptions import ObjectDoesNotExist\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.core.workflows import (\n"
    "    BaseWorkflow,\n"
    "    WorkflowContext,\n"
    "    WorkflowResult,\n"
    ")\n"
    "from apps.patient_management.patient_documents.events import (\n"
    "    PatientDocumentUpdatedEvent,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocument,\n"
    ")\n"
    "from apps.patient_management.patient_documents.policies import (\n"
    "    PatientDocumentPolicy,\n"
    ")\n"
    "from apps.patient_management.patient_documents.services import (\n"
    "    PatientDocumentService,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentUpdateRequest:\n"
    '    """Input for Patient Document updates."""\n'
    "\n"
    "    document_id: UUID\n"
    "    data: Mapping[str, Any]\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentUpdateData:\n"
    '    """Successful Patient Document update result."""\n'
    "\n"
    "    document_id: UUID\n"
    "    updated: bool\n"
    "    event_id: UUID | None = None\n"
    "\n"
    "\n"
    "class PatientDocumentUpdateWorkflow(\n"
    "    BaseWorkflow[PatientDocumentUpdateData],\n"
    "):\n"
    '    """Authorize and update a tenant-scoped patient document."""\n'
    "\n"
    '    workflow_name = "patient_document.update"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentUpdateRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentUpdateData]:\n"
    "        try:\n"
    "            actor = User.objects.get(\n"
    "                pk=context.actor_id,\n"
    "            )\n"
    "            document = (\n"
    "                PatientDocument.objects\n"
    "                .select_related(\n"
    '                    "organization",\n'
    '                    "patient",\n'
    "                )\n"
    "                .get(\n"
    "                    pk=self._request.document_id,\n"
    "                    organization__tenant_id=context.tenant_id,\n"
    "                )\n"
    "            )\n"
    "        except ObjectDoesNotExist as exc:\n"
    "            raise ValueError(\n"
    '                "Patient document was not found.",\n'
    "            ) from exc\n"
    "\n"
    "        if not self._policy.can_update(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to update this patient document.",\n'
    "            )\n"
    "\n"
    "        updated = PatientDocumentService.update(\n"
    "            instance=document,\n"
    "            validated_data=self._request.data,\n"
    "            performed_by=actor,\n"
    "        )\n"
    "\n"
    "        event = PatientDocumentUpdatedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=updated.id,\n"
    "            patient_id=updated.patient_id,\n"
    "            organization_id=updated.organization_id,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentUpdateData(\n"
    "                document_id=updated.id,\n"
    "                updated=True,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document updated successfully.",\n'
    '            code="patient_document_updated",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentUpdateData",\n'
    '    "PatientDocumentUpdateRequest",\n'
    '    "PatientDocumentUpdateWorkflow",\n'
    ")\n",
    "storage.py": '"""Patient Document storage boundary.\n'
    "\n"
    "Physical storage remains owned by the common document-storage infrastructure.\n"
    "This bounded context stores only references and metadata.\n"
    '"""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from django.conf import settings\n"
    "\n"
    "from apps.common.storage.service import (\n"
    "    document_storage,\n"
    ")\n"
    "\n"
    "\n"
    'DEFAULT_BACKEND = "local"\n'
    "\n"
    "\n"
    "def _backend_name() -> str:\n"
    '    """Return the configured document-storage provider name."""\n'
    "    return str(\n"
    "        getattr(\n"
    "            settings,\n"
    '            "DOCUMENT_STORAGE_BACKEND",\n'
    "            DEFAULT_BACKEND,\n"
    "        ),\n"
    "    )\n"
    "\n"
    "\n"
    "class PatientDocumentStorage:\n"
    '    """Application-facing storage gateway for patient documents."""\n'
    "\n"
    "    def download(\n"
    "        self,\n"
    "        *,\n"
    "        storage_key: str,\n"
    "    ) -> object:\n"
    '        """Download a stored document through common storage."""\n'
    "        return document_storage.download(\n"
    "            storage_key,\n"
    "            backend=_backend_name(),\n"
    "        )\n"
    "\n"
    "    def delete(\n"
    "        self,\n"
    "        *,\n"
    "        storage_key: str,\n"
    "    ) -> None:\n"
    '        """Delete a stored object through common storage."""\n'
    "        document_storage.delete(\n"
    "            storage_key,\n"
    "            backend=_backend_name(),\n"
    "        )\n"
    "\n"
    "\n"
    "patient_document_storage = PatientDocumentStorage()\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentStorage",\n'
    '    "patient_document_storage",\n'
    ")\n",
    "api/serializers/version.py": '"""Serializers for Patient Document versions."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from rest_framework import serializers\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocumentVersion,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentVersionSerializer(\n"
    "    serializers.ModelSerializer,\n"
    "):\n"
    '    """Serialize immutable document-version metadata."""\n'
    "\n"
    "    class Meta:\n"
    '        """Serializer metadata."""\n'
    "\n"
    "        model = PatientDocumentVersion\n"
    "        fields = (\n"
    '            "id",\n'
    '            "patient_document",\n'
    '            "version_number",\n'
    '            "storage_key",\n'
    '            "original_filename",\n'
    '            "mime_type",\n'
    '            "file_size",\n'
    '            "checksum",\n'
    '            "status",\n'
    '            "notes",\n'
    '            "created_by",\n'
    '            "created_at",\n'
    "        )\n"
    "        read_only_fields = fields\n"
    "\n"
    "\n"
    "class PatientDocumentVersionCreateSerializer(\n"
    "    serializers.Serializer,\n"
    "):\n"
    '    """Validate creation of a new document version."""\n'
    "\n"
    "    storage_key = serializers.CharField(\n"
    "        max_length=500,\n"
    "    )\n"
    "    original_filename = serializers.CharField(\n"
    "        max_length=255,\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    mime_type = serializers.CharField(\n"
    "        max_length=150,\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    file_size = serializers.IntegerField(\n"
    "        min_value=0,\n"
    "        required=False,\n"
    "        default=0,\n"
    "    )\n"
    "    checksum = serializers.CharField(\n"
    "        max_length=255,\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "    notes = serializers.CharField(\n"
    "        required=False,\n"
    "        allow_blank=True,\n"
    "    )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentVersionCreateSerializer",\n'
    '    "PatientDocumentVersionSerializer",\n'
    ")\n",
    "api/serializers/access_log.py": '"""Serializers for Patient Document access audit records."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from rest_framework import serializers\n"
    "\n"
    "from apps.patient_management.patient_documents.models import (\n"
    "    PatientDocumentAccessLog,\n"
    ")\n"
    "\n"
    "\n"
    "class PatientDocumentAccessLogSerializer(\n"
    "    serializers.ModelSerializer,\n"
    "):\n"
    '    """Serialize immutable document access audit records."""\n'
    "\n"
    "    class Meta:\n"
    '        """Serializer metadata."""\n'
    "\n"
    "        model = PatientDocumentAccessLog\n"
    "        fields = (\n"
    '            "id",\n'
    '            "patient_document",\n'
    '            "user",\n'
    '            "action",\n'
    '            "accessed_at",\n'
    '            "ip_address",\n'
    '            "user_agent",\n'
    '            "metadata",\n'
    "        )\n"
    "        read_only_fields = fields\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessLogSerializer",\n'
    ")\n",
    "workflows/version_creation.py": '"""Patient Document version creation workflow."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from collections.abc import Mapping\n"
    "from dataclasses import dataclass\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from django.core.exceptions import ObjectDoesNotExist\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.core.workflows import (\n"
    "    BaseWorkflow,\n"
    "    WorkflowContext,\n"
    "    WorkflowResult,\n"
    ")\n"
    "from apps.patient_management.patient_documents.events import (\n"
    "    PatientDocumentVersionCreatedEvent,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import PatientDocument\n"
    "from apps.patient_management.patient_documents.policies import "
    "PatientDocumentPolicy\n"
    "from apps.patient_management.patient_documents.services import "
    "PatientDocumentVersionService\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentVersionCreationRequest:\n"
    '    """Input for creation of one immutable document version."""\n'
    "\n"
    "    document_id: UUID\n"
    "    data: Mapping[str, Any]\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentVersionCreationData:\n"
    '    """Successful document-version creation result."""\n'
    "\n"
    "    version: object\n"
    "    event_id: UUID\n"
    "\n"
    "\n"
    "class PatientDocumentVersionCreationWorkflow(\n"
    "    BaseWorkflow[PatientDocumentVersionCreationData],\n"
    "):\n"
    '    """Authorize and create the next immutable document version."""\n'
    "\n"
    '    workflow_name = "patient_document.version.create"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentVersionCreationRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    '        """Initialize the workflow."""\n'
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentVersionCreationData]:\n"
    '        """Execute version creation inside the tenant transaction."""\n'
    "        try:\n"
    "            actor = User.objects.get(\n"
    "                pk=context.actor_id,\n"
    "            )\n"
    "            document = (\n"
    "                PatientDocument.objects\n"
    "                .select_related(\n"
    '                    "organization",\n'
    '                    "patient",\n'
    "                )\n"
    "                .get(\n"
    "                    pk=self._request.document_id,\n"
    "                    organization__tenant_id=context.tenant_id,\n"
    "                )\n"
    "            )\n"
    "        except ObjectDoesNotExist as exc:\n"
    "            raise ValueError(\n"
    '                "Patient document was not found.",\n'
    "            ) from exc\n"
    "\n"
    "        if not self._policy.can_create_version(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to create document versions.",\n'
    "            )\n"
    "\n"
    "        version = PatientDocumentVersionService.create(\n"
    "            patient_document=document,\n"
    "            performed_by=actor,\n"
    "            **dict(self._request.data),\n"
    "        )\n"
    "        event = PatientDocumentVersionCreatedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=document.id,\n"
    "            patient_id=document.patient_id,\n"
    "            organization_id=document.organization_id,\n"
    "            version_id=version.id,\n"
    "            version_number=version.version_number,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentVersionCreationData(\n"
    "                version=version,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document version created successfully.",\n'
    '            code="patient_document_version_created",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentVersionCreationData",\n'
    '    "PatientDocumentVersionCreationRequest",\n'
    '    "PatientDocumentVersionCreationWorkflow",\n'
    ")\n",
    "events/document_version_created.py": '"""Patient Document version-created domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentVersionCreatedEvent(DomainEvent):\n"
    '    """Describe creation of one immutable document version."""\n'
    "\n"
    '    event_type = "patient_document.version_created"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "        version_id: UUID,\n"
    "        version_number: int,\n"
    "    ) -> None:\n"
    '        """Initialize the version-created event."""\n'
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    '                "version_id": str(version_id),\n'
    '                "version_number": version_number,\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentVersionCreatedEvent",\n'
    ")\n",
    "events/document_accessed.py": '"""Patient Document access-audited domain event."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from uuid import UUID\n"
    "\n"
    "from apps.core.events import DomainEvent\n"
    "\n"
    "\n"
    "class PatientDocumentAccessedEvent(DomainEvent):\n"
    '    """Describe one successful patient-document access operation."""\n'
    "\n"
    '    event_type = "patient_document.accessed"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        tenant_id: UUID,\n"
    "        actor_id: UUID,\n"
    "        document_id: UUID,\n"
    "        patient_id: UUID,\n"
    "        organization_id: UUID,\n"
    "        action: str,\n"
    "        access_log_id: UUID,\n"
    "    ) -> None:\n"
    '        """Initialize the access-audited domain event."""\n'
    "        super().__init__(\n"
    "            tenant_id=tenant_id,\n"
    "            actor_id=actor_id,\n"
    "            payload={\n"
    '                "document_id": str(document_id),\n'
    '                "patient_id": str(patient_id),\n'
    '                "organization_id": str(organization_id),\n'
    '                "action": action,\n'
    '                "access_log_id": str(access_log_id),\n'
    "            },\n"
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessedEvent",\n'
    ")\n",
    "workflows/access.py": '"""Patient Document access-audit workflow."""\n'
    "\n"
    "from __future__ import annotations\n"
    "\n"
    "from collections.abc import Mapping\n"
    "from dataclasses import dataclass\n"
    "from typing import Any\n"
    "from uuid import UUID\n"
    "\n"
    "from django.core.exceptions import ObjectDoesNotExist\n"
    "from django.db import transaction\n"
    "\n"
    "from apps.core.workflows import (\n"
    "    BaseWorkflow,\n"
    "    WorkflowContext,\n"
    "    WorkflowResult,\n"
    ")\n"
    "from apps.patient_management.patient_documents.events import (\n"
    "    PatientDocumentAccessedEvent,\n"
    ")\n"
    "from apps.patient_management.patient_documents.models import PatientDocument\n"
    "from apps.patient_management.patient_documents.policies import (\n"
    "    PatientDocumentPolicy,\n"
    ")\n"
    "from apps.patient_management.patient_documents.services import (\n"
    "    PatientDocumentAccessLogService,\n"
    ")\n"
    "from apps.platform.accounts.models import User\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentAccessRequest:\n"
    '    """Input required to record one document access operation."""\n'
    "\n"
    "    document_id: UUID\n"
    "    action: str\n"
    "    ip_address: str | None = None\n"
    '    user_agent: str = ""\n'
    "    metadata: Mapping[str, Any] | None = None\n"
    "\n"
    "\n"
    "@dataclass(\n"
    "    frozen=True,\n"
    "    slots=True,\n"
    "    kw_only=True,\n"
    ")\n"
    "class PatientDocumentAccessData:\n"
    '    """Successful document-access workflow result."""\n'
    "\n"
    "    access_log: object\n"
    "    event_id: UUID\n"
    "\n"
    "\n"
    "class PatientDocumentAccessWorkflow(\n"
    "    BaseWorkflow[PatientDocumentAccessData],\n"
    "):\n"
    '    """Authorize, audit, and publish one document access operation."""\n'
    "\n"
    '    workflow_name = "patient_document.access"\n'
    "\n"
    "    def __init__(\n"
    "        self,\n"
    "        *,\n"
    "        request: PatientDocumentAccessRequest,\n"
    "        policy: PatientDocumentPolicy | None = None,\n"
    "        logger_=None,\n"
    "    ) -> None:\n"
    '        """Initialize the access workflow."""\n'
    "        super().__init__(\n"
    "            logger_=logger_,\n"
    "            payload=request,\n"
    "        )\n"
    "        self._request = request\n"
    "        self._policy = policy or PatientDocumentPolicy()\n"
    "\n"
    "    @transaction.atomic\n"
    "    def _run(\n"
    "        self,\n"
    "        context: WorkflowContext,\n"
    "    ) -> WorkflowResult[PatientDocumentAccessData]:\n"
    '        """Record access after tenant and object authorization."""\n'
    "        try:\n"
    "            actor = User.objects.get(\n"
    "                pk=context.actor_id,\n"
    "            )\n"
    "            document = (\n"
    "                PatientDocument.objects\n"
    "                .select_related(\n"
    '                    "organization",\n'
    '                    "patient",\n'
    "                )\n"
    "                .get(\n"
    "                    pk=self._request.document_id,\n"
    "                    organization__tenant_id=context.tenant_id,\n"
    "                )\n"
    "            )\n"
    "        except ObjectDoesNotExist as exc:\n"
    "            raise ValueError(\n"
    '                "Patient document was not found.",\n'
    "            ) from exc\n"
    "\n"
    "        if not self._policy.can_view(\n"
    "            actor=actor,\n"
    "            document=document,\n"
    "        ):\n"
    "            raise PermissionError(\n"
    '                "You do not have permission to view patient documents.",\n'
    "            )\n"
    "\n"
    "        access_log = PatientDocumentAccessLogService.record(\n"
    "            patient_document=document,\n"
    "            user=actor,\n"
    "            action=self._request.action,\n"
    "            ip_address=self._request.ip_address,\n"
    "            user_agent=self._request.user_agent,\n"
    "            metadata=dict(self._request.metadata or {}),\n"
    "        )\n"
    "        event = PatientDocumentAccessedEvent(\n"
    "            tenant_id=context.tenant_id,\n"
    "            actor_id=context.actor_id,\n"
    "            document_id=document.id,\n"
    "            patient_id=document.patient_id,\n"
    "            organization_id=document.organization_id,\n"
    "            action=self._request.action,\n"
    "            access_log_id=access_log.id,\n"
    "        )\n"
    "        self.publish_after_commit(event)\n"
    "\n"
    "        return WorkflowResult.ok(\n"
    "            context=context,\n"
    "            data=PatientDocumentAccessData(\n"
    "                access_log=access_log,\n"
    "                event_id=event.event_id,\n"
    "            ),\n"
    '            message="Patient document access recorded successfully.",\n'
    '            code="patient_document_access_recorded",\n'
    "        )\n"
    "\n"
    "\n"
    "__all__ = (\n"
    '    "PatientDocumentAccessData",\n'
    '    "PatientDocumentAccessRequest",\n'
    '    "PatientDocumentAccessWorkflow",\n'
    ")\n",
}

REQUIRED_FILES = (
    ".installer_manifest.json",
    "__init__.py",
    "admin.py",
    "apps.py",
    "constants.py",
    "exceptions.py",
    "managers.py",
    "permissions.py",
    "urls.py",
    "validators.py",
    "workflow_registry.py",
    "api/__init__.py",
    "api/filters.py",
    "api/serializers/__init__.py",
    "api/serializers/create.py",
    "api/serializers/detail.py",
    "api/serializers/list.py",
    "api/serializers/update.py",
    "api/urls.py",
    "api/views.py",
    "events/__init__.py",
    "events/document_created.py",
    "events/document_deleted.py",
    "events/document_restored.py",
    "events/document_status_changed.py",
    "events/document_updated.py",
    "models/__init__.py",
    "models/document_access_log.py",
    "models/document_version.py",
    "models/patient_document.py",
    "policies/__init__.py",
    "policies/patient_document.py",
    "selectors/__init__.py",
    "selectors/document_access_log.py",
    "selectors/document_version.py",
    "selectors/patient_document.py",
    "services/__init__.py",
    "services/document_access_log.py",
    "services/document_version.py",
    "services/patient_document.py",
    "workflows/__init__.py",
    "workflows/access.py",
    "workflows/creation.py",
    "workflows/deletion.py",
    "workflows/lifecycle.py",
    "workflows/update.py",
    "events/document_accessed.py",
    "migrations/__init__.py",
    "tests/test_architecture.py",
)


def validate_manifest() -> None:
    """Validate the embedded installer manifest."""
    manifest = json.loads(FILES[".installer_manifest.json"])
    if manifest["module"] != "patient_documents":
        raise RuntimeError("Invalid module manifest.")
    if manifest["version"] != VERSION:
        raise RuntimeError("Invalid installer version.")
    if manifest["canonical_patient"] != (
        "apps.patient_management.patients.models.Patient"
    ):
        raise RuntimeError("Canonical Patient reference is invalid.")
    if manifest["migration_policy"] != "no_migrations":
        raise RuntimeError("Migration policy must remain no_migrations.")
    print("MANIFEST: PASS")


def validate_structure() -> None:
    """Validate required Patient Documents files."""
    missing = [path for path in REQUIRED_FILES if path not in FILES]
    if missing:
        raise RuntimeError(
            "Missing Patient Documents files:\n  " + "\n  ".join(missing)
        )
    print("STRUCTURE: PASS")


def validate_style() -> None:
    """Validate Python module conventions and AST correctness."""
    count = 0

    for relative_path, source in FILES.items():
        if not relative_path.endswith(".py"):
            continue

        tree = ast.parse(
            source,
            filename=relative_path,
        )

        if not tree.body or not isinstance(
            tree.body[0],
            ast.Expr,
        ):
            raise RuntimeError(f"Missing module docstring: {relative_path}")

        if not any(
            isinstance(node, ast.ImportFrom) and node.module == "__future__"
            for node in tree.body
        ):
            raise RuntimeError(f"Missing future annotations import: {relative_path}")

        count += 1

    model_source = FILES["models/patient_document.py"]
    if "apps.patient_management.patients.models" not in model_source:
        raise RuntimeError("Canonical Patient import is missing.")

    print(f"STYLE: PASS ({count} Python files)")


def validate_architecture() -> None:
    """Validate required layers and protected orchestration boundaries."""
    required_tokens = (
        "permissions.py",
        "policies/patient_document.py",
        "selectors/patient_document.py",
        "services/patient_document.py",
        "workflows/access.py",
        "workflows/creation.py",
        "events/document_accessed.py",
        "events/document_created.py",
        "api/views.py",
    )
    for path in required_tokens:
        if path not in FILES:
            raise RuntimeError(f"Required architecture layer missing: {path}")

    workflow_source = FILES["workflow_registry.py"]
    workflow_names = (
        "patient_document.access",
        "patient_document.create",
        "patient_document.update",
        "patient_document.delete",
        "patient_document.activate",
        "patient_document.archive",
        "patient_document.restore",
        "patient_document.version.create",
    )
    for name in workflow_names:
        if name not in workflow_source:
            raise RuntimeError(f"Workflow registry missing: {name}")

    api_source = FILES["api/views.py"]
    for token in (
        "PatientDocumentVersionService.create(",
        "PatientDocumentAccessLogService.record(",
    ):
        if token in api_source:
            raise RuntimeError(f"API must not directly invoke domain service: {token}")

    if "PatientDocumentVersionCreationWorkflow(" not in api_source:
        raise RuntimeError("Version creation workflow is missing from the API.")
    if "PatientDocumentAccessWorkflow(" not in api_source:
        raise RuntimeError("Access workflow is missing from the API.")
    if "PatientDocumentActivationAPIView" not in api_source:
        raise RuntimeError("Document activation API is missing.")
    if 'name="activate"' not in FILES["api/urls.py"]:
        raise RuntimeError("Document activation route is missing.")
    if 'name="access-audit"' not in FILES["api/urls.py"]:
        raise RuntimeError("Document access-audit route is missing.")
    if FILES["api/urls.py"].count("PatientDocumentAccessAuditAPIView,") != 1:
        raise RuntimeError("Duplicate access-audit import detected.")
    if '"data": asdict(result.data)' not in api_source:
        raise RuntimeError(
            "Creation response must serialize slotted workflow data safely."
        )

    print("ARCHITECTURE: PASS")


def validate_compile() -> None:
    """Compile every generated Python source file."""
    count = 0

    for relative_path, source in FILES.items():
        if not relative_path.endswith(".py"):
            continue

        compile(
            source,
            relative_path,
            "exec",
        )
        count += 1

    print(f"PY_COMPILE: PASS ({count} Python files)")


def install() -> None:
    """Delete the old bounded context and write the fresh implementation."""
    if TARGET.exists():
        shutil.rmtree(TARGET)

    for relative_path, source in FILES.items():
        destination = TARGET / relative_path
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        destination.write_text(
            source,
            encoding="utf-8",
            newline="\n",
        )

    print("OLD MODULE: DELETED")
    print(f"FILES WRITTEN: {len(FILES)}")
    print("MIGRATIONS: NOT GENERATED")
    print("PATIENT DOCUMENTS INSTALLATION COMPLETE")


def main() -> None:
    """Validate and install Patient Documents."""
    print(f"DatavionOS {MODULE_NAME} Production Installer v{VERSION}")
    print(f"Target: {TARGET}")

    validate_manifest()
    validate_structure()
    validate_style()
    validate_architecture()
    validate_compile()
    install()


if __name__ == "__main__":
    main()
