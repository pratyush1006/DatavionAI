"""End-to-end live tracking persistence tests."""

from __future__ import annotations

import uuid

import pytest
from django.contrib.auth import get_user_model

from apps.platform.geography.models.tracking import TrackingParticipant
from apps.platform.geography.services.tracking import TrackingService


@pytest.mark.django_db
def test_tracking_session_lifecycle_and_location_persistence():
    user = get_user_model().objects.create_user(
        username=f"geo-{uuid.uuid4().hex[:8]}",
        email=f"geo-{uuid.uuid4().hex[:8]}@example.com",
        password="x",
    )
    s = TrackingService.start_session(
        tenant_id=uuid.uuid4(),
        user_id=user.pk,
        subject_type="ambulance",
        subject_id="AMB-001",
    )
    assert s.status == "active"
    assert TrackingParticipant.objects.filter(
        session=s, user_id=user.pk, role="owner"
    ).exists()
    u = TrackingService.record_location(
        session_id=s.id,
        user_id=user.pk,
        latitude="12.971600",
        longitude="77.594600",
        accuracy_meters=8,
    )
    assert u.sequence == 1
    assert (
        TrackingService.stop_session(session_id=s.id, user_id=user.pk).status
        == "completed"
    )
