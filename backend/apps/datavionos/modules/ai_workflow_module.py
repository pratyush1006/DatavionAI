"""
AI workflow module contracts for DatavionOS.

This file declares platform-level DatavionOS module contracts
for AI-powered healthcare OS features.
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

AI_WORKFLOW_MODULE_ID = "ai-workflow"


def ai_workflow_module() -> ModuleContract:
    """
    Return the AI Workflow module contract.
    """

    return ModuleContract(
        # ------------------------------------------------------------------
        # Identity
        # ------------------------------------------------------------------
        identifier=AI_WORKFLOW_MODULE_ID,
        name="AI Workflow",
        display_name="AI Workflow",
        category=ModuleCategory.AI,
        version="1.0.0",
        description=("AI-powered clinical workflows (assistive, review required)."),
        icon="/static/datavionos/icons/ai-workflow.svg",
        route="/ai/workflows",
        api_prefix="/api/ai/workflows",
        # ------------------------------------------------------------------
        # Runtime
        # ------------------------------------------------------------------
        enabled=True,
        system=False,
        tenant_scoped=True,
        order=50,
        # ------------------------------------------------------------------
        # Navigation
        # ------------------------------------------------------------------
        navigation=NavigationConfig(
            title="AI Workflow",
            route="/ai/workflows",
            icon="workflow",
            category="ai",
            order=50,
        ),
        # ------------------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------------------
        dashboard=DashboardConfig(
            enabled=True,
            title="AI Workflow",
            description=(
                "AI-powered healthcare workflows with human review and approval."
            ),
            icon="workflow",
            route="/ai/workflows",
            order=50,
        ),
        # ------------------------------------------------------------------
        # Discovery
        # ------------------------------------------------------------------
        tags=(
            "ai",
            "workflows",
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
        feature_flags=("ai_workflows",),
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
    "AI_WORKFLOW_MODULE_ID",
    "ai_workflow_module",
]
