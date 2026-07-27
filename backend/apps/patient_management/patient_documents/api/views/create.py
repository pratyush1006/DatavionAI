"""
Create Patient Document API.
"""

from __future__ import annotations

from rest_framework import status

from apps.common.api import BaseAPIView
from apps.common.api.responses import success_response
from apps.patient_management.patient_documents.api.serializers import (
    PatientDocumentCreateSerializer,
)
from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)


class PatientDocumentCreateAPIView(BaseAPIView):
    """
    API for creating a patient document.
    """

    permission_required = (PatientDocumentPermission.CREATE,)

    serializer_class = PatientDocumentCreateSerializer

    def post(self, request):
        """
        Create a patient document.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        document = serializer.save()

        return success_response(
            data=self.serializer_class(document).data,
            status_code=status.HTTP_201_CREATED,
        )
