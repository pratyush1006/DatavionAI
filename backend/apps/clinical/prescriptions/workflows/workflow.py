"""Fresh workflow surface for Prescription."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
    workflow_registry,
)

from ..services import PrescriptionService


@dataclass(frozen=True, slots=True)
class PrescriptionWorkflowRequest:
    organization_id: UUID
    record_id: UUID | None = None
    data: dict[str, Any] | None = None


def _organization(request: PrescriptionWorkflowRequest, context: WorkflowContext):
    return PrescriptionService.resolve_organization(
        organization_id=request.organization_id,
        tenant_id=context.tenant_id,
    )


def _actor(context: WorkflowContext):
    return PrescriptionService.resolve_actor(actor_id=context.actor_id)


class PrescriptionCreateWorkflow(BaseWorkflow):
    workflow_name = "prescription.create"

    def __init__(self, *, request: PrescriptionWorkflowRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        obj = PrescriptionService.create(
            organization=_organization(self.request, context),
            data=self.request.data or {},
            performed_by=_actor(context),
        )
        return WorkflowResult.ok(
            context=context,
            data=obj,
            message="Prescription created.",
            code="prescription_created",
        )

    def run(self, context):
        """Execute the workflow through the platform contract."""
        execute = getattr(super(), "run", None)
        if execute is not None:
            return execute(context=context)
        execute = getattr(super(), "execute", None)
        if execute is not None:
            return execute(context=context)
        return self._run(context)


class PrescriptionUpdateWorkflow(BaseWorkflow):
    workflow_name = "prescription.update"

    def __init__(self, *, request: PrescriptionWorkflowRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        obj = PrescriptionService.update(
            organization=_organization(self.request, context),
            record_id=self.request.record_id,
            data=self.request.data or {},
            performed_by=_actor(context),
        )
        return WorkflowResult.ok(
            context=context,
            data=obj,
            message="Prescription updated.",
            code="prescription_updated",
        )

    def run(self, context):
        """Execute the workflow through the platform contract."""
        execute = getattr(super(), "run", None)
        if execute is not None:
            return execute(context=context)
        execute = getattr(super(), "execute", None)
        if execute is not None:
            return execute(context=context)
        return self._run(context)


class PrescriptionDeleteWorkflow(BaseWorkflow):
    workflow_name = "prescription.delete"

    def __init__(self, *, request: PrescriptionWorkflowRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        obj = PrescriptionService.delete(
            organization=_organization(self.request, context),
            record_id=self.request.record_id,
            performed_by=_actor(context),
        )
        return WorkflowResult.ok(
            context=context,
            data=obj,
            message="Prescription deleted.",
            code="prescription_deleted",
        )

    def run(self, context):
        """Execute the workflow through the platform contract."""
        execute = getattr(super(), "run", None)
        if execute is not None:
            return execute(context=context)
        execute = getattr(super(), "execute", None)
        if execute is not None:
            return execute(context=context)
        return self._run(context)


class PrescriptionLifecycleWorkflow(BaseWorkflow):
    workflow_name = "prescription.lifecycle"

    def __init__(self, *, request: PrescriptionWorkflowRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        payload = self.request.data or {}
        target = str(payload.get("target", "")).strip()
        if not target:
            raise ValueError("Lifecycle target is required.")
        obj = PrescriptionService.transition(
            organization=_organization(self.request, context),
            record_id=self.request.record_id,
            target=target,
            performed_by=_actor(context),
        )
        return WorkflowResult.ok(
            context=context,
            data=obj,
            message="Prescription lifecycle updated.",
            code="prescription_lifecycle",
        )

    def run(self, context):
        """Execute the workflow through the platform contract."""
        execute = getattr(super(), "run", None)
        if execute is not None:
            return execute(context=context)
        execute = getattr(super(), "execute", None)
        if execute is not None:
            return execute(context=context)
        return self._run(context)


workflow_registry.register(
    name="prescription.create", workflow=PrescriptionCreateWorkflow
)
workflow_registry.register(
    name="prescription.update", workflow=PrescriptionUpdateWorkflow
)
workflow_registry.register(
    name="prescription.delete", workflow=PrescriptionDeleteWorkflow
)
workflow_registry.register(
    name="prescription.lifecycle", workflow=PrescriptionLifecycleWorkflow
)

from .workflow import (
    PrescriptionCreateWorkflow,
    PrescriptionDeleteWorkflow,
    PrescriptionLifecycleWorkflow,
    PrescriptionUpdateWorkflow,
    PrescriptionWorkflowRequest,
)

__all__ = (
    "PrescriptionCreateWorkflow",
    "PrescriptionUpdateWorkflow",
    "PrescriptionDeleteWorkflow",
    "PrescriptionLifecycleWorkflow",
    "PrescriptionWorkflowRequest",
)
