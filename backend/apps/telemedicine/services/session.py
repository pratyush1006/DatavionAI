from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.telemedicine.constants import SessionStatus
from apps.telemedicine.integrations.video_provider import get_video_provider
from apps.telemedicine.models import TelemedicineSession

ALLOWED_TRANSITIONS = {
    SessionStatus.DRAFT: {
        SessionStatus.SCHEDULED,
        SessionStatus.CANCELLED,
        SessionStatus.FAILED,
    },
    SessionStatus.SCHEDULED: {
        SessionStatus.CONFIRMED,
        SessionStatus.CANCELLED,
        SessionStatus.NO_SHOW,
        SessionStatus.FAILED,
    },
    SessionStatus.CONFIRMED: {
        SessionStatus.READY,
        SessionStatus.CANCELLED,
        SessionStatus.FAILED,
    },
    SessionStatus.READY: {
        SessionStatus.IN_PROGRESS,
        SessionStatus.CANCELLED,
        SessionStatus.NO_SHOW,
        SessionStatus.FAILED,
    },
    SessionStatus.IN_PROGRESS: {
        SessionStatus.COMPLETED,
        SessionStatus.CANCELLED,
        SessionStatus.FAILED,
    },
    SessionStatus.COMPLETED: set(),
    SessionStatus.CANCELLED: set(),
    SessionStatus.NO_SHOW: set(),
    SessionStatus.FAILED: set(),
}


class SessionService:
    @staticmethod
    @transaction.atomic
    def create(*, validated_data):
        s = TelemedicineSession(**validated_data)
        s.full_clean()
        s.save()
        return s

    @staticmethod
    @transaction.atomic
    def update(*, session, validated_data):
        if session.status not in {
            SessionStatus.DRAFT,
            SessionStatus.SCHEDULED,
            SessionStatus.CONFIRMED,
        }:
            raise ValueError(
                "Only draft, scheduled, or confirmed sessions can be edited."
            )
        for f, v in validated_data.items():
            setattr(session, f, v)
        session.full_clean()
        session.save()
        return session

    @staticmethod
    @transaction.atomic
    def transition(
        *,
        session_id,
        target_status,
        organization_id,
        cancellation_reason="",
        failure_reason="",
    ):
        s = TelemedicineSession.objects.select_for_update().get(
            session_id=session_id, organization_id=organization_id
        )
        allowed = ALLOWED_TRANSITIONS[s.status]
        if target_status not in allowed:
            raise ValueError(
                f"Invalid Telemedicine transition: {s.status} -> {target_status}."
            )
        now = timezone.now()
        s.status = target_status
        if target_status == SessionStatus.IN_PROGRESS:
            s.actual_start = now
        if target_status == SessionStatus.COMPLETED:
            s.actual_start = s.actual_start or now
            s.actual_end = now
        if target_status == SessionStatus.CANCELLED:
            s.cancellation_reason = cancellation_reason.strip()
        if target_status == SessionStatus.FAILED:
            s.failure_reason = failure_reason.strip()
        s.save(
            update_fields=[
                "status",
                "actual_start",
                "actual_end",
                "cancellation_reason",
                "failure_reason",
                "updated_at",
            ]
        )
        return s

    @staticmethod
    @transaction.atomic
    def prepare(*, session_id, organization_id):
        s = TelemedicineSession.objects.select_for_update().get(
            session_id=session_id, organization_id=organization_id
        )
        if s.status != SessionStatus.CONFIRMED:
            raise ValueError("Only confirmed sessions can be prepared.")
        room = get_video_provider().create_room(
            session_id=str(s.session_id), session_type=s.session_type
        )
        s.connection_id = room.connection_id
        s.connection_url = room.connection_url
        s.provider_name = room.provider_name
        s.status = SessionStatus.READY
        s.save(
            update_fields=[
                "connection_id",
                "connection_url",
                "provider_name",
                "status",
                "updated_at",
            ]
        )
        return s
