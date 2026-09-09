"""
Django application configuration for Revenue Cycle.

Workflow registration is intentionally deferred until ``ready()`` so that
Django can complete application and model initialization before Revenue Cycle
loads workflow implementations.
"""

from __future__ import annotations

from django.apps import AppConfig


class RevenueCycleConfig(AppConfig):
    """Configure the Revenue Cycle bounded context."""

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.revenue_cycle"

    label = "revenue_cycle"

    verbose_name = "Revenue Cycle"

    def ready(self) -> None:
        """
        Register Revenue Cycle workflows after Django initialization.

        Workflow registries are imported lazily here to prevent application
        registry initialization errors caused by workflow implementations
        importing Django models.
        """

        from apps.revenue_cycle.insurance_verification.workflow_registry import (
            register_workflows as register_insurance_verification_workflows,
        )
        from apps.revenue_cycle.prior_authorization.workflow_registry import (
            register_workflows as register_prior_authorization_workflows,
        )

        register_prior_authorization_workflows()
        register_insurance_verification_workflows()


__all__: tuple[str, ...] = ("RevenueCycleConfig",)
