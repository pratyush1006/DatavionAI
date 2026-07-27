"""
List Patient Documents API.
"""

from __future__ import annotations

from apps.common.api import BaseAPIView
from apps.common.api.responses import success_response
from apps.patient_management.patient_documents.api.filters import (
    PatientDocumentFilter,
)
from apps.patient_management.patient_documents.api.serializers import (
    PatientDocumentListSerializer,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)


class PatientDocumentListAPIView(BaseAPIView):
    """
    API for listing patient documents.
    """

    permission_required = (PatientDocumentPermission.LIST,)

    serializer_class = PatientDocumentListSerializer

    filterset_class = PatientDocumentFilter

    queryset = PatientDocument.objects.all()

    def get(self, request):
        """
        List patient documents.
        """

        queryset = self.filter_queryset(
            self.get_queryset(),
        )

        serializer = self.serializer_class(
            queryset,
            many=True,
        )

        return success_response(
            data=serializer.data,
        )
