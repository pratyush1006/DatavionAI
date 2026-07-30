"""
Department settings domain services.

Manages department configuration.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.organization.departments.models import (
    Department,
    DepartmentSetting,
)
from django.db import transaction

type DepartmentSettingsData = Mapping[str, Any]


class DepartmentSettingsService:
    """
    Department configuration services.
    """

    @staticmethod
    @transaction.atomic
    def create_default(
        *,
        department: Department,
    ) -> DepartmentSetting:
        """
        Create default department settings.
        """

        setting = DepartmentSetting(
            department=department,
            configuration={},
        )

        setting.full_clean()

        setting.save()

        return setting

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: DepartmentSetting,
        configuration: DepartmentSettingsData,
    ) -> DepartmentSetting:
        """
        Update department configuration.
        """

        if instance.is_locked:
            raise PermissionError("Department settings are locked.")

        instance.configuration = dict(
            configuration,
        )

        instance.full_clean()

        instance.save(
            update_fields=[
                "configuration",
            ],
        )

        return instance

    @staticmethod
    def get_configuration(
        *,
        department: Department,
    ) -> dict:
        """
        Return department configuration.
        """

        try:
            return department.department_settings.configuration

        except DepartmentSetting.DoesNotExist:
            return {}

    @staticmethod
    @transaction.atomic
    def lock(
        *,
        instance: DepartmentSetting,
    ) -> DepartmentSetting:
        """
        Lock configuration changes.
        """

        instance.is_locked = True

        instance.save(
            update_fields=[
                "is_locked",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def unlock(
        *,
        instance: DepartmentSetting,
    ) -> DepartmentSetting:
        """
        Unlock configuration changes.
        """

        instance.is_locked = False

        instance.save(
            update_fields=[
                "is_locked",
            ],
        )

        return instance


__all__ = ("DepartmentSettingsService",)
