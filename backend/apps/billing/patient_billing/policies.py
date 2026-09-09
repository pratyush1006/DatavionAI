"""Patient Billing authorization policies."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.engines import user_has_permission


class PatientBillingPolicy:
    """Centralize Patient Billing authorization decisions."""

    ACCOUNT_VIEW = "billing.patient_account.view"
    ACCOUNT_CREATE = "billing.patient_account.create"
    ACCOUNT_UPDATE = "billing.patient_account.update"
    ACCOUNT_LIFECYCLE = "billing.patient_account.lifecycle"
    GUARANTOR_VIEW = "billing.guarantor.view"
    GUARANTOR_CREATE = "billing.guarantor.create"
    GUARANTOR_UPDATE = "billing.guarantor.update"
    GUARANTOR_DELETE = "billing.guarantor.delete"
    GUARANTOR_RESTORE = "billing.guarantor.restore"
    RESPONSIBILITY_VIEW = "billing.responsibility.view"
    RESPONSIBILITY_CREATE = "billing.responsibility.create"
    RESPONSIBILITY_UPDATE = "billing.responsibility.update"
    RESPONSIBILITY_DELETE = "billing.responsibility.delete"
    RESPONSIBILITY_RESTORE = "billing.responsibility.restore"
    STATEMENT_VIEW = "billing.statement.view"
    STATEMENT_CREATE = "billing.statement.create"
    STATEMENT_ISSUE = "billing.statement.issue"
    STATEMENT_VOID = "billing.statement.void"

    @staticmethod
    def allowed(
        *,
        actor: Any,
        permission: str,
        organization: Any,
    ) -> bool:
        """Return whether the actor has an exact organization permission."""

        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    @staticmethod
    def require(
        *,
        actor: Any,
        permission: str,
        organization: Any,
    ) -> None:
        """Raise when the actor lacks the requested permission."""

        if not PatientBillingPolicy.allowed(
            actor=actor,
            permission=permission,
            organization=organization,
        ):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You do not have permission to perform this billing operation.",
            )


__all__ = ("PatientBillingPolicy",)
