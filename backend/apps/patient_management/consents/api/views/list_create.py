"""
Patient Consent list/create API view.
"""

from __future__ import annotations

from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from apps.patient_management.consents.api.filters import (
    PatientConsentFilter,
)
from apps.patient_management.consents.api.serializers import (
    PatientConsentCreateSerializer,
    PatientConsentListSerializer,
)
from apps.patient_management.consents.selectors import (
    list_organization_consents,
)
from apps.patient_management.consents.workflows import (
    PatientConsentCreationRequest,
    PatientConsentCreationWorkflow,
)


class PatientConsentListCreateView(
    generics.ListCreateAPIView,
):
    """
    Provide list and create operations for Patient Consents.
    """

    permission_classes = (IsAuthenticated,)
    filterset_class = PatientConsentFilter

    def get_serializer_class(
        self,
    ):
        """
        Select the serializer appropriate to the HTTP operation.
        """
        if self.request.method == "POST":
            return PatientConsentCreateSerializer

        return PatientConsentListSerializer

    def get_queryset(
        self,
    ):
        """
        Return organization-scoped consent records.
        """
        organization = (
            self.request.user.organization_roles.select_related(
                "organization",
            )
            .first()
            .organization
        )

        tenant_id = organization.tenant_id

        return list_organization_consents(
            tenant_id=tenant_id,
            organization_id=organization.pk,
        )

    def perform_create(
        self,
        serializer,
    ) -> None:
        """
        Create a Patient Consent through the workflow layer.
        """
        data = serializer.validated_data
        organization = data["organization"]

        workflow = PatientConsentCreationWorkflow(
            request=PatientConsentCreationRequest(
                organization_id=organization.pk,
                patient_id=data["patient"].pk,
                data=data,
            ),
        )

        try:
            workflow.run(
                actor_id=self.request.user.pk,
                tenant_id=organization.tenant_id,
            )
        except (PermissionError, ValueError) as exc:
            raise APIException(
                str(exc),
            ) from exc


__all__ = ("PatientConsentListCreateView",)
