"""
Domain event emitted after referral lifecycle changes.
"""

from __future__ import annotations

from apps.core.events import DomainEvent


class ReferralStatusChangedEvent(DomainEvent):
    """Represent a referral lifecycle transition."""

    event_type = "patient_referral.status_changed"

    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        referral_id,
        patient_id,
        organization_id,
        previous_status,
        status,
    ) -> None:
        """Initialize the status-change event."""

        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "referral_id": str(referral_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "previous_status": previous_status,
                "status": status,
            },
        )


__all__ = ("ReferralStatusChangedEvent",)
