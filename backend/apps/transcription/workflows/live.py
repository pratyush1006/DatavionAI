"""Concurrency-safe live session state transitions."""

from django.db import transaction
from django.utils import timezone

from apps.transcription.constants.live import LiveSessionStatus
from apps.transcription.models import LiveTranscriptionSession


class LiveTranscriptionWorkflow:
    @staticmethod
    @transaction.atomic
    def start(*, session_id, organization_id):
        s = LiveTranscriptionSession.objects.select_for_update().get(
            session_id=session_id, organization_id=organization_id
        )
        if s.status not in {
            LiveSessionStatus.READY,
            LiveSessionStatus.RECONNECTING,
            LiveSessionStatus.CREATED,
        }:
            raise ValueError("Live session cannot start from its current state.")
        s.status = LiveSessionStatus.RECORDING
        s.started_at = s.started_at or timezone.now()
        s.last_error = ""
        s.save(update_fields=("status", "started_at", "last_error", "updated_at"))
        return s

    @staticmethod
    @transaction.atomic
    def pause(*, session_id, organization_id):
        s = LiveTranscriptionSession.objects.select_for_update().get(
            session_id=session_id, organization_id=organization_id
        )
        if s.status != LiveSessionStatus.RECORDING:
            raise ValueError("Only recording sessions can be paused.")
        s.status = LiveSessionStatus.PAUSED
        s.save(update_fields=("status", "updated_at"))
        return s

    @staticmethod
    @transaction.atomic
    def reconnect(*, session_id, organization_id):
        s = LiveTranscriptionSession.objects.select_for_update().get(
            session_id=session_id, organization_id=organization_id
        )
        s.status = LiveSessionStatus.RECONNECTING
        s.save(update_fields=("status", "updated_at"))
        return s

    @staticmethod
    @transaction.atomic
    def complete(*, session_id, organization_id):
        s = LiveTranscriptionSession.objects.select_for_update().get(
            session_id=session_id, organization_id=organization_id
        )
        s.status = LiveSessionStatus.COMPLETED
        s.ended_at = timezone.now()
        s.save(update_fields=("status", "ended_at", "updated_at"))
        return s
