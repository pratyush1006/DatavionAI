"""
Feature flag constants for DatavionOS.

Defines framework-wide constants for feature evaluation,
rollout strategies, and SaaS module control.
"""

from __future__ import annotations

###############################################################################
# Feature States
###############################################################################

FEATURE_ENABLED = "enabled"

FEATURE_DISABLED = "disabled"

FEATURE_DEFAULT = "default"


###############################################################################
# Evaluation Strategies
###############################################################################

STRATEGY_BOOLEAN = "boolean"

STRATEGY_TENANT = "tenant"

STRATEGY_ORGANIZATION = "organization"

STRATEGY_SUBSCRIPTION = "subscription"

STRATEGY_PERCENTAGE = "percentage"


###############################################################################
# Feature Categories
###############################################################################

CATEGORY_CORE = "core"

CATEGORY_MODULE = "module"

CATEGORY_EXPERIMENTAL = "experimental"

CATEGORY_ENTERPRISE = "enterprise"

CATEGORY_AI = "ai"


###############################################################################
# Default Configuration
###############################################################################

DEFAULT_FEATURE_STATE = FEATURE_DISABLED

DEFAULT_EVALUATION_STRATEGY = STRATEGY_BOOLEAN


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "CATEGORY_AI",
    "CATEGORY_CORE",
    "CATEGORY_ENTERPRISE",
    "CATEGORY_EXPERIMENTAL",
    "CATEGORY_MODULE",
    "DEFAULT_EVALUATION_STRATEGY",
    "DEFAULT_FEATURE_STATE",
    "FEATURE_DEFAULT",
    "FEATURE_DISABLED",
    "FEATURE_ENABLED",
    "STRATEGY_BOOLEAN",
    "STRATEGY_ORGANIZATION",
    "STRATEGY_PERCENTAGE",
    "STRATEGY_SUBSCRIPTION",
    "STRATEGY_TENANT",
)
