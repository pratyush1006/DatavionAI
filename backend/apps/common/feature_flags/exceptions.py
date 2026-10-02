"""
Feature flag exception hierarchy for DatavionOS.

Provides reusable exceptions for the feature flag framework.
"""

from __future__ import annotations


class FeatureFlagError(
    Exception,
):
    """
    Base exception for feature flag errors.
    """


class FeatureFlagConfigurationError(
    FeatureFlagError,
):
    """
    Raised when feature flag configuration is invalid.
    """


class FeatureFlagNotFoundError(
    FeatureFlagError,
):
    """
    Raised when a requested feature flag does not exist.
    """


class FeatureFlagRegistrationError(
    FeatureFlagError,
):
    """
    Raised when feature registration fails.
    """


class FeatureFlagAlreadyRegisteredError(
    FeatureFlagRegistrationError,
):
    """
    Raised when a feature flag is registered twice.
    """


class FeatureFlagEvaluationError(
    FeatureFlagError,
):
    """
    Raised when feature evaluation fails.
    """


class FeatureFlagContextError(
    FeatureFlagEvaluationError,
):
    """
    Raised when evaluation context is invalid.
    """


__all__: tuple[str, ...] = (
    "FeatureFlagAlreadyRegisteredError",
    "FeatureFlagConfigurationError",
    "FeatureFlagContextError",
    "FeatureFlagError",
    "FeatureFlagEvaluationError",
    "FeatureFlagNotFoundError",
    "FeatureFlagRegistrationError",
)
