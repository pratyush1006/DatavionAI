"""
Selector tests for the Patient Consents module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.consents.constants import (
    ConsentType,
)
from apps.patient_management.consents.selectors import (
    count_patient_consents,
    get_active_consent,
    get_consent_by_id,
    list_organization_consents,
    list_patient_consents,
)
from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


def test_get_consent_by_id():
    consent = ConsentFactory()

    result = get_consent_by_id(
        consent.id,
    )

    assert result == consent


def test_list_patient_consents():
    consent = ConsentFactory()

    queryset = list_patient_consents(
        consent.patient.id,
    )

    assert consent in queryset


def test_list_organization_consents():
    consent = ConsentFactory()

    queryset = list_organization_consents(
        consent.organization.id,
    )

    assert consent in queryset


def test_get_active_consent():
    consent = ConsentFactory()

    result = get_active_consent(
        consent.patient.id,
        ConsentType.TREATMENT,
    )

    assert result == consent


def test_count_patient_consents():
    consent = ConsentFactory()

    assert (
        count_patient_consents(
            consent.patient.id,
        )
        == 1
    )
