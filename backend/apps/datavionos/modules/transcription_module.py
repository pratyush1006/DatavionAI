from apps.datavionos.constants.capability import ModuleCategory, ModuleStatus
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

MODULE_ID = "transcription"


def transcription_module() -> ModuleContract:
    return ModuleContract(
        identifier=MODULE_ID,
        name="Transcription",
        display_name="Transcription",
        category=ModuleCategory.CLINICAL,
        version="1.0.0",
        description="Transcription workspace and operational capabilities.",
        icon="/static/datavionos/icons/transcription.svg",
        route="/workspace/transcription",
        api_prefix="/api/transcription",
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=180,
        navigation=NavigationConfig(
            title="Transcription",
            route="/workspace/transcription",
            icon="grid",
            category="clinical",
            order=180,
        ),
        dashboard=DashboardConfig(
            enabled=True,
            title="Transcription",
            description="Transcription workspace and operational capabilities.",
            icon="grid",
            route="/workspace/transcription",
            order=180,
        ),
        tags=("clinical", "transcription"),
        permissions=("transcription.view",),
        dependencies=(),
        optional_dependencies=(),
        feature_flags=(),
        metadata={
            "domain": "clinical",
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
