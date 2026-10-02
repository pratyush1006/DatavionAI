from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)


def department_manager_module() -> ModuleContract:
    return ModuleContract(
        identifier="department-manager",
        name="Department Manager",
        display_name="Department Manager",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Department staffing, patient activity, appointments, tasks, and performance.",
        icon="/static/datavionos/icons/departments.svg",
        route="/workspace/department-manager",
        api_prefix="/api/departments",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=22,
        navigation=NavigationConfig(
            title="Department Manager",
            route="/workspace/department-manager",
            icon="building",
            category="operations",
            order=22,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Department Manager",
            description="Department operational management.",
            icon="building",
            route="/workspace/department-manager",
            order=22,
        ),
        tags=("operations", "departments", "management"),
        permissions=("departments.view",),
        dependencies=("departments",),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "organization",
            "source": "datavionos-canonical-module-catalog",
        },
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )
