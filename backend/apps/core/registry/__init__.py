"""
DatavionOS platform registry package.

Provides the public registry API for the DatavionOS kernel.

Registries included:

- Module registry
- Feature registry
- Permission registry
- Provider registry

The registry layer enables:

- Dynamic module discovery
- Subscription capability management
- RBAC permission discovery
- External provider registration
"""

from __future__ import annotations

from .base import (
    Registry,
    RegistryAlreadyRegisteredError,
    RegistryNotFoundError,
)
from .feature import (
    FeatureDefinition,
    feature_registry,
)
from .module import (
    ModuleDefinition,
    module_registry,
)
from .permission import (
    PermissionDefinition,
    permission_registry,
)
from .provider import (
    ProviderDefinition,
    provider_registry,
)

__all__: tuple[str, ...] = (
    # Base Registry
    "Registry",
    "RegistryAlreadyRegisteredError",
    "RegistryNotFoundError",
    # Module Registry
    "ModuleDefinition",
    "module_registry",
    # Feature Registry
    "FeatureDefinition",
    "feature_registry",
    # Permission Registry
    "PermissionDefinition",
    "permission_registry",
    # Provider Registry
    "ProviderDefinition",
    "provider_registry",
)
