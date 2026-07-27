"""
Manager tests for Patient Consents.
"""

from __future__ import annotations

import pytest

from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


def test_active_manager():
    ConsentFactory()

    assert Consent.objects.active().count() == 1


def test_pending_manager():
    ConsentFactory(
        status="PENDING",
    )

    assert Consent.objects.pending().count() == 1


def test_granted_manager():
    ConsentFactory(
        status="GRANTED",
    )

    assert Consent.objects.granted().count() == 1


def test_revoked_manager():
    ConsentFactory(
        status="REVOKED",
    )

    assert Consent.objects.revoked().count() == 1


def test_expired_manager():
    ConsentFactory(
        status="EXPIRED",
    )

    assert Consent.objects.expired().count() == 1


def test_for_patient():
    consent = ConsentFactory()

    assert (
        Consent.objects.for_patient(
            consent.patient.id,
        ).count()
        == 1
    )


def test_for_organization():
    consent = ConsentFactory()

    assert (
        Consent.objects.for_organization(
            consent.organization.id,
        ).count()
        == 1
    )


def test_by_type():
    ConsentFactory()

    assert (
        Consent.objects.by_type(
            "TREATMENT",
        ).count()
        == 1
    )
