"""
Patient Consent lifecycle API views.
"""

from __future__ import annotations

from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.consents.selectors import (
    get_consent,
)
from apps.patient_management.consents.workflows import (
    PatientConsentGrantWorkflow,
    PatientConsentLifecycleRequest,
    PatientConsentRestoreWorkflow,
    PatientConsentRevokeWorkflow,
)


class PatientConsentGrantView(
    APIView,
):
    """
    Grant a Patient Consent through its workflow.
    """

    permission_classes = (IsAuthenticated,)

    def post(
        self,
        request,
        pk,
    ):
        """
        Execute the grant workflow.
        """
        consent = get_consent(
            tenant_id=request.user.tenant_id,
            consent_id=UUID(
                str(pk),
            ),
        )
        result = PatientConsentGrantWorkflow(
            request=PatientConsentLifecycleRequest(
                consent_id=consent.pk,
            ),
        ).run(
            actor_id=request.user.pk,
            tenant_id=consent.organization.tenant_id,
        )
        return Response(
            result.data,
            status=status.HTTP_200_OK,
        )


class PatientConsentRevokeView(
    APIView,
):
    """
    Revoke a Patient Consent through its workflow.
    """

    permission_classes = (IsAuthenticated,)

    def post(
        self,
        request,
        pk,
    ):
        """
        Execute the revoke workflow.
        """
        consent = get_consent(
            tenant_id=request.user.tenant_id,
            consent_id=UUID(
                str(pk),
            ),
        )
        result = PatientConsentRevokeWorkflow(
            request=PatientConsentLifecycleRequest(
                consent_id=consent.pk,
            ),
        ).run(
            actor_id=request.user.pk,
            tenant_id=consent.organization.tenant_id,
        )
        return Response(
            result.data,
            status=status.HTTP_200_OK,
        )


class PatientConsentRestoreView(
    APIView,
):
    """
    Restore a deleted Patient Consent through its workflow.
    """

    permission_classes = (IsAuthenticated,)

    def post(
        self,
        request,
        pk,
    ):
        """
        Execute the restore workflow.
        """
        consent = get_consent(
            tenant_id=request.user.tenant_id,
            consent_id=UUID(
                str(pk),
            ),
        )
        result = PatientConsentRestoreWorkflow(
            request=PatientConsentLifecycleRequest(
                consent_id=consent.pk,
            ),
        ).run(
            actor_id=request.user.pk,
            tenant_id=consent.organization.tenant_id,
        )
        return Response(
            result.data,
            status=status.HTTP_200_OK,
        )


__all__ = (
    "PatientConsentGrantView",
    "PatientConsentRestoreView",
    "PatientConsentRevokeView",
)
