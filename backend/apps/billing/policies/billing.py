"""
Billing Core authorization policy.
"""

from __future__ import annotations

from apps.billing.permissions import BillingPermission
from apps.platform.rbac.engines import user_has_permission


class BillingPolicy:
    """Evaluate organization-scoped Billing RBAC decisions."""

    @staticmethod
    def _check(
        *,
        actor,
        permission: str,
        organization,
    ) -> bool:
        """Evaluate one organization-scoped permission."""
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    @classmethod
    def can_list(cls, *, actor, organization) -> bool:
        """Check billing list permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.LIST,
            organization=organization,
        )

    @classmethod
    def can_view(cls, *, actor, organization) -> bool:
        """Check billing view permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.VIEW,
            organization=organization,
        )

    @classmethod
    def can_create_invoice(cls, *, actor, organization) -> bool:
        """Check invoice creation permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.INVOICE_CREATE,
            organization=organization,
        )

    @classmethod
    def can_update_invoice(cls, *, actor, organization) -> bool:
        """Check invoice update permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.INVOICE_UPDATE,
            organization=organization,
        )

    @classmethod
    def can_delete_invoice(cls, *, actor, organization) -> bool:
        """Check invoice deletion permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.INVOICE_DELETE,
            organization=organization,
        )

    @classmethod
    def can_void_invoice(cls, *, actor, organization) -> bool:
        """Check invoice void permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.INVOICE_VOID,
            organization=organization,
        )

    @classmethod
    def can_process_payment(cls, *, actor, organization) -> bool:
        """Check payment processing permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.PAYMENT_CREATE,
            organization=organization,
        )

    @classmethod
    def can_submit_claim(cls, *, actor, organization) -> bool:
        """Check claim submission permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.CLAIM_CREATE,
            organization=organization,
        )

    @classmethod
    def can_approve_claim(cls, *, actor, organization) -> bool:
        """Check claim approval permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.CLAIM_APPROVE,
            organization=organization,
        )

    @classmethod
    def can_settle_claim(cls, *, actor, organization) -> bool:
        """Check claim settlement permission."""
        return cls._check(
            actor=actor,
            permission=BillingPermission.CLAIM_SETTLE,
            organization=organization,
        )


__all__ = ("BillingPolicy",)
