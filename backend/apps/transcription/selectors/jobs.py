"""
Tenant-scoped transcription job selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.transcription.models import TranscriptionJob


class TranscriptionJobSelector:
    @staticmethod
    def queryset(*, organization_id) -> QuerySet[TranscriptionJob]:
        return TranscriptionJob.objects.select_related(
            "organization",
            "patient",
            "encounter",
            "created_by",
        ).filter(organization_id=organization_id)

    @classmethod
    def get(cls, *, job_id, organization_id) -> TranscriptionJob:
        return cls.queryset(
            organization_id=organization_id,
        ).get(job_id=job_id)
