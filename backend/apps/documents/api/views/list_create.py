from __future__ import annotations

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.documents.api.serializers import (
    DocumentCreateSerializer,
    DocumentDetailSerializer,
    DocumentListSerializer,
)
from apps.documents.permissions import CanCreateDocument, CanViewDocument
from apps.documents.workflows import DocumentCreationRequest, DocumentCreationWorkflow


class DocumentListCreateAPIView(BaseListCreateAPIView):
    queryset = None
    permission_classes_map = {"GET": (CanViewDocument,), "POST": (CanCreateDocument,)}
    list_serializer_class = DocumentListSerializer
    detail_serializer_class = DocumentDetailSerializer
    create_serializer_class = DocumentCreateSerializer
    create_workflow = DocumentCreationWorkflow

    def get_queryset(self):
        from apps.documents.models import Document

        tenant = self.current_tenant
        organization = self.current_organization
        queryset = Document.objects.select_related("organization", "tenant")
        if tenant is None or organization is None:
            return queryset.none()
        if organization.tenant_id != tenant.id:
            return queryset.none()
        return queryset.filter(tenant_id=tenant.id, organization_id=organization.id)

    def build_workflow_request(self, validated_data):
        return DocumentCreationRequest(
            organization_id=validated_data["organization"].id,
            title=validated_data["title"],
            storage_key=validated_data["storage_key"],
            document_type=validated_data["document_type"],
            original_filename=validated_data.get("original_filename", ""),
            mime_type=validated_data.get("mime_type", ""),
            file_size=validated_data.get("file_size", 0),
            checksum=validated_data.get("checksum", ""),
            metadata=validated_data.get("metadata", {}),
        )
