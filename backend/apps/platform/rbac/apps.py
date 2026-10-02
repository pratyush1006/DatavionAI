from django.apps import AppConfig


class RBACConfig(AppConfig):
    """
    RBAC application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.rbac"

    label = "rbac"

    verbose_name = "Role Based Access Control"
