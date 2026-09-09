"""
Domain event emitted after referral restoration.
"""

from __future__ import annotations

from apps.core.events import DomainEvent


class ReferralRestoredEvent(DomainEvent):
    """Represent restoration of a deleted referral."""

    event_type = "patient_referral.restored"

    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        referral_id,
        patient_id,
        organization_id,
    ) -> None:
        """Initialize the referral-restored event."""

        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "referral_id": str(referral_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
            },
        )


__all__ = ("ReferralRestoredEvent",)
