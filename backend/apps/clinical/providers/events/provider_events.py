"""
Provider domain events.

Defines lifecycle events emitted by
the Provider bounded context.

All events inherit from
apps.core.events.DomainEvent.

Events are published after successful
workflow transactions.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import (
    DomainEvent,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderCreatedEvent(
    DomainEvent,
):
    """
    Emitted when a provider is created.
    """

    provider_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderUpdatedEvent(
    DomainEvent,
):
    """
    Emitted when provider details are updated.
    """

    provider_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderVerifiedEvent(
    DomainEvent,
):
    """
    Emitted when provider verification completes.
    """

    provider_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderActivatedEvent(
    DomainEvent,
):
    """
    Emitted when provider becomes active.
    """

    provider_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderDeactivatedEvent(
    DomainEvent,
):
    """
    Emitted when provider becomes inactive.
    """

    provider_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderAssignedEvent(
    DomainEvent,
):
    """
    Emitted when provider is assigned
    to department/team/facility.
    """

    provider_id: UUID

    organization_id: UUID

    assignment_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderCredentialAddedEvent(
    DomainEvent,
):
    """
    Emitted when a credential is added.
    """

    provider_id: UUID

    credential_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderCredentialVerifiedEvent(
    DomainEvent,
):
    """
    Emitted when credential verification succeeds.
    """

    provider_id: UUID

    credential_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderLicenseAddedEvent(
    DomainEvent,
):
    """
    Emitted when a license is added.
    """

    provider_id: UUID

    license_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderLicenseVerifiedEvent(
    DomainEvent,
):
    """
    Emitted when license verification succeeds.
    """

    provider_id: UUID

    license_id: UUID

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderAvailabilityUpdatedEvent(
    DomainEvent,
):
    """
    Emitted when provider availability changes.
    """

    provider_id: UUID

    availability_id: UUID

    organization_id: UUID


__all__ = [
    "ProviderCreatedEvent",
    "ProviderUpdatedEvent",
    "ProviderVerifiedEvent",
    "ProviderActivatedEvent",
    "ProviderDeactivatedEvent",
    "ProviderAssignedEvent",
    "ProviderCredentialAddedEvent",
    "ProviderCredentialVerifiedEvent",
    "ProviderLicenseAddedEvent",
    "ProviderLicenseVerifiedEvent",
    "ProviderAvailabilityUpdatedEvent",
]
