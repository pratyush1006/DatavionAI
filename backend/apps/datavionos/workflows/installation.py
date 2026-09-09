"""
DatavionOS platform installation workflow.

The workflow is generic: it consumes discovered ModuleContract metadata and
never contains a module-name catalogue.
"""

from __future__ import annotations

from typing import Any

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.datavionos.modules.discovery import discover_modules
from apps.datavionos.registries.module import module_registry


class DatavionOSInstallationWorkflow(BaseWorkflow[dict[str, Any]]):
    """Validate and register the discovered DatavionOS module graph."""

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[dict[str, Any]]:
        modules = discover_modules()
        ordered = module_registry.dependency_order(modules)
        registered = {module.identifier for module in module_registry.all()}
        pending = tuple(
            module for module in ordered if module.identifier not in registered
        )
        if pending:
            module_registry.register_modules(pending)
        return WorkflowResult(
            success=True,
            data={
                "discovered": len(modules),
                "registered": len(pending),
                "modules": [module.identifier for module in ordered],
            },
            message="DatavionOS metadata installation completed.",
            code="DATAVIONOS_INSTALLATION_COMPLETE",
        )


__all__ = [
    "DatavionOSInstallationWorkflow",
]
