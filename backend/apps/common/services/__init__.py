"""
DatavionOS Service Framework.

Public service-layer API.

Provides:

- Base services
- Validation helpers
- Permission helpers
- Transaction helpers
- Service responses
- Service registry
"""

from __future__ import annotations

from .base import (
    BaseService,
)
from .mixins import (
    AuditMixin,
    ContextMixin,
    LoggingMixin,
    PermissionMixin,
    TransactionMixin,
    ValidationMixin,
)
from .permissions import (
    PermissionService,
)
from .registry import (
    SERVICE_REGISTRY,
    get_service,
    has_service,
    list_services,
    register_service,
    service,
    unregister_service,
)
from .response import (
    ServiceResponse,
    failure,
    success,
)
from .transaction import (
    TransactionService,
)
from .validation import (
    ValidationService,
)

__all__: tuple[str, ...] = (
    # Base
    "BaseService",
    # Mixins
    "AuditMixin",
    "ContextMixin",
    "LoggingMixin",
    "PermissionMixin",
    "TransactionMixin",
    "ValidationMixin",
    # Services
    "PermissionService",
    "TransactionService",
    "ValidationService",
    # Responses
    "ServiceResponse",
    "success",
    "failure",
    # Registry
    "SERVICE_REGISTRY",
    "register_service",
    "unregister_service",
    "get_service",
    "has_service",
    "list_services",
    "service",
)
