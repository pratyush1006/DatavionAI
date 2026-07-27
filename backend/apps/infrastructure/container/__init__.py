"""
DatavionOS dependency injection container.
"""

from apps.infrastructure.container.container import (
    Container,
)
from apps.infrastructure.container.exceptions import (
    CircularDependencyError,
    ContainerError,
    DuplicateServiceRegistrationError,
    InvalidServiceRegistrationError,
    ScopedServiceResolutionError,
    ServiceNotRegisteredError,
)
from apps.infrastructure.container.registry import (
    ServiceLifetime,
    ServiceRegistration,
)
from apps.infrastructure.container.service_provider import (
    ServiceProvider,
)

__all__ = [
    "Container",
    "ContainerError",
    "ServiceNotRegisteredError",
    "DuplicateServiceRegistrationError",
    "InvalidServiceRegistrationError",
    "CircularDependencyError",
    "ScopedServiceResolutionError",
    "ServiceLifetime",
    "ServiceRegistration",
    "ServiceProvider",
]
