from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "hr"


def hr_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Human Resources",
        display_name="Human Resources",
        category=ModuleCategory.UTILITY,
        version="1.0.0",
        description="Human Resources workspace and operational capabilities.",
        icon="/static/datavionos/icons/hr.svg",
        route="/workspace/hr",
        api_prefix="/api/hr",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=160,
        navigation=NavigationConfig(
            title="Human Resources",
            route="/workspace/hr",
            icon="grid",
            category="utility",
            order=160,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Human Resources",
            description="Human Resources workspace and operational capabilities.",
            icon="grid",
            route="/workspace/hr",
            order=160,
        ),
        tags=("utility", "hr"),
        permissions=("hr.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "utility",
            "tenant_types": ("clinic", "hospital", "enterprise"),
            "source": "datavionos-canonical-module-catalog",
        },
        status=ModuleStatus.ACTIVE,
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )
