"""
DatavionOS feature flag framework.

Provides the public API for runtime feature management.

Supports:

- Feature definitions
- Feature registration
- Runtime evaluation
- Tenant overrides
- Organization overrides
- SaaS module activation

Business applications should import feature flag utilities from
this package instead of internal modules.
"""

from __future__ import annotations

from .config import (
    DEFAULT_FEATURE_EVALUATION_CONFIGURATION,
    FeatureEvaluationConfiguration,
    FeatureFlagConfiguration,
)
from .constants import (
    CATEGORY_AI,
    CATEGORY_CORE,
    CATEGORY_ENTERPRISE,
    CATEGORY_EXPERIMENTAL,
    CATEGORY_MODULE,
    DEFAULT_EVALUATION_STRATEGY,
    DEFAULT_FEATURE_STATE,
    FEATURE_DEFAULT,
    FEATURE_DISABLED,
    FEATURE_ENABLED,
    STRATEGY_BOOLEAN,
    STRATEGY_ORGANIZATION,
    STRATEGY_PERCENTAGE,
    STRATEGY_SUBSCRIPTION,
    STRATEGY_TENANT,
)
from .evaluator import (
    FeatureFlagEvaluator,
    feature_enabled,
    feature_flag_evaluator,
)
from .exceptions import (
    FeatureFlagAlreadyRegisteredError,
    FeatureFlagConfigurationError,
    FeatureFlagContextError,
    FeatureFlagError,
    FeatureFlagEvaluationError,
    FeatureFlagNotFoundError,
    FeatureFlagRegistrationError,
)
from .models import (
    FeatureEvaluationResult,
    FeatureFlag,
    FeatureOverride,
)
from .registry import (
    FeatureFlagRegistry,
    feature_flag_registry,
)
from .services import (
    FeatureFlagService,
    feature_flag_service,
)
from .types import (
    FeatureContext,
    FeatureKey,
    FeatureName,
    FeatureValue,
    OrganizationID,
    TenantID,
)

__all__: tuple[str, ...] = (
    # Models
    "FeatureFlag",
    "FeatureOverride",
    "FeatureEvaluationResult",
    # Services
    "FeatureFlagService",
    "feature_flag_service",
    # Registry
    "FeatureFlagRegistry",
    "feature_flag_registry",
    # Evaluator
    "FeatureFlagEvaluator",
    "feature_flag_evaluator",
    "feature_enabled",
    # Configuration
    "FeatureFlagConfiguration",
    "FeatureEvaluationConfiguration",
    "DEFAULT_FEATURE_EVALUATION_CONFIGURATION",
    # Types
    "FeatureKey",
    "FeatureName",
    "FeatureValue",
    "FeatureContext",
    "TenantID",
    "OrganizationID",
    # Constants
    "FEATURE_ENABLED",
    "FEATURE_DISABLED",
    "FEATURE_DEFAULT",
    "DEFAULT_FEATURE_STATE",
    "DEFAULT_EVALUATION_STRATEGY",
    "STRATEGY_BOOLEAN",
    "STRATEGY_TENANT",
    "STRATEGY_ORGANIZATION",
    "STRATEGY_SUBSCRIPTION",
    "STRATEGY_PERCENTAGE",
    "CATEGORY_CORE",
    "CATEGORY_MODULE",
    "CATEGORY_AI",
    "CATEGORY_ENTERPRISE",
    "CATEGORY_EXPERIMENTAL",
    # Exceptions
    "FeatureFlagError",
    "FeatureFlagConfigurationError",
    "FeatureFlagRegistrationError",
    "FeatureFlagAlreadyRegisteredError",
    "FeatureFlagNotFoundError",
    "FeatureFlagEvaluationError",
    "FeatureFlagContextError",
)
