"""
DatavionOS configuration contracts.
"""

from __future__ import annotations

from .configuration import (
    ConfigurationEntry,
    ConfigurationScope,
    ConfigurationSnapshot,
)
from .exceptions import (
    ConfigurationError,
    ConfigurationProviderError,
    ConfigurationValidationError,
    SecretProviderError,
)
from .provider import (
    ConfigurationProvider,
)
from .secrets import (
    Secret,
    SecretProvider,
)
from .services import (
    ConfigurationServices,
)
from .validation import (
    ConfigurationValidator,
    ValidationError,
    ValidationResult,
)

__all__ = [
    # Configuration
    "ConfigurationEntry",
    "ConfigurationScope",
    "ConfigurationSnapshot",
    # Provider
    "ConfigurationProvider",
    # Secrets
    "Secret",
    "SecretProvider",
    # Validation
    "ConfigurationValidator",
    "ValidationError",
    "ValidationResult",
    # Service aggregation
    "ConfigurationServices",
    # Exceptions
    "ConfigurationError",
    "ConfigurationProviderError",
    "SecretProviderError",
    "ConfigurationValidationError",
]
