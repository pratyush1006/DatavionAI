"""
Workflow for reviewing a generated clinical note.
"""

from __future__ import annotations

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows._base import TranscriptionWorkflow


class ClinicalNoteReviewWorkflow(TranscriptionWorkflow):
    workflow_name = "transcription.note.review"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        note = TranscriptionService.review_note(**payload)
        return self._ok(
            context,
            data=note,
            message="Clinical note review recorded.",
            code="transcription_note_reviewed",
        )
