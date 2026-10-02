"""
SaaS Billing application configuration.

DatavionOS billing domain:

- Billing Accounts
- Plans
- Subscriptions
- Invoices
- Payments
- Usage Metering
- Entitlements
- Domain Events
- Workflow Engine
"""

from django.apps import AppConfig


class SaaSBillingConfig(
    AppConfig,
):
    """
    DatavionOS SaaS Billing configuration.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.saas_billing"

    label = "saas_billing"

    verbose_name = "DatavionOS SaaS Billing"

    _initialized = False

    def ready(
        self,
    ):
        """
        Application startup hooks.

        Registers:

        - Domain events
        - Event handlers
        - Billing workflows
        """

        if self._initialized:
            return

        self._initialized = True

        from .events.registry import (
            register_billing_events,
        )
        from .workflows.registration import (
            register_billing_workflows,
        )

        register_billing_events()

        register_billing_workflows()
