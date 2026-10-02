"""
Business policies for transcription jobs.
"""

from __future__ import annotations

from apps.transcription.constants import TranscriptionStatus
from apps.transcription.rbac import has_permission


class TranscriptionJobPolicy:
    @staticmethod
    def can_view(*, actor, job) -> bool:
        return bool(
            actor
            and actor.is_authenticated
            and job.organization_id == getattr(actor, "organization_id", None)
            and has_permission(
                user=actor,
                organization=job.organization,
                permission="transcription.view",
            )
        )

    @staticmethod
    def can_run(*, actor, job) -> bool:
        return (
            TranscriptionJobPolicy.can_view(actor=actor, job=job)
            and has_permission(
                user=actor,
                organization=job.organization,
                permission="transcription.run",
            )
            and job.status
            in {
                TranscriptionStatus.CREATED,
                TranscriptionStatus.QUEUED,
            }
        )

    @staticmethod
    def can_cancel(*, actor, job) -> bool:
        return (
            TranscriptionJobPolicy.can_view(actor=actor, job=job)
            and has_permission(
                user=actor,
                organization=job.organization,
                permission="transcription.cancel",
            )
            and job.status
            in {
                TranscriptionStatus.CREATED,
                TranscriptionStatus.QUEUED,
                TranscriptionStatus.PROCESSING,
            }
        )
