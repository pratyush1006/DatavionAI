"""
Managers and querysets for Patient Referrals.
"""

from __future__ import annotations

from apps.core.models.managers import SoftDeleteManager
from apps.core.models.querysets import SoftDeleteQuerySet


class PatientReferralQuerySet(SoftDeleteQuerySet):
    """Query helpers for alive and deleted referrals."""

    def for_patient(self, patient_id):
        """Return referrals belonging to one patient."""

        return self.filter(patient_id=patient_id)

    def by_status(self, status):
        """Return referrals in the requested lifecycle state."""

        return self.filter(status=status)

    def urgent(self):
        """Return urgent or stat referrals."""

        return self.filter(priority__in=("URGENT", "STAT"))


class PatientReferralManager(
    SoftDeleteManager.from_queryset(PatientReferralQuerySet),
):
    """Default manager exposing alive referrals only."""


__all__ = (
    "PatientReferralManager",
    "PatientReferralQuerySet",
)
