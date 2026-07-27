"""
Organization identity.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.domain.shared.identity.entity_id import (
    EntityId,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationId(
    EntityId,
):
    """
    Strongly typed organization identity.
    """
