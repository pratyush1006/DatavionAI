from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.billing.finance"
    label = "finance"
    verbose_name = "DatavionOS Finance"
