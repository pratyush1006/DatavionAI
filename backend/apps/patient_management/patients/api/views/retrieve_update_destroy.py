"""
Patient API views for retrieving, updating, and deleting patients.

GET
---
Selector driven.

PUT/PATCH
---------
Workflow driven.

DELETE
------
Workflow driven.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.patient_management.patients.api.serializers import (
    PatientDetailSerializer,
    PatientUpdateSerializer,
)
from apps.patient_management.patients.permissions import (
    CanDeletePatient,
    CanUpdatePatient,
    CanViewPatient,
)
from apps.patient_management.patients.selectors import (
    PatientSelector,
)
from apps.patient_management.patients.workflows import (
    PatientDeletionRequest,
    PatientDeletionWorkflow,
    PatientUpdateRequest,
    PatientUpdateWorkflow,
)

PATIENT_TAG: Final[tuple[str, ...]] = ("Patients",)


@extend_schema(
    tags=PATIENT_TAG,
)
class PatientRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a Patient.

    GET:
        Selector driven.

    PUT/PATCH:
        PatientUpdateWorkflow.

    DELETE:
        PatientDeletionWorkflow.
    """

    lookup_url_kwarg = "patient_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPatient,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdatePatient,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdatePatient,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeletePatient,
        ),
    }

    serializer_classes = {
        "GET": PatientDetailSerializer,
        "PUT": PatientUpdateSerializer,
        "PATCH": PatientUpdateSerializer,
    }

    detail_serializer_class = PatientDetailSerializer

    update_workflow = PatientUpdateWorkflow

    delete_workflow = PatientDeletionWorkflow

    update_success_message = "Patient updated successfully."

    delete_success_message = "Patient deleted successfully."

    def get_object(self):
        """
        Return the tenant/organization-scoped Patient.
        """

        organization = getattr(
            self.request,
            "organization",
            None,
        )

        tenant = getattr(
            self.request,
            "tenant",
            None,
        )

        tenant_id = getattr(
            tenant,
            "id",
            None,
        )

        return PatientSelector.get(
            patient_id=self.kwargs[self.lookup_url_kwarg],
            organization=organization,
            tenant_id=tenant_id,
        )

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ) -> PatientUpdateRequest:
        """
        Build Patient update workflow request.
        """

        return PatientUpdateRequest(
            patient_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ) -> PatientDeletionRequest:
        """
        Build Patient deletion workflow request.
        """

        return PatientDeletionRequest(
            patient_id=instance.id,
        )


__all__ = ("PatientRetrieveUpdateDestroyAPIView",)
