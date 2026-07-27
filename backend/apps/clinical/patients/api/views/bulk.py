"""
Bulk patient operations API view.
"""

from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.patients.api.serializers import (
    PatientCreateSerializer,
    PatientDetailSerializer,
    PatientUpdateSerializer,
)
from apps.clinical.patients.models import Patient
from apps.clinical.patients.selectors import PatientSelector
from apps.clinical.patients.services import PatientService
from apps.common.api.responses import success_response
from apps.common.permissions import IsAuthenticatedAndActive


class PatientBulkCreateAPIView(APIView):
    """
    Bulk create patients.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = PatientCreateSerializer

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple patients.
        """

        serializer = self.serializer_class(
            data=request.data,
            many=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        patients = PatientService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = PatientDetailSerializer(
            patients,
            many=True,
        )

        return success_response(
            message="Patients created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class PatientBulkUpdateAPIView(APIView):
    """
    Bulk update patients.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    serializer_class = PatientUpdateSerializer

    def patch(
        self,
        request: Request,
    ) -> Response:
        """
        Update multiple patients.
        """

        if not isinstance(request.data, list):
            return Response(
                {"detail": "Expected a list of patient updates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_patients: list[Patient] = []
        errors: list[dict[str, Any]] = []

        for item in request.data:
            patient_id = item.get("id")

            if patient_id is None:
                errors.append(
                    {
                        "id": item.get("id"),
                        "error": "Missing 'id' field.",
                    }
                )
                continue

            try:
                patient = PatientSelector.get(
                    patient_id=patient_id,
                )
            except Exception:
                errors.append(
                    {
                        "id": patient_id,
                        "error": "Patient not found.",
                    }
                )
                continue

            serializer = self.serializer_class(
                data=item,
                partial=True,
            )

            if not serializer.is_valid():
                errors.append(
                    {
                        "id": patient_id,
                        "error": serializer.errors,
                    }
                )
                continue

            updated_patient = PatientService.bulk_update(
                validated_data_list=[
                    (patient, serializer.validated_data),
                ],
                performed_by=request.user,
            )[0]

            updated_patients.append(updated_patient)

        response_serializer = PatientDetailSerializer(
            updated_patients,
            many=True,
        )

        return success_response(
            message="Patients updated successfully.",
            data={
                "updated": response_serializer.data,
                "errors": errors,
            },
        )


class PatientBulkDeleteAPIView(APIView):
    """
    Bulk delete patients.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def delete(
        self,
        request: Request,
    ) -> Response:
        """
        Delete multiple patients.
        """

        patient_ids = request.data.get(
            "ids",
            [],
        )

        if not patient_ids:
            return Response(
                {"detail": "No patient IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        patients = PatientSelector.queryset().filter(
            pk__in=patient_ids,
        )

        PatientService.bulk_delete(
            instances=list(patients),
            performed_by=request.user,
        )

        return success_response(
            message="Patients deleted successfully.",
            data={
                "deleted_count": len(patient_ids),
            },
        )


__all__ = [
    "PatientBulkCreateAPIView",
    "PatientBulkDeleteAPIView",
    "PatientBulkUpdateAPIView",
]
