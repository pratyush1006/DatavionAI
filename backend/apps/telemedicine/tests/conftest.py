import pytest


@pytest.fixture
def session(db, organization, patient, provider):
    from datetime import timedelta

    from django.utils import timezone

    from apps.telemedicine.models import TelemedicineSession

    return TelemedicineSession.objects.create(
        organization=organization,
        patient=patient,
        provider=provider,
        scheduled_start=timezone.now() + timedelta(hours=1),
        scheduled_end=timezone.now() + timedelta(hours=2),
    )
