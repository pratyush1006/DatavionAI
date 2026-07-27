"""
Filter tests for the Patient Consents module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.consents.api.filters import (
    ConsentFilter,
)
from apps.patient_management.consents.constants import (
    ConsentStatus,
    ConsentType,
)
from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


def test_filter_patient():
    consent = ConsentFactory()

    filtered = ConsentFilter(
        {
            "patient": consent.patient.id,
        },
        queryset=Consent.objects.all(),
    )

    assert filtered.qs.count() == 1


def test_filter_status():
    ConsentFactory(
        status=ConsentStatus.GRANTED,
    )

    filtered = ConsentFilter(
        {
            "status": ConsentStatus.GRANTED,
        },
        queryset=Consent.objects.all(),
    )

    assert filtered.qs.count() == 1


def test_filter_type():
    ConsentFactory(
        consent_type=ConsentType.TREATMENT,
    )

    filtered = ConsentFilter(
        {
            "consent_type": ConsentType.TREATMENT,
        },
        queryset=Consent.objects.all(),
    )

    assert filtered.qs.count() == 1


def test_search():
    ConsentFactory(
        title="Surgery Consent",
    )

    filtered = ConsentFilter(
        {
            "search": "Surgery",
        },
        queryset=Consent.objects.all(),
    )

    assert filtered.qs.count() == 1
