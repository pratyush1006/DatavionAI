from django.apps import AppConfig


class DevicePlatformConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.device_platform"
    label = "device_platform"
    verbose_name = "Device Platform"

    def ready(self):
        from apps.device_platform.workflow_registry import register_device_workflows

        register_device_workflows()
