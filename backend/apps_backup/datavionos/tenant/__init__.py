"""
DatavionOS tenant runtime contracts.
"""

from .context import (
    TenantContext,
)
from .exceptions import (
    OrganizationNotFoundError,
    SubscriptionError,
    TenantAccessDeniedError,
    TenantError,
    TenantNotFoundError,
    TenantResolutionError,
)
from .organization import (
    Organization,
    OrganizationStatus,
    OrganizationType,
)
from .resolver import (
    TenantResolver,
)
from .services import (
    TenantServices,
)
from .subscription import (
    Subscription,
    SubscriptionPlan,
    SubscriptionStatus,
)
from .tenant import (
    Tenant,
    TenantStatus,
)
from .user import (
    User,
    UserStatus,
)

__all__ = [
    # Runtime
    "TenantContext",
    "TenantServices",
    "TenantResolver",
    # Tenant
    "Tenant",
    "TenantStatus",
    # Organization
    "Organization",
    "OrganizationType",
    "OrganizationStatus",
    # Subscription
    "Subscription",
    "SubscriptionPlan",
    "SubscriptionStatus",
    # User
    "User",
    "UserStatus",
    # Exceptions
    "TenantError",
    "TenantNotFoundError",
    "OrganizationNotFoundError",
    "SubscriptionError",
    "TenantResolutionError",
    "TenantAccessDeniedError",
]
