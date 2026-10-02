"""
Canonical workflow registration for clinical transcription.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.transcription.workflows import (
    ClinicalNoteGenerateWorkflow,
    ClinicalNoteReviewWorkflow,
    ClinicalNoteSignWorkflow,
    TranscriptionJobCancelWorkflow,
    TranscriptionJobCreateWorkflow,
    TranscriptionJobQueueWorkflow,
    TranscriptionJobRunWorkflow,
)

WORKFLOW_MAP = {
    "transcription.job.create": TranscriptionJobCreateWorkflow,
    "transcription.job.queue": TranscriptionJobQueueWorkflow,
    "transcription.job.run": TranscriptionJobRunWorkflow,
    "transcription.job.cancel": TranscriptionJobCancelWorkflow,
    "transcription.note.generate": ClinicalNoteGenerateWorkflow,
    "transcription.note.review": ClinicalNoteReviewWorkflow,
    "transcription.note.sign": ClinicalNoteSignWorkflow,
}


def register_transcription_workflows() -> None:
    for name, workflow in WORKFLOW_MAP.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("WORKFLOW_MAP", "register_transcription_workflows")
