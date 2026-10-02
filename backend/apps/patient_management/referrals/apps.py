"""
Django application configuration for Patient Referrals.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientReferralsConfig(AppConfig):
    """Configure the Patient Referrals application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.referrals"
    label = "patient_referrals"
    verbose_name = _("Patient Referrals")


__all__ = ("PatientReferralsConfig",)
