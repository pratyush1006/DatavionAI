"""
Django application configuration for Patient Family Members.
"""

from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FamilyMembersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.family_members"
    label = "patient_family_members"
    verbose_name = _("Patient Family Members")

    def ready(self) -> None:
        from apps.patient_management.family_members.workflow_registry import (
            register_family_member_workflows,
        )

        register_family_member_workflows()


__all__ = ("FamilyMembersConfig",)
