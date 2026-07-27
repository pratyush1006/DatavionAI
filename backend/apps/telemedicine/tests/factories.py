"""
Factories for Telemedicine tests.
"""

from __future__ import annotations

from datetime import (
    datetime,
    timedelta,
)

import factory

from apps.clinical.patients.tests.factories import PatientFactory
from apps.clinical.providers.constants import ProviderType
from apps.clinical.providers.models import Provider
from apps.platform.organizations.tests.factories import OrganizationFactory
from apps.telemedicine.constants import (
    SessionStatus,
    SessionType,
)
from apps.telemedicine.models import (
    Participant,
    Recording,
    TelemedicineSession,
)


class TelemedicineSessionFactory(factory.django.DjangoModelFactory):
    """
    Factory for TelemedicineSession model.
    """

    class Meta:
        model = TelemedicineSession

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    provider = factory.SubFactory(
        "apps.telemedicine.tests.factories.ProviderFactory",
    )

    appointment = None

    session_id = factory.Sequence(
        lambda n: f"session-{n:08d}",
    )

    scheduled_start = factory.LazyFunction(
        lambda: datetime.now() + timedelta(days=1),
    )

    scheduled_end = factory.LazyFunction(
        lambda: datetime.now() + timedelta(days=1, hours=1),
    )

    actual_start = None

    actual_end = None

    status = SessionStatus.SCHEDULED

    session_type = SessionType.VIDEO

    connection_url = factory.LazyFunction(
        lambda: "https://telemedicine.example.com/room/test-session",
    )

    connection_id = ""

    recording_url = ""

    recording_consent = False

    notes = ""


class RecordingFactory(factory.django.DjangoModelFactory):
    """
    Factory for Recording model.
    """

    class Meta:
        model = Recording

    session = factory.SubFactory(
        TelemedicineSessionFactory,
    )

    recording_url = factory.LazyFunction(
        lambda: "https://storage.example.com/recordings/test.mp4",
    )

    duration_seconds = 1800

    file_size_bytes = 52428800

    transcript_url = ""

    transcript_text = ""

    is_processed = False


class ParticipantFactory(factory.django.DjangoModelFactory):
    """
    Factory for Participant model.
    """

    class Meta:
        model = Participant

    session = factory.SubFactory(
        TelemedicineSessionFactory,
    )

    user = factory.SubFactory(
        "apps.platform.accounts.tests.factories.UserFactory",
    )

    participant_type = "patient"

    joined_at = None

    left_at = None

    is_present = False

    connection_quality = ""


class ProviderFactory(factory.django.DjangoModelFactory):
    """
    Factory for Provider model.
    """

    class Meta:
        model = Provider
        django_get_or_create = ("provider_number",)

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    employee = factory.SubFactory(
        "apps.notes.tests.factories.EmployeeFactory",
        organization=factory.SelfAttribute("..organization"),
    )

    provider_number = factory.Sequence(
        lambda n: f"PRV{n:06d}",
    )

    license_number = factory.Sequence(
        lambda n: f"LIC{n:06d}",
    )

    provider_type = ProviderType.PHYSICIAN


__all__ = [
    "ParticipantFactory",
    "ProviderFactory",
    "RecordingFactory",
    "TelemedicineSessionFactory",
]
