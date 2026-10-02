from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)


def departments_module() -> ModuleContract:
    return ModuleContract(
        identifier="departments",
        name="Departments",
        display_name="Departments",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Organization departments, structure, and membership.",
        icon="/static/datavionos/icons/departments.svg",
        route="/workspace/departments",
        api_prefix="/api/departments",
        enabled=True,
        system=True,
        tenant_scoped=True,
        order=20,
        navigation=NavigationConfig(
            title="Departments",
            route="/workspace/departments",
            icon="building",
            category="core",
            order=20,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Departments",
            description="Organization departments and membership.",
            icon="building",
            route="/workspace/departments",
            order=20,
        ),
        tags=("core", "organization", "departments"),
        permissions=("departments.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={"domain": "organization"},
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )
