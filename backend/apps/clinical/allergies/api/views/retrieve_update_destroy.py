"""
API views for retrieving, updating, and deleting allergies.
"""

from __future__ import annotations

from typing import Final
from uuid import uuid4

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.allergies.api.serializers import (
    AllergyDetailSerializer,
    AllergyUpdateSerializer,
)
from apps.clinical.allergies.models import Allergy
from apps.clinical.allergies.permissions import (
    CanDeleteAllergy,
    CanUpdateAllergy,
    CanViewAllergy,
)
from apps.clinical.allergies.selectors import (
    get_allergy_by_id,
)
from apps.clinical.allergies.services import (
    delete_allergy,
    update_allergy,
)
from apps.clinical.allergies.workflows import (
    AllergyDeletionRequest,
    AllergyDeletionWorkflow,
    AllergyUpdateRequest,
    AllergyUpdateWorkflow,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.core.workflows import WorkflowContext

ALLERGY_TAG: Final[tuple[str, ...]] = ("Allergies",)


@extend_schema(tags=ALLERGY_TAG)
class AllergyRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an allergy.
    """

    lookup_url_kwarg = "allergy_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewAllergy,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateAllergy,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateAllergy,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteAllergy,
        ),
    }

    serializer_classes = {
        "GET": AllergyDetailSerializer,
        "PUT": AllergyUpdateSerializer,
        "PATCH": AllergyUpdateSerializer,
    }

    detail_serializer_class = AllergyDetailSerializer

    update_service = update_allergy

    delete_service = delete_allergy

    def get_object(
        self,
    ) -> Allergy:
        """
        Return the requested allergy.
        """

        return get_allergy_by_id(
            allergy_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "AllergyRetrieveUpdateDestroyAPIView",
]


def _allergy_detail_workflow_context(self):
    user = self.request.user
    tenant = self.current_tenant
    organization = self.current_organization
    if organization is None:
        instance = self.get_object()
        organization = getattr(instance, "organization", None)
    if tenant is None and organization is not None:
        tenant = organization.tenant
    if tenant is None:
        raise RuntimeError("Tenant context is required.")
    return WorkflowContext(
        tenant_id=tenant.id,
        actor_id=user.id,
        correlation_id=str(uuid4()),
        request_id=str(uuid4()),
        workflow_name="allergy.update",
    )


AllergyRetrieveUpdateDestroyAPIView.get_workflow_context = (
    _allergy_detail_workflow_context
)


def _allergy_build_update_workflow_request(self, instance, validated_data):
    return AllergyUpdateRequest(
        organization_id=instance.organization_id,
        allergy_id=instance.id,
        data=dict(validated_data),
    )


def _allergy_build_delete_workflow_request(self, instance):
    return AllergyDeletionRequest(
        organization_id=instance.organization_id, allergy_id=instance.id
    )


AllergyRetrieveUpdateDestroyAPIView.build_update_workflow_request = (
    _allergy_build_update_workflow_request
)
AllergyRetrieveUpdateDestroyAPIView.build_delete_workflow_request = (
    _allergy_build_delete_workflow_request
)
AllergyRetrieveUpdateDestroyAPIView.update_workflow = AllergyUpdateWorkflow
AllergyRetrieveUpdateDestroyAPIView.delete_workflow = AllergyDeletionWorkflow
