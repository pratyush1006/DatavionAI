"""Workflow orchestration for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from .policies import ARPolicy
from .services import ARService


class ARWorkflow:
    """Orchestrate authorized Accounts Receivable mutations."""

    @staticmethod
    def post_transaction(
        *,
        user: Any,
        organization: Any,
        account_id: UUID,
        transaction_type: str,
        amount: Any,
        transaction_number: str,
        transaction_date: Any,
        source_type: str = "",
        source_id: UUID | None = None,
        external_reference: str = "",
        note: str = "",
    ) -> Any:
        """Authorize and post an AR transaction."""

        if not ARPolicy.can_post(user=user, organization=organization):
            raise PermissionError("Accounts Receivable posting permission is required.")
        return ARService.post_transaction(
            organization=organization,
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            transaction_number=transaction_number,
            transaction_date=transaction_date,
            actor=user,
            source_type=source_type,
            source_id=source_id,
            external_reference=external_reference,
            note=note,
        )

    @staticmethod
    def reverse_transaction(
        *,
        user: Any,
        organization: Any,
        transaction_id: UUID,
    ) -> Any:
        """Authorize and reverse an AR transaction."""

        if not ARPolicy.can_reverse(user=user, organization=organization):
            raise PermissionError(
                "Accounts Receivable reversal permission is required."
            )
        return ARService.reverse_transaction(
            organization=organization,
            transaction_id=transaction_id,
            actor=user,
        )

    @staticmethod
    def hold(
        *,
        user: Any,
        organization: Any,
        account_id: UUID,
        reason: str,
        note: str = "",
    ) -> Any:
        """Authorize and place an AR account on hold."""

        if not ARPolicy.can_hold(user=user, organization=organization):
            raise PermissionError("Accounts Receivable hold permission is required.")
        return ARService.set_hold(
            organization=organization,
            account_id=account_id,
            reason=reason,
            note=note,
            actor=user,
        )

    @staticmethod
    def release_hold(
        *,
        user: Any,
        organization: Any,
        account_id: UUID,
    ) -> Any:
        """Authorize and release an AR account hold."""

        if not ARPolicy.can_hold(user=user, organization=organization):
            raise PermissionError("Accounts Receivable hold permission is required.")
        return ARService.release_hold(
            organization=organization,
            account_id=account_id,
            actor=user,
        )

    @staticmethod
    def write_off(
        *,
        user: Any,
        organization: Any,
        account_id: UUID,
        transaction_number: str,
        note: str = "",
    ) -> Any:
        """Authorize and write off the outstanding AR balance."""

        if not ARPolicy.can_write_off(user=user, organization=organization):
            raise PermissionError(
                "Accounts Receivable write-off permission is required."
            )
        return ARService.write_off(
            organization=organization,
            account_id=account_id,
            transaction_number=transaction_number,
            actor=user,
            note=note,
        )


__all__ = ("ARWorkflow",)
