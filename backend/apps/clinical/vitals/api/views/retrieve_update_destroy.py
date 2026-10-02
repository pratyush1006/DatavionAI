"""
API views for retrieving, updating, and deleting vitals.
"""

from __future__ import annotations

from typing import Final
from uuid import uuid4

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.clinical.vitals.api.serializers import (
    VitalDetailSerializer,
    VitalUpdateSerializer,
)
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.permissions import (
    CanDeleteVital,
    CanUpdateVital,
    CanViewVital,
)
from apps.clinical.vitals.selectors import (
    get_vital_by_id,
)
from apps.clinical.vitals.services import (
    delete_vital,
    update_vital,
)
from apps.clinical.vitals.workflows import (
    VitalDeletionRequest,
    VitalDeletionWorkflow,
    VitalUpdateRequest,
    VitalUpdateWorkflow,
)
from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.core.workflows import WorkflowContext

VITAL_TAG: Final[tuple[str, ...]] = ("Vitals",)


@extend_schema(tags=VITAL_TAG)
class VitalRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a vital record.
    """

    lookup_url_kwarg = "vital_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewVital,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateVital,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateVital,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteVital,
        ),
    }

    serializer_classes = {
        "GET": VitalDetailSerializer,
        "PUT": VitalUpdateSerializer,
        "PATCH": VitalUpdateSerializer,
    }

    detail_serializer_class = VitalDetailSerializer

    update_service = update_vital

    delete_service = delete_vital

    def get_object(
        self,
    ) -> Vital:
        """
        Return the requested vital.
        """

        return get_vital_by_id(
            vital_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "VitalRetrieveUpdateDestroyAPIView",
]


def _vital_detail_workflow_context(self):
    user = self.request.user
    instance = self.get_object()
    tenant_id = getattr(user, "tenant_id", None) or instance.organization.tenant_id
    if tenant_id is None:
        raise RuntimeError("Tenant context is required.")
    return WorkflowContext(
        tenant_id=tenant_id,
        actor_id=user.id,
        correlation_id=str(uuid4()),
        request_id=str(uuid4()),
        workflow_name="vital.update",
    )


VitalRetrieveUpdateDestroyAPIView.get_workflow_context = _vital_detail_workflow_context


def _vital_build_update_workflow_request(self, instance, validated_data):
    return VitalUpdateRequest(vital_id=instance.id, data=dict(validated_data))


def _vital_build_delete_workflow_request(self, instance):
    return VitalDeletionRequest(vital_id=instance.id)


VitalRetrieveUpdateDestroyAPIView.build_update_workflow_request = (
    _vital_build_update_workflow_request
)
VitalRetrieveUpdateDestroyAPIView.build_delete_workflow_request = (
    _vital_build_delete_workflow_request
)
VitalRetrieveUpdateDestroyAPIView.update_workflow = VitalUpdateWorkflow
VitalRetrieveUpdateDestroyAPIView.delete_workflow = VitalDeletionWorkflow
