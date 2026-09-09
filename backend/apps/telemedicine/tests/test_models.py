from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.telemedicine.models import TelemedicineSession


@pytest.mark.django_db
def test_session_rejects_invalid_schedule(organization, patient, provider):
    session = TelemedicineSession(
        organization=organization,
        patient=patient,
        provider=provider,
        scheduled_start=timezone.now(),
        scheduled_end=timezone.now() - timedelta(minutes=1),
    )
    with pytest.raises(ValidationError):
        session.full_clean()
