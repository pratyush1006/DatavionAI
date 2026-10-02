from __future__ import annotations

from apps.common.api.base_generics import BaseRetrieveUpdateDestroyAPIView
from apps.documents.api.serializers import (
    DocumentDetailSerializer,
    DocumentUpdateSerializer,
)
from apps.documents.permissions import (
    CanDeleteDocument,
    CanUpdateDocument,
    CanViewDocument,
)
from apps.documents.workflows import DocumentDeletionWorkflow, DocumentUpdateWorkflow


class DocumentRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    permission_classes_map = {
        "GET": (CanViewDocument,),
        "PUT": (CanUpdateDocument,),
        "PATCH": (CanUpdateDocument,),
        "DELETE": (CanDeleteDocument,),
    }
    detail_serializer_class = DocumentDetailSerializer
    update_serializer_class = DocumentUpdateSerializer
    update_workflow = DocumentUpdateWorkflow
    delete_workflow = DocumentDeletionWorkflow

    # URLs use <uuid:uuid>; Document's UUID primary key is named `id`.
    lookup_field = "id"
    lookup_url_kwarg = "uuid"

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
