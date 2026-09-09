"""Lifecycle API views for Patient Relationships."""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.patient_management.relationships.workflows import (
    PatientRelationshipActivationWorkflow,
    PatientRelationshipDeactivationWorkflow,
    PatientRelationshipLifecycleRequest,
    PatientRelationshipRestoreWorkflow,
    PatientRelationshipSetPrimaryWorkflow,
    PatientRelationshipTerminateWorkflow,
    PatientRelationshipVerifyWorkflow,
)

RELATIONSHIP_TAG: Final[tuple[str, ...]] = ("Patient Relationships",)


class PatientRelationshipLifecycleAPIView(BaseGenericAPIView):
    """Common API adapter for Relationship lifecycle workflows."""

    permission_classes = (IsAuthenticated,)

    def build_request(self) -> PatientRelationshipLifecycleRequest:
        relationship_id = self.kwargs.get("relationship_id")
        if relationship_id is None:
            raise ValueError("Relationship identifier is required.")
        return PatientRelationshipLifecycleRequest(
            relationship_id=relationship_id,
        )

    def execute_relationship_workflow(self, *, workflow, workflow_name: str):
        context = self.build_workflow_context(workflow_name=workflow_name)
        result = workflow(
            request=self.build_request(),
        ).execute(context=context)
        return self.handle_workflow_result(result)


@extend_schema(tags=RELATIONSHIP_TAG)
class PatientRelationshipActivateAPIView(PatientRelationshipLifecycleAPIView):
    """Activate a Patient Relationship."""

    def post(self, request, *args, **kwargs):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipActivationWorkflow,
            workflow_name="relationship.activate",
        )


@extend_schema(tags=RELATIONSHIP_TAG)
class PatientRelationshipDeactivateAPIView(PatientRelationshipLifecycleAPIView):
    """Deactivate a Patient Relationship."""

    def post(self, request, *args, **kwargs):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipDeactivationWorkflow,
            workflow_name="relationship.deactivate",
        )


@extend_schema(tags=RELATIONSHIP_TAG)
class PatientRelationshipRestoreAPIView(PatientRelationshipLifecycleAPIView):
    """Restore a deleted Patient Relationship."""

    def post(self, request, *args, **kwargs):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipRestoreWorkflow,
            workflow_name="relationship.restore",
        )


@extend_schema(tags=RELATIONSHIP_TAG)
class PatientRelationshipVerifyAPIView(PatientRelationshipLifecycleAPIView):
    """Verify a Patient Relationship."""

    def post(self, request, *args, **kwargs):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipVerifyWorkflow,
            workflow_name="relationship.verify",
        )


@extend_schema(tags=RELATIONSHIP_TAG)
class PatientRelationshipTerminateAPIView(PatientRelationshipLifecycleAPIView):
    """Terminate a Patient Relationship."""

    def post(self, request, *args, **kwargs):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipTerminateWorkflow,
            workflow_name="relationship.terminate",
        )


@extend_schema(tags=RELATIONSHIP_TAG)
class PatientRelationshipSetPrimaryAPIView(PatientRelationshipLifecycleAPIView):
    """Mark a Patient Relationship as primary."""

    def post(self, request, *args, **kwargs):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipSetPrimaryWorkflow,
            workflow_name="relationship.set_primary",
        )


__all__ = (
    "PatientRelationshipActivateAPIView",
    "PatientRelationshipDeactivateAPIView",
    "PatientRelationshipRestoreAPIView",
    "PatientRelationshipSetPrimaryAPIView",
    "PatientRelationshipTerminateAPIView",
    "PatientRelationshipVerifyAPIView",
)
