"""
DatavionOS platform contracts.

This package defines the public platform abstractions used by the
kernel, tenant runtime, modules, workflows, AI runtime, and plugins.

Only stable public contracts are exported from this package.
"""

from .audit import (
    AuditRecord,
    AuditService,
    AuditSeverity,
)
from .cache import (
    CacheLock,
    CacheOptions,
    CacheProvider,
)
from .configuration import (
    ConfigurationContext,
    ConfigurationProvider,
    ConfigurationScope,
)
from .exceptions import (
    AuditError,
    CacheError,
    ConfigurationProviderError,
    FeatureFlagError,
    HealthRegistryError,
    LoggerError,
    MetricsError,
    NotificationError,
    PlatformError,
    SchedulerError,
    SecretProviderError,
    StorageError,
    TelemetryError,
)
from .feature_flags import (
    FeatureContext,
    FeatureFlagService,
    FeatureScope,
)
from .health import (
    HealthCheck,
    HealthProbe,
    HealthRegistry,
    HealthResult,
    HealthStatus,
)
from .logger import (
    Logger,
    LogScope,
)
from .metrics import (
    MetricsCollector,
    MetricTags,
    Timer,
)
from .notifications import (
    NotificationChannel,
    NotificationMessage,
    NotificationPriority,
    NotificationRecipient,
    NotificationResult,
    NotificationService,
    NotificationStatus,
)
from .scheduler import (
    Job,
    JobContext,
    JobResult,
    JobStatus,
    JobTrigger,
    Scheduler,
    TriggerType,
)
from .secrets import (
    SecretContext,
    SecretMetadata,
    SecretProvider,
    SecretScope,
)
from .services import (
    PlatformServices,
)
from .storage import (
    SignedUrl,
    StorageObject,
    StorageProvider,
    UploadOptions,
)
from .telemetry import (
    Span,
    TelemetryAttributes,
    TelemetryService,
    Tracer,
)

__all__ = [
    # Aggregate
    "PlatformServices",
    # Logger
    "Logger",
    "LogScope",
    # Metrics
    "MetricsCollector",
    "MetricTags",
    "Timer",
    # Telemetry
    "TelemetryAttributes",
    "Span",
    "Tracer",
    "TelemetryService",
    # Audit
    "AuditSeverity",
    "AuditRecord",
    "AuditService",
    # Feature Flags
    "FeatureScope",
    "FeatureContext",
    "FeatureFlagService",
    # Configuration
    "ConfigurationScope",
    "ConfigurationContext",
    "ConfigurationProvider",
    # Health
    "HealthStatus",
    "HealthProbe",
    "HealthResult",
    "HealthCheck",
    "HealthRegistry",
    # Scheduler
    "TriggerType",
    "JobStatus",
    "JobTrigger",
    "JobContext",
    "JobResult",
    "Job",
    "Scheduler",
    # Cache
    "CacheOptions",
    "CacheLock",
    "CacheProvider",
    # Storage
    "StorageObject",
    "UploadOptions",
    "SignedUrl",
    "StorageProvider",
    # Notifications
    "NotificationChannel",
    "NotificationPriority",
    "NotificationStatus",
    "NotificationRecipient",
    "NotificationMessage",
    "NotificationResult",
    "NotificationService",
    # Secrets
    "SecretScope",
    "SecretContext",
    "SecretMetadata",
    "SecretProvider",
    # Exceptions
    "PlatformError",
    "LoggerError",
    "MetricsError",
    "TelemetryError",
    "AuditError",
    "FeatureFlagError",
    "ConfigurationProviderError",
    "HealthRegistryError",
    "SchedulerError",
    "CacheError",
    "StorageError",
    "NotificationError",
    "SecretProviderError",
]
