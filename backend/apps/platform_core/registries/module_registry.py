"""
Platform module registry.
"""

from __future__ import annotations

from apps.platform_core.registries.base import BaseRegistry
from apps.platform_core.registries.module import PlatformModule


class ModuleRegistry(
    BaseRegistry[PlatformModule],
):
    """
    Registry of platform modules.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self._register_defaults()

    def _register_defaults(
        self,
    ) -> None:
        """
        Register built-in platform modules.
        """

        self.register(
            "organizations",
            PlatformModule(
                key="organizations",
                title="Organizations",
                description="Organization Management",
                route="/organizations",
                icon="building",
                permission="organizations.view_organization",
                category="Administration",
                order=10,
            ),
        )

        self.register(
            "departments",
            PlatformModule(
                key="departments",
                title="Departments",
                description="Department Management",
                route="/departments",
                icon="layers",
                permission="departments.view_department",
                category="Administration",
                order=20,
            ),
        )

        self.register(
            "teams",
            PlatformModule(
                key="teams",
                title="Teams",
                description="Team Management",
                route="/teams",
                icon="users",
                permission="teams.view_team",
                category="Administration",
                order=30,
            ),
        )

        self.register(
            "employees",
            PlatformModule(
                key="employees",
                title="Employees",
                description="Employee Management",
                route="/employees",
                icon="user-check",
                permission="employees.view_employee",
                category="Administration",
                order=40,
            ),
        )

        self.register(
            "patients",
            PlatformModule(
                key="patients",
                title="Patients",
                description="Patient Management",
                route="/patients",
                icon="heart",
                permission="patients.view_patient",
                category="Clinical",
                order=100,
            ),
        )

        self.register(
            "providers",
            PlatformModule(
                key="providers",
                title="Providers",
                description="Provider Management",
                route="/providers",
                icon="stethoscope",
                permission="providers.view_provider",
                category="Clinical",
                order=110,
            ),
        )

        self.register(
            "appointments",
            PlatformModule(
                key="appointments",
                title="Appointments",
                description="Appointment Management",
                route="/appointments",
                icon="calendar",
                permission="appointments.view_appointment",
                category="Clinical",
                order=120,
            ),
        )

        self.register(
            "laboratories",
            PlatformModule(
                key="laboratories",
                title="Laboratories",
                description="Laboratory Management",
                route="/laboratories",
                icon="flask",
                permission="laboratories.view_laboratoryorder",
                category="Clinical",
                order=130,
            ),
        )

        self.register(
            "configuration",
            PlatformModule(
                key="configuration",
                title="Configuration",
                description="Platform Configuration",
                route="/configuration",
                icon="settings",
                permission="configuration.view_configuration",
                category="Platform",
                order=900,
            ),
        )

        self.register(
            "storage",
            PlatformModule(
                key="storage",
                title="Storage",
                description="Asset Storage",
                route="/storage",
                icon="database",
                permission="storage.view_asset",
                category="Platform",
                order=910,
            ),
        )


module_registry = ModuleRegistry()


__all__ = [
    "ModuleRegistry",
    "module_registry",
]
