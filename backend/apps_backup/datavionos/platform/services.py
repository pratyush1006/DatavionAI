"""
Platform services aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.platform.audit import (
    AuditService,
)
from apps.datavionos.platform.cache import (
    CacheProvider,
)
from apps.datavionos.platform.configuration import (
    ConfigurationProvider,
)
from apps.datavionos.platform.feature_flags import (
    FeatureFlagService,
)
from apps.datavionos.platform.health import (
    HealthRegistry,
)
from apps.datavionos.platform.logger import (
    Logger,
)
from apps.datavionos.platform.metrics import (
    MetricsCollector,
)
from apps.datavionos.platform.notifications import (
    NotificationService,
)
from apps.datavionos.platform.scheduler import (
    Scheduler,
)
from apps.datavionos.platform.secrets import (
    SecretProvider,
)
from apps.datavionos.platform.storage import (
    StorageProvider,
)
from apps.datavionos.platform.telemetry import (
    TelemetryService,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformServices:
    """
    Aggregates all DatavionOS platform
    service contracts.

    This object is passed throughout
    the platform instead of injecting
    individual services separately.
    """

    logger: Logger

    metrics: MetricsCollector

    telemetry: TelemetryService

    audit: AuditService

    feature_flags: FeatureFlagService

    configuration: ConfigurationProvider

    health: HealthRegistry

    scheduler: Scheduler

    cache: CacheProvider

    storage: StorageProvider

    notifications: NotificationService

    secrets: SecretProvider


__all__ = [
    "PlatformServices",
]
