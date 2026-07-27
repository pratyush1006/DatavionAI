"""
Update Patient Document API.
"""

from __future__ import annotations

from apps.common.api import BaseAPIView
from apps.common.api.responses import success_response
from apps.patient_management.patient_documents.api.serializers import (
    PatientDocumentUpdateSerializer,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)


class PatientDocumentUpdateAPIView(
    BaseAPIView,
):
    """
    API for updating a patient document.
    """

    permission_required = (PatientDocumentPermission.UPDATE,)

    serializer_class = PatientDocumentUpdateSerializer

    queryset = PatientDocument.objects.all()

    lookup_field = "id"

    def patch(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Update a patient document.
        """

        document = self.get_object()

        serializer = self.serializer_class(
            document,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        document = serializer.save()

        return success_response(
            data=self.serializer_class(
                document,
            ).data,
        )
