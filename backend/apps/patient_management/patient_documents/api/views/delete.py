"""
Delete Patient Document API.
"""

from __future__ import annotations

from rest_framework import status

from apps.common.api import BaseAPIView
from apps.common.api.responses import success_response
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.permissions import (
    PatientDocumentPermission,
)
from apps.patient_management.patient_documents.services import (
    delete_patient_document,
)


class PatientDocumentDeleteAPIView(
    BaseAPIView,
):
    """
    API for deleting a patient document.
    """

    permission_required = (PatientDocumentPermission.DELETE,)

    queryset = PatientDocument.objects.all()

    lookup_field = "id"

    def delete(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Soft delete a patient document.
        """

        document = self.get_object()

        delete_patient_document(
            document=document,
        )

        return success_response(
            message="Patient document deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )
