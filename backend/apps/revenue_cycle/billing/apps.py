from django.apps import AppConfig


class RCMBillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.billing"
    label = "revenue_cycle_billing"
    verbose_name = "Revenue Cycle Billing"
