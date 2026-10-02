"""Patient-owned account resolution for self-service dashboard reads."""

from __future__ import annotations

from django.db.models import F

from apps.patient_management.portal.constants import PortalAccountStatus
from apps.patient_management.portal.models import PatientPortalAccount


def get_patient_portal_account_for_user(*, user) -> PatientPortalAccount | None:
    """Resolve one verified active portal account for the authenticated user.

    Email is used as the identity bridge because portal accounts predate a
    direct User foreign key. Both the platform identity and portal account
    must have verified the same address; ambiguous matches fail closed.
    """
    if (
        not user
        or not getattr(user, "is_authenticated", False)
        or not getattr(user, "is_verified", False)
        or not str(getattr(user, "email", "")).strip()
    ):
        return None

    matches = list(
        PatientPortalAccount.objects.filter(
            email__iexact=user.email.strip(),
            email_verified=True,
            status=PortalAccountStatus.ACTIVE,
            is_active=True,
            patient__organization_id=F("organization_id"),
            patient__is_deleted=False,
        )
        .select_related("patient", "organization")
        .order_by("pk")[:2]
    )

    return matches[0] if len(matches) == 1 else None


__all__ = ("get_patient_portal_account_for_user",)
