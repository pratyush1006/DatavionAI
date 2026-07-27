"""
Constants for the Family Members module.
"""

from __future__ import annotations

from django.db.models import TextChoices

__all__ = [
    "FamilyMemberGender",
    "FamilyMemberRelationship",
    "FamilyMemberStatus",
]


class FamilyMemberRelationship(TextChoices):
    """
    Supported family relationships.
    """

    FATHER = "FATHER", "Father"
    MOTHER = "MOTHER", "Mother"
    HUSBAND = "HUSBAND", "Husband"
    WIFE = "WIFE", "Wife"
    SPOUSE = "SPOUSE", "Spouse"

    SON = "SON", "Son"
    DAUGHTER = "DAUGHTER", "Daughter"

    BROTHER = "BROTHER", "Brother"
    SISTER = "SISTER", "Sister"

    GRANDFATHER = "GRANDFATHER", "Grandfather"
    GRANDMOTHER = "GRANDMOTHER", "Grandmother"

    UNCLE = "UNCLE", "Uncle"
    AUNT = "AUNT", "Aunt"

    COUSIN = "COUSIN", "Cousin"

    GUARDIAN = "GUARDIAN", "Guardian"
    CAREGIVER = "CAREGIVER", "Caregiver"

    FATHER_IN_LAW = "FATHER_IN_LAW", "Father-in-law"
    MOTHER_IN_LAW = "MOTHER_IN_LAW", "Mother-in-law"
    BROTHER_IN_LAW = "BROTHER_IN_LAW", "Brother-in-law"
    SISTER_IN_LAW = "SISTER_IN_LAW", "Sister-in-law"

    STEP_FATHER = "STEP_FATHER", "Step Father"
    STEP_MOTHER = "STEP_MOTHER", "Step Mother"
    STEP_BROTHER = "STEP_BROTHER", "Step Brother"
    STEP_SISTER = "STEP_SISTER", "Step Sister"

    LEGAL_GUARDIAN = "LEGAL_GUARDIAN", "Legal Guardian"

    OTHER = "OTHER", "Other"


class FamilyMemberGender(TextChoices):
    """
    Gender choices.
    """

    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    UNKNOWN = "UNKNOWN", "Unknown"


class FamilyMemberStatus(TextChoices):
    """
    Status of a family member record.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
