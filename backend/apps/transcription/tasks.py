"""
Asynchronous transcription task entrypoints.
"""

from __future__ import annotations

from celery import shared_task

from apps.transcription.services import TranscriptionService


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_transcription(self, job_id, organization_id):
    job = TranscriptionService.run(
        job_id=job_id,
        organization_id=organization_id,
    )
    return str(job.job_id)
