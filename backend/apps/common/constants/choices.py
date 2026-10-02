"""
DatavionAI Choice Constants.

Shared Django model choices used across the platform.

Design Principles
-----------------
- Reusable
- Immutable
- Type-safe
- Framework independent
"""

from __future__ import annotations

from django.db.models import TextChoices


class ActiveStatus(TextChoices):
    """
    Generic active status.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class RecordStatus(TextChoices):
    """
    Generic record lifecycle.
    """

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    ARCHIVED = "ARCHIVED", "Archived"
    DELETED = "DELETED", "Deleted"


class YesNo(TextChoices):
    """
    Generic yes/no choices.
    """

    YES = "YES", "Yes"
    NO = "NO", "No"


class Gender(TextChoices):
    """
    Generic gender choices.
    """

    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    UNKNOWN = "UNKNOWN", "Unknown"


class Priority(TextChoices):
    """
    Generic priority levels.
    """

    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class Severity(TextChoices):
    """
    Generic severity levels.
    """

    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class Language(TextChoices):
    """
    Common language choices.
    """

    ENGLISH = "en", "English"
    HINDI = "hi", "Hindi"


class BooleanChoice(TextChoices):
    """
    Boolean-like string choices.
    """

    TRUE = "TRUE", "True"
    FALSE = "FALSE", "False"


__all__ = (
    "ActiveStatus",
    "BooleanChoice",
    "Gender",
    "Language",
    "Priority",
    "RecordStatus",
    "Severity",
    "YesNo",
)
