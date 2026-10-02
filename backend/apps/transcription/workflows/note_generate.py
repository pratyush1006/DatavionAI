"""
Workflow for generating a clinical note from a completed transcription.
"""

from __future__ import annotations

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows._base import TranscriptionWorkflow


class ClinicalNoteGenerateWorkflow(TranscriptionWorkflow):
    workflow_name = "transcription.note.generate"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        note = TranscriptionService.generate_note(**payload)
        return self._ok(
            context,
            data=note,
            message="Clinical note draft generated.",
            code="transcription_note_generated",
        )
