"""
Organization suspended domain event.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.domain.common import DomainEvent
from apps.domain.organizations.value_objects.organization_id import (
    OrganizationId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationSuspended(
    DomainEvent,
):
    """
    Raised when an organization is suspended.
    """

    organization_id: OrganizationId
