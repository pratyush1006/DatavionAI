"""
Constants for the Laboratories application.
"""

from __future__ import annotations

from django.db import models

###############################################################################
# Laboratory Order Status
###############################################################################


class LaboratoryOrderStatus(models.TextChoices):
    """
    Status of a laboratory order.
    """

    ORDERED = (
        "ordered",
        "Ordered",
    )

    SPECIMEN_COLLECTED = (
        "specimen_collected",
        "Specimen Collected",
    )

    IN_PROGRESS = (
        "in_progress",
        "In Progress",
    )

    COMPLETED = (
        "completed",
        "Completed",
    )

    CANCELLED = (
        "cancelled",
        "Cancelled",
    )


DEFAULT_LABORATORY_ORDER_STATUS = LaboratoryOrderStatus.ORDERED


###############################################################################
# Laboratory Test Status
###############################################################################


class LaboratoryTestStatus(models.TextChoices):
    """
    Status of an individual laboratory test.
    """

    PENDING = (
        "pending",
        "Pending",
    )

    IN_PROGRESS = (
        "in_progress",
        "In Progress",
    )

    COMPLETED = (
        "completed",
        "Completed",
    )

    CANCELLED = (
        "cancelled",
        "Cancelled",
    )


DEFAULT_LABORATORY_TEST_STATUS = LaboratoryTestStatus.PENDING


###############################################################################
# Laboratory Priority
###############################################################################


class LaboratoryPriority(models.TextChoices):
    """
    Priority of a laboratory order or laboratory test.
    """

    ROUTINE = (
        "routine",
        "Routine",
    )

    URGENT = (
        "urgent",
        "Urgent",
    )

    STAT = (
        "stat",
        "STAT",
    )


DEFAULT_LABORATORY_PRIORITY = LaboratoryPriority.ROUTINE


###############################################################################
# Laboratory Category
###############################################################################


class LaboratoryCategory(models.TextChoices):
    """
    Clinical category of a laboratory test.
    """

    HEMATOLOGY = (
        "hematology",
        "Hematology",
    )

    CHEMISTRY = (
        "chemistry",
        "Chemistry",
    )

    MICROBIOLOGY = (
        "microbiology",
        "Microbiology",
    )

    SEROLOGY = (
        "serology",
        "Serology",
    )

    PATHOLOGY = (
        "pathology",
        "Pathology",
    )

    IMMUNOLOGY = (
        "immunology",
        "Immunology",
    )

    MOLECULAR = (
        "molecular",
        "Molecular",
    )


###############################################################################
# Laboratory Specimen Type
###############################################################################


class LaboratorySpecimenType(models.TextChoices):
    """
    Specimen type required for a laboratory test.
    """

    BLOOD = (
        "blood",
        "Blood",
    )

    URINE = (
        "urine",
        "Urine",
    )

    STOOL = (
        "stool",
        "Stool",
    )

    SPUTUM = (
        "sputum",
        "Sputum",
    )

    SALIVA = (
        "saliva",
        "Saliva",
    )

    TISSUE = (
        "tissue",
        "Tissue",
    )

    SWAB = (
        "swab",
        "Swab",
    )

    OTHER = (
        "other",
        "Other",
    )


###############################################################################
# Laboratory Result Status
###############################################################################


class LaboratoryResultStatus(models.TextChoices):
    """
    Status of a laboratory result.
    """

    RECORDED = (
        "recorded",
        "Recorded",
    )

    VERIFIED = (
        "verified",
        "Verified",
    )

    FINAL = (
        "final",
        "Final",
    )

    AMENDED = (
        "amended",
        "Amended",
    )

    INVALIDATED = (
        "invalidated",
        "Invalidated",
    )


DEFAULT_LABORATORY_RESULT_STATUS = LaboratoryResultStatus.RECORDED
###############################################################################
# Laboratory Result Verification Status
###############################################################################


class LaboratoryResultVerificationStatus(models.TextChoices):
    """
    Verification status of a laboratory result.
    """

    UNVERIFIED = (
        "unverified",
        "Unverified",
    )

    VERIFIED = (
        "verified",
        "Verified",
    )


DEFAULT_LABORATORY_RESULT_VERIFICATION_STATUS = (
    LaboratoryResultVerificationStatus.UNVERIFIED
)


###############################################################################
# Laboratory Result Flag
###############################################################################


class LaboratoryResultFlag(models.TextChoices):
    """
    Abnormality flag for a laboratory result.
    """

    NORMAL = (
        "normal",
        "Normal",
    )

    HIGH = (
        "high",
        "High",
    )

    LOW = (
        "low",
        "Low",
    )

    CRITICAL = (
        "critical",
        "Critical",
    )

    ABNORMAL = (
        "abnormal",
        "Abnormal",
    )


DEFAULT_LABORATORY_RESULT_FLAG = LaboratoryResultFlag.NORMAL


__all__ = [
    "DEFAULT_LABORATORY_ORDER_STATUS",
    "DEFAULT_LABORATORY_PRIORITY",
    "DEFAULT_LABORATORY_RESULT_FLAG",
    "DEFAULT_LABORATORY_RESULT_STATUS",
    "DEFAULT_LABORATORY_RESULT_VERIFICATION_STATUS",
    "DEFAULT_LABORATORY_TEST_STATUS",
    "LaboratoryCategory",
    "LaboratoryOrderStatus",
    "LaboratoryPriority",
    "LaboratoryResultFlag",
    "LaboratoryResultStatus",
    "LaboratoryResultVerificationStatus",
    "LaboratorySpecimenType",
    "LaboratoryTestStatus",
]
