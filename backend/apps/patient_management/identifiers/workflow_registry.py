"""
Patient Identifier workflow registration.

Registration is intentionally idempotent so Django application startup
can safely import this module more than once.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.identifiers.workflows import (
    IdentifierActivationWorkflow,
    IdentifierCreationWorkflow,
    IdentifierDeactivationWorkflow,
    IdentifierDeletionWorkflow,
    IdentifierPrimaryWorkflow,
    IdentifierRevocationWorkflow,
    IdentifierUpdateWorkflow,
    IdentifierVerificationWorkflow,
)

_IDENTIFIER_WORKFLOWS = {
    "identifier.create": IdentifierCreationWorkflow,
    "identifier.update": IdentifierUpdateWorkflow,
    "identifier.verify": IdentifierVerificationWorkflow,
    "identifier.activate": IdentifierActivationWorkflow,
    "identifier.deactivate": IdentifierDeactivationWorkflow,
    "identifier.revoke": IdentifierRevocationWorkflow,
    "identifier.set_primary": IdentifierPrimaryWorkflow,
    "identifier.delete": IdentifierDeletionWorkflow,
}


def register_identifier_workflows() -> None:
    """Register all Patient Identifier workflows exactly once."""
    for name, workflow in _IDENTIFIER_WORKFLOWS.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_identifier_workflows()


__all__ = ("register_identifier_workflows",)
