from django.apps import AppConfig


class ModuleRegistryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.platform.module_registry"
    verbose_name = "Module Registry"
