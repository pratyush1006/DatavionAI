"""
Application configuration for the Organizations app.
"""

from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    """
    Configuration for the Organizations application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.organizations"

    verbose_name = "Organizations"
