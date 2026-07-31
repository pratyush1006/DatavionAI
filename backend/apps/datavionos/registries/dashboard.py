"""
DatavionOS dashboard registry.

Resolves dashboard widgets based on
enabled SaaS modules.

Architecture:

Plan Modules
      |
      v
Module Registry
      |
      v
Dashboard Registry
      |
      v
Frontend Dashboard
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class DashboardWidget:
    """
    DatavionOS dashboard widget definition.
    """

    code: str

    title: str

    description: str

    route: str

    icon: str

    module: str

    category: str


class DashboardRegistry:
    """
    Runtime dashboard widget registry.
    """

    _widgets: dict[str, DashboardWidget] = {}

    @classmethod
    def register(
        cls,
        widget: DashboardWidget,
    ) -> None:
        """
        Register dashboard widget.
        """

        cls._widgets[widget.module] = widget

    @classmethod
    def resolve(
        cls,
        modules: list,
    ) -> list[DashboardWidget]:
        """
        Resolve widgets from enabled modules.
        """

        widgets = []

        for module in modules:
            widget = cls._widgets.get(
                module.code,
            )

            if widget:
                widgets.append(
                    widget,
                )

        return widgets


# ==========================================================
# Core Widgets
# ==========================================================


DashboardRegistry.register(
    DashboardWidget(
        code="ai_assistant",
        title="AI Healthcare Copilot",
        description="AI powered healthcare assistant",
        route="/ai",
        icon="brain",
        module="ai",
        category="artificial_intelligence",
    )
)


DashboardRegistry.register(
    DashboardWidget(
        code="billing_summary",
        title="Billing Overview",
        description="Subscription and billing insights",
        route="/billing",
        icon="credit-card",
        module="billing",
        category="platform",
    )
)


DashboardRegistry.register(
    DashboardWidget(
        code="patient_summary",
        title="Patient Overview",
        description="Patient statistics and insights",
        route="/patients",
        icon="users",
        module="patients",
        category="clinical",
    )
)


DashboardRegistry.register(
    DashboardWidget(
        code="appointment_summary",
        title="Appointment Overview",
        description="Appointment analytics",
        route="/appointments",
        icon="calendar",
        module="appointments",
        category="clinical",
    )
)


__all__ = [
    "DashboardWidget",
    "DashboardRegistry",
]
