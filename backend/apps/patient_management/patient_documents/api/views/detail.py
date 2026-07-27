"""
Retrieve Patient Document API.
"""

from __future__ import annotations

from apps.common.api import BaseAPIView
from apps.common.api.responses import success_response
from apps.patient_management.patient_documents.api.serializers import (
    PatientDocumentDetailSerializer,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)


class PatientDocumentDetailAPIView(BaseAPIView):
    """
    API for retrieving a patient document.
    """

    permission_required = (PatientDocumentPermission.VIEW,)

    serializer_class = PatientDocumentDetailSerializer

    queryset = PatientDocument.objects.all()

    lookup_field = "id"

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Retrieve a patient document.
        """

        document = self.get_object()

        serializer = self.serializer_class(
            document,
        )

        return success_response(
            data=serializer.data,
        )
