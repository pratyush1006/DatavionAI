"""
AI assistant module contracts for DatavionOS.
"""

from __future__ import annotations

from apps.datavionos.constants import (
    ModuleCategory,
    ModuleStatus,
)
from apps.datavionos.contracts.module import (
    DashboardConfig,
    ModuleContract,
    NavigationConfig,
)

AI_ASSISTANT_MODULE_ID = "ai-assistant"


def ai_assistant_module() -> ModuleContract:
    """
    Return the AI Assistant module contract.
    """

    return ModuleContract(
        # ------------------------------------------------------------------
        # Identity
        # ------------------------------------------------------------------
        identifier=AI_ASSISTANT_MODULE_ID,
        name="AI Assistant",
        display_name="AI Assistant",
        category=ModuleCategory.AI,
        version="1.0.0",
        description=(
            "AI copilot for clinical documentation and decision support (assistive)."
        ),
        icon="/static/datavionos/icons/ai-assistant.svg",
        route="/ai/assistant",
        api_prefix="/api/ai/assistant",
        # ------------------------------------------------------------------
        # Runtime
        # ------------------------------------------------------------------
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=40,
        # ------------------------------------------------------------------
        # Navigation
        # ------------------------------------------------------------------
        navigation=NavigationConfig(
            title="AI Assistant",
            route="/ai/assistant",
            icon="sparkles",
            category="ai",
            order=40,
        ),
        # ------------------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------------------
        dashboard=DashboardConfig(
            enabled=True,
            title="AI Assistant",
            description=(
                "AI-powered clinical assistant for documentation and decision support."
            ),
            icon="sparkles",
            route="/ai/assistant",
            order=40,
        ),
        # ------------------------------------------------------------------
        # Discovery
        # ------------------------------------------------------------------
        tags=(
            "ai",
            "assistant",
        ),
        # ------------------------------------------------------------------
        # RBAC
        # ------------------------------------------------------------------
        permissions=("ai.view",),
        # ------------------------------------------------------------------
        # Dependencies
        # ------------------------------------------------------------------
        dependencies=(),
        optional_dependencies=(),
        # ------------------------------------------------------------------
        # Feature Entitlement
        # ------------------------------------------------------------------
        feature_flags=("ai_assistant",),
        # ------------------------------------------------------------------
        # SaaS Metadata
        # ------------------------------------------------------------------
        metadata={
            "assistive": True,
            "tenant_types": [
                "clinic",
                "hospital",
                "enterprise",
            ],
        },
        # ------------------------------------------------------------------
        # Lifecycle
        # ------------------------------------------------------------------
        status=ModuleStatus.ACTIVE,
        # ------------------------------------------------------------------
        # Ownership
        # ------------------------------------------------------------------
        owner="datavionos",
        homepage="",
        documentation="",
        support_email="",
        license="",
    )


__all__ = [
    "AI_ASSISTANT_MODULE_ID",
    "ai_assistant_module",
]
