"""
Workflow for creating a transcription job.
"""

from __future__ import annotations

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows._base import TranscriptionWorkflow


class TranscriptionJobCreateWorkflow(TranscriptionWorkflow):
    workflow_name = "transcription.job.create"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        job = TranscriptionService.create_job(**payload)
        return self._ok(
            context,
            data=job,
            message="Transcription job created.",
            code="transcription_job_created",
        )
