"""
DatavionOS Dependency Injection Framework.

Provides the enterprise dependency injection
container used throughout DatavionOS.
"""

from __future__ import annotations

from apps.datavionos.container.builder import (
    ContainerBuilder,
)
from apps.datavionos.container.container import (
    Container,
)
from apps.datavionos.container.descriptor import (
    FactoryType,
    ServiceDescriptor,
)
from apps.datavionos.container.exceptions import (
    CircularDependencyError,
    ContainerBuildError,
    ContainerError,
    DuplicateRegistrationError,
    FrozenContainerError,
    InvalidDescriptorError,
    RegistrationError,
    ResolutionError,
    ScopeError,
    ServiceNotFoundError,
)
from apps.datavionos.container.lifetime import (
    ServiceLifetime,
    is_cacheable,
    is_scoped,
    is_singleton,
    is_transient,
    requires_scope,
)
from apps.datavionos.container.provider import (
    ServiceProvider,
)
from apps.datavionos.container.registry import (
    ServiceRegistry,
)
from apps.datavionos.container.resolver import (
    ServiceResolver,
)
from apps.datavionos.container.scope import (
    ServiceScope,
)
from apps.datavionos.container.service import (
    AsyncDisposable,
    AsyncInitializable,
    Disposable,
    HealthCheck,
    Initializable,
    Service,
    Startable,
    Stoppable,
)

__all__ = [
    # Core
    "Container",
    "ContainerBuilder",
    # Registration
    "ServiceDescriptor",
    "FactoryType",
    "ServiceLifetime",
    # Runtime
    "ServiceRegistry",
    "ServiceResolver",
    "ServiceProvider",
    "ServiceScope",
    # Lifecycle
    "Service",
    "Disposable",
    "AsyncDisposable",
    "Initializable",
    "AsyncInitializable",
    "HealthCheck",
    "Startable",
    "Stoppable",
    # Lifetime Helpers
    "is_singleton",
    "is_scoped",
    "is_transient",
    "requires_scope",
    "is_cacheable",
    # Exceptions
    "ContainerError",
    "RegistrationError",
    "DuplicateRegistrationError",
    "InvalidDescriptorError",
    "ResolutionError",
    "ServiceNotFoundError",
    "CircularDependencyError",
    "ScopeError",
    "ContainerBuildError",
    "FrozenContainerError",
]
