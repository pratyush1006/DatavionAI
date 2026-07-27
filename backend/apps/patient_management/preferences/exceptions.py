"""
Exceptions for the Patient Preferences module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class PatientPreferenceError(DatavionException):
    """
    Base exception for patient preferences.
    """

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Patient preference operation failed."


class PatientPreferenceNotFoundError(
    PatientPreferenceError,
):
    """
    Preference not found.
    """

    default_detail = "Patient preference not found."


class DuplicatePatientPreferenceError(
    PatientPreferenceError,
):
    """
    Duplicate preference.
    """

    default_detail = "Patient preference already exists."


class CommunicationPreferenceError(
    PatientPreferenceError,
):
    """
    Communication preference error.
    """

    default_detail = "Communication preference operation failed."


class CommunicationPreferenceNotFoundError(
    CommunicationPreferenceError,
):
    """
    Communication preference not found.
    """

    default_detail = "Communication preference not found."


class DuplicateCommunicationPreferenceError(
    CommunicationPreferenceError,
):
    """
    Duplicate communication preference.
    """

    default_detail = "Communication preference already exists."


__all__ = [
    "CommunicationPreferenceError",
    "CommunicationPreferenceNotFoundError",
    "DuplicateCommunicationPreferenceError",
    "DuplicatePatientPreferenceError",
    "PatientPreferenceError",
    "PatientPreferenceNotFoundError",
]
