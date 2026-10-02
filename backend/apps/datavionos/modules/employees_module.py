from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)


def employees_module() -> ModuleContract:
    return ModuleContract(
        identifier="employees",
        name="Employees",
        display_name="Employees",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Organization employee directory and lifecycle.",
        icon="/static/datavionos/icons/employees.svg",
        route="/employees",
        api_prefix="/api/employees",
        enabled=True,
        system=True,
        tenant_scoped=True,
        order=30,
        navigation=NavigationConfig(
            title="Employees",
            route="/employees",
            icon="users",
            category="core",
            order=30,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Employees",
            description="Organization employee directory and lifecycle.",
            icon="users",
            route="/employees",
            order=30,
        ),
        tags=("core", "organization", "employees"),
        permissions=("employees.view",),
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
