"""Permission-enforced document upload and download endpoints."""

from __future__ import annotations

from uuid import uuid4

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.documents.api.serializers import DocumentDetailSerializer
from apps.documents.constants import DEFAULT_ACCESS_LEVEL, DEFAULT_DOCUMENT_TYPE
from apps.documents.models import Document
from apps.documents.permissions import CanDownloadDocument, CanUploadDocument
from apps.documents.services.document import create_document
from apps.documents.services.media import delete_uploaded_media, media_url, upload_media


class DocumentUploadAPIView(APIView):
    """Create a document from a multipart upload; storage keys are server-owned."""

    permission_classes = (CanUploadDocument,)
    parser_classes = (MultiPartParser, FormParser)

    @property
    def current_tenant(self):
        return getattr(self.request, "tenant", None)

    @property
    def current_organization(self):
        return getattr(self.request, "organization", None)

    def post(self, request):
        tenant, organization = self.current_tenant, self.current_organization
        uploaded = request.FILES.get("file")
        if (
            tenant is None
            or organization is None
            or organization.tenant_id != tenant.id
        ):
            return Response(
                {"detail": "Active organization context is required."}, status=400
            )
        if uploaded is None:
            return Response({"detail": "A document file is required."}, status=400)

        document_id = uuid4()
        try:
            descriptor = upload_media(
                content=uploaded.read(),
                filename=uploaded.name,
                mime_type=uploaded.content_type or "application/octet-stream",
                tenant_id=tenant.id,
                organization_id=organization.id,
                document_id=document_id,
                version_number=1,
            )
        except DjangoValidationError as exc:
            return Response({"detail": str(exc)}, status=400)

        try:
            with transaction.atomic():
                document = create_document(
                    tenant_id=tenant.id,
                    organization_id=organization.id,
                    title=str(request.data.get("title") or uploaded.name).strip(),
                    storage_key=descriptor.storage_key,
                    document_type=str(
                        request.data.get("document_type") or DEFAULT_DOCUMENT_TYPE
                    ),
                    original_filename=descriptor.original_filename,
                    mime_type=descriptor.mime_type,
                    file_size=descriptor.file_size,
                    checksum=descriptor.checksum,
                )
                document.access_level = str(
                    request.data.get("access_level") or DEFAULT_ACCESS_LEVEL
                ).lower()
                document.full_clean()
                document.save(update_fields=("access_level", "updated_at"))
        except Exception:
            delete_uploaded_media(storage_key=descriptor.storage_key)
            raise
        return Response(
            DocumentDetailSerializer(document).data, status=status.HTTP_201_CREATED
        )


class DocumentDownloadAPIView(APIView):
    permission_classes = (CanDownloadDocument,)

    @property
    def current_tenant(self):
        return getattr(self.request, "tenant", None)

    @property
    def current_organization(self):
        return getattr(self.request, "organization", None)

    def get(self, request, uuid):
        document = Document.objects.filter(
            id=uuid,
            tenant=self.current_tenant,
            organization=self.current_organization,
            status="active",
        ).first()
        if document is None:
            return Response({"detail": "Document was not found."}, status=404)
        return Response(
            {
                "url": media_url(storage_key=document.storage_key),
                "filename": document.original_filename,
                "mime_type": document.mime_type,
            }
        )
