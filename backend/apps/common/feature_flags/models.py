"""
Feature flag models for DatavionOS.

Defines immutable framework-level models for feature management.

These models represent platform capability only.

Business-specific rules belong to domain modules:

- subscriptions
- organizations
- healthcare modules
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)

from apps.common.feature_flags.constants import (
    DEFAULT_FEATURE_STATE,
    STRATEGY_BOOLEAN,
)
from apps.common.feature_flags.types import (
    FeatureContext,
    FeatureKey,
    FeatureName,
)


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureFlag:
    """
    Feature flag definition.

    Represents a platform feature capability.
    """

    key: FeatureKey

    name: FeatureName

    description: str = ""

    enabled: bool = False

    state: str = DEFAULT_FEATURE_STATE

    strategy: str = STRATEGY_BOOLEAN

    metadata: FeatureContext = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureOverride:
    """
    Runtime feature override.

    Used for tenant, organization, or subscription level
    customisation.
    """

    feature_key: FeatureKey

    enabled: bool

    tenant_id: str | int | None = None

    organization_id: str | int | None = None

    metadata: FeatureContext = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureEvaluationResult:
    """
    Result returned after evaluating a feature.
    """

    feature_key: FeatureKey

    enabled: bool

    reason: str

    context: FeatureContext = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "FeatureEvaluationResult",
    "FeatureFlag",
    "FeatureOverride",
)
