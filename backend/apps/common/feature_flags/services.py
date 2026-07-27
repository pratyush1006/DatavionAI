"""
Feature flag services for DatavionOS.

Provides the application service layer for feature management.

Business applications should use this service layer instead of
directly accessing registries or evaluators.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.feature_flags.evaluator import (
    feature_flag_evaluator,
)
from apps.common.feature_flags.models import (
    FeatureEvaluationResult,
    FeatureFlag,
    FeatureOverride,
)
from apps.common.feature_flags.registry import (
    feature_flag_registry,
)
from apps.common.feature_flags.types import (
    FeatureContext,
    FeatureKey,
)


class FeatureFlagService:
    """
    Feature flag application service.

    Provides:

    - Feature registration
    - Feature discovery
    - Runtime evaluation
    - Feature checks
    """

    def register(
        self,
        feature: FeatureFlag,
    ) -> None:
        """
        Register a feature flag.
        """

        feature_flag_registry.register(
            feature,
        )

    def unregister(
        self,
        key: FeatureKey,
    ) -> None:
        """
        Remove a feature flag.
        """

        feature_flag_registry.unregister(
            key,
        )

    def get(
        self,
        key: FeatureKey,
    ) -> FeatureFlag:
        """
        Return a feature definition.
        """

        return feature_flag_registry.get(
            key,
        )

    def all(
        self,
    ) -> Iterable[FeatureFlag]:
        """
        Return all registered features.
        """

        return feature_flag_registry.all()

    def evaluate(
        self,
        key: FeatureKey,
        *,
        context: FeatureContext | None = None,
        overrides: tuple[
            FeatureOverride,
            ...,
        ] = (),
    ) -> FeatureEvaluationResult:
        """
        Evaluate a feature flag.
        """

        return feature_flag_evaluator.evaluate(
            key,
            context=context,
            overrides=overrides,
        )

    def enabled(
        self,
        key: FeatureKey,
        *,
        context: FeatureContext | None = None,
        overrides: tuple[
            FeatureOverride,
            ...,
        ] = (),
    ) -> bool:
        """
        Check feature availability.
        """

        return feature_flag_evaluator.is_enabled(
            key,
            context=context,
            overrides=overrides,
        )


feature_flag_service = FeatureFlagService()


__all__: tuple[str, ...] = (
    "FeatureFlagService",
    "feature_flag_service",
)
