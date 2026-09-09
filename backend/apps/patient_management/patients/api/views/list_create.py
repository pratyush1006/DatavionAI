"""
Patient API views for listing and creating patients.

GET
---
Selector driven.

POST
----
Workflow driven.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.patient_management.patients.api.serializers import (
    PatientCreateSerializer,
    PatientDetailSerializer,
    PatientListSerializer,
)
from apps.patient_management.patients.models import Patient
from apps.patient_management.patients.permissions import (
    CanCreatePatient,
    CanViewPatient,
)
from apps.patient_management.patients.selectors import (
    PatientSelector,
)
from apps.patient_management.patients.workflows import (
    PatientCreationRequest,
    PatientCreationWorkflow,
)

PATIENT_TAG: Final[tuple[str, ...]] = ("Patients",)


@extend_schema(
    tags=PATIENT_TAG,
)
class PatientListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List or create patients.

    GET:
        Selector driven.

    POST:
        PatientCreationWorkflow.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPatient,
        ),
        "POST": (
            IsAuthenticated,
            CanCreatePatient,
        ),
    }

    serializer_classes = {
        "GET": PatientListSerializer,
        "POST": PatientCreateSerializer,
    }

    detail_serializer_class = PatientDetailSerializer

    create_workflow = PatientCreationWorkflow

    create_success_message = "Patient created successfully."

    search_fields = (
        "mrn",
        "first_name",
        "middle_name",
        "last_name",
        "preferred_name",
        "phone",
        "email",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    ordering_fields = (
        "mrn",
        "first_name",
        "last_name",
        "date_of_birth",
        "status",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "status",
        "gender",
        "marital_status",
        "blood_group",
        "is_active",
    )

    def build_workflow_request(
        self,
        validated_data,
    ) -> PatientCreationRequest:
        """
        Build the Patient creation workflow request.
        """

        return PatientCreationRequest(
            organization_id=validated_data["organization"].id,
            mrn=validated_data["mrn"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            middle_name=validated_data.get(
                "middle_name",
                "",
            ),
            preferred_name=validated_data.get(
                "preferred_name",
                "",
            ),
            date_of_birth=validated_data.get(
                "date_of_birth",
            ),
            gender=validated_data.get(
                "gender",
            ),
            marital_status=validated_data.get(
                "marital_status",
            ),
            blood_group=validated_data.get(
                "blood_group",
            ),
            phone=validated_data.get(
                "phone",
                "",
            ),
            email=validated_data.get(
                "email",
                "",
            ),
            address=validated_data.get(
                "address",
                "",
            ),
            city=validated_data.get(
                "city",
                "",
            ),
            state=validated_data.get(
                "state",
                "",
            ),
            country=validated_data.get(
                "country",
                "",
            ),
            postal_code=validated_data.get(
                "postal_code",
                "",
            ),
        )

    def get_queryset(
        self,
    ) -> QuerySet[Patient]:
        """
        Return organization-scoped patients.
        """

        organization = getattr(
            self.request,
            "organization",
            None,
        )

        if organization is not None:
            return PatientSelector.list(
                organization=organization,
            )

        return PatientSelector.queryset()


__all__ = ("PatientListCreateAPIView",)
