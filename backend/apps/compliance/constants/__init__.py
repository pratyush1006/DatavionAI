"""
Compliance constants.
"""

from __future__ import annotations


class ConsentStatus:
    """
    Consent lifecycle states.
    """

    GRANTED = "granted"

    REVOKED = "revoked"

    PENDING = "pending"

    EXPIRED = "expired"

    CHOICES = (
        (GRANTED, "Granted"),
        (REVOKED, "Revoked"),
        (PENDING, "Pending"),
        (EXPIRED, "Expired"),
    )


class ConsentPurpose:
    """
    Common consent purposes under HIPAA.
    """

    TREATMENT = "treatment"

    PAYMENT = "payment"

    OPERATIONS = "operations"

    RESEARCH = "research"

    CHOICES = (
        (TREATMENT, "Treatment"),
        (PAYMENT, "Payment"),
        (OPERATIONS, "Operations"),
        (RESEARCH, "Research"),
    )


class PhiAccessAction:
    """
    Categories of PHI access for audit logging.
    """

    VIEW = "view"

    EXPORT = "export"

    MODIFY = "modify"

    DELETE = "delete"

    CHOICES = (
        (VIEW, "View"),
        (EXPORT, "Export"),
        (MODIFY, "Modify"),
        (DELETE, "Delete"),
    )


__all__ = [
    "ConsentPurpose",
    "ConsentStatus",
    "PhiAccessAction",
]
