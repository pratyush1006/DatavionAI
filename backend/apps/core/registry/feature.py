"""
DatavionOS platform feature registry.

Defines dynamically available platform capabilities.

Features control:

- subscription capabilities
- tenant availability
- UI visibility
- API behaviour
- AI capabilities
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Registry


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureDefinition:
    """
    Defines a DatavionOS feature.

    Examples:

        ai.assistant

        telemedicine.enabled

        fhir.integration

        advanced.analytics
    """

    key: str

    description: str

    module: str | None = None

    category: str = "platform"

    enabled: bool = True

    subscription_required: bool = True

    beta: bool = False


feature_registry = Registry[FeatureDefinition]()


__all__: tuple[str, ...] = (
    "FeatureDefinition",
    "feature_registry",
)
