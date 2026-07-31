"""
Document retrieve, update and destroy API views.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.documents.api.serializers import (
    DocumentDetailSerializer,
    DocumentUpdateSerializer,
)
from apps.documents.permissions import (
    CanDeleteDocument,
    CanUpdateDocument,
    CanViewDocument,
)
from apps.documents.workflows import (
    DocumentDeletionRequest,
    DocumentDeletionWorkflow,
    DocumentUpdateRequest,
    DocumentUpdateWorkflow,
)


class DocumentRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete documents.
    """

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

    lookup_field = "uuid"

    def get_queryset(
        self,
    ):
        """
        Tenant scoped documents.
        """

        from apps.documents.models import (
            Document,
        )

        queryset = Document.objects.select_related(
            "organization",
            "tenant",
        )

        if self.current_tenant:
            queryset = queryset.filter(
                tenant=self.current_tenant,
            )

        return queryset

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ):
        """
        Build document update request.
        """

        return DocumentUpdateRequest(
            document_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ):
        """
        Build document delete request.
        """

        return DocumentDeletionRequest(
            document_id=instance.id,
        )


__all__ = ("DocumentRetrieveUpdateDestroyAPIView",)
