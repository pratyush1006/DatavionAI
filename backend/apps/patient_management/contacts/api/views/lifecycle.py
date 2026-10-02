"""
Patient Contact lifecycle API.

Lifecycle mutations are always executed through dedicated workflows.

Architecture
------------

POST
    API
      |
      +--> Authentication
      |
      +--> Organization-scoped Selector
      |
      +--> Object-level Permission
      |
      +--> Workflow
      |
      +--> Policy
      |
      +--> Domain Service
      |
      +--> Domain Event
"""

from __future__ import annotations

from typing import Any, Final
from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.patient_management.contacts.api.serializers import (
    ContactDetailSerializer,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.permissions import (
    CanActivateContact,
    CanDeactivateContact,
    CanSetPrimaryContact,
    CanVerifyContact,
)
from apps.patient_management.contacts.selectors import (
    ContactSelector,
)
from apps.patient_management.contacts.workflows import (
    ContactActivationRequest,
    ContactActivationWorkflow,
    ContactDeactivationRequest,
    ContactDeactivationWorkflow,
    ContactPrimaryRequest,
    ContactPrimaryWorkflow,
    ContactVerificationRequest,
    ContactVerificationWorkflow,
)

CONTACT_TAG: Final[tuple[str, ...]] = ("Patient Contacts",)


class ContactLifecycleAPIView(
    BaseGenericAPIView,
):
    """
    Common base for patient contact lifecycle endpoints.

    Responsibilities
    ----------------
    - Resolve the current organization.
    - Resolve the contact through the organization-scoped selector.
    - Enforce object-level permissions for the current lifecycle action.
    - Serialize the refreshed contact.
    - Return the standard DatavionOS response envelope.

    Business mutation logic remains inside dedicated workflows.
    """

    def _get_contact(
        self,
        contact_id: UUID,
    ) -> Contact:
        """
        Resolve a contact inside the current organization boundary.

        Object-level authorization is evaluated after the selector resolves
        the object so the lifecycle-specific permission class is applied to
        the actual Contact instance.
        """
        organization = self.current_organization

        if organization is None:
            raise RuntimeError(
                "Organization context is required.",
            )

        contact = ContactSelector.get(
            organization=organization,
            contact_id=contact_id,
        )

        self.check_object_permissions(
            contact,
        )

        return contact

    def _serialize_contact(
        self,
        contact: Contact,
    ) -> ContactDetailSerializer:
        """
        Serialize a contact using the canonical detail serializer.
        """
        return ContactDetailSerializer(
            contact,
            context={
                "request": self.request,
            },
        )

    def _success(
        self,
        *,
        contact: Contact,
        message: str,
    ) -> Response:
        """
        Return the standard successful lifecycle response.
        """
        serializer = self._serialize_contact(
            contact,
        )

        return self.success_response(
            data=serializer.data,
            message=message,
        )


@extend_schema(
    tags=CONTACT_TAG,
)
class ContactVerifyAPIView(
    ContactLifecycleAPIView,
):
    """
    Verify a patient contact.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanVerifyContact,
        ),
    }

    def post(
        self,
        request,
        contact_id: UUID,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Execute contact verification through the canonical workflow.
        """
        contact = self._get_contact(
            contact_id,
        )

        result = ContactVerificationWorkflow(
            request=ContactVerificationRequest(
                contact_id=contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_contact(
            contact.id,
        )

        return self._success(
            contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=CONTACT_TAG,
)
class ContactActivateAPIView(
    ContactLifecycleAPIView,
):
    """
    Activate a patient contact.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanActivateContact,
        ),
    }

    def post(
        self,
        request,
        contact_id: UUID,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Execute contact activation through the canonical workflow.
        """
        contact = self._get_contact(
            contact_id,
        )

        result = ContactActivationWorkflow(
            request=ContactActivationRequest(
                contact_id=contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_contact(
            contact.id,
        )

        return self._success(
            contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=CONTACT_TAG,
)
class ContactDeactivateAPIView(
    ContactLifecycleAPIView,
):
    """
    Deactivate a patient contact.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanDeactivateContact,
        ),
    }

    def post(
        self,
        request,
        contact_id: UUID,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Execute contact deactivation through the canonical workflow.
        """
        contact = self._get_contact(
            contact_id,
        )

        result = ContactDeactivationWorkflow(
            request=ContactDeactivationRequest(
                contact_id=contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_contact(
            contact.id,
        )

        return self._success(
            contact=refreshed,
            message=result.message,
        )


@extend_schema(
    tags=CONTACT_TAG,
)
class ContactSetPrimaryAPIView(
    ContactLifecycleAPIView,
):
    """
    Set a patient contact as primary.
    """

    permission_classes_map = {
        "POST": (
            IsAuthenticated,
            CanSetPrimaryContact,
        ),
    }

    def post(
        self,
        request,
        contact_id: UUID,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Execute primary-contact selection through the canonical workflow.
        """
        contact = self._get_contact(
            contact_id,
        )

        result = ContactPrimaryWorkflow(
            request=ContactPrimaryRequest(
                contact_id=contact.id,
            ),
        ).execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        refreshed = self._get_contact(
            contact.id,
        )

        return self._success(
            contact=refreshed,
            message=result.message,
        )


__all__ = (
    "ContactActivateAPIView",
    "ContactDeactivateAPIView",
    "ContactSetPrimaryAPIView",
    "ContactVerifyAPIView",
)
