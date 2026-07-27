"""
Service tests for the Patient Consents module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.consents.constants import (
    ConsentStatus,
)
from apps.patient_management.consents.services import (
    expire_consent,
    grant_consent,
    revoke_consent,
    update_consent,
    withdraw_consent,
)
from apps.patient_management.consents.tests.factories import (
    ConsentFactory,
)

pytestmark = pytest.mark.django_db


def test_update_consent():
    consent = ConsentFactory()

    update_consent(
        consent=consent,
        title="Updated Consent",
    )

    consent.refresh_from_db()

    assert consent.title == "Updated Consent"


def test_grant_consent():
    consent = ConsentFactory()

    grant_consent(
        consent,
    )

    consent.refresh_from_db()

    assert consent.status == ConsentStatus.GRANTED
    assert consent.granted_at is not None


def test_revoke_consent():
    consent = ConsentFactory()

    revoke_consent(
        consent,
    )

    consent.refresh_from_db()

    assert consent.status == ConsentStatus.REVOKED
    assert consent.revoked_at is not None
    assert consent.is_active is False


def test_withdraw_consent():
    consent = ConsentFactory()

    withdraw_consent(
        consent,
    )

    consent.refresh_from_db()

    assert consent.status == ConsentStatus.WITHDRAWN
    assert consent.withdrawn_at is not None
    assert consent.is_active is False


def test_expire_consent():
    consent = ConsentFactory()

    expire_consent(
        consent,
    )

    consent.refresh_from_db()

    assert consent.status == ConsentStatus.EXPIRED
    assert consent.is_active is False
