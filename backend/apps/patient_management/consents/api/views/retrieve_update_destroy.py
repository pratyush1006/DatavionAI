"""
Patient Consent retrieve/update/delete API view.
"""

from __future__ import annotations

from uuid import UUID

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.patient_management.consents.api.serializers import (
    PatientConsentDetailSerializer,
    PatientConsentUpdateSerializer,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)
from apps.patient_management.consents.selectors import (
    get_consent,
)
from apps.patient_management.consents.workflows import (
    PatientConsentDeletionRequest,
    PatientConsentDeletionWorkflow,
    PatientConsentUpdateRequest,
    PatientConsentUpdateWorkflow,
)


class PatientConsentRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView,
):
    """
    Provide retrieve, update, and delete operations for Patient Consents.
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(
        self,
    ):
        """
        Select detail or update serialization.
        """
        if self.request.method in {
            "PUT",
            "PATCH",
        }:
            return PatientConsentUpdateSerializer

        return PatientConsentDetailSerializer

    def get_object(
        self,
    ) -> PatientConsent:
        """
        Resolve a consent through the tenant-scoped selector.
        """
        return get_consent(
            tenant_id=self.request.user.tenant_id,
            consent_id=UUID(
                str(self.kwargs["pk"]),
            ),
        )

    def perform_update(
        self,
        serializer,
    ) -> None:
        """
        Update the consent through its workflow.
        """
        workflow = PatientConsentUpdateWorkflow(
            request=PatientConsentUpdateRequest(
                consent_id=self.get_object().pk,
                data=serializer.validated_data,
            ),
        )
        workflow.run(
            actor_id=self.request.user.pk,
            tenant_id=self.get_object().organization.tenant_id,
        )

    def perform_destroy(
        self,
        instance,
    ) -> None:
        """
        Delete the consent through its workflow.
        """
        workflow = PatientConsentDeletionWorkflow(
            request=PatientConsentDeletionRequest(
                consent_id=instance.pk,
            ),
        )
        workflow.run(
            actor_id=self.request.user.pk,
            tenant_id=instance.organization.tenant_id,
        )


__all__ = ("PatientConsentRetrieveUpdateDestroyView",)
