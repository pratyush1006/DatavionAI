"""
Workflow for cancelling a transcription job.
"""

from __future__ import annotations

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows._base import TranscriptionWorkflow


class TranscriptionJobCancelWorkflow(TranscriptionWorkflow):
    workflow_name = "transcription.job.cancel"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        job = TranscriptionService.cancel(
            job_id=payload["job_id"],
            organization_id=payload["organization_id"],
        )
        return self._ok(
            context,
            data=job,
            message="Transcription job cancelled.",
            code="transcription_job_cancelled",
        )
