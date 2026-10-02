"""
Workflow for signing a reviewed clinical note.
"""

from __future__ import annotations

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.transcription.services import TranscriptionService
from apps.transcription.workflows._base import TranscriptionWorkflow


class ClinicalNoteSignWorkflow(TranscriptionWorkflow):
    workflow_name = "transcription.note.sign"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        note = TranscriptionService.sign_note(**payload)
        return self._ok(
            context,
            data=note,
            message="Clinical note signed.",
            code="transcription_note_signed",
        )
