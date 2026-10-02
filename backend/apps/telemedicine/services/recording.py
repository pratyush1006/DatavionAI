from __future__ import annotations

import uuid

from django.db import transaction
from django.utils import timezone

from apps.core.events import publisher
from apps.telemedicine.constants import RecordingStatus, SessionStatus
from apps.telemedicine.events import RecordingFinalizedEvent, RecordingStartedEvent
from apps.telemedicine.integrations.video_provider import get_video_provider
from apps.telemedicine.models import Recording, TelemedicineSession


class RecordingService:
    @staticmethod
    @transaction.atomic
    def start(*, session_id, organization_id) -> Recording:
        session = (
            TelemedicineSession.objects.select_for_update()
            .select_related("organization")
            .get(session_id=session_id, organization_id=organization_id)
        )
        if session.status not in {SessionStatus.READY, SessionStatus.IN_PROGRESS}:
            raise ValueError(
                "Recording can only start for a ready or in-progress session."
            )
        if not session.recording_consent:
            raise ValueError(
                "Recording consent is required before recording can start."
            )
        active = Recording.objects.filter(
            session=session,
            status__in={RecordingStatus.RECORDING, RecordingStatus.FINALIZING},
        ).first()
        if active:
            return active
        recording = Recording.objects.create(
            session=session,
            recording_id=uuid.uuid4(),
            status=RecordingStatus.RECORDING,
            started_at=timezone.now(),
        )
        get_video_provider().start_recording(
            connection_id=session.connection_id,
            recording_id=str(recording.recording_id),
        )
        event = RecordingStartedEvent(
            tenant_id=session.organization.tenant_id,
            recording_id=recording.recording_id,
            session_id=session.session_id,
            organization_id=session.organization_id,
        )
        transaction.on_commit(lambda: publisher.publish(event))
        return recording

    @staticmethod
    @transaction.atomic
    def finalize(
        *,
        recording_id,
        organization_id,
        recording_url: str,
        duration_seconds: int | None = None,
        file_size_bytes: int | None = None,
        transcript_url: str = "",
    ) -> Recording:
        recording = (
            Recording.objects.select_for_update()
            .select_related("session__organization")
            .get(recording_id=recording_id, session__organization_id=organization_id)
        )
        if recording.status not in {
            RecordingStatus.RECORDING,
            RecordingStatus.FINALIZING,
        }:
            raise ValueError("Only active recordings can be finalized.")
        if not recording_url.strip():
            raise ValueError("recording_url is required when finalizing a recording.")
        recording.status = RecordingStatus.READY
        recording.recording_url = recording_url.strip()
        recording.duration_seconds = duration_seconds
        recording.file_size_bytes = file_size_bytes
        recording.transcript_url = transcript_url.strip()
        recording.finalized_at = timezone.now()
        recording.save(
            update_fields=[
                "status",
                "recording_url",
                "duration_seconds",
                "file_size_bytes",
                "transcript_url",
                "finalized_at",
                "updated_at",
            ]
        )
        get_video_provider().stop_recording(
            connection_id=recording.session.connection_id,
            recording_id=str(recording.recording_id),
        )
        event = RecordingFinalizedEvent(
            tenant_id=recording.session.organization.tenant_id,
            recording_id=recording.recording_id,
            session_id=recording.session_id,
            organization_id=organization_id,
        )
        transaction.on_commit(lambda: publisher.publish(event))
        return recording
