"""
Document list and create API views.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.documents.api.serializers import (
    DocumentCreateSerializer,
    DocumentDetailSerializer,
    DocumentListSerializer,
)
from apps.documents.permissions import (
    CanCreateDocument,
    CanViewDocument,
)
from apps.documents.workflows import (
    DocumentCreationRequest,
    DocumentCreationWorkflow,
)


class DocumentListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create documents.

    Creation is handled by workflow layer.
    """

    queryset = None

    permission_classes_map = {
        "GET": (CanViewDocument,),
        "POST": (CanCreateDocument,),
    }

    list_serializer_class = DocumentListSerializer

    detail_serializer_class = DocumentDetailSerializer

    create_serializer_class = DocumentCreateSerializer

    create_workflow = DocumentCreationWorkflow

    def get_queryset(
        self,
    ):
        """
        Return tenant scoped documents.
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

    def build_workflow_request(
        self,
        validated_data,
    ):
        """
        Build document creation request.
        """

        return DocumentCreationRequest(
            organization_id=(validated_data["organization"].id),
            title=(validated_data["title"]),
            storage_key=(validated_data["storage_key"]),
            document_type=(validated_data["document_type"]),
            original_filename=(
                validated_data.get(
                    "original_filename",
                    "",
                )
            ),
            mime_type=(
                validated_data.get(
                    "mime_type",
                    "",
                )
            ),
            file_size=(
                validated_data.get(
                    "file_size",
                    0,
                )
            ),
            checksum=(
                validated_data.get(
                    "checksum",
                    "",
                )
            ),
            metadata=(
                validated_data.get(
                    "metadata",
                    {},
                )
            ),
        )


__all__ = ("DocumentListCreateAPIView",)
