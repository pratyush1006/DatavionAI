"""
Patient Registration workflow registry.

Registers all canonical Registration workflows with the shared platform
workflow registry.
"""

from __future__ import annotations

from typing import Any, cast

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.registry import workflow_registry
from apps.patient_management.registration.workflows.registration_cancellation import (
    RegistrationCancellationWorkflow,
)
from apps.patient_management.registration.workflows.registration_check_in import (
    RegistrationCheckInWorkflow,
)
from apps.patient_management.registration.workflows.registration_completion import (
    RegistrationCompletionWorkflow,
)
from apps.patient_management.registration.workflows.registration_creation import (
    RegistrationCreationWorkflow,
)
from apps.patient_management.registration.workflows.registration_deletion import (
    RegistrationDeletionWorkflow,
)
from apps.patient_management.registration.workflows.registration_no_show import (
    RegistrationNoShowWorkflow,
)
from apps.patient_management.registration.workflows.registration_rejection import (
    RegistrationRejectionWorkflow,
)
from apps.patient_management.registration.workflows.registration_update import (
    RegistrationUpdateWorkflow,
)
from apps.patient_management.registration.workflows.registration_verification import (
    RegistrationVerificationWorkflow,
)

_REGISTRATION_WORKFLOWS = cast(
    dict[str, type[BaseWorkflow[Any]]],
    {
        "registration.create": RegistrationCreationWorkflow,
        "registration.update": RegistrationUpdateWorkflow,
        "registration.verify": RegistrationVerificationWorkflow,
        "registration.check_in": RegistrationCheckInWorkflow,
        "registration.complete": RegistrationCompletionWorkflow,
        "registration.cancel": RegistrationCancellationWorkflow,
        "registration.reject": RegistrationRejectionWorkflow,
        "registration.no_show": RegistrationNoShowWorkflow,
        "registration.delete": RegistrationDeletionWorkflow,
    },
)


def register_registration_workflows() -> None:
    """
    Register all Patient Registration workflows.

    Registration is registered with the shared workflow kernel rather than
    maintaining a module-specific workflow engine.
    """
    for name, workflow in _REGISTRATION_WORKFLOWS.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_registration_workflows()


__all__ = ("register_registration_workflows",)
