"""
Document workflow registry.

Registers document workflows into the
DatavionOS core workflow registry.
"""

from __future__ import annotations

from apps.core.workflows import (
    workflow_registry,
)
from apps.documents.workflows import (
    DocumentCreationWorkflow,
    DocumentDeletionWorkflow,
    DocumentUpdateWorkflow,
    DocumentVersionCreationWorkflow,
)


def register_document_workflows() -> None:
    """
    Register document workflows.

    Naming convention:

        <domain>.<capability>

    Examples:

        document.create
        document.update
        document.version.create
        document.delete
    """

    workflows = {
        #
        # Document lifecycle
        #
        "document.create": (DocumentCreationWorkflow),
        "document.update": (DocumentUpdateWorkflow),
        "document.delete": (DocumentDeletionWorkflow),
        #
        # Version lifecycle
        #
        "document.version.create": (DocumentVersionCreationWorkflow),
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_document_workflows",)
