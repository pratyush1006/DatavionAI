"""Live tracking persistence models for Platform Geography."""

from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone


class TrackingSession(models.Model):
    """Bounded live-location session for an opaque operational subject."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)
    organization_id = models.UUIDField(null=True, blank=True, db_index=True)
    subject_type = models.CharField(max_length=64)
    subject_id = models.CharField(max_length=128)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ACTIVE
    )
    created_by_id = models.UUIDField(db_index=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    last_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    last_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    last_accuracy_meters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "geography_tracking_sessions"
        ordering = ("-started_at",)
        indexes = (
            models.Index(
                fields=("tenant_id", "status"), name="geo_track_tenant_status"
            ),
            models.Index(
                fields=("subject_type", "subject_id"), name="geo_track_subject"
            ),
            models.Index(
                fields=("organization_id", "status"), name="geo_track_org_status"
            ),
        )


class TrackingParticipant(models.Model):
    """Authorized user for a live tracking session."""

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        UPDATER = "updater", "Updater"
        VIEWER = "viewer", "Viewer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        TrackingSession, on_delete=models.CASCADE, related_name="participants"
    )
    user_id = models.UUIDField(db_index=True)
    role = models.CharField(max_length=16, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "geography_tracking_participants"
        constraints = (
            models.UniqueConstraint(
                fields=("session", "user_id"), name="geo_track_participant_unique"
            ),
        )
        indexes = (
            models.Index(fields=("user_id", "is_active"), name="geo_track_part_user"),
        )


class LocationUpdate(models.Model):
    """Immutable location sample persisted during a live session."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        TrackingSession, on_delete=models.CASCADE, related_name="locations"
    )
    sequence = models.PositiveBigIntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accuracy_meters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    altitude_meters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    speed_mps = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )
    heading_degrees = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    recorded_at = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32, default="device")
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "geography_location_updates"
        ordering = ("-recorded_at", "-sequence")
        constraints = (
            models.UniqueConstraint(
                fields=("session", "sequence"),
                name="geo_track_location_sequence_unique",
            ),
        )
        indexes = (
            models.Index(fields=("session", "recorded_at"), name="geo_track_loc_time"),
        )


__all__ = ("TrackingSession", "TrackingParticipant", "LocationUpdate")
