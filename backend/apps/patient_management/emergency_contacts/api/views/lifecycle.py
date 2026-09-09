"""
Patient Emergency Contact lifecycle API.

Lifecycle mutations are executed only through dedicated workflows.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.patient_management.emergency_contacts.api.serializers import (
    EmergencyContactDetailSerializer,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.permissions import (
    CanActivateEmergencyContact,
    CanBlockEmergencyContact,
    CanDeactivateEmergencyContact,
    CanSetPrimaryEmergencyContact,
    CanVerifyEmergencyContact,
)
from apps.patient_management.emergency_contacts.selectors import (
    EmergencyContactSelector,
)
from apps.patient_management.emergency_contacts.workflows import (
    EmergencyContactActivationRequest,
    EmergencyContactActivationWorkflow,
    EmergencyContactBlockRequest,
    EmergencyContactBlockWorkflow,
    EmergencyContactDeactivationRequest,
    EmergencyContactDeactivationWorkflow,
    EmergencyContactPrimaryRequest,
    EmergencyContactPrimaryWorkflow,
    EmergencyContactVerificationRequest,
    EmergencyContactVerificationWorkflow,
)

EMERGENCY_CONTACT_TAG: Final[tuple[str, ...]] = ("Patient Emergency Contacts",)


class EmergencyContactLifecycleAPIView(
    BaseGenericAPIView,
):
    """
    Shared base for Emergency Contact lifecycle endpoints.
    """

    serializer_class = EmergencyContactDetailSerializer

    lookup_url_kwarg = "emergency_contact_id"

    def _get_emergency_contact(
        self,
        emergency_contact_id,
    ) -> EmergencyContact:
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        emergency_contact = EmergencyContactSelector.get(
            organization=organization,
            emergency_contact_id=emergency_contact_id,
        )

        self.check_object_permissions(
            emergency_contact,
        )

        return emergency_contact

    def _success(
        self,
        *,
        emergency_contact: EmergencyContact,
        message: str,
    ):
        return self.success_response(
            data=self.get_serializer(
                emergency_contact,
            ).data,
            message=message,
        )


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactVerifyAPIView(
    EmergencyContactLifecycleAPIView,
):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanVerifyEmergencyContact,
        ),
    }

    def post(
        self,
        request,
        emergency_contact_id,
        *args,
        **kwargs,
    ):
        emergency_contact = self._get_emergency_contact(
            emergency_contact_id,
        )

        result = EmergencyContactVerificationWorkflow(
            request=EmergencyContactVerificationRequest(
                emergency_contact_id=emergency_contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_emergency_contact(
            emergency_contact.id,
        )

        return self._success(
            emergency_contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactActivateAPIView(
    EmergencyContactLifecycleAPIView,
):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanActivateEmergencyContact,
        ),
    }

    def post(
        self,
        request,
        emergency_contact_id,
        *args,
        **kwargs,
    ):
        emergency_contact = self._get_emergency_contact(
            emergency_contact_id,
        )

        result = EmergencyContactActivationWorkflow(
            request=EmergencyContactActivationRequest(
                emergency_contact_id=emergency_contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_emergency_contact(
            emergency_contact.id,
        )

        return self._success(
            emergency_contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactDeactivateAPIView(
    EmergencyContactLifecycleAPIView,
):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanDeactivateEmergencyContact,
        ),
    }

    def post(
        self,
        request,
        emergency_contact_id,
        *args,
        **kwargs,
    ):
        emergency_contact = self._get_emergency_contact(
            emergency_contact_id,
        )

        result = EmergencyContactDeactivationWorkflow(
            request=EmergencyContactDeactivationRequest(
                emergency_contact_id=emergency_contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_emergency_contact(
            emergency_contact.id,
        )

        return self._success(
            emergency_contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactBlockAPIView(
    EmergencyContactLifecycleAPIView,
):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanBlockEmergencyContact,
        ),
    }

    def post(
        self,
        request,
        emergency_contact_id,
        *args,
        **kwargs,
    ):
        emergency_contact = self._get_emergency_contact(
            emergency_contact_id,
        )

        result = EmergencyContactBlockWorkflow(
            request=EmergencyContactBlockRequest(
                emergency_contact_id=emergency_contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_emergency_contact(
            emergency_contact.id,
        )

        return self._success(
            emergency_contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=EMERGENCY_CONTACT_TAG,
)
class EmergencyContactSetPrimaryAPIView(
    EmergencyContactLifecycleAPIView,
):
    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanSetPrimaryEmergencyContact,
        ),
    }

    def post(
        self,
        request,
        emergency_contact_id,
        *args,
        **kwargs,
    ):
        emergency_contact = self._get_emergency_contact(
            emergency_contact_id,
        )

        result = EmergencyContactPrimaryWorkflow(
            request=EmergencyContactPrimaryRequest(
                emergency_contact_id=emergency_contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_emergency_contact(
            emergency_contact.id,
        )

        return self._success(
            emergency_contact=refreshed,
            message=result.message,
        )


__all__ = (
    "EmergencyContactActivateAPIView",
    "EmergencyContactBlockAPIView",
    "EmergencyContactDeactivateAPIView",
    "EmergencyContactSetPrimaryAPIView",
    "EmergencyContactVerifyAPIView",
)
