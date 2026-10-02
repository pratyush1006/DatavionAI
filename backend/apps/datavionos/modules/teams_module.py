from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)


def teams_module() -> ModuleContract:
    return ModuleContract(
        identifier="teams",
        name="Teams",
        display_name="Teams",
        category=ModuleCategory.CORE,
        version="1.0.0",
        description="Organization teams and collaborative membership.",
        icon="/static/datavionos/icons/teams.svg",
        route="/workspace/teams",
        api_prefix="/api/teams",
        enabled=True,
        system=True,
        tenant_scoped=True,
        order=40,
        navigation=NavigationConfig(
            title="Teams",
            route="/workspace/teams",
            icon="users-round",
            category="core",
            order=40,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Teams",
            description="Organization teams and collaborative membership.",
            icon="users-round",
            route="/workspace/teams",
            order=40,
        ),
        tags=("core", "organization", "teams"),
        permissions=("teams.view",),
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
