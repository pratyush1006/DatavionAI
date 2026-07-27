"""
DatavionOS Kernel Configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class KernelConfiguration:
    """
    Immutable runtime configuration for
    the DatavionOS Kernel.
    """

    #
    # Application
    #

    application_name: str = "DatavionOS"

    application_version: str = "1.0.0"

    environment: str = "development"

    debug: bool = False

    #
    # Runtime
    #

    enable_dependency_injection: bool = True

    enable_commands: bool = True

    enable_queries: bool = True

    enable_events: bool = True

    enable_scheduler: bool = True

    enable_workflows: bool = True

    enable_messaging: bool = True

    enable_observability: bool = True

    enable_ai_runtime: bool = True

    #
    # Discovery
    #

    module_packages: tuple[str, ...] = ()

    plugin_packages: tuple[str, ...] = ()

    #
    # Infrastructure
    #

    request_timeout: int = 30

    shutdown_timeout: int = 30

    health_check_interval: int = 60

    max_parallel_tasks: int = 4

    #
    # Logging
    #

    log_level: str = "INFO"

    structured_logging: bool = True

    #
    # Metadata
    #

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def is_development(
        self,
    ) -> bool:
        """
        Whether the runtime is running
        in development mode.
        """

        return self.environment.lower() == "development"

    @property
    def is_testing(
        self,
    ) -> bool:
        """
        Whether the runtime is running
        in testing mode.
        """

        return self.environment.lower() == "testing"

    @property
    def is_production(
        self,
    ) -> bool:
        """
        Whether the runtime is running
        in production mode.
        """

        return self.environment.lower() == "production"

    def with_metadata(
        self,
        **metadata: Any,
    ) -> KernelConfiguration:
        """
        Return a new configuration with
        merged metadata.
        """

        updated = dict(
            self.metadata,
        )

        updated.update(
            metadata,
        )

        return KernelConfiguration(
            application_name=self.application_name,
            application_version=self.application_version,
            environment=self.environment,
            debug=self.debug,
            enable_dependency_injection=self.enable_dependency_injection,
            enable_commands=self.enable_commands,
            enable_queries=self.enable_queries,
            enable_events=self.enable_events,
            enable_scheduler=self.enable_scheduler,
            enable_workflows=self.enable_workflows,
            enable_messaging=self.enable_messaging,
            enable_observability=self.enable_observability,
            enable_ai_runtime=self.enable_ai_runtime,
            module_packages=self.module_packages,
            plugin_packages=self.plugin_packages,
            request_timeout=self.request_timeout,
            shutdown_timeout=self.shutdown_timeout,
            health_check_interval=self.health_check_interval,
            max_parallel_tasks=self.max_parallel_tasks,
            log_level=self.log_level,
            structured_logging=self.structured_logging,
            metadata=updated,
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "KernelConfiguration("
            f"application={self.application_name}, "
            f"environment={self.environment}, "
            f"debug={self.debug})"
        )


__all__ = [
    "KernelConfiguration",
]
