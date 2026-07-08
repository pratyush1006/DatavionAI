"""
Selectors for laboratory results.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.laboratories.constants import (
    LaboratoryResultFlag,
    LaboratoryResultStatus,
)
from apps.laboratories.models import (
    LaboratoryResult,
)

###############################################################################
# Core Selectors
###############################################################################


def list_laboratory_results() -> QuerySet[LaboratoryResult]:
    """
    Return all laboratory results.
    """

    return LaboratoryResult.objects.select_related(
        "laboratory_test",
        "laboratory_test__laboratory_order",
        "laboratory_test__laboratory_order__organization",
        "laboratory_test__laboratory_order__patient",
        "laboratory_test__laboratory_order__provider",
        "laboratory_test__laboratory_order__encounter",
        "verified_by",
    )


def get_laboratory_result(
    *,
    pk: int,
) -> LaboratoryResult:
    """
    Return a laboratory result by primary key.

    Raises:
        LaboratoryResult.DoesNotExist:
            If the laboratory result does not exist.
    """

    return list_laboratory_results().get(
        pk=pk,
    )


###############################################################################
# Relationship Selectors
###############################################################################


def list_laboratory_test_results(
    *,
    laboratory_test_id: int,
) -> QuerySet[LaboratoryResult]:
    """
    Return all laboratory results for a laboratory test.
    """

    return list_laboratory_results().filter(
        laboratory_test_id=laboratory_test_id,
    )


def list_patient_laboratory_results(
    *,
    patient_id: int,
) -> QuerySet[LaboratoryResult]:
    """
    Return all laboratory results for a patient.
    """

    return list_laboratory_results().filter(
        laboratory_test__laboratory_order__patient_id=patient_id,
    )


def list_encounter_laboratory_results(
    *,
    encounter_id: int,
) -> QuerySet[LaboratoryResult]:
    """
    Return all laboratory results for an encounter.
    """

    return list_laboratory_results().filter(
        laboratory_test__laboratory_order__encounter_id=encounter_id,
    )


def list_provider_verified_results(
    *,
    provider_id: int,
) -> QuerySet[LaboratoryResult]:
    """
    Return all laboratory results verified by a provider.
    """

    return list_laboratory_results().filter(
        verified_by_id=provider_id,
    )


###############################################################################
# Filter Selectors
###############################################################################


def list_status_laboratory_results(
    *,
    status: LaboratoryResultStatus,
) -> QuerySet[LaboratoryResult]:
    """
    Return laboratory results filtered by status.
    """

    return list_laboratory_results().filter(
        status=status,
    )


def list_flagged_laboratory_results(
    *,
    flag: LaboratoryResultFlag,
) -> QuerySet[LaboratoryResult]:
    """
    Return laboratory results filtered by abnormality flag.
    """

    return list_laboratory_results().filter(
        abnormal_flag=flag,
    )


def list_verified_laboratory_results() -> QuerySet[LaboratoryResult]:
    """
    Return all verified laboratory results.
    """

    return list_status_laboratory_results(
        status=LaboratoryResultStatus.VERIFIED,
    )


def list_pending_laboratory_results() -> QuerySet[LaboratoryResult]:
    """
    Return all pending laboratory results.
    """

    return list_status_laboratory_results(
        status=LaboratoryResultStatus.RECORDED,
    )


def list_critical_laboratory_results() -> QuerySet[LaboratoryResult]:
    """
    Return all critical laboratory results.
    """

    return list_flagged_laboratory_results(
        flag=LaboratoryResultFlag.CRITICAL,
    )


###############################################################################
# Aggregate Selectors
###############################################################################


def exists_laboratory_result(
    *,
    laboratory_test_id: int,
) -> bool:
    """
    Return whether a laboratory result exists
    for a laboratory test.
    """

    return LaboratoryResult.objects.filter(
        laboratory_test_id=laboratory_test_id,
    ).exists()


def count_patient_laboratory_results(
    *,
    patient_id: int,
) -> int:
    """
    Return the total number of laboratory results
    for a patient.
    """

    return list_patient_laboratory_results(
        patient_id=patient_id,
    ).count()


__all__ = [
    "count_patient_laboratory_results",
    "exists_laboratory_result",
    "get_laboratory_result",
    "list_critical_laboratory_results",
    "list_encounter_laboratory_results",
    "list_flagged_laboratory_results",
    "list_laboratory_results",
    "list_laboratory_test_results",
    "list_patient_laboratory_results",
    "list_pending_laboratory_results",
    "list_provider_verified_results",
    "list_status_laboratory_results",
    "list_verified_laboratory_results",
]
