"""
Domain event emitted after referral creation.
"""

from __future__ import annotations

from apps.core.events import DomainEvent


class ReferralCreatedEvent(DomainEvent):
    """Represent successful creation of a patient referral."""

    event_type = "patient_referral.created"

    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        referral_id,
        patient_id,
        organization_id,
    ) -> None:
        """Initialize the referral-created event."""

        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "referral_id": str(referral_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
            },
        )


__all__ = ("ReferralCreatedEvent",)
