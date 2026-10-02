"""
Notifications application configuration.
"""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """
    Notifications application configuration.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.platform.notifications"

    label = "notifications"

    verbose_name = "Notifications"
