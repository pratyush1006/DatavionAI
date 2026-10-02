"""
Django application configuration for the DatavionOS kernel.
"""

from __future__ import annotations

from django.apps import AppConfig


class DatavionOSConfig(AppConfig):
    """
    Django application configuration for the DatavionOS kernel.

    The DatavionOS kernel serves as the runtime foundation of the
    DatavionAI platform. It is responsible for orchestrating platform
    capabilities such as plugin registration, runtime composition,
    capability resolution, and application bootstrap.

    The application configuration intentionally performs minimal work
    during Django startup. Runtime initialization is deferred to the
    kernel lifecycle manager to keep imports deterministic and avoid
    circular dependencies.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.datavionos"

    label = "datavionos"

    verbose_name = "DatavionOS"

    def ready(self) -> None:
        """
        Perform lightweight application initialization.

        This method should remain free of heavy startup logic.
        Runtime services, registries, event buses, schedulers,
        and plugin discovery are initialized explicitly by the
        DatavionOS kernel lifecycle rather than during Django's
        application loading process.

        Keeping this method lightweight improves startup time,
        simplifies testing, and prevents circular imports.
        """
        # Register DatavionOS module contracts used by navigation/dashboard.
        try:
            from apps.datavionos.module_registry_initializer import (
                initialize_module_registry,
            )

            initialize_module_registry()

        except Exception:
            # Module contract registration must never break Django startup.
            # Failures will surface when modules are missing from navigation.
            return
