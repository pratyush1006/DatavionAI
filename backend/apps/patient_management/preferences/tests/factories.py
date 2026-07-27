"""
Factories for the Patient Preferences module.
"""

from __future__ import annotations

import factory

from apps.patient_management.patients.models import (
    Patient,
)
from apps.patient_management.preferences.constants import (
    CommunicationChannel,
    PreferenceStatus,
    ReminderPreference,
    ThemePreference,
)
from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)
from apps.platform.organizations.models import (
    Organization,
)


class OrganizationFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Organization.
    """

    class Meta:
        model = Organization

    name = factory.Sequence(
        lambda n: f"Test Organization {n}",
    )


class PatientFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Patient.
    """

    class Meta:
        model = Patient

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    first_name = factory.Faker(
        "first_name",
    )

    last_name = factory.Faker(
        "last_name",
    )

    email = factory.Faker(
        "email",
    )


class PatientPreferenceFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for PatientPreference.
    """

    class Meta:
        model = PatientPreference

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
        organization=factory.SelfAttribute(
            "..organization",
        ),
    )

    preferred_name = factory.Faker(
        "first_name",
    )

    language = "en"

    timezone = "Asia/Kolkata"

    portal_theme = ThemePreference.SYSTEM

    appointment_reminder = ReminderPreference.EMAIL

    accessibility_mode = False

    ai_personalization = True

    data_sharing_consent = True

    status = PreferenceStatus.ACTIVE


class PatientCommunicationPreferenceFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for PatientCommunicationPreference.
    """

    class Meta:
        model = PatientCommunicationPreference

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
        organization=factory.SelfAttribute(
            "..organization",
        ),
    )

    channel = CommunicationChannel.EMAIL

    priority = 1

    enabled = True

    appointment_notifications = True

    clinical_notifications = True

    laboratory_notifications = True

    radiology_notifications = True

    pharmacy_notifications = True

    billing_notifications = True

    insurance_notifications = True

    marketing_notifications = False

    emergency_notifications = True

    ai_assistant_notifications = True
