"""
Recording selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.telemedicine.models import Recording


class RecordingSelector:
    """
    Read-only queries for telemedicine recordings.

    This selector centralizes all recording retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[Recording]:
        """
        Return the base recording queryset.
        """

        return Recording.objects.select_related(
            "session",
            "session__patient",
            "session__provider",
            "session__organization",
        )

    @staticmethod
    def list() -> QuerySet[Recording]:
        """
        Return all recordings.
        """

        return RecordingSelector.queryset()

    @staticmethod
    def get(
        *,
        recording_id: UUID,
    ) -> Recording:
        """
        Return a recording by identifier.
        """

        return get_object_or_404(
            RecordingSelector.queryset(),
            pk=recording_id,
        )

    @staticmethod
    def list_by_session(
        *,
        session_id: UUID,
    ) -> QuerySet[Recording]:
        """
        Return all recordings for a session.
        """

        return RecordingSelector.queryset().filter(
            session_id=session_id,
        )

    @staticmethod
    def list_processed() -> QuerySet[Recording]:
        """
        Return all processed recordings.
        """

        return RecordingSelector.queryset().filter(
            is_processed=True,
        )

    @staticmethod
    def search(
        *,
        query: str,
    ) -> QuerySet[Recording]:
        """
        Search recordings by URL or transcript text.
        """

        return RecordingSelector.queryset().filter(
            Q(
                recording_url__icontains=query,
            )
            | Q(
                transcript_text__icontains=query,
            )
        )

    @staticmethod
    def count(
        *,
        session_id: UUID | None = None,
        is_processed: bool | None = None,
    ) -> int:
        """
        Return the count of recordings matching the given filters.
        """

        queryset = RecordingSelector.queryset()

        if session_id is not None:
            queryset = queryset.filter(
                session_id=session_id,
            )

        if is_processed is not None:
            queryset = queryset.filter(
                is_processed=is_processed,
            )

        return queryset.count()


__all__ = [
    "RecordingSelector",
]
