"""Application service for Geography live tracking."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.platform.geography.models.tracking import (
    LocationUpdate,
    TrackingParticipant,
    TrackingSession,
)
from apps.platform.geography.policies.tracking import validate_tracking_sample


class TrackingService:
    """Manage authenticated tracking sessions and persisted GPS samples."""

    @staticmethod
    def _participant(
        session_id: UUID | str, user_id: UUID | str
    ) -> TrackingParticipant:
        participant = (
            TrackingParticipant.objects.select_related("session")
            .filter(session_id=session_id, user_id=user_id, is_active=True)
            .first()
        )
        if participant is None:
            raise PermissionError(
                "User is not an active participant in this tracking session."
            )
        return participant

    @classmethod
    @transaction.atomic
    def start_session(
        cls,
        *,
        tenant_id: UUID,
        user_id: UUID,
        subject_type: str,
        subject_id: str,
        organization_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TrackingSession:
        """Create an active session and make the creator its owner."""
        subject_type = subject_type.strip().lower()
        subject_id = subject_id.strip()
        if not subject_type or not subject_id:
            raise ValueError("subject_type and subject_id are required.")

        session = TrackingSession.objects.create(
            tenant_id=tenant_id,
            organization_id=organization_id,
            subject_type=subject_type,
            subject_id=subject_id,
            created_by_id=user_id,
            metadata=metadata or {},
        )
        TrackingParticipant.objects.create(
            session=session,
            user_id=user_id,
            role=TrackingParticipant.Role.OWNER,
        )
        return session

    @classmethod
    @transaction.atomic
    def add_participant(
        cls,
        *,
        session_id: UUID,
        user_id: UUID,
        role: str,
    ) -> TrackingParticipant:
        """Add or reactivate an updater/viewer participant."""
        if role not in (
            TrackingParticipant.Role.UPDATER,
            TrackingParticipant.Role.VIEWER,
        ):
            raise ValueError("Only updater or viewer participants may be added.")
        session = TrackingSession.objects.select_for_update().get(pk=session_id)
        if session.status != TrackingSession.Status.ACTIVE:
            raise ValueError("Only active tracking sessions accept participants.")
        participant, _ = TrackingParticipant.objects.update_or_create(
            session=session,
            user_id=user_id,
            defaults={"role": role, "is_active": True},
        )
        return participant

    @classmethod
    @transaction.atomic
    def stop_session(cls, *, session_id: UUID, user_id: UUID) -> TrackingSession:
        """Complete an active session; only its owner may stop it."""
        participant = cls._participant(session_id, user_id)
        if participant.role != TrackingParticipant.Role.OWNER:
            raise PermissionError("Only the session owner can stop a tracking session.")
        session = TrackingSession.objects.select_for_update().get(pk=session_id)
        if session.status == TrackingSession.Status.ACTIVE:
            session.status = TrackingSession.Status.COMPLETED
            session.ended_at = timezone.now()
            session.save(update_fields=("status", "ended_at"))
        return session

    @classmethod
    @transaction.atomic
    def record_location(
        cls,
        *,
        session_id: UUID | str,
        user_id: UUID | str,
        latitude: float | str,
        longitude: float | str,
        accuracy_meters: float | str | None = None,
        altitude_meters: float | str | None = None,
        speed_mps: float | str | None = None,
        heading_degrees: float | str | None = None,
        recorded_at: datetime | str | None = None,
        source: str = "device",
        metadata: dict[str, Any] | None = None,
    ) -> LocationUpdate:
        """Validate, persist, sequence, and publishable-state-update a GPS sample."""
        participant = cls._participant(session_id, user_id)
        if participant.role not in (
            TrackingParticipant.Role.OWNER,
            TrackingParticipant.Role.UPDATER,
        ):
            raise PermissionError("Viewer participants cannot publish locations.")

        session = TrackingSession.objects.select_for_update().get(pk=session_id)
        if session.status != TrackingSession.Status.ACTIVE:
            raise ValueError(
                "Cannot record a location for an inactive tracking session."
            )

        lat = Decimal(str(latitude))
        lon = Decimal(str(longitude))
        if not Decimal("-90") <= lat <= Decimal("90"):
            raise ValueError("latitude must be between -90 and 90.")
        if not Decimal("-180") <= lon <= Decimal("180"):
            raise ValueError("longitude must be between -180 and 180.")

        def optional_decimal(value: float | str | None) -> Decimal | None:
            return None if value is None else Decimal(str(value))

        accuracy = optional_decimal(accuracy_meters)
        speed = optional_decimal(speed_mps)
        heading = optional_decimal(heading_degrees)
        validate_tracking_sample(
            accuracy_meters=float(accuracy) if accuracy is not None else None,
            speed_mps=float(speed) if speed is not None else None,
            heading_degrees=float(heading) if heading is not None else None,
        )

        altitude = optional_decimal(altitude_meters)
        if recorded_at is None:
            recorded = timezone.now()
        elif isinstance(recorded_at, datetime):
            recorded = recorded_at
            if timezone.is_naive(recorded):
                recorded = timezone.make_aware(
                    recorded, timezone.get_current_timezone()
                )
        else:
            recorded = datetime.fromisoformat(str(recorded_at).replace("Z", "+00:00"))
            if timezone.is_naive(recorded):
                recorded = timezone.make_aware(
                    recorded, timezone.get_current_timezone()
                )

        last = (
            LocationUpdate.objects.filter(session=session)
            .order_by("-sequence")
            .values_list("sequence", flat=True)
            .first()
        )
        sequence = int(last or 0) + 1
        update = LocationUpdate.objects.create(
            session=session,
            sequence=sequence,
            latitude=lat,
            longitude=lon,
            accuracy_meters=accuracy,
            altitude_meters=altitude,
            speed_mps=speed,
            heading_degrees=heading,
            recorded_at=recorded,
            source=(source or "device")[:32],
            metadata=metadata or {},
        )
        session.last_seen_at = timezone.now()
        session.last_latitude = lat
        session.last_longitude = lon
        session.last_accuracy_meters = accuracy
        session.save(
            update_fields=(
                "last_seen_at",
                "last_latitude",
                "last_longitude",
                "last_accuracy_meters",
            )
        )
        return update

    @staticmethod
    def serialize_update(update: LocationUpdate) -> dict[str, Any]:
        """Return a JSON-safe tracking update payload."""
        return {
            "id": str(update.id),
            "session_id": str(update.session_id),
            "sequence": update.sequence,
            "latitude": float(update.latitude),
            "longitude": float(update.longitude),
            "accuracy_meters": (
                float(update.accuracy_meters)
                if update.accuracy_meters is not None
                else None
            ),
            "altitude_meters": (
                float(update.altitude_meters)
                if update.altitude_meters is not None
                else None
            ),
            "speed_mps": (
                float(update.speed_mps) if update.speed_mps is not None else None
            ),
            "heading_degrees": (
                float(update.heading_degrees)
                if update.heading_degrees is not None
                else None
            ),
            "recorded_at": update.recorded_at.isoformat(),
            "received_at": update.received_at.isoformat(),
            "source": update.source,
            "metadata": update.metadata,
        }


__all__ = ("TrackingService",)
