"""
DatavionOS audit framework.

Provides the public API for platform audit capabilities.

Supports:

- Audit record creation
- Actor tracking
- Tenant-aware auditing
- Resource change tracking
- Audit handler registration
- Compliance-ready audit processing

Business applications should import audit utilities from this
package instead of internal modules.
"""

from __future__ import annotations

from .config import (
    DEFAULT_AUDIT_COMPLIANCE_CONFIGURATION,
    DEFAULT_AUDIT_CONFIGURATION,
    DEFAULT_AUDIT_RETENTION_CONFIGURATION,
    AuditComplianceConfiguration,
    AuditConfiguration,
    AuditRetentionConfiguration,
)
from .constants import (
    ACTION_APPROVE,
    ACTION_CREATE,
    ACTION_DELETE,
    ACTION_EXPORT,
    ACTION_IMPORT,
    ACTION_LOGIN,
    ACTION_LOGOUT,
    ACTION_READ,
    ACTION_REJECT,
    ACTION_UPDATE,
    CATEGORY_AUTHENTICATION,
    CATEGORY_AUTHORIZATION,
    CATEGORY_CONFIGURATION,
    CATEGORY_DATA,
    CATEGORY_INTEGRATION,
    CATEGORY_SECURITY,
    CATEGORY_SYSTEM,
    CATEGORY_WORKFLOW,
    DEFAULT_ACTION,
    DEFAULT_CATEGORY,
    DEFAULT_LEVEL,
    LEVEL_CRITICAL,
    LEVEL_ERROR,
    LEVEL_INFO,
    LEVEL_WARNING,
)
from .exceptions import (
    AuditAlreadyRegisteredError,
    AuditConfigurationError,
    AuditContextError,
    AuditError,
    AuditNotFoundError,
    AuditRecordError,
    AuditRecordingError,
    AuditRegistryError,
    AuditStorageError,
)
from .models import (
    AuditActor,
    AuditChange,
    AuditRecord,
    AuditResult,
)
from .recorder import (
    AuditRecorder,
    audit_recorder,
)
from .registry import (
    AuditHandler,
    AuditRegistry,
    audit_registry,
)
from .services import (
    AuditService,
    audit_service,
)
from .types import (
    ActorID,
    AuditAction,
    AuditCategory,
    AuditChanges,
    AuditContext,
    AuditID,
    AuditMetadata,
    AuditResource,
    OrganizationID,
    TenantID,
)

__all__: tuple[str, ...] = (
    # Models
    "AuditActor",
    "AuditChange",
    "AuditRecord",
    "AuditResult",
    # Services
    "AuditService",
    "audit_service",
    # Recorder
    "AuditRecorder",
    "audit_recorder",
    # Registry
    "AuditHandler",
    "AuditRegistry",
    "audit_registry",
    # Types
    "AuditID",
    "AuditAction",
    "AuditCategory",
    "AuditResource",
    "AuditChanges",
    "AuditContext",
    "AuditMetadata",
    "ActorID",
    "TenantID",
    "OrganizationID",
    # Configuration
    "AuditConfiguration",
    "AuditRetentionConfiguration",
    "AuditComplianceConfiguration",
    "DEFAULT_AUDIT_CONFIGURATION",
    "DEFAULT_AUDIT_RETENTION_CONFIGURATION",
    "DEFAULT_AUDIT_COMPLIANCE_CONFIGURATION",
    # Actions
    "ACTION_CREATE",
    "ACTION_READ",
    "ACTION_UPDATE",
    "ACTION_DELETE",
    "ACTION_LOGIN",
    "ACTION_LOGOUT",
    "ACTION_EXPORT",
    "ACTION_IMPORT",
    "ACTION_APPROVE",
    "ACTION_REJECT",
    # Categories
    "CATEGORY_AUTHENTICATION",
    "CATEGORY_AUTHORIZATION",
    "CATEGORY_DATA",
    "CATEGORY_SECURITY",
    "CATEGORY_CONFIGURATION",
    "CATEGORY_WORKFLOW",
    "CATEGORY_SYSTEM",
    "CATEGORY_INTEGRATION",
    # Levels
    "LEVEL_INFO",
    "LEVEL_WARNING",
    "LEVEL_ERROR",
    "LEVEL_CRITICAL",
    # Defaults
    "DEFAULT_ACTION",
    "DEFAULT_CATEGORY",
    "DEFAULT_LEVEL",
    # Exceptions
    "AuditError",
    "AuditConfigurationError",
    "AuditRecordError",
    "AuditRecordingError",
    "AuditStorageError",
    "AuditRegistryError",
    "AuditAlreadyRegisteredError",
    "AuditNotFoundError",
    "AuditContextError",
)
