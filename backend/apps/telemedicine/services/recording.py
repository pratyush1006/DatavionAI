"""
Telemedicine recording service.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.platform.accounts.models import User
from apps.telemedicine.models import Recording


class RecordingService:
    """
    Application service responsible for telemedicine recording operations.

    This service is the single entry point for all recording lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Automatic transcription
    - Storage optimization
    - Compliance checks
    - Domain events
    - Notifications
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Recording:
        """
        Create a new recording.
        """

        recording = Recording(
            **validated_data,
        )

        recording.full_clean()

        recording.save()

        return recording

    @staticmethod
    @transaction.atomic
    def process(
        *,
        instance: Recording,
        performed_by: User | None = None,
    ) -> Recording:
        """
        Mark a recording as processed.
        """

        instance.is_processed = True

        instance.save(
            update_fields=[
                "is_processed",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[Recording]:
        """
        Create multiple recordings.
        """

        recordings: list[Recording] = []

        for validated_data in validated_data_list:
            recording = Recording(
                **validated_data,
            )

            recording.full_clean()

            recording.save()

            recordings.append(recording)

        return recordings


create_recording = RecordingService.create
process_recording = RecordingService.process


__all__ = [
    "RecordingService",
    "create_recording",
    "process_recording",
]
