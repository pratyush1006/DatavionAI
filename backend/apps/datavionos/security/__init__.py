"""
DatavionOS Security Contracts.
"""

from .authentication import (
    AuthenticationRequest,
    AuthenticationResult,
    AuthenticationService,
)
from .authorization import (
    AuthorizationRequest,
    AuthorizationResult,
    AuthorizationService,
)
from .context import (
    SecurityContext,
)
from .evaluator import (
    AuthorizationEvaluator,
)
from .identity import (
    Identity,
    IdentityProvider,
    IdentityStatus,
)
from .permission import (
    Permission,
    PermissionScope,
)
from .policy import (
    Policy,
    PolicyContext,
    PolicyEffect,
    PolicyResult,
)
from .principal import (
    Principal,
    PrincipalType,
)
from .role import (
    Role,
    RoleScope,
)
from .services import (
    SecurityServices,
)

__all__ = [
    # Exceptions
    "SecurityError",
    "AuthenticationError",
    "AuthorizationError",
    "IdentityNotFoundError",
    "PrincipalNotFoundError",
    "PermissionDeniedError",
    "PolicyEvaluationError",
    "InvalidCredentialError",
    "SessionExpiredError",
    "MultiFactorAuthenticationRequiredError",
    # Authentication
    "AuthenticationRequest",
    "AuthenticationResult",
    "AuthenticationService",
    # Authorization
    "AuthorizationRequest",
    "AuthorizationResult",
    "AuthorizationService",
    # Identity
    "Identity",
    "IdentityProvider",
    "IdentityStatus",
    # Principal
    "Principal",
    "PrincipalType",
    # Role
    "Role",
    "RoleScope",
    # Permission
    "Permission",
    "PermissionScope",
    # Policy
    "Policy",
    "PolicyContext",
    "PolicyEffect",
    "PolicyResult",
    # Context
    "SecurityContext",
    # Evaluator
    "AuthorizationEvaluator",
    # Aggregate
    "SecurityServices",
]
