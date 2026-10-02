"""
Feature flag evaluator for DatavionOS.

Provides runtime feature evaluation.

Evaluation priority:

1. Explicit organization override
2. Explicit tenant override
3. Feature default state

Subscription-based evaluation will be integrated through the
subscription domain layer without coupling the common framework.
"""

from __future__ import annotations

from apps.common.feature_flags.exceptions import (
    FeatureFlagEvaluationError,
)
from apps.common.feature_flags.models import (
    FeatureEvaluationResult,
    FeatureOverride,
)
from apps.common.feature_flags.registry import (
    feature_flag_registry,
)
from apps.common.feature_flags.types import (
    FeatureContext,
    FeatureKey,
)


class FeatureFlagEvaluator:
    """
    Runtime feature evaluation engine.
    """

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
        Evaluate whether a feature is enabled.

        Args:
            key:
                Feature identifier.

            context:
                Runtime evaluation context.

            overrides:
                Tenant or organization overrides.

        Returns:
            Feature evaluation result.
        """

        try:
            feature = feature_flag_registry.get(
                key,
            )

            evaluation_context = context or {}

            organization_id = evaluation_context.get(
                "organization_id",
            )

            tenant_id = evaluation_context.get(
                "tenant_id",
            )

            # Organization override has highest priority
            for override in overrides:
                if (
                    override.feature_key == key
                    and override.organization_id == organization_id
                ):
                    return FeatureEvaluationResult(
                        feature_key=key,
                        enabled=override.enabled,
                        reason=("organization_override"),
                        context=evaluation_context,
                    )

            # Tenant override
            for override in overrides:
                if override.feature_key == key and override.tenant_id == tenant_id:
                    return FeatureEvaluationResult(
                        feature_key=key,
                        enabled=override.enabled,
                        reason="tenant_override",
                        context=evaluation_context,
                    )

            # Default feature state
            return FeatureEvaluationResult(
                feature_key=key,
                enabled=feature.enabled,
                reason="default",
                context=evaluation_context,
            )

        except Exception as exc:
            raise FeatureFlagEvaluationError(
                str(exc),
            ) from exc

    def is_enabled(
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
        Check whether a feature is enabled.
        """

        return self.evaluate(
            key,
            context=context,
            overrides=overrides,
        ).enabled


feature_flag_evaluator = FeatureFlagEvaluator()


def feature_enabled(
    key: FeatureKey,
    *,
    context: FeatureContext | None = None,
    overrides: tuple[
        FeatureOverride,
        ...,
    ] = (),
) -> bool:
    """
    Convenience helper for feature checks.
    """

    return feature_flag_evaluator.is_enabled(
        key,
        context=context,
        overrides=overrides,
    )


__all__: tuple[str, ...] = (
    "FeatureFlagEvaluator",
    "feature_enabled",
    "feature_flag_evaluator",
)
