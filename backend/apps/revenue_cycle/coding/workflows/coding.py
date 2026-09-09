from __future__ import annotations

"""Workflow orchestration for Revenue Cycle Coding."""

from typing import Any
from uuid import UUID

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult

from ..services import CodingService


class CodingWorkflow(BaseWorkflow):
    """Orchestrate Coding service operations."""

    def __init__(
        self,
        *,
        logger_: Any = None,
        payload: Any = None,
    ) -> None:
        """Initialize the Coding workflow."""

        super().__init__(
            logger_=logger_,
            payload=payload,
        )

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the requested Coding operation."""

        payload = self.payload or {}
        operation = payload.get("operation")
        organization = context.organization
        actor = context.actor
        tenant_id = UUID(str(payload["tenant_id"]))

        if operation == "create":
            record = CodingService.create(
                organization=organization,
                tenant_id=tenant_id,
                patient=payload["patient"],
                actor=actor,
                idempotency_key=payload["idempotency_key"],
                source_reference=payload["source_reference"],
                service_date=payload["service_date"],
                coding_type=payload["coding_type"],
                encounter_type=payload.get("encounter_type", ""),
                clinical_summary=payload.get("clinical_summary", ""),
                documentation=payload.get("documentation"),
                coding_notes=payload.get("coding_notes", ""),
            )
        elif operation == "update":
            record = CodingService.update(
                record_id=UUID(str(payload["record_id"])),
                organization=organization,
                tenant_id=tenant_id,
                actor=actor,
                **payload.get("changes", {}),
            )
        elif operation == "transition":
            record = CodingService.transition(
                record_id=UUID(str(payload["record_id"])),
                organization=organization,
                tenant_id=tenant_id,
                actor=actor,
                target_status=payload["target_status"],
                note=payload.get("note", ""),
            )
        elif operation == "add_code":
            record = CodingService.add_code(
                record_id=UUID(str(payload["record_id"])),
                organization=organization,
                tenant_id=tenant_id,
                actor=actor,
                code_system=payload["code_system"],
                code=payload["code"],
                description=payload.get("description", ""),
                sequence=payload.get("sequence", 1),
                is_primary=payload.get("is_primary", False),
                present_on_admission=payload.get(
                    "present_on_admission",
                ),
                evidence=payload.get("evidence"),
            )
        elif operation == "delete":
            record = CodingService.delete(
                record_id=UUID(str(payload["record_id"])),
                organization=organization,
                tenant_id=tenant_id,
                actor=actor,
            )
        elif operation == "restore":
            record = CodingService.restore(
                record_id=UUID(str(payload["record_id"])),
                organization=organization,
                tenant_id=tenant_id,
                actor=actor,
            )
        else:
            return WorkflowResult.fail(
                message="Unsupported Coding workflow operation.",
            )

        return WorkflowResult.ok(data=record)


__all__ = ("CodingWorkflow",)
