"""
Feature flag configuration models for DatavionOS.

Provides immutable configuration objects used by the feature
flag evaluation framework.

The configuration layer is independent from any storage or
database implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.feature_flags.constants import (
    DEFAULT_EVALUATION_STRATEGY,
    DEFAULT_FEATURE_STATE,
)
from apps.common.feature_flags.types import (
    FeatureKey,
)


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureFlagConfiguration:
    """
    Feature flag definition configuration.

    Controls how a feature is evaluated.
    """

    key: FeatureKey

    enabled: bool = False

    default_state: str = DEFAULT_FEATURE_STATE

    strategy: str = DEFAULT_EVALUATION_STRATEGY

    cache_enabled: bool = True

    cache_timeout: int = 300


@dataclass(
    frozen=True,
    slots=True,
)
class FeatureEvaluationConfiguration:
    """
    Runtime evaluation configuration.

    Controls global evaluation behaviour.
    """

    allow_tenant_override: bool = True

    allow_organization_override: bool = True

    allow_subscription_override: bool = True

    fail_safe_default: bool = False


DEFAULT_FEATURE_EVALUATION_CONFIGURATION = FeatureEvaluationConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_FEATURE_EVALUATION_CONFIGURATION",
    "FeatureEvaluationConfiguration",
    "FeatureFlagConfiguration",
)
