"""
Organization model signals.
"""

from __future__ import annotations

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.platform.organizations.models import Organization


@receiver(
    post_save,
    sender=Organization,
    dispatch_uid="organizations.organization.post_save",
)
def organization_post_save(
    sender: type[Organization],
    instance: Organization,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Handle organization post-save events.

    Intentionally lightweight.

    Domain services are responsible for business logic and
    publishing domain events.
    """
    return


@receiver(
    post_delete,
    sender=Organization,
    dispatch_uid="organizations.organization.post_delete",
)
def organization_post_delete(
    sender: type[Organization],
    instance: Organization,
    **kwargs: object,
) -> None:
    """
    Handle organization post-delete events.

    Intentionally lightweight.

    Domain services are responsible for business logic and
    publishing domain events.
    """
    return


__all__: tuple[str, ...] = (
    "organization_post_delete",
    "organization_post_save",
)
