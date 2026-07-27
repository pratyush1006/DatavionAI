"""
Celery tasks for transcription pipelines.
"""

from __future__ import annotations

from celery import shared_task

from apps.transcription.models import TranscriptionJob
from apps.transcription.services import TranscriptionService


@shared_task(
    queue="transcription",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    max_retries=3,
)
def process_transcription(
    self,
    job_id: str,
) -> str:
    """
    Transcribe an audio job and generate a structured note draft.
    """

    job = TranscriptionJob.objects.get(pk=job_id)
    TranscriptionService.transcribe(job=job)

    if job.status == "completed":
        TranscriptionService.generate_note(job=job)

    return job.status


__all__ = [
    "process_transcription",
]
