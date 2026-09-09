"""
Domain services for Patient Portal account mutations.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.portal.constants import (
    ALLOWED_STATUS_TRANSITIONS,
    PortalAccountStatus,
)
from apps.patient_management.portal.exceptions import (
    PortalLifecycleError,
    PortalOrganizationError,
)
from apps.patient_management.portal.models import PatientPortalAccount
from apps.platform.accounts.models import User


class PatientPortalAccountService:
    """Encapsulate validated Patient Portal account mutations."""

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "created_at",
            "updated_at",
            "status",
            "activated_at",
            "invitation_sent_at",
            "last_login_at",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        },
    )

    @staticmethod
    def _ensure_boundary(
        *,
        patient: Any,
        organization: Any,
    ) -> None:
        """Ensure the patient and organization share the same tenant."""

        if patient.organization_id != organization.pk:
            raise PortalOrganizationError(
                "Patient does not belong to the selected organization.",
            )

        if patient.organization.tenant_id != organization.tenant_id:
            raise PortalOrganizationError(
                "Patient and portal organization belong to different tenants.",
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        organization: Any,
        patient: Any,
        username: str,
        email: str = "",
        auth_provider: str = "LOCAL",
        preferred_language: str = "English",
        performed_by: User | None = None,
    ) -> PatientPortalAccount:
        """Create a validated invited portal account."""

        cls._ensure_boundary(
            patient=patient,
            organization=organization,
        )

        username = username.strip()
        email = email.strip()
        preferred_language = preferred_language.strip()

        if not username:
            raise ValidationError(
                {"username": "Username is required."},
            )

        account = PatientPortalAccount(
            organization=organization,
            patient=patient,
            username=username,
            email=email,
            auth_provider=auth_provider,
            preferred_language=preferred_language or "English",
        )

        account.full_clean()
        account.save()

        return account

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        account: PatientPortalAccount,
        data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> PatientPortalAccount:
        """Update mutable portal account metadata."""

        if account.is_deleted:
            raise ValidationError(
                {"detail": "Deleted portal accounts cannot be updated."},
            )

        allowed_fields = {
            "username",
            "email",
            "auth_provider",
            "preferred_language",
            "email_verified",
            "two_factor_enabled",
        }

        unknown = set(data) - allowed_fields
        if unknown:
            raise ValidationError(
                {
                    "detail": (
                        "Unsupported portal account fields: "
                        + ", ".join(sorted(unknown))
                    ),
                },
            )

        for field, value in data.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(account, field, value)

        account.full_clean()
        account.save()

        return account

    @classmethod
    @transaction.atomic
    def transition(
        cls,
        *,
        account: PatientPortalAccount,
        status: str,
        performed_by: User | None = None,
    ) -> PatientPortalAccount:
        """Apply one explicitly allowed portal lifecycle transition."""

        if account.is_deleted:
            raise PortalLifecycleError(
                "Deleted portal accounts cannot change lifecycle state.",
            )

        try:
            allowed = ALLOWED_STATUS_TRANSITIONS[account.status]
        except KeyError as exc:
            raise PortalLifecycleError(
                f"Unknown portal status: {account.status}.",
            ) from exc

        if status not in allowed:
            raise PortalLifecycleError(
                f"Invalid portal transition: {account.status} -> {status}.",
            )

        now = timezone.now()
        account.status = status

        if status == PortalAccountStatus.ACTIVE:
            account.is_active = True
            account.activated_at = account.activated_at or now
        elif status in {
            PortalAccountStatus.DEACTIVATED,
            PortalAccountStatus.SUSPENDED,
            PortalAccountStatus.LOCKED,
        }:
            account.is_active = False

        account.full_clean()
        account.save()
        return account

    @classmethod
    @transaction.atomic
    def mark_invitation_sent(
        cls,
        *,
        account: PatientPortalAccount,
    ) -> PatientPortalAccount:
        """Record that an invitation notification was issued."""

        if account.is_deleted:
            raise PortalLifecycleError(
                "Deleted portal accounts cannot receive invitations.",
            )

        if account.status != PortalAccountStatus.INVITED:
            raise PortalLifecycleError(
                "Invitations may only be sent for invited accounts.",
            )

        if not account.email.strip():
            raise ValidationError(
                {"email": "An email address is required to issue an invitation."},
            )

        account.invitation_sent_at = timezone.now()
        account.save(
            update_fields=(
                "invitation_sent_at",
                "updated_at",
            ),
        )
        return account

    @classmethod
    @transaction.atomic
    def record_login(
        cls,
        *,
        account: PatientPortalAccount,
    ) -> PatientPortalAccount:
        """Record a successful portal login."""

        if account.status != PortalAccountStatus.ACTIVE:
            raise PortalLifecycleError(
                "Only active portal accounts may record a login.",
            )

        account.last_login_at = timezone.now()
        account.save(
            update_fields=(
                "last_login_at",
                "updated_at",
            ),
        )
        return account

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        account: PatientPortalAccount,
        performed_by: User | None = None,
    ) -> PatientPortalAccount:
        """Soft-delete a portal account."""

        if performed_by is None:
            raise ValidationError(
                {"detail": "An actor is required to delete a portal account."},
            )

        account.delete(user_id=performed_by.pk)
        return account

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        account: PatientPortalAccount,
        performed_by: User | None = None,
    ) -> PatientPortalAccount:
        """Restore a previously soft-deleted portal account."""

        if performed_by is None:
            raise ValidationError(
                {"detail": "An actor is required to restore a portal account."},
            )

        account.restore()
        return account


__all__ = ("PatientPortalAccountService",)
