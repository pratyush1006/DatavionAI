"""
DatavionAI Exception Framework.

Enterprise exception framework for the DatavionAI platform.

Provides:

- Base exception hierarchy
- Standardized error contracts
- Error codes
- Exception utilities
- DRF integration

Public application imports should use this package.
"""

from __future__ import annotations

from . import (
    base,
    builders,
    codes,
    handlers,
    messages,
    mixins,
    registry,
    utils,
)
from .base import (
    AuditException,
    AuthenticationException,
    AuthorizationException,
    CacheException,
    ClientException,
    ConfigurationException,
    DatabaseException,
    DatavionException,
    IntegrationException,
    ResourceConflictException,
    ResourceNotFoundException,
    ServerException,
    ValidationException,
    WorkflowException,
)
from .codes import (
    ErrorCode,
)

__all__ = (
    # Modules
    "base",
    "builders",
    "codes",
    "handlers",
    "messages",
    "mixins",
    "registry",
    "utils",
    # Error Codes
    "ErrorCode",
    # Base Exceptions
    "DatavionException",
    "ClientException",
    "ServerException",
    # Client Exceptions
    "ValidationException",
    "AuthenticationException",
    "AuthorizationException",
    "ResourceNotFoundException",
    "ResourceConflictException",
    # Server Exceptions
    "DatabaseException",
    "CacheException",
    "IntegrationException",
    "ConfigurationException",
    "WorkflowException",
    "AuditException",
)
