"""
Organization feature disabled domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class FeatureDisabledEvent(DomainEvent):
    """
    Raised when a feature is disabled for an organization.
    """

    organization_id: UUID

    feature_code: str


__all__: tuple[str, ...] = ("FeatureDisabledEvent",)
