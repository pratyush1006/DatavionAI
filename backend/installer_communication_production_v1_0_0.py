from __future__ import annotations

"""DatavionOS Patient Communication production installer."""

import json
import shutil
from pathlib import Path

TARGET = Path(
    r"D:\Datavion-Payment\DatavionAI\backend\apps\patient_management\communication"
)

FILES = {}


def add(path: str, source: str) -> None:
    FILES[path] = source.strip() + "\n"


add(
    "__init__.py",
    '''"""Patient Communication domain module."""

from __future__ import annotations

__all__ = ()''',
)
add(
    "apps.py",
    '''"""Django application configuration for Patient Communication."""

from __future__ import annotations

from django.apps import AppConfig


class PatientCommunicationConfig(AppConfig):
    """Configure the Patient Communication Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient_management.communication"
    label = "patient_communication"
    verbose_name = "Patient Communication"


__all__ = ("PatientCommunicationConfig",)''',
)
add(
    "constants.py",
    '''"""Patient Communication domain constants."""

from __future__ import annotations

from django.db import models


class CommunicationChannel(models.TextChoices):
    """Supported patient communication channels."""

    SMS = "sms", "SMS"
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"
    PORTAL = "portal", "Patient Portal"
    LETTER = "letter", "Letter"
    IN_PERSON = "in_person", "In Person"
    OTHER = "other", "Other"


class CommunicationDirection(models.TextChoices):
    """Direction of a communication interaction."""

    OUTBOUND = "outbound", "Outbound"
    INBOUND = "inbound", "Inbound"


class CommunicationStatus(models.TextChoices):
    """Lifecycle status of a communication interaction."""

    DRAFT = "draft", "Draft"
    QUEUED = "queued", "Queued"
    SENT = "sent", "Sent"
    DELIVERED = "delivered", "Delivered"
    READ = "read", "Read"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"
    ARCHIVED = "archived", "Archived"


class CommunicationType(models.TextChoices):
    """Business classification for a communication."""

    GENERAL = "general", "General"
    APPOINTMENT = "appointment", "Appointment"
    CLINICAL = "clinical", "Clinical"
    BILLING = "billing", "Billing"
    FOLLOW_UP = "follow_up", "Follow Up"
    REMINDER = "reminder", "Reminder"
    ADMINISTRATIVE = "administrative", "Administrative"


__all__ = (
    "CommunicationChannel",
    "CommunicationDirection",
    "CommunicationStatus",
    "CommunicationType",
)''',
)
add(
    "exceptions.py",
    '''"""Patient Communication domain exceptions."""

from __future__ import annotations


class PatientCommunicationError(Exception):
    """Base exception for Patient Communication errors."""


class PatientCommunicationValidationError(PatientCommunicationError):
    """Raised when communication data violates domain rules."""


class PatientCommunicationNotFoundError(PatientCommunicationError):
    """Raised when a communication cannot be found."""


__all__ = (
    "PatientCommunicationError",
    "PatientCommunicationValidationError",
    "PatientCommunicationNotFoundError",
)''',
)
add(
    "validators.py",
    '''"""Validation helpers for Patient Communication."""

from __future__ import annotations

from typing import Any

from apps.patient_management.communication.constants import CommunicationChannel
from apps.patient_management.communication.constants import CommunicationDirection
from apps.patient_management.communication.exceptions import PatientCommunicationValidationError


def validate_communication_data(data: dict[str, Any]) -> None:
    """Validate cross-field communication invariants."""
    channel = data.get("channel")
    direction = data.get("direction")
    content = data.get("content")
    if channel == CommunicationChannel.PHONE and not content:
        raise PatientCommunicationValidationError("Phone communications require a note or summary.")
    if direction == CommunicationDirection.INBOUND and data.get("status") == "queued":
        raise PatientCommunicationValidationError("Inbound communications cannot be queued for delivery.")


__all__ = ("validate_communication_data",)''',
)
add(
    "managers.py",
    '''"""Managers and querysets for Patient Communication."""

from __future__ import annotations

from uuid import UUID

from apps.core.models.managers import SoftDeleteManager
from apps.core.models.querysets import SoftDeleteQuerySet


class CommunicationQuerySet(SoftDeleteQuerySet):
    """Provide reusable tenant and patient communication queries."""

    def for_patient(self, patient_id: UUID) -> "CommunicationQuerySet":
        """Return communications for one patient."""
        return self.filter(patient_id=patient_id)

    def for_organization(self, organization_id: UUID) -> "CommunicationQuerySet":
        """Return communications for one organization."""
        return self.filter(organization_id=organization_id)

    def by_status(self, status: str) -> "CommunicationQuerySet":
        """Return communications with the requested status."""
        return self.filter(status=status)

    def by_channel(self, channel: str) -> "CommunicationQuerySet":
        """Return communications on the requested channel."""
        return self.filter(channel=channel)


class CommunicationManager(SoftDeleteManager):
    """Default manager exposing only non-deleted communications."""

    def get_queryset(self) -> CommunicationQuerySet:
        """Return an alive communication queryset."""
        return CommunicationQuerySet(self.model, using=self._db).alive()


__all__ = ("CommunicationManager", "CommunicationQuerySet")''',
)
add(
    "models/__init__.py",
    '''"""Patient Communication model exports."""

from __future__ import annotations

from apps.patient_management.communication.models.communication import PatientCommunication

__all__ = ("PatientCommunication",)''',
)
add(
    "models/communication.py",
    '''"""Patient Communication persistence model."""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.communication.constants import CommunicationChannel
from apps.patient_management.communication.constants import CommunicationDirection
from apps.patient_management.communication.constants import CommunicationStatus
from apps.patient_management.communication.constants import CommunicationType
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class PatientCommunication(BaseModel):
    """Record a tenant-scoped communication interaction with a patient."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_communications",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="communications",
    )
    channel = models.CharField(max_length=20, choices=CommunicationChannel.choices)
    direction = models.CharField(max_length=20, choices=CommunicationDirection.choices)
    communication_type = models.CharField(max_length=30, choices=CommunicationType.choices, default=CommunicationType.GENERAL)
    status = models.CharField(max_length=20, choices=CommunicationStatus.choices, default=CommunicationStatus.DRAFT, db_index=True)
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    external_reference = models.CharField(max_length=255, blank=True)
    occurred_at = models.DateTimeField(null=True, blank=True, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    failed_reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_patient_communications",
    )

    objects = __import__("apps.patient_management.communication.managers", fromlist=["CommunicationManager"]).CommunicationManager()

    class Meta:
        """Database metadata for Patient Communication."""

        db_table = "patient_communications"
        ordering = ("-occurred_at", "-created_at")
        indexes = [
            models.Index(fields=("organization", "patient", "occurred_at")),
            models.Index(fields=("organization", "status", "is_deleted")),
            models.Index(fields=("organization", "channel", "occurred_at")),
        ]

    def __str__(self) -> str:
        """Return a readable communication identifier."""
        return f"{self.patient_id} - {self.channel} - {self.status}"


__all__ = ("PatientCommunication",)''',
)
# replace dynamic import with normal import after file construction
FILES["models/communication.py"] = (
    FILES["models/communication.py"]
    .replace(
        "from apps.patient_management.communication.constants import CommunicationType\n",
        "from apps.patient_management.communication.constants import CommunicationType\nfrom apps.patient_management.communication.managers import CommunicationManager\n",
    )
    .replace(
        'objects = __import__("apps.patient_management.communication.managers", fromlist=["CommunicationManager"]).CommunicationManager()',
        "objects = CommunicationManager()",
    )
)

add(
    "permissions/__init__.py",
    '''"""Patient Communication permission exports."""

from __future__ import annotations

from apps.patient_management.communication.permissions.communication import PatientCommunicationPermission

__all__ = ("PatientCommunicationPermission",)''',
)
add(
    "permissions/communication.py",
    '''"""RBAC permissions for Patient Communication."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class PatientCommunicationPermission(RBACPermissionBase):
    """Define RBAC permission codes for Patient Communication."""

    VIEW = "patient_communication.view"
    CREATE = "patient_communication.create"
    UPDATE = "patient_communication.update"
    DELETE = "patient_communication.delete"
    RESTORE = "patient_communication.restore"
    QUEUE = "patient_communication.queue"
    SEND = "patient_communication.send"
    DELIVER = "patient_communication.deliver"
    READ = "patient_communication.read"
    FAIL = "patient_communication.fail"
    CANCEL = "patient_communication.cancel"
    ARCHIVE = "patient_communication.archive"


__all__ = ("PatientCommunicationPermission",)''',
)
add(
    "policies/__init__.py",
    '''"""Patient Communication policy exports."""

from __future__ import annotations

from apps.patient_management.communication.policies.communication import PatientCommunicationPolicy

__all__ = ("PatientCommunicationPolicy",)''',
)
add(
    "policies/communication.py",
    '''"""Authorization policy for Patient Communication."""

from __future__ import annotations

from typing import Any

from apps.patient_management.communication.permissions.communication import PatientCommunicationPermission
from apps.platform.rbac.services import user_has_permission


class PatientCommunicationPolicy:
    """Enforce RBAC decisions within an organization boundary."""

    @staticmethod
    def _allowed(actor: Any, permission: str, organization: Any) -> bool:
        """Return whether the actor has the requested permission."""
        return user_has_permission(user=actor, permission=permission, organization=organization)

    @classmethod
    def can_view(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize viewing communications."""
        return cls._allowed(actor, PatientCommunicationPermission.VIEW, organization)

    @classmethod
    def can_create(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication creation."""
        return cls._allowed(actor, PatientCommunicationPermission.CREATE, organization)

    @classmethod
    def can_update(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication updates."""
        return cls._allowed(actor, PatientCommunicationPermission.UPDATE, organization)

    @classmethod
    def can_delete(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication deletion."""
        return cls._allowed(actor, PatientCommunicationPermission.DELETE, organization)

    @classmethod
    def can_restore(cls, *, actor: Any, organization: Any) -> bool:
        """Authorize communication restoration."""
        return cls._allowed(actor, PatientCommunicationPermission.RESTORE, organization)

    @classmethod
    def can_status(cls, *, actor: Any, organization: Any, status: str) -> bool:
        """Authorize a status transition."""
        permission_map = {
            "queued": PatientCommunicationPermission.QUEUE,
            "sent": PatientCommunicationPermission.SEND,
            "delivered": PatientCommunicationPermission.DELIVER,
            "read": PatientCommunicationPermission.READ,
            "failed": PatientCommunicationPermission.FAIL,
            "cancelled": PatientCommunicationPermission.CANCEL,
            "archived": PatientCommunicationPermission.ARCHIVE,
        }
        permission = permission_map.get(status)
        return permission is not None and cls._allowed(actor, permission, organization)


__all__ = ("PatientCommunicationPolicy",)''',
)
add(
    "selectors/__init__.py",
    '''"""Patient Communication selector exports."""

from __future__ import annotations

from apps.patient_management.communication.selectors.communication import get_communication, list_communications

__all__ = ("get_communication", "list_communications")''',
)
add(
    "selectors/communication.py",
    '''"""Read selectors for Patient Communication."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.communication.models import PatientCommunication


def list_communications(*, tenant_id: UUID, patient_id: UUID | None = None, organization_id: UUID | None = None) -> QuerySet[PatientCommunication]:
    """Return alive communications inside the tenant boundary."""
    queryset = PatientCommunication.objects.filter(organization__tenant_id=tenant_id)
    if patient_id is not None:
        queryset = queryset.filter(patient_id=patient_id)
    if organization_id is not None:
        queryset = queryset.filter(organization_id=organization_id)
    return queryset.select_related("organization", "patient", "created_by")


def get_communication(*, tenant_id: UUID, communication_id: UUID, include_deleted: bool = False) -> PatientCommunication:
    """Return one communication inside the tenant boundary."""
    manager = PatientCommunication.all_objects if include_deleted else PatientCommunication.objects
    return manager.filter(
        pk=communication_id,
        organization__tenant_id=tenant_id,
    ).select_related("organization", "patient", "created_by").get()


__all__ = ("get_communication", "list_communications")''',
)
add(
    "services/__init__.py",
    '''"""Patient Communication service exports."""

from __future__ import annotations

from apps.patient_management.communication.services.communication import PatientCommunicationService

__all__ = ("PatientCommunicationService",)''',
)
add(
    "services/communication.py",
    '''"""Domain services for Patient Communication."""

from __future__ import annotations

from typing import Any

from django.utils import timezone

from apps.patient_management.communication.constants import CommunicationStatus
from apps.patient_management.communication.models import PatientCommunication
from apps.patient_management.communication.validators import validate_communication_data


class PatientCommunicationService:
    """Own communication persistence, validation, normalization and lifecycle mutation."""

    @staticmethod
    def create(*, validated_data: dict[str, Any], performed_by: Any = None) -> PatientCommunication:
        """Create a communication record."""
        validate_communication_data(validated_data)
        data = dict(validated_data)
        data["created_by"] = performed_by
        return PatientCommunication.objects.create(**data)

    @staticmethod
    def update(*, instance: PatientCommunication, validated_data: dict[str, Any], performed_by: Any = None) -> PatientCommunication:
        """Update a communication record."""
        data = dict(validated_data)
        validate_communication_data({**model_to_dict(instance), **data})
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    @staticmethod
    def transition(*, instance: PatientCommunication, status: str, performed_by: Any = None) -> PatientCommunication:
        """Apply a supported communication status transition."""
        if instance.is_deleted:
            raise ValueError("Deleted communications cannot change status.")
        now = timezone.now()
        instance.status = status
        if status == CommunicationStatus.SENT:
            instance.sent_at = instance.sent_at or now
        elif status == CommunicationStatus.DELIVERED:
            instance.delivered_at = instance.delivered_at or now
        elif status == CommunicationStatus.READ:
            instance.read_at = instance.read_at or now
        if status == CommunicationStatus.ARCHIVED:
            instance.is_active = False
        else:
            instance.is_active = True
        instance.save()
        return instance

    @staticmethod
    def delete(*, instance: PatientCommunication, performed_by: Any = None) -> PatientCommunication:
        """Soft-delete a communication record."""
        instance.is_active = False
        instance.status = CommunicationStatus.ARCHIVED
        instance.save(update_fields=("is_active", "status", "updated_at"))
        instance.delete(user_id=getattr(performed_by, "id", performed_by))
        return instance

    @staticmethod
    def restore(*, instance: PatientCommunication, performed_by: Any = None) -> PatientCommunication:
        """Restore a soft-deleted communication as an inactive draft."""
        instance.restore()
        instance.status = CommunicationStatus.DRAFT
        instance.is_active = False
        instance.save(update_fields=("status", "is_active", "updated_at"))
        return instance


def model_to_dict(instance: PatientCommunication) -> dict[str, Any]:
    """Return model fields needed for cross-field validation."""
    return {
        "channel": instance.channel,
        "direction": instance.direction,
        "status": instance.status,
        "content": instance.content,
    }


__all__ = ("PatientCommunicationService",)''',
)

# Events
for fn, cls, verb in [
    ("created", "CommunicationCreatedEvent", "created"),
    ("updated", "CommunicationUpdatedEvent", "updated"),
    ("deleted", "CommunicationDeletedEvent", "deleted"),
    ("status_changed", "CommunicationStatusChangedEvent", "status_changed"),
    ("restored", "CommunicationRestoredEvent", "restored"),
]:
    source = f"""'''Patient Communication {verb} domain event.'''

from __future__ import annotations

from typing import Any

from apps.core.events import DomainEvent


class {cls}(DomainEvent):
    '''Represent a Patient Communication {verb} event.'''

    event_name = "patient_communication.{verb}"

    def __init__(self, *, communication: Any, actor_id: Any = None, payload: dict[str, Any] | None = None) -> None:
        '''Initialize the domain event.'''
        super().__init__(
            aggregate_id=communication.id,
            actor_id=actor_id,
            payload=payload or {{
                "communication_id": str(communication.id),
                "patient_id": str(communication.patient_id),
                "organization_id": str(communication.organization_id),
                "status": communication.status,
            }},
        )


__all__ = ("{cls}",)"""
    add(f"events/{fn}.py", source)
add(
    "events/__init__.py",
    '''"""Patient Communication domain event exports."""

from __future__ import annotations

from apps.patient_management.communication.events.created import CommunicationCreatedEvent
from apps.patient_management.communication.events.deleted import CommunicationDeletedEvent
from apps.patient_management.communication.events.restored import CommunicationRestoredEvent
from apps.patient_management.communication.events.status_changed import CommunicationStatusChangedEvent
from apps.patient_management.communication.events.updated import CommunicationUpdatedEvent

__all__ = (
    "CommunicationCreatedEvent",
    "CommunicationDeletedEvent",
    "CommunicationRestoredEvent",
    "CommunicationStatusChangedEvent",
    "CommunicationUpdatedEvent",
)''',
)

# Workflow generator
workflow_defs = {
    "creation": (
        "CommunicationCreationData",
        "CommunicationCreationRequest",
        "CommunicationCreationWorkflow",
        "patient_communication.create",
        "PatientCommunicationPermission.CREATE",
        "can_create",
        "create",
        "CommunicationCreatedEvent",
        "communication_created",
    ),
    "update": (
        "CommunicationUpdateData",
        "CommunicationUpdateRequest",
        "CommunicationUpdateWorkflow",
        "patient_communication.update",
        "PatientCommunicationPermission.UPDATE",
        "can_update",
        "update",
        "CommunicationUpdatedEvent",
        "communication_updated",
    ),
    "deletion": (
        "CommunicationDeletionData",
        "CommunicationDeletionRequest",
        "CommunicationDeletionWorkflow",
        "patient_communication.delete",
        "PatientCommunicationPermission.DELETE",
        "can_delete",
        "delete",
        "CommunicationDeletedEvent",
        "communication_deleted",
    ),
    "restore": (
        "CommunicationRestoreData",
        "CommunicationRestoreRequest",
        "CommunicationRestoreWorkflow",
        "patient_communication.restore",
        "PatientCommunicationPermission.RESTORE",
        "can_restore",
        "restore",
        "CommunicationRestoredEvent",
        "communication_restored",
    ),
}
for key, (
    data_cls,
    req_cls,
    wf_cls,
    name,
    perm,
    policy,
    service_method,
    event_cls,
    result_key,
) in workflow_defs.items():
    add(
        f"workflows/{key}.py",
        f'''"""Patient Communication {key} workflow."""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass, field\nfrom typing import Any\nfrom uuid import UUID\n\nfrom django.db import transaction\n\nfrom apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult, workflow_registry\nfrom apps.patient_management.communication.events.{"restored" if key == "restore" else "updated" if key == "update" else "deleted" if key == "deletion" else key} import {event_cls}\nfrom apps.patient_management.communication.policies.communication import PatientCommunicationPolicy\nfrom apps.patient_management.communication.selectors.communication import get_communication\nfrom apps.patient_management.communication.services.communication import PatientCommunicationService\n\n\n@dataclass(frozen=True)\nclass {data_cls}:\n    """Workflow output data."""\n\n    communication: Any\n\n\n@dataclass(frozen=True)\nclass {req_cls}:\n    """Workflow input data."""\n\n    tenant_id: UUID\n    communication_id: UUID | None = None\n    organization: Any = None\n    validated_data: dict[str, Any] = field(default_factory=dict)\n    actor: Any = None\n\n\nclass {wf_cls}(BaseWorkflow):\n    """Orchestrate Patient Communication {key} through policy and service layers."""\n\n    name = "{name}"\n\n    def __init__(self, *, request: {req_cls}, logger_: Any = None) -> None:\n        """Initialize the workflow."""\n        super().__init__(logger_=logger_, payload=request)\n        self.request = request\n\n    @transaction.atomic\n    def _run(self, context: WorkflowContext) -> WorkflowResult:\n        """Execute the workflow transaction."""\n        request = self.request\n        actor = request.actor\n        if request.communication_id is None:\n            raise ValueError("communication_id is required")\n        communication = get_communication(tenant_id=request.tenant_id, communication_id=request.communication_id, include_deleted={str(key == "restore")})\n        organization = communication.organization\n        if not PatientCommunicationPolicy.{policy}(actor=actor, organization=organization):\n            raise PermissionError("Insufficient permission for Patient Communication {key}.")\n        if "{key}" == "update":
            communication = PatientCommunicationService.{service_method}(
                instance=communication,
                validated_data=request.validated_data,
                performed_by=actor,
            )
        else:
            communication = PatientCommunicationService.{service_method}(
                instance=communication,
                performed_by=actor,
            )\n        event = {event_cls}(communication=communication, actor_id=getattr(actor, "id", actor))\n        self.publish_after_commit(event)\n        return WorkflowResult.ok(data={{"{result_key}": communication}})\n\n\nworkflow_registry.register(name="{name}", workflow={wf_cls})\n\n__all__ = ("{data_cls}", "{req_cls}", "{wf_cls}")''',
    )
# creation needs special source
FILES["workflows/creation.py"] = '''"""Patient Communication creation workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult, workflow_registry
from apps.patient_management.communication.events.created import CommunicationCreatedEvent
from apps.patient_management.communication.policies.communication import PatientCommunicationPolicy
from apps.patient_management.communication.services.communication import PatientCommunicationService


@dataclass(frozen=True)
class CommunicationCreationData:
    """Workflow output data."""

    communication: Any


@dataclass(frozen=True)
class CommunicationCreationRequest:
    """Workflow input data."""

    tenant_id: UUID
    organization: Any
    validated_data: dict[str, Any] = field(default_factory=dict)
    actor: Any = None


class CommunicationCreationWorkflow(BaseWorkflow):
    """Create Patient Communication through policy and service layers."""

    name = "patient_communication.create"

    def __init__(self, *, request: CommunicationCreationRequest, logger_: Any = None) -> None:
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the creation transaction."""
        request = self.request
        if not PatientCommunicationPolicy.can_create(actor=request.actor, organization=request.organization):
            raise PermissionError("Insufficient permission to create Patient Communication.")
        communication = PatientCommunicationService.create(
            validated_data=request.validated_data,
            performed_by=request.actor,
        )
        event = CommunicationCreatedEvent(communication=communication, actor_id=getattr(request.actor, "id", request.actor))
        self.publish_after_commit(event)
        return WorkflowResult.ok(data={"communication_created": communication})


workflow_registry.register(name="patient_communication.create", workflow=CommunicationCreationWorkflow)

__all__ = ("CommunicationCreationData", "CommunicationCreationRequest", "CommunicationCreationWorkflow")'''

# Lifecycle
add(
    "workflows/lifecycle.py",
    '''"""Patient Communication lifecycle workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult, workflow_registry
from apps.patient_management.communication.events.status_changed import CommunicationStatusChangedEvent
from apps.patient_management.communication.policies.communication import PatientCommunicationPolicy
from apps.patient_management.communication.selectors.communication import get_communication
from apps.patient_management.communication.services.communication import PatientCommunicationService


@dataclass(frozen=True)
class CommunicationLifecycleData:
    """Workflow output data."""

    communication: Any


@dataclass(frozen=True)
class CommunicationLifecycleRequest:
    """Workflow input data."""

    tenant_id: UUID
    communication_id: UUID
    status: str
    actor: Any = None


class CommunicationLifecycleWorkflow(BaseWorkflow):
    """Apply an authorized communication status transition."""

    name = "patient_communication.lifecycle"

    def __init__(self, *, request: CommunicationLifecycleRequest, logger_: Any = None) -> None:
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the lifecycle transaction."""
        request = self.request
        communication = get_communication(tenant_id=request.tenant_id, communication_id=request.communication_id)
        if not PatientCommunicationPolicy.can_status(actor=request.actor, organization=communication.organization, status=request.status):
            raise PermissionError("Insufficient permission for Patient Communication lifecycle transition.")
        old_status = communication.status
        communication = PatientCommunicationService.transition(instance=communication, status=request.status, performed_by=request.actor)
        event = CommunicationStatusChangedEvent(communication=communication, actor_id=getattr(request.actor, "id", request.actor), payload={"old_status": old_status, "new_status": communication.status})
        self.publish_after_commit(event)
        return WorkflowResult.ok(data={"communication_status_changed": communication})


workflow_registry.register(name="patient_communication.lifecycle", workflow=CommunicationLifecycleWorkflow)

__all__ = ("CommunicationLifecycleData", "CommunicationLifecycleRequest", "CommunicationLifecycleWorkflow")''',
)

add(
    "workflows/__init__.py",
    '''"""Patient Communication workflow exports."""

from __future__ import annotations

from apps.patient_management.communication.workflows.creation import CommunicationCreationData, CommunicationCreationRequest, CommunicationCreationWorkflow
from apps.patient_management.communication.workflows.deletion import CommunicationDeletionData, CommunicationDeletionRequest, CommunicationDeletionWorkflow
from apps.patient_management.communication.workflows.lifecycle import CommunicationLifecycleData, CommunicationLifecycleRequest, CommunicationLifecycleWorkflow
from apps.patient_management.communication.workflows.restore import CommunicationRestoreData, CommunicationRestoreRequest, CommunicationRestoreWorkflow
from apps.patient_management.communication.workflows.update import CommunicationUpdateData, CommunicationUpdateRequest, CommunicationUpdateWorkflow

__all__ = (
    "CommunicationCreationData", "CommunicationCreationRequest", "CommunicationCreationWorkflow",
    "CommunicationDeletionData", "CommunicationDeletionRequest", "CommunicationDeletionWorkflow",
    "CommunicationLifecycleData", "CommunicationLifecycleRequest", "CommunicationLifecycleWorkflow",
    "CommunicationRestoreData", "CommunicationRestoreRequest", "CommunicationRestoreWorkflow",
    "CommunicationUpdateData", "CommunicationUpdateRequest", "CommunicationUpdateWorkflow",
)''',
)

# API serializers
add(
    "api/__init__.py",
    '''"""Patient Communication API package."""

from __future__ import annotations

__all__ = ()''',
)
add(
    "api/serializers/__init__.py",
    '''"""Patient Communication serializer exports."""

from __future__ import annotations

from apps.patient_management.communication.api.serializers.create import CommunicationCreateSerializer
from apps.patient_management.communication.api.serializers.detail import CommunicationDetailSerializer
from apps.patient_management.communication.api.serializers.list import CommunicationListSerializer
from apps.patient_management.communication.api.serializers.update import CommunicationUpdateSerializer

__all__ = ("CommunicationCreateSerializer", "CommunicationDetailSerializer", "CommunicationListSerializer", "CommunicationUpdateSerializer")''',
)
add(
    "api/serializers/create.py",
    '''"""Patient Communication creation serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationCreateSerializer(serializers.ModelSerializer):
    """Validate Patient Communication creation payloads."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = ("organization", "patient", "channel", "direction", "communication_type", "subject", "content", "external_reference", "occurred_at", "metadata")


__all__ = ("CommunicationCreateSerializer",)''',
)
add(
    "api/serializers/update.py",
    '''"""Patient Communication update serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationUpdateSerializer(serializers.ModelSerializer):
    """Validate mutable Patient Communication fields."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = ("channel", "direction", "communication_type", "subject", "content", "external_reference", "occurred_at", "metadata")


__all__ = ("CommunicationUpdateSerializer",)''',
)
add(
    "api/serializers/detail.py",
    '''"""Patient Communication detail serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationDetailSerializer(serializers.ModelSerializer):
    """Serialize a complete Patient Communication record."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = "__all__"


__all__ = ("CommunicationDetailSerializer",)''',
)
add(
    "api/serializers/list.py",
    '''"""Patient Communication list serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationListSerializer(serializers.ModelSerializer):
    """Serialize Patient Communication list results."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = ("id", "patient", "organization", "channel", "direction", "communication_type", "status", "subject", "occurred_at", "created_at", "updated_at", "is_active")


__all__ = ("CommunicationListSerializer",)''',
)
add(
    "api/filters.py",
    '''"""Patient Communication API filters."""

from __future__ import annotations

from django_filters import rest_framework as filters

from apps.patient_management.communication.models import PatientCommunication


class CommunicationFilter(filters.FilterSet):
    """Filter communications by patient, channel, status and type."""

    class Meta:
        """Filter metadata."""

        model = PatientCommunication
        fields = ("patient", "organization", "channel", "direction", "communication_type", "status")


__all__ = ("CommunicationFilter",)''',
)

# Views
add(
    "api/views/__init__.py",
    '''"""Patient Communication API view exports."""

from __future__ import annotations

from apps.patient_management.communication.api.views.list_create import CommunicationListCreateView
from apps.patient_management.communication.api.views.lifecycle import CommunicationLifecycleView
from apps.patient_management.communication.api.views.retrieve_update_destroy import CommunicationRetrieveUpdateDestroyView

__all__ = ("CommunicationListCreateView", "CommunicationLifecycleView", "CommunicationRetrieveUpdateDestroyView")''',
)
add(
    "api/views/list_create.py",
    '''"""List and create Patient Communication API view."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.communication.api.serializers.create import CommunicationCreateSerializer
from apps.patient_management.communication.api.serializers.list import CommunicationListSerializer
from apps.patient_management.communication.selectors.communication import list_communications
from apps.patient_management.communication.workflows.creation import CommunicationCreationRequest, CommunicationCreationWorkflow


class CommunicationListCreateView(APIView):
    """Handle tenant-scoped communication listing and creation."""

    permission_classes = (IsAuthenticated,)

    def _tenant_id(self, request):
        """Resolve the active tenant from the authenticated organization role."""
        if getattr(request, "tenant", None) is not None:
            return request.tenant.id
        role = request.user.organization_roles.select_related("organization__tenant").first()
        if role is None:
            raise PermissionError("No organization tenant is available.")
        return role.organization.tenant_id

    def get(self, request):
        """List communications for the active tenant."""
        queryset = list_communications(tenant_id=self._tenant_id(request), patient_id=request.query_params.get("patient_id"))
        return Response(CommunicationListSerializer(queryset, many=True).data)

    def post(self, request):
        """Create a communication through the domain workflow."""
        serializer = CommunicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.validated_data["organization"]
        workflow = CommunicationCreationWorkflow(request=CommunicationCreationRequest(tenant_id=organization.tenant_id, organization=organization, validated_data=serializer.validated_data, actor=request.user))
        result = workflow.run()
        return Response(CommunicationListSerializer(result.data["communication_created"]).data, status=201)


__all__ = ("CommunicationListCreateView",)''',
)
add(
    "api/views/retrieve_update_destroy.py",
    '''"""Retrieve, update and destroy Patient Communication API view."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.communication.api.serializers.detail import CommunicationDetailSerializer
from apps.patient_management.communication.api.serializers.update import CommunicationUpdateSerializer
from apps.patient_management.communication.selectors.communication import get_communication
from apps.patient_management.communication.workflows.deletion import CommunicationDeletionRequest, CommunicationDeletionWorkflow
from apps.patient_management.communication.workflows.update import CommunicationUpdateRequest, CommunicationUpdateWorkflow


class CommunicationRetrieveUpdateDestroyView(APIView):
    """Handle a single tenant-scoped communication."""

    permission_classes = (IsAuthenticated,)

    def _tenant_id(self, request):
        """Resolve the active tenant."""
        if getattr(request, "tenant", None) is not None:
            return request.tenant.id
        role = request.user.organization_roles.select_related("organization__tenant").first()
        if role is None:
            raise PermissionError("No organization tenant is available.")
        return role.organization.tenant_id

    def get(self, request, communication_id):
        """Return one communication."""
        communication = get_communication(tenant_id=self._tenant_id(request), communication_id=communication_id)
        return Response(CommunicationDetailSerializer(communication).data)

    def put(self, request, communication_id):
        """Update one communication through its workflow."""
        communication = get_communication(tenant_id=self._tenant_id(request), communication_id=communication_id)
        serializer = CommunicationUpdateSerializer(communication, data=request.data)
        serializer.is_valid(raise_exception=True)
        result = CommunicationUpdateWorkflow(request=CommunicationUpdateRequest(tenant_id=self._tenant_id(request), communication_id=communication.id, validated_data=serializer.validated_data, actor=request.user)).run()
        return Response(CommunicationDetailSerializer(result.data["communication_updated"]).data)

    def patch(self, request, communication_id):
        """Partially update one communication."""
        communication = get_communication(tenant_id=self._tenant_id(request), communication_id=communication_id)
        serializer = CommunicationUpdateSerializer(communication, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = CommunicationUpdateWorkflow(request=CommunicationUpdateRequest(tenant_id=self._tenant_id(request), communication_id=communication.id, validated_data=serializer.validated_data, actor=request.user)).run()
        return Response(CommunicationDetailSerializer(result.data["communication_updated"]).data)

    def delete(self, request, communication_id):
        """Soft-delete one communication."""
        result = CommunicationDeletionWorkflow(request=CommunicationDeletionRequest(tenant_id=self._tenant_id(request), communication_id=communication_id, actor=request.user)).run()
        return Response(CommunicationDetailSerializer(result.data["communication_deleted"]).data)


__all__ = ("CommunicationRetrieveUpdateDestroyView",)''',
)
add(
    "api/views/lifecycle.py",
    '''"""Patient Communication lifecycle API view."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.communication.api.serializers.detail import CommunicationDetailSerializer
from apps.patient_management.communication.workflows.lifecycle import CommunicationLifecycleRequest, CommunicationLifecycleWorkflow


class CommunicationLifecycleView(APIView):
    """Apply an authorized communication status transition."""

    permission_classes = (IsAuthenticated,)

    def _tenant_id(self, request):
        """Resolve the active tenant."""
        if getattr(request, "tenant", None) is not None:
            return request.tenant.id
        role = request.user.organization_roles.select_related("organization__tenant").first()
        if role is None:
            raise PermissionError("No organization tenant is available.")
        return role.organization.tenant_id

    def post(self, request, communication_id):
        """Transition communication status."""
        status_value = request.data.get("status")
        if not status_value:
            return Response({"detail": "status is required."}, status=400)
        result = CommunicationLifecycleWorkflow(request=CommunicationLifecycleRequest(tenant_id=self._tenant_id(request), communication_id=communication_id, status=status_value, actor=request.user)).run()
        return Response(CommunicationDetailSerializer(result.data["communication_status_changed"]).data)


__all__ = ("CommunicationLifecycleView",)''',
)
add(
    "api/urls/communication.py",
    '''"""Patient Communication API routes."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.communication.api.views import CommunicationLifecycleView, CommunicationListCreateView, CommunicationRetrieveUpdateDestroyView

urlpatterns = [
    path("", CommunicationListCreateView.as_view(), name="communication-list-create"),
    path("<uuid:communication_id>/", CommunicationRetrieveUpdateDestroyView.as_view(), name="communication-detail"),
    path("<uuid:communication_id>/lifecycle/", CommunicationLifecycleView.as_view(), name="communication-lifecycle"),
]

__all__ = ("urlpatterns",)''',
)
add(
    "api/urls/__init__.py",
    '''"""Patient Communication API URL exports."""

from __future__ import annotations

from apps.patient_management.communication.api.urls.communication import urlpatterns

__all__ = ("urlpatterns",)''',
)
add(
    "api/urls.py",
    '''"""Patient Communication API URL compatibility module."""

from __future__ import annotations

from apps.patient_management.communication.api.urls.communication import urlpatterns

__all__ = ("urlpatterns",)''',
)
add(
    "urls.py",
    '''"""Patient Communication URL compatibility module."""

from __future__ import annotations

from apps.patient_management.communication.api.urls.communication import urlpatterns

__all__ = ("urlpatterns",)''',
)
add(
    "admin.py",
    '''"""Django admin configuration for Patient Communication."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.communication.models import PatientCommunication


@admin.register(PatientCommunication)
class PatientCommunicationAdmin(admin.ModelAdmin):
    """Admin configuration for communication records."""

    list_display = ("id", "patient", "channel", "direction", "status", "occurred_at", "is_active", "is_deleted")
    list_filter = ("channel", "direction", "communication_type", "status", "is_active", "is_deleted")
    search_fields = ("id", "patient__id", "subject", "external_reference")
    readonly_fields = ("created_at", "updated_at", "deleted_at", "deleted_by_id")


__all__ = ("PatientCommunicationAdmin",)''',
)
add(
    "workflow_registry.py",
    '''"""Workflow registration for Patient Communication."""

from __future__ import annotations

from apps.patient_management.communication.workflows.creation import CommunicationCreationWorkflow
from apps.patient_management.communication.workflows.deletion import CommunicationDeletionWorkflow
from apps.patient_management.communication.workflows.lifecycle import CommunicationLifecycleWorkflow
from apps.patient_management.communication.workflows.restore import CommunicationRestoreWorkflow
from apps.patient_management.communication.workflows.update import CommunicationUpdateWorkflow


WORKFLOW_NAMES = (
    "patient_communication.create",
    "patient_communication.update",
    "patient_communication.delete",
    "patient_communication.restore",
    "patient_communication.lifecycle",
)

__all__ = ("WORKFLOW_NAMES", "CommunicationCreationWorkflow", "CommunicationDeletionWorkflow", "CommunicationLifecycleWorkflow", "CommunicationRestoreWorkflow", "CommunicationUpdateWorkflow")''',
)
add(
    "tests/__init__.py",
    '''"""Patient Communication test package."""

from __future__ import annotations

__all__ = ()''',
)
add(
    "migrations/__init__.py",
    '''"""Patient Communication migrations package."""

from __future__ import annotations

__all__ = ()''',
)
manifest = {
    "installer": "DatavionOS Patient Communication Production Installer",
    "version": "1.0.0",
    "module": "apps.patient_management.communication",
    "canonical_patient": "apps.patient_management.patients.models.Patient",
    "persistence_base": "apps.core.models.BaseModel",
    "architecture": "API -> RBAC -> Workflow -> Policy -> Service -> Model -> Domain Event",
    "fresh_install": True,
    "delete_existing_module_before_install": True,
    "migrations_generated": False,
    "backup_generated": False,
    "pycache_generated": False,
    "workflow_names": [
        "patient_communication.create",
        "patient_communication.update",
        "patient_communication.delete",
        "patient_communication.restore",
        "patient_communication.lifecycle",
    ],
}
add(".installer_manifest.json", json.dumps(manifest, indent=2))

EXPECTED = (
    "models/communication.py",
    "managers.py",
    "permissions/communication.py",
    "policies/communication.py",
    "selectors/communication.py",
    "services/communication.py",
    "events/created.py",
    "events/updated.py",
    "events/deleted.py",
    "events/restored.py",
    "events/status_changed.py",
    "workflows/creation.py",
    "workflows/update.py",
    "workflows/deletion.py",
    "workflows/restore.py",
    "workflows/lifecycle.py",
    "api/serializers/create.py",
    "api/serializers/detail.py",
    "api/serializers/list.py",
    "api/serializers/update.py",
    "api/views/list_create.py",
    "api/views/retrieve_update_destroy.py",
    "api/views/lifecycle.py",
    "api/urls/communication.py",
)


def validate() -> None:
    """Validate structure, architecture, manifest and Python syntax."""
    missing = [path for path in EXPECTED if path not in FILES]
    if missing:
        raise RuntimeError(f"Missing architecture files: {missing}")
    manifest_data = json.loads(FILES[".installer_manifest.json"])
    if (
        manifest_data["canonical_patient"]
        != "apps.patient_management.patients.models.Patient"
    ):
        raise RuntimeError("Canonical Patient reference is invalid.")
    for name in manifest_data["workflow_names"]:
        if (
            name not in FILES["workflow_registry.py"]
            and name not in FILES["workflows/" + name.split(".")[-1] + ".py"]
        ):
            raise RuntimeError(f"Workflow not represented: {name}")
    for path, source in FILES.items():
        if path.endswith(".py"):
            compile(source, path, "exec")
    print("MANIFEST: PASS")
    print("STRUCTURE: PASS")
    print("ARCHITECTURE: PASS")
    print(
        f"PY_COMPILE: PASS ({sum(path.endswith('.py') for path in FILES)} Python files)"
    )
    print(f"EMBEDDED FILES: {len(FILES)}")


def install() -> None:
    """Fresh-install the module after validation."""
    validate()
    if TARGET.exists():
        shutil.rmtree(TARGET)
        print("OLD MODULE: DELETED")
    TARGET.mkdir(parents=True, exist_ok=True)
    for relative_path, source in FILES.items():
        destination = TARGET / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source, encoding="utf-8", newline="\n")
    print(f"FILES WRITTEN: {len(FILES)}")
    print("MIGRATIONS: NOT GENERATED")
    print("PATIENT COMMUNICATION INSTALLATION COMPLETE")


if __name__ == "__main__":
    install()
