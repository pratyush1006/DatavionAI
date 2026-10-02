from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.platform.organizations.models import Organization
from apps.platform.organizations.services.finance_provisioning import (
    provision_organization_finance,
)


@receiver(
    post_save,
    sender=Organization,
    dispatch_uid="datavionos.organization.finance.auto_provision.v10",
)
def provision_finance_after_organization_creation(
    *,
    sender,
    instance,
    created,
    **kwargs,
) -> None:
    """Create the current finance fiscal period for a new organization."""

    if not created:
        return

    provision_organization_finance(
        organization=instance,
    )


__all__ = [
    "provision_finance_after_organization_creation",
]
