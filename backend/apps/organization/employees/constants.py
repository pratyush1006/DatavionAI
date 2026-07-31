"""
Employee domain constants.

Shared constants and enumerations used throughout the Employee
bounded context.

Design Principles
-----------------
- Single source of truth
- Reusable across models, serializers, services and workflows
- Framework friendly
- MyPy compatible
- No business logic
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

# ==============================================================================
# Employment
# ==============================================================================


class EmploymentStatus(models.TextChoices):
    """
    Employee lifecycle status.
    """

    DRAFT = "DRAFT", _("Draft")

    ACTIVE = "ACTIVE", _("Active")

    PROBATION = "PROBATION", _("Probation")

    NOTICE_PERIOD = (
        "NOTICE_PERIOD",
        _("Notice Period"),
    )

    SUSPENDED = "SUSPENDED", _("Suspended")

    TERMINATED = "TERMINATED", _("Terminated")

    RESIGNED = "RESIGNED", _("Resigned")

    RETIRED = "RETIRED", _("Retired")


DEFAULT_EMPLOYMENT_STATUS = EmploymentStatus.ACTIVE


class EmploymentType(models.TextChoices):
    """
    Employee employment type.
    """

    FULL_TIME = "FULL_TIME", _("Full Time")

    PART_TIME = "PART_TIME", _("Part Time")

    CONTRACT = "CONTRACT", _("Contract")

    CONSULTANT = "CONSULTANT", _("Consultant")

    INTERN = "INTERN", _("Intern")

    TEMPORARY = "TEMPORARY", _("Temporary")

    VOLUNTEER = "VOLUNTEER", _("Volunteer")


DEFAULT_EMPLOYMENT_TYPE = EmploymentType.FULL_TIME


class ContractStatus(models.TextChoices):
    """
    Employment contract lifecycle status.
    """

    DRAFT = "DRAFT", _("Draft")

    ACTIVE = "ACTIVE", _("Active")

    EXPIRED = "EXPIRED", _("Expired")

    CANCELLED = "CANCELLED", _("Cancelled")

    RENEWED = "RENEWED", _("Renewed")


# ==============================================================================
# Personal Information
# ==============================================================================


class Gender(models.TextChoices):
    """
    Gender classification.
    """

    MALE = "MALE", _("Male")

    FEMALE = "FEMALE", _("Female")

    OTHER = "OTHER", _("Other")

    PREFER_NOT_TO_SAY = (
        "PREFER_NOT_TO_SAY",
        _("Prefer not to say"),
    )


class MaritalStatus(models.TextChoices):
    """
    Marital status.
    """

    SINGLE = "SINGLE", _("Single")

    MARRIED = "MARRIED", _("Married")

    DIVORCED = "DIVORCED", _("Divorced")

    WIDOWED = "WIDOWED", _("Widowed")

    SEPARATED = "SEPARATED", _("Separated")


class BloodGroup(models.TextChoices):
    """
    Blood group.
    """

    A_POSITIVE = "A+", _("A+")

    A_NEGATIVE = "A-", _("A-")

    B_POSITIVE = "B+", _("B+")

    B_NEGATIVE = "B-", _("B-")

    AB_POSITIVE = "AB+", _("AB+")

    AB_NEGATIVE = "AB-", _("AB-")

    O_POSITIVE = "O+", _("O+")

    O_NEGATIVE = "O-", _("O-")


class RelationshipType(models.TextChoices):
    """
    Emergency contact relationship type.
    """

    SPOUSE = "SPOUSE", _("Spouse")

    FATHER = "FATHER", _("Father")

    MOTHER = "MOTHER", _("Mother")

    SON = "SON", _("Son")

    DAUGHTER = "DAUGHTER", _("Daughter")

    BROTHER = "BROTHER", _("Brother")

    SISTER = "SISTER", _("Sister")

    GUARDIAN = "GUARDIAN", _("Guardian")

    FRIEND = "FRIEND", _("Friend")

    OTHER = "OTHER", _("Other")


# ==============================================================================
# Address
# ==============================================================================


class AddressType(models.TextChoices):
    """
    Employee address type.
    """

    HOME = "HOME", _("Home")

    CURRENT = "CURRENT", _("Current")

    PERMANENT = "PERMANENT", _("Permanent")

    OFFICE = "OFFICE", _("Office")

    OTHER = "OTHER", _("Other")


# ==============================================================================
# Position
# ==============================================================================


class PositionLevel(models.TextChoices):
    """
    Employee career level.
    """

    JUNIOR = "JUNIOR", _("Junior")

    MID = "MID", _("Mid Level")

    SENIOR = "SENIOR", _("Senior")

    LEAD = "LEAD", _("Lead")

    MANAGER = "MANAGER", _("Manager")

    DIRECTOR = "DIRECTOR", _("Director")

    EXECUTIVE = "EXECUTIVE", _("Executive")


# ==============================================================================
# Assignment
# ==============================================================================


class AssignmentType(models.TextChoices):
    """
    Employee assignment type.
    """

    PRIMARY = "PRIMARY", _("Primary")

    TEMPORARY = "TEMPORARY", _("Temporary")

    SECONDARY = "SECONDARY", _("Secondary")

    ACTING = "ACTING", _("Acting")

    DEPUTATION = "DEPUTATION", _("Deputation")


# ==============================================================================
# Contracts
# ==============================================================================


class ContractType(models.TextChoices):
    """
    Employment contract type.
    """

    PERMANENT = "PERMANENT", _("Permanent")

    FIXED_TERM = "FIXED_TERM", _("Fixed Term")

    TEMPORARY = "TEMPORARY", _("Temporary")

    CONSULTANCY = "CONSULTANCY", _("Consultancy")


# ==============================================================================
# Identifiers
# ==============================================================================


class IdentifierType(models.TextChoices):
    """
    Employee identifier type.
    """

    EMPLOYEE_ID = (
        "EMPLOYEE_ID",
        _("Employee ID"),
    )

    LICENSE = (
        "LICENSE",
        _("Professional License"),
    )

    PASSPORT = "PASSPORT", _("Passport")

    NATIONAL_ID = (
        "NATIONAL_ID",
        _("National ID"),
    )

    TAX_ID = "TAX_ID", _("Tax ID")

    OTHER = "OTHER", _("Other")


# ==============================================================================
# Documents
# ==============================================================================


class DocumentType(models.TextChoices):
    """
    Employee document classification.
    """

    IDENTITY_PROOF = (
        "IDENTITY_PROOF",
        _("Identity Proof"),
    )

    ADDRESS_PROOF = (
        "ADDRESS_PROOF",
        _("Address Proof"),
    )

    EMPLOYMENT_CONTRACT = (
        "EMPLOYMENT_CONTRACT",
        _("Employment Contract"),
    )

    RESUME = "RESUME", _("Resume")

    EDUCATION_CERTIFICATE = (
        "EDUCATION_CERTIFICATE",
        _("Education Certificate"),
    )

    PROFESSIONAL_LICENSE = (
        "PROFESSIONAL_LICENSE",
        _("Professional License"),
    )

    MEDICAL_CERTIFICATE = (
        "MEDICAL_CERTIFICATE",
        _("Medical Certificate"),
    )

    PROFILE_PHOTO = (
        "PROFILE_PHOTO",
        _("Profile Photo"),
    )

    OTHER = "OTHER", _("Other")


class VerificationStatus(models.TextChoices):
    """
    Verification lifecycle status.
    """

    PENDING = "PENDING", _("Pending")

    VERIFIED = "VERIFIED", _("Verified")

    REJECTED = "REJECTED", _("Rejected")

    EXPIRED = "EXPIRED", _("Expired")


# ==============================================================================
# Skills
# ==============================================================================


class SkillCategory(models.TextChoices):
    """
    Employee skill category.
    """

    CLINICAL = "CLINICAL", _("Clinical")

    TECHNICAL = "TECHNICAL", _("Technical")

    ADMINISTRATIVE = (
        "ADMINISTRATIVE",
        _("Administrative"),
    )

    RESEARCH = "RESEARCH", _("Research")

    LEADERSHIP = "LEADERSHIP", _("Leadership")

    COMMUNICATION = (
        "COMMUNICATION",
        _("Communication"),
    )

    OTHER = "OTHER", _("Other")


class SkillProficiencyLevel(models.TextChoices):
    """
    Employee skill proficiency level.
    """

    BEGINNER = "BEGINNER", _("Beginner")

    INTERMEDIATE = (
        "INTERMEDIATE",
        _("Intermediate"),
    )

    ADVANCED = "ADVANCED", _("Advanced")

    EXPERT = "EXPERT", _("Expert")


# ==============================================================================
# Education
# ==============================================================================


class EducationLevel(models.TextChoices):
    """
    Education qualification level.
    """

    HIGH_SCHOOL = (
        "HIGH_SCHOOL",
        _("High School"),
    )

    DIPLOMA = "DIPLOMA", _("Diploma")

    BACHELOR = "BACHELOR", _("Bachelor")

    MASTER = "MASTER", _("Master")

    DOCTORATE = (
        "DOCTORATE",
        _("Doctorate"),
    )

    FELLOWSHIP = (
        "FELLOWSHIP",
        _("Fellowship"),
    )

    CERTIFICATION = (
        "CERTIFICATION",
        _("Certification"),
    )


# ==============================================================================
# Experience
# ==============================================================================


class ExperienceType(models.TextChoices):
    """
    Previous experience category.
    """

    CLINICAL = "CLINICAL", _("Clinical")

    ADMINISTRATIVE = (
        "ADMINISTRATIVE",
        _("Administrative"),
    )

    RESEARCH = "RESEARCH", _("Research")

    ACADEMIC = "ACADEMIC", _("Academic")

    INDUSTRY = "INDUSTRY", _("Industry")

    OTHER = "OTHER", _("Other")


# ==============================================================================
# Employee History
# ==============================================================================


class EmployeeHistoryEvent(models.TextChoices):
    """
    Employee business lifecycle events.
    """

    CREATED = "CREATED", _("Created")

    ACTIVATED = "ACTIVATED", _("Activated")

    PROFILE_UPDATED = (
        "PROFILE_UPDATED",
        _("Profile Updated"),
    )

    POSITION_CHANGED = (
        "POSITION_CHANGED",
        _("Position Changed"),
    )

    ASSIGNMENT_CHANGED = (
        "ASSIGNMENT_CHANGED",
        _("Assignment Changed"),
    )

    MANAGER_CHANGED = (
        "MANAGER_CHANGED",
        _("Manager Changed"),
    )

    CONTRACT_CREATED = (
        "CONTRACT_CREATED",
        _("Contract Created"),
    )

    CONTRACT_RENEWED = (
        "CONTRACT_RENEWED",
        _("Contract Renewed"),
    )

    STATUS_CHANGED = (
        "STATUS_CHANGED",
        _("Status Changed"),
    )

    SUSPENDED = "SUSPENDED", _("Suspended")

    RESIGNED = "RESIGNED", _("Resigned")

    TERMINATED = (
        "TERMINATED",
        _("Terminated"),
    )

    REHIRED = "REHIRED", _("Rehired")


class HistorySource(models.TextChoices):
    """
    Source that created employee history.
    """

    SYSTEM = "SYSTEM", _("System")

    USER = "USER", _("User")

    WORKFLOW = "WORKFLOW", _("Workflow")

    IMPORT = "IMPORT", _("Import")

    API = "API", _("API")


# ==============================================================================
# Public Exports
# ==============================================================================


__all__: tuple[str, ...] = (
    "AddressType",
    "AssignmentType",
    "BloodGroup",
    "ContractStatus",
    "ContractType",
    "DEFAULT_EMPLOYMENT_STATUS",
    "DEFAULT_EMPLOYMENT_TYPE",
    "DocumentType",
    "EducationLevel",
    "EmployeeHistoryEvent",
    "EmploymentStatus",
    "EmploymentType",
    "ExperienceType",
    "Gender",
    "HistorySource",
    "IdentifierType",
    "MaritalStatus",
    "PositionLevel",
    "RelationshipType",
    "SkillCategory",
    "SkillProficiencyLevel",
    "VerificationStatus",
)
