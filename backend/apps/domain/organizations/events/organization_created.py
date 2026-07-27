"""
Organization created domain event.
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
class OrganizationCreated(
    DomainEvent,
):
    """
    Raised when an organization is created.
    """

    organization_id: OrganizationId
