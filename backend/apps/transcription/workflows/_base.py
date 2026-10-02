"""
Base workflow for the clinical transcription bounded context.
"""

from __future__ import annotations

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult


class TranscriptionWorkflow(BaseWorkflow):
    domain = "transcription"

    def _ok(
        self,
        context: WorkflowContext,
        *,
        data,
        message: str,
        code: str,
    ) -> WorkflowResult:
        return WorkflowResult.ok(
            context=context,
            data=data,
            message=message,
            code=code,
        )
