"""
Shared pytest fixtures for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.preferences.tests.factories import (
    OrganizationFactory,
    PatientCommunicationPreferenceFactory,
    PatientFactory,
    PatientPreferenceFactory,
)


@pytest.fixture
def organization():
    """
    Create an organization.
    """
    return OrganizationFactory()


@pytest.fixture
def patient(
    organization,
):
    """
    Create a patient.
    """
    return PatientFactory(
        organization=organization,
    )


@pytest.fixture
def patient_preference(
    organization,
    patient,
):
    """
    Create a patient preference.
    """
    return PatientPreferenceFactory(
        organization=organization,
        patient=patient,
    )


@pytest.fixture
def communication_preference(
    organization,
    patient,
):
    """
    Create a patient communication preference.
    """
    return PatientCommunicationPreferenceFactory(
        organization=organization,
        patient=patient,
    )


@pytest.fixture
def patient_preferences(
    organization,
):
    """
    Create multiple patient preferences.
    """
    return PatientPreferenceFactory.create_batch(
        size=5,
        organization=organization,
    )


@pytest.fixture
def communication_preferences(
    organization,
):
    """
    Create multiple communication preferences.
    """
    return PatientCommunicationPreferenceFactory.create_batch(
        size=5,
        organization=organization,
    )
