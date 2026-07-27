"""
Application configuration for the Patient Documents module.
"""

from django.apps import AppConfig


class PatientDocumentsConfig(AppConfig):
    """
    Configuration for the Patient Documents application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.patient_management.patient_documents"

    verbose_name = "Patient Documents"
