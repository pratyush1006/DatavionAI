"""
DatavionOS Patient Consents Fresh Installer v2.1.0.

Recreates the Patient Management Consents module from zero.

The target structure is intentionally identical to the established
Medical History structure:

    consents/
        .installer_manifest.json
        admin.py
        apps.py
        constants.py
        exceptions.py
        managers.py
        urls.py
        validators.py
        workflow_registry.py
        __init__.py
        api/
            filters.py
            urls.py
            __init__.py
            serializers/
            urls/
            views/
        events/
        migrations/
        models/
        permissions/
        policies/
        selectors/
        services/
        tests/
        workflows/

The installer deletes the complete existing Consents directory before
creating the fresh implementation. It does not create a backup or
generate migrations.
"""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

TARGET = Path(__file__).resolve().parent / "apps" / "patient_management" / "consents"


FILES = {
    "__init__.py": '"""\nDatavionOS Patient Consents module.\n"""\n\nfrom __future__ import annotations\n\n__all__ = ()\n',
    "apps.py": '"""\nDjango application configuration for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom django.apps import AppConfig\n\n\nclass ConsentsConfig(AppConfig):\n    """\n    Configure the Patient Consents application.\n    """\n\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "apps.patient_management.consents"\n    label = "patient_management_consents"\n    verbose_name = "Patient Consents"\n\n\n__all__ = (\n    "ConsentsConfig",\n)\n',
    "constants.py": '"""\nConstants for the Patient Consents domain.\n"""\n\nfrom __future__ import annotations\n\nfrom django.db import models\n\n\nclass ConsentPurpose(models.TextChoices):\n    """\n    Supported purposes for a patient consent.\n    """\n\n    TREATMENT = "treatment", "Treatment"\n    PAYMENT = "payment", "Payment"\n    OPERATIONS = "operations", "Operations"\n    RESEARCH = "research", "Research"\n\n\nclass ConsentStatus(models.TextChoices):\n    """\n    Lifecycle states for a patient consent.\n    """\n\n    PENDING = "pending", "Pending"\n    GRANTED = "granted", "Granted"\n    REVOKED = "revoked", "Revoked"\n    EXPIRED = "expired", "Expired"\n\n\n__all__ = (\n    "ConsentPurpose",\n    "ConsentStatus",\n)\n',
    "managers.py": '"""\nManagers and querysets for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom django.db import models\n\nfrom apps.core.models import (\n    BaseManager,\n    BaseQuerySet,\n)\n\n\nclass ConsentQuerySet(\n    BaseQuerySet["PatientConsent"],\n):\n    """\n    Query helpers for Patient Consent records.\n    """\n\n    def for_patient(\n        self,\n        patient_id,\n    ) -> ConsentQuerySet:\n        """\n        Return consent records belonging to a patient.\n        """\n        return self.filter(\n            patient_id=patient_id,\n        )\n\n    def for_organization(\n        self,\n        organization_id,\n    ) -> ConsentQuerySet:\n        """\n        Return consent records belonging to an organization.\n        """\n        return self.filter(\n            organization_id=organization_id,\n        )\n\n    def active(\n        self,\n    ) -> ConsentQuerySet:\n        """\n        Return active, non-deleted consent records.\n        """\n        return self.filter(\n            is_active=True,\n            is_deleted=False,\n        )\n\n    def granted(\n        self,\n    ) -> ConsentQuerySet:\n        """\n        Return currently granted consent records.\n        """\n        return self.filter(\n            status="granted",\n            is_deleted=False,\n        )\n\n\nclass ConsentManager(\n    BaseManager.from_queryset(ConsentQuerySet),\n):\n    """\n    Default manager for Patient Consent records.\n    """\n\n\n__all__ = (\n    "ConsentManager",\n    "ConsentQuerySet",\n)\n',
    "models/__init__.py": '"""\nPatient Consent model exports.\n"""\n\nfrom __future__ import annotations\n\nfrom .consent import (\n    PatientConsent,\n)\n\n__all__ = (\n    "PatientConsent",\n)\n',
    "models/consent.py": '"""\nPatient Consent model.\n\nStores tenant-scoped consent decisions and their lifecycle metadata.\n"""\n\nfrom __future__ import annotations\n\nfrom django.conf import settings\nfrom django.db import models\nfrom django.utils import timezone\n\nfrom apps.core.models import (\n    BaseModel,\n)\nfrom apps.patient_management.patients.models import Patient\nfrom apps.patient_management.consents.constants import (\n    ConsentPurpose,\n    ConsentStatus,\n)\nfrom apps.patient_management.consents.managers import (\n    ConsentManager,\n)\nfrom apps.platform.organizations.models import Organization\n\n\nclass PatientConsent(BaseModel):\n    """\n    Represent a consent granted, pending, revoked, or expired for a patient.\n\n    Patient and organization are deliberately both stored to make tenant and\n    organization boundaries explicit and queryable.\n    """\n\n    objects = ConsentManager()\n\n    organization = models.ForeignKey(\n        Organization,\n        on_delete=models.CASCADE,\n        related_name="patient_consents",\n        help_text="Organization that owns the consent.",\n    )\n\n    patient = models.ForeignKey(\n        Patient,\n        on_delete=models.CASCADE,\n        related_name="patient_consents",\n        help_text="Patient to whom the consent applies.",\n    )\n\n    purpose = models.CharField(\n        max_length=30,\n        choices=ConsentPurpose.choices,\n        help_text="Purpose covered by the consent.",\n    )\n\n    status = models.CharField(\n        max_length=20,\n        choices=ConsentStatus.choices,\n        default=ConsentStatus.PENDING,\n        db_index=True,\n    )\n\n    granted_at = models.DateTimeField(\n        blank=True,\n        null=True,\n    )\n\n    revoked_at = models.DateTimeField(\n        blank=True,\n        null=True,\n    )\n\n    expires_at = models.DateTimeField(\n        blank=True,\n        null=True,\n    )\n\n    granted_by = models.ForeignKey(\n        settings.AUTH_USER_MODEL,\n        on_delete=models.SET_NULL,\n        null=True,\n        blank=True,\n        related_name="granted_patient_consents",\n    )\n\n    notes = models.TextField(\n        blank=True,\n    )\n\n    version = models.CharField(\n        max_length=50,\n        blank=True,\n        default="1",\n    )\n\n    evidence_reference = models.CharField(\n        max_length=255,\n        blank=True,\n        help_text="Reference to the consent evidence or source record.",\n    )\n\n    class Meta:\n        """\n        Configure persistence and indexes for Patient Consents.\n        """\n\n        db_table = "patient_management_consents"\n        verbose_name = "Patient Consent"\n        verbose_name_plural = "Patient Consents"\n        ordering = ("-created_at",)\n        constraints = [\n            models.Index(\n                fields=[\n                    "organization",\n                    "patient",\n                    "status",\n                ],\n                name="pm_consent_org_patient_status_idx",\n            ),\n        ]\n\n    def __str__(\n        self,\n    ) -> str:\n        """\n        Return a stable human-readable representation.\n        """\n        return f"{self.patient_id} - {self.purpose} - {self.status}"\n\n    @property\n    def is_granted(\n        self,\n    ) -> bool:\n        """\n        Return whether the consent is currently granted.\n        """\n        if self.status != ConsentStatus.GRANTED:\n            return False\n\n        if self.expires_at is not None and self.expires_at <= timezone.now():\n            return False\n\n        return True\n\n\n__all__ = (\n    "PatientConsent",\n)\n',
    "policies/__init__.py": '"""\nAuthorization policy exports for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom .consent import (\n    PatientConsentPolicy,\n)\n\n__all__ = (\n    "PatientConsentPolicy",\n)\n',
    "policies/consent.py": '"""\nAuthorization policy for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom apps.patient_management.consents.permissions.consent import (\n    PatientConsentPermission,\n)\nfrom apps.platform.rbac.engines.permission import (\n    user_has_permission,\n)\n\n\nclass PatientConsentPolicy:\n    """\n    Authorize Patient Consent operations through platform RBAC.\n    """\n\n    @staticmethod\n    def _check(\n        *,\n        actor,\n        permission: str,\n        organization,\n    ) -> bool:\n        """\n        Check one RBAC permission within an organization.\n        """\n        return user_has_permission(\n            user=actor,\n            permission=permission,\n            organization=organization,\n        )\n\n    def can_view(\n        self,\n        *,\n        actor,\n        consent,\n    ) -> bool:\n        """\n        Determine whether the actor may view a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.VIEW,\n            organization=consent.organization,\n        )\n\n    def can_list(\n        self,\n        *,\n        actor,\n        organization,\n    ) -> bool:\n        """\n        Determine whether the actor may list consents.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.LIST,\n            organization=organization,\n        )\n\n    def can_create(\n        self,\n        *,\n        actor,\n        organization,\n    ) -> bool:\n        """\n        Determine whether the actor may create a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.CREATE,\n            organization=organization,\n        )\n\n    def can_update(\n        self,\n        *,\n        actor,\n        consent,\n    ) -> bool:\n        """\n        Determine whether the actor may update a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.UPDATE,\n            organization=consent.organization,\n        )\n\n    def can_delete(\n        self,\n        *,\n        actor,\n        consent,\n    ) -> bool:\n        """\n        Determine whether the actor may delete a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.DELETE,\n            organization=consent.organization,\n        )\n\n    def can_restore(\n        self,\n        *,\n        actor,\n        consent,\n    ) -> bool:\n        """\n        Determine whether the actor may restore a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.RESTORE,\n            organization=consent.organization,\n        )\n\n    def can_grant(\n        self,\n        *,\n        actor,\n        consent,\n    ) -> bool:\n        """\n        Determine whether the actor may grant a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.GRANT,\n            organization=consent.organization,\n        )\n\n    def can_revoke(\n        self,\n        *,\n        actor,\n        consent,\n    ) -> bool:\n        """\n        Determine whether the actor may revoke a consent.\n        """\n        return self._check(\n            actor=actor,\n            permission=PatientConsentPermission.REVOKE,\n            organization=consent.organization,\n        )\n\n\n__all__ = (\n    "PatientConsentPolicy",\n)\n',
    "selectors/__init__.py": '"""\nPatient Consent selector exports.\n"""\n\nfrom __future__ import annotations\n\nfrom .consent import (\n    get_consent,\n    list_patient_consents,\n    list_organization_consents,\n)\n\n__all__ = (\n    "get_consent",\n    "list_organization_consents",\n    "list_patient_consents",\n)\n',
    "selectors/consent.py": '"""\nSelectors for Patient Consents.\n\nSelectors own read-side tenant and organization filtering.\n"""\n\nfrom __future__ import annotations\n\nfrom uuid import UUID\n\nfrom apps.common.exceptions import ObjectNotFoundException\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\n\n\ndef get_consent(\n    *,\n    tenant_id: UUID,\n    consent_id: UUID,\n) -> PatientConsent:\n    """\n    Retrieve one consent within the requested tenant.\n    """\n    try:\n        return (\n            PatientConsent.objects\n            .select_related(\n                "organization",\n                "patient",\n                "granted_by",\n            )\n            .get(\n                pk=consent_id,\n                organization__tenant_id=tenant_id,\n            )\n        )\n    except PatientConsent.DoesNotExist as exc:\n        raise ObjectNotFoundException(\n            "Patient consent was not found.",\n        ) from exc\n\n\ndef list_patient_consents(\n    *,\n    tenant_id: UUID,\n    patient_id: UUID,\n):\n    """\n    Return non-deleted consents for one patient in the tenant.\n    """\n    return (\n        PatientConsent.objects\n        .select_related(\n            "organization",\n            "patient",\n            "granted_by",\n        )\n        .filter(\n            patient_id=patient_id,\n            organization__tenant_id=tenant_id,\n            is_deleted=False,\n        )\n        .order_by(\n            "-created_at",\n        )\n    )\n\n\ndef list_organization_consents(\n    *,\n    tenant_id: UUID,\n    organization_id: UUID,\n):\n    """\n    Return non-deleted consents for one organization in the tenant.\n    """\n    return (\n        PatientConsent.objects\n        .select_related(\n            "patient",\n            "granted_by",\n        )\n        .filter(\n            organization_id=organization_id,\n            organization__tenant_id=tenant_id,\n            is_deleted=False,\n        )\n        .order_by(\n            "-created_at",\n        )\n    )\n\n\n__all__ = (\n    "get_consent",\n    "list_organization_consents",\n    "list_patient_consents",\n)\n',
    "services/__init__.py": '"""\nPatient Consent service exports.\n"""\n\nfrom __future__ import annotations\n\nfrom .consent import (\n    create_consent,\n    update_consent,\n    delete_consent,\n    restore_consent,\n    grant_consent,\n    revoke_consent,\n)\n\n__all__ = (\n    "create_consent",\n    "delete_consent",\n    "grant_consent",\n    "restore_consent",\n    "revoke_consent",\n    "update_consent",\n)\n',
    "services/consent.py": '"""\nDomain services for Patient Consents.\n\nAll mutations remain behind this service boundary.\n"""\n\nfrom __future__ import annotations\n\nfrom collections.abc import Mapping\nfrom typing import Any\n\nfrom django.db import transaction\nfrom django.utils import timezone\n\nfrom apps.patient_management.consents.constants import (\n    ConsentStatus,\n)\nfrom apps.patient_management.consents.exceptions import (\n    ConsentAlreadyGrantedError,\n    InvalidConsentStateError,\n)\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\n\n\n@transaction.atomic\ndef create_consent(\n    *,\n    validated_data: Mapping[str, Any],\n    performed_by,\n) -> PatientConsent:\n    """\n    Create a Patient Consent.\n    """\n    data = dict(validated_data)\n    data["created_by"] = performed_by\n\n    return PatientConsent.objects.create(\n        **data,\n    )\n\n\n@transaction.atomic\ndef update_consent(\n    *,\n    instance: PatientConsent,\n    validated_data: Mapping[str, Any],\n    performed_by,\n) -> PatientConsent:\n    """\n    Update mutable Patient Consent fields.\n    """\n    protected = {\n        "id",\n        "organization",\n        "organization_id",\n        "patient",\n        "patient_id",\n        "created_at",\n        "created_by",\n        "created_by_id",\n        "granted_by",\n        "granted_at",\n        "revoked_at",\n        "status",\n        "is_deleted",\n        "deleted_at",\n        "deleted_by_id",\n    }\n\n    changes = {\n        key: value\n        for key, value in dict(validated_data).items()\n        if key not in protected\n    }\n\n    for field, value in changes.items():\n        setattr(\n            instance,\n            field,\n            value,\n        )\n\n    if changes:\n        instance.save(\n            update_fields=[\n                *changes.keys(),\n                "updated_at",\n            ],\n        )\n\n    return instance\n\n\n@transaction.atomic\ndef delete_consent(\n    *,\n    instance: PatientConsent,\n    performed_by,\n) -> PatientConsent:\n    """\n    Soft-delete a Patient Consent.\n    """\n    instance.is_deleted = True\n    instance.is_active = False\n    instance.deleted_at = timezone.now()\n    instance.deleted_by_id = performed_by.pk\n    instance.save(\n        update_fields=[\n            "is_deleted",\n            "is_active",\n            "deleted_at",\n            "deleted_by_id",\n            "updated_at",\n        ],\n    )\n    return instance\n\n\n@transaction.atomic\ndef restore_consent(\n    *,\n    instance: PatientConsent,\n    performed_by,\n) -> PatientConsent:\n    """\n    Restore a previously deleted Patient Consent.\n    """\n    instance.is_deleted = False\n    instance.is_active = True\n    instance.deleted_at = None\n    instance.deleted_by_id = None\n    instance.save(\n        update_fields=[\n            "is_deleted",\n            "is_active",\n            "deleted_at",\n            "deleted_by_id",\n            "updated_at",\n        ],\n    )\n    return instance\n\n\n@transaction.atomic\ndef grant_consent(\n    *,\n    instance: PatientConsent,\n    performed_by,\n) -> PatientConsent:\n    """\n    Grant a pending Patient Consent.\n    """\n    if instance.status == ConsentStatus.GRANTED:\n        raise ConsentAlreadyGrantedError(\n            "Patient consent is already granted.",\n        )\n\n    if instance.status in {\n        ConsentStatus.REVOKED,\n        ConsentStatus.EXPIRED,\n    }:\n        raise InvalidConsentStateError(\n            "A revoked or expired consent cannot be granted again.",\n        )\n\n    instance.status = ConsentStatus.GRANTED\n    instance.granted_at = timezone.now()\n    instance.revoked_at = None\n    instance.granted_by = performed_by\n    instance.save(\n        update_fields=[\n            "status",\n            "granted_at",\n            "revoked_at",\n            "granted_by",\n            "updated_at",\n        ],\n    )\n    return instance\n\n\n@transaction.atomic\ndef revoke_consent(\n    *,\n    instance: PatientConsent,\n    performed_by,\n) -> PatientConsent:\n    """\n    Revoke a granted Patient Consent.\n    """\n    if instance.status != ConsentStatus.GRANTED:\n        raise InvalidConsentStateError(\n            "Only a granted consent can be revoked.",\n        )\n\n    instance.status = ConsentStatus.REVOKED\n    instance.revoked_at = timezone.now()\n    instance.is_active = False\n    instance.save(\n        update_fields=[\n            "status",\n            "revoked_at",\n            "is_active",\n            "updated_at",\n        ],\n    )\n    return instance\n\n\n__all__ = (\n    "create_consent",\n    "delete_consent",\n    "grant_consent",\n    "restore_consent",\n    "revoke_consent",\n    "update_consent",\n)\n',
    "events/__init__.py": '"""\nDomain event exports for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom .created import (\n    PatientConsentCreatedEvent,\n)\nfrom .updated import (\n    PatientConsentUpdatedEvent,\n)\nfrom .deleted import (\n    PatientConsentDeletedEvent,\n)\nfrom .status_changed import (\n    PatientConsentStatusChangedEvent,\n)\n\n__all__ = (\n    "PatientConsentCreatedEvent",\n    "PatientConsentDeletedEvent",\n    "PatientConsentStatusChangedEvent",\n    "PatientConsentUpdatedEvent",\n)\n',
    "events/created.py": '"""\nPatient Consent created domain event.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom uuid import UUID\n\nfrom apps.core.events import DomainEvent\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n)\nclass PatientConsentCreatedEvent(\n    DomainEvent,\n):\n    """\n    Emitted after a Patient Consent is successfully created.\n    """\n\n    tenant_id: UUID\n    actor_id: UUID\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    purpose: str\n    status: str\n\n\n__all__ = (\n    "PatientConsentCreatedEvent",\n)\n',
    "events/updated.py": '"""\nPatient Consent updated domain event.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom typing import Any\nfrom uuid import UUID\n\nfrom apps.core.events import DomainEvent\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n)\nclass PatientConsentUpdatedEvent(\n    DomainEvent,\n):\n    """\n    Emitted after a Patient Consent is updated.\n    """\n\n    tenant_id: UUID\n    actor_id: UUID\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    changes: dict[str, Any]\n\n\n__all__ = (\n    "PatientConsentUpdatedEvent",\n)\n',
    "events/deleted.py": '"""\nPatient Consent deleted domain event.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom uuid import UUID\n\nfrom apps.core.events import DomainEvent\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n)\nclass PatientConsentDeletedEvent(\n    DomainEvent,\n):\n    """\n    Emitted after a Patient Consent is deleted.\n    """\n\n    tenant_id: UUID\n    actor_id: UUID\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n\n\n__all__ = (\n    "PatientConsentDeletedEvent",\n)\n',
    "events/status_changed.py": '"""\nPatient Consent status changed domain event.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom uuid import UUID\n\nfrom apps.core.events import DomainEvent\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n)\nclass PatientConsentStatusChangedEvent(\n    DomainEvent,\n):\n    """\n    Emitted after a Patient Consent status transition.\n    """\n\n    tenant_id: UUID\n    actor_id: UUID\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    previous_status: str\n    new_status: str\n\n\n__all__ = (\n    "PatientConsentStatusChangedEvent",\n)\n',
    "workflows/__init__.py": '"""\nWorkflow exports for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom .creation import (\n    PatientConsentCreationData,\n    PatientConsentCreationRequest,\n    PatientConsentCreationWorkflow,\n)\nfrom .update import (\n    PatientConsentUpdateData,\n    PatientConsentUpdateRequest,\n    PatientConsentUpdateWorkflow,\n)\nfrom .deletion import (\n    PatientConsentDeletionData,\n    PatientConsentDeletionRequest,\n    PatientConsentDeletionWorkflow,\n)\nfrom .lifecycle import (\n    PatientConsentLifecycleData,\n    PatientConsentLifecycleRequest,\n    PatientConsentGrantWorkflow,\n    PatientConsentRevokeWorkflow,\n    PatientConsentRestoreWorkflow,\n)\n\n__all__ = (\n    "PatientConsentCreationData",\n    "PatientConsentCreationRequest",\n    "PatientConsentCreationWorkflow",\n    "PatientConsentDeletionData",\n    "PatientConsentDeletionRequest",\n    "PatientConsentDeletionWorkflow",\n    "PatientConsentGrantWorkflow",\n    "PatientConsentLifecycleData",\n    "PatientConsentLifecycleRequest",\n    "PatientConsentRevokeWorkflow",\n    "PatientConsentRestoreWorkflow",\n    "PatientConsentUpdateData",\n    "PatientConsentUpdateRequest",\n    "PatientConsentUpdateWorkflow",\n)\n',
    "workflows/creation.py": '"""\nPatient Consent creation workflow.\n"""\n\nfrom __future__ import annotations\n\nfrom collections.abc import Mapping\nfrom dataclasses import dataclass\nfrom typing import Any\nfrom uuid import UUID\n\nfrom django.core.exceptions import ObjectDoesNotExist\nfrom django.db import transaction\n\nfrom apps.core.workflows import (\n    BaseWorkflow,\n    WorkflowContext,\n    WorkflowResult,\n)\nfrom apps.patient_management.consents.events import (\n    PatientConsentCreatedEvent,\n)\nfrom apps.patient_management.consents.policies import (\n    PatientConsentPolicy,\n)\nfrom apps.patient_management.consents.services import (\n    create_consent,\n)\nfrom apps.patient_management.patients.models import (\n    Patient,\n)\nfrom apps.platform.accounts.models import (\n    User,\n)\nfrom apps.platform.organizations.models import (\n    Organization,\n)\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentCreationRequest:\n    """\n    Input required to create a Patient Consent.\n    """\n\n    organization_id: UUID\n    patient_id: UUID\n    data: Mapping[str, Any]\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentCreationData:\n    """\n    Result returned after Patient Consent creation.\n    """\n\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    created: bool\n    event_id: UUID | None = None\n\n\nclass PatientConsentCreationWorkflow(\n    BaseWorkflow[PatientConsentCreationData],\n):\n    """\n    Create a Patient Consent within the current tenant.\n    """\n\n    workflow_name = "consent.create"\n\n    def __init__(\n        self,\n        *,\n        request: PatientConsentCreationRequest,\n        policy: PatientConsentPolicy | None = None,\n        logger_=None,\n    ) -> None:\n        """Initialize the workflow instance."""\n        super().__init__(\n            logger_=logger_,\n            payload=request,\n        )\n        self._request = request\n        self._policy = policy or PatientConsentPolicy()\n\n    @transaction.atomic\n    def _run(\n        self,\n        context: WorkflowContext,\n    ) -> WorkflowResult[PatientConsentCreationData]:\n        """\n        Execute the Patient Consent creation workflow.\n        """\n        try:\n            actor = User.objects.get(\n                pk=context.actor_id,\n            )\n            organization = Organization.objects.get(\n                pk=self._request.organization_id,\n                tenant_id=context.tenant_id,\n            )\n            patient = Patient.objects.get(\n                pk=self._request.patient_id,\n                organization_id=organization.pk,\n            )\n        except ObjectDoesNotExist as exc:\n            raise ValueError(\n                "The requested organization or patient was not found.",\n            ) from exc\n\n        if not self._policy.can_create(\n            actor=actor,\n            organization=organization,\n        ):\n            raise PermissionError(\n                "You do not have permission to create a patient consent.",\n            )\n\n        data = dict(\n            self._request.data,\n        )\n        data["organization"] = organization\n        data["patient"] = patient\n\n        consent = create_consent(\n            validated_data=data,\n            performed_by=actor,\n        )\n\n        event = PatientConsentCreatedEvent(\n            tenant_id=context.tenant_id,\n            actor_id=actor.pk,\n            consent_id=consent.pk,\n            patient_id=consent.patient_id,\n            organization_id=consent.organization_id,\n            purpose=consent.purpose,\n            status=consent.status,\n        )\n\n        self.publish_after_commit(\n            event,\n        )\n\n        return WorkflowResult.ok(\n            context=context,\n            data=PatientConsentCreationData(\n                consent_id=consent.pk,\n                patient_id=consent.patient_id,\n                organization_id=consent.organization_id,\n                created=True,\n                event_id=event.event_id,\n            ),\n            message="Patient consent created successfully.",\n            code="consent_created",\n        )\n\n\n__all__ = (\n    "PatientConsentCreationData",\n    "PatientConsentCreationRequest",\n    "PatientConsentCreationWorkflow",\n)\n',
    "workflows/update.py": '"""\nPatient Consent update workflow.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom typing import Any\nfrom uuid import UUID\n\nfrom django.core.exceptions import ObjectDoesNotExist\nfrom django.db import transaction\n\nfrom apps.core.workflows import (\n    BaseWorkflow,\n    WorkflowContext,\n    WorkflowResult,\n)\nfrom apps.patient_management.consents.events import (\n    PatientConsentUpdatedEvent,\n)\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\nfrom apps.patient_management.consents.policies import (\n    PatientConsentPolicy,\n)\nfrom apps.patient_management.consents.services import (\n    update_consent,\n)\nfrom apps.platform.accounts.models import (\n    User,\n)\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentUpdateRequest:\n    """\n    Input required to update a Patient Consent.\n    """\n\n    consent_id: UUID\n    data: dict[str, Any]\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentUpdateData:\n    """\n    Result returned after Patient Consent update.\n    """\n\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    updated: bool\n    event_id: UUID | None = None\n\n\nclass PatientConsentUpdateWorkflow(\n    BaseWorkflow[PatientConsentUpdateData],\n):\n    """\n    Update a Patient Consent within the current tenant.\n    """\n\n    workflow_name = "consent.update"\n\n    def __init__(\n        self,\n        *,\n        request: PatientConsentUpdateRequest,\n        policy: PatientConsentPolicy | None = None,\n        logger_=None,\n    ) -> None:\n        """Initialize the workflow instance."""\n        super().__init__(\n            logger_=logger_,\n            payload=request,\n        )\n        self._request = request\n        self._policy = policy or PatientConsentPolicy()\n\n    @transaction.atomic\n    def _run(\n        self,\n        context: WorkflowContext,\n    ) -> WorkflowResult[PatientConsentUpdateData]:\n        """\n        Execute the Patient Consent update workflow.\n        """\n        try:\n            actor = User.objects.get(\n                pk=context.actor_id,\n            )\n            consent = (\n                PatientConsent.objects\n                .select_related(\n                    "organization",\n                    "patient",\n                )\n                .get(\n                    pk=self._request.consent_id,\n                    organization__tenant_id=context.tenant_id,\n                    is_deleted=False,\n                )\n            )\n        except ObjectDoesNotExist as exc:\n            raise ValueError(\n                "Patient consent was not found.",\n            ) from exc\n\n        if not self._policy.can_update(\n            actor=actor,\n            consent=consent,\n        ):\n            raise PermissionError(\n                "You do not have permission to update this patient consent.",\n            )\n\n        changes = dict(\n            self._request.data,\n        )\n\n        if not changes:\n            return WorkflowResult.ok(\n                context=context,\n                data=PatientConsentUpdateData(\n                    consent_id=consent.pk,\n                    patient_id=consent.patient_id,\n                    organization_id=consent.organization_id,\n                    updated=False,\n                ),\n                message="No consent changes were supplied.",\n                code="consent_unchanged",\n            )\n\n        updated = update_consent(\n            instance=consent,\n            validated_data=changes,\n            performed_by=actor,\n        )\n\n        event = PatientConsentUpdatedEvent(\n            tenant_id=context.tenant_id,\n            actor_id=actor.pk,\n            consent_id=updated.pk,\n            patient_id=updated.patient_id,\n            organization_id=updated.organization_id,\n            changes=changes,\n        )\n\n        self.publish_after_commit(\n            event,\n        )\n\n        return WorkflowResult.ok(\n            context=context,\n            data=PatientConsentUpdateData(\n                consent_id=updated.pk,\n                patient_id=updated.patient_id,\n                organization_id=updated.organization_id,\n                updated=True,\n                event_id=event.event_id,\n            ),\n            message="Patient consent updated successfully.",\n            code="consent_updated",\n        )\n\n\n__all__ = (\n    "PatientConsentUpdateData",\n    "PatientConsentUpdateRequest",\n    "PatientConsentUpdateWorkflow",\n)\n',
    "workflows/deletion.py": '"""\nPatient Consent deletion workflow.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom uuid import UUID\n\nfrom django.core.exceptions import ObjectDoesNotExist\nfrom django.db import transaction\n\nfrom apps.core.workflows import (\n    BaseWorkflow,\n    WorkflowContext,\n    WorkflowResult,\n)\nfrom apps.patient_management.consents.events import (\n    PatientConsentDeletedEvent,\n)\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\nfrom apps.patient_management.consents.policies import (\n    PatientConsentPolicy,\n)\nfrom apps.patient_management.consents.services import (\n    delete_consent,\n)\nfrom apps.platform.accounts.models import (\n    User,\n)\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentDeletionRequest:\n    """\n    Input required to delete a Patient Consent.\n    """\n\n    consent_id: UUID\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentDeletionData:\n    """\n    Result returned after Patient Consent deletion.\n    """\n\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    deleted: bool\n    event_id: UUID | None = None\n\n\nclass PatientConsentDeletionWorkflow(\n    BaseWorkflow[PatientConsentDeletionData],\n):\n    """\n    Soft-delete a Patient Consent within the current tenant.\n    """\n\n    workflow_name = "consent.delete"\n\n    def __init__(\n        self,\n        *,\n        request: PatientConsentDeletionRequest,\n        policy: PatientConsentPolicy | None = None,\n        logger_=None,\n    ) -> None:\n        """Initialize the workflow instance."""\n        super().__init__(\n            logger_=logger_,\n            payload=request,\n        )\n        self._request = request\n        self._policy = policy or PatientConsentPolicy()\n\n    @transaction.atomic\n    def _run(\n        self,\n        context: WorkflowContext,\n    ) -> WorkflowResult[PatientConsentDeletionData]:\n        """\n        Execute the Patient Consent deletion workflow.\n        """\n        try:\n            actor = User.objects.get(\n                pk=context.actor_id,\n            )\n            consent = (\n                PatientConsent.objects\n                .select_related(\n                    "organization",\n                    "patient",\n                )\n                .get(\n                    pk=self._request.consent_id,\n                    organization__tenant_id=context.tenant_id,\n                    is_deleted=False,\n                )\n            )\n        except ObjectDoesNotExist as exc:\n            raise ValueError(\n                "Patient consent was not found.",\n            ) from exc\n\n        if not self._policy.can_delete(\n            actor=actor,\n            consent=consent,\n        ):\n            raise PermissionError(\n                "You do not have permission to delete this patient consent.",\n            )\n\n        delete_consent(\n            instance=consent,\n            performed_by=actor,\n        )\n\n        event = PatientConsentDeletedEvent(\n            tenant_id=context.tenant_id,\n            actor_id=actor.pk,\n            consent_id=consent.pk,\n            patient_id=consent.patient_id,\n            organization_id=consent.organization_id,\n        )\n\n        self.publish_after_commit(\n            event,\n        )\n\n        return WorkflowResult.ok(\n            context=context,\n            data=PatientConsentDeletionData(\n                consent_id=consent.pk,\n                patient_id=consent.patient_id,\n                organization_id=consent.organization_id,\n                deleted=True,\n                event_id=event.event_id,\n            ),\n            message="Patient consent deleted successfully.",\n            code="consent_deleted",\n        )\n\n\n__all__ = (\n    "PatientConsentDeletionData",\n    "PatientConsentDeletionRequest",\n    "PatientConsentDeletionWorkflow",\n)\n',
    "workflows/lifecycle.py": '"""\nPatient Consent lifecycle workflows.\n"""\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom uuid import UUID\n\nfrom django.core.exceptions import ObjectDoesNotExist\nfrom django.db import transaction\n\nfrom apps.core.workflows import (\n    BaseWorkflow,\n    WorkflowContext,\n    WorkflowResult,\n)\nfrom apps.patient_management.consents.events import (\n    PatientConsentStatusChangedEvent,\n)\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\nfrom apps.patient_management.consents.policies import (\n    PatientConsentPolicy,\n)\nfrom apps.patient_management.consents.services import (\n    grant_consent,\n    restore_consent,\n    revoke_consent,\n)\nfrom apps.platform.accounts.models import (\n    User,\n)\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentLifecycleRequest:\n    """\n    Input required for a Patient Consent lifecycle transition.\n    """\n\n    consent_id: UUID\n\n\n@dataclass(\n    frozen=True,\n    slots=True,\n    kw_only=True,\n)\nclass PatientConsentLifecycleData:\n    """\n    Result returned after a Patient Consent lifecycle transition.\n    """\n\n    consent_id: UUID\n    patient_id: UUID\n    organization_id: UUID\n    previous_status: str\n    new_status: str\n    changed: bool\n    event_id: UUID | None = None\n\n\ndef _load_consent(\n    *,\n    context: WorkflowContext,\n    consent_id: UUID,\n    deleted: bool = False,\n):\n    """\n    Load one consent inside the current tenant.\n    """\n    return (\n        PatientConsent.objects\n        .select_related(\n            "organization",\n            "patient",\n        )\n        .get(\n            pk=consent_id,\n            organization__tenant_id=context.tenant_id,\n            is_deleted=deleted,\n        )\n    )\n\n\nclass PatientConsentGrantWorkflow(\n    BaseWorkflow[PatientConsentLifecycleData],\n):\n    """\n    Grant a pending Patient Consent.\n    """\n\n    workflow_name = "consent.grant"\n\n    def __init__(\n        self,\n        *,\n        request: PatientConsentLifecycleRequest,\n        policy: PatientConsentPolicy | None = None,\n        logger_=None,\n    ) -> None:\n        """Initialize the workflow instance."""\n        super().__init__(\n            logger_=logger_,\n            payload=request,\n        )\n        self._request = request\n        self._policy = policy or PatientConsentPolicy()\n\n    @transaction.atomic\n    def _run(\n        self,\n        context: WorkflowContext,\n    ) -> WorkflowResult[PatientConsentLifecycleData]:\n        """\n        Execute the grant transition.\n        """\n        try:\n            actor = User.objects.get(\n                pk=context.actor_id,\n            )\n            consent = _load_consent(\n                context=context,\n                consent_id=self._request.consent_id,\n            )\n        except ObjectDoesNotExist as exc:\n            raise ValueError(\n                "Patient consent was not found.",\n            ) from exc\n\n        if not self._policy.can_grant(\n            actor=actor,\n            consent=consent,\n        ):\n            raise PermissionError(\n                "You do not have permission to grant this patient consent.",\n            )\n\n        previous = consent.status\n        consent = grant_consent(\n            instance=consent,\n            performed_by=actor,\n        )\n\n        event = PatientConsentStatusChangedEvent(\n            tenant_id=context.tenant_id,\n            actor_id=actor.pk,\n            consent_id=consent.pk,\n            patient_id=consent.patient_id,\n            organization_id=consent.organization_id,\n            previous_status=previous,\n            new_status=consent.status,\n        )\n        self.publish_after_commit(\n            event,\n        )\n\n        return WorkflowResult.ok(\n            context=context,\n            data=PatientConsentLifecycleData(\n                consent_id=consent.pk,\n                patient_id=consent.patient_id,\n                organization_id=consent.organization_id,\n                previous_status=previous,\n                new_status=consent.status,\n                changed=True,\n                event_id=event.event_id,\n            ),\n            message="Patient consent granted successfully.",\n            code="consent_granted",\n        )\n\n\nclass PatientConsentRevokeWorkflow(\n    BaseWorkflow[PatientConsentLifecycleData],\n):\n    """\n    Revoke a granted Patient Consent.\n    """\n\n    workflow_name = "consent.revoke"\n\n    def __init__(\n        self,\n        *,\n        request: PatientConsentLifecycleRequest,\n        policy: PatientConsentPolicy | None = None,\n        logger_=None,\n    ) -> None:\n        """Initialize the workflow instance."""\n        super().__init__(\n            logger_=logger_,\n            payload=request,\n        )\n        self._request = request\n        self._policy = policy or PatientConsentPolicy()\n\n    @transaction.atomic\n    def _run(\n        self,\n        context: WorkflowContext,\n    ) -> WorkflowResult[PatientConsentLifecycleData]:\n        """\n        Execute the revoke transition.\n        """\n        try:\n            actor = User.objects.get(\n                pk=context.actor_id,\n            )\n            consent = _load_consent(\n                context=context,\n                consent_id=self._request.consent_id,\n            )\n        except ObjectDoesNotExist as exc:\n            raise ValueError(\n                "Patient consent was not found.",\n            ) from exc\n\n        if not self._policy.can_revoke(\n            actor=actor,\n            consent=consent,\n        ):\n            raise PermissionError(\n                "You do not have permission to revoke this patient consent.",\n            )\n\n        previous = consent.status\n        consent = revoke_consent(\n            instance=consent,\n            performed_by=actor,\n        )\n\n        event = PatientConsentStatusChangedEvent(\n            tenant_id=context.tenant_id,\n            actor_id=actor.pk,\n            consent_id=consent.pk,\n            patient_id=consent.patient_id,\n            organization_id=consent.organization_id,\n            previous_status=previous,\n            new_status=consent.status,\n        )\n        self.publish_after_commit(\n            event,\n        )\n\n        return WorkflowResult.ok(\n            context=context,\n            data=PatientConsentLifecycleData(\n                consent_id=consent.pk,\n                patient_id=consent.patient_id,\n                organization_id=consent.organization_id,\n                previous_status=previous,\n                new_status=consent.status,\n                changed=True,\n                event_id=event.event_id,\n            ),\n            message="Patient consent revoked successfully.",\n            code="consent_revoked",\n        )\n\n\nclass PatientConsentRestoreWorkflow(\n    BaseWorkflow[PatientConsentLifecycleData],\n):\n    """\n    Restore a deleted Patient Consent.\n    """\n\n    workflow_name = "consent.restore"\n\n    def __init__(\n        self,\n        *,\n        request: PatientConsentLifecycleRequest,\n        policy: PatientConsentPolicy | None = None,\n        logger_=None,\n    ) -> None:\n        """Initialize the workflow instance."""\n        super().__init__(\n            logger_=logger_,\n            payload=request,\n        )\n        self._request = request\n        self._policy = policy or PatientConsentPolicy()\n\n    @transaction.atomic\n    def _run(\n        self,\n        context: WorkflowContext,\n    ) -> WorkflowResult[PatientConsentLifecycleData]:\n        """\n        Execute the restore transition.\n        """\n        try:\n            actor = User.objects.get(\n                pk=context.actor_id,\n            )\n            consent = _load_consent(\n                context=context,\n                consent_id=self._request.consent_id,\n                deleted=True,\n            )\n        except ObjectDoesNotExist as exc:\n            raise ValueError(\n                "Deleted patient consent was not found.",\n            ) from exc\n\n        if not self._policy.can_restore(\n            actor=actor,\n            consent=consent,\n        ):\n            raise PermissionError(\n                "You do not have permission to restore this patient consent.",\n            )\n\n        previous = consent.status\n        consent = restore_consent(\n            instance=consent,\n            performed_by=actor,\n        )\n\n        return WorkflowResult.ok(\n            context=context,\n            data=PatientConsentLifecycleData(\n                consent_id=consent.pk,\n                patient_id=consent.patient_id,\n                organization_id=consent.organization_id,\n                previous_status=previous,\n                new_status=consent.status,\n                changed=True,\n            ),\n            message="Patient consent restored successfully.",\n            code="consent_restored",\n        )\n\n\n__all__ = (\n    "PatientConsentGrantWorkflow",\n    "PatientConsentLifecycleData",\n    "PatientConsentLifecycleRequest",\n    "PatientConsentRevokeWorkflow",\n    "PatientConsentRestoreWorkflow",\n)\n',
    "workflow_registry.py": '"""\nWorkflow registry for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom apps.core.workflows import (\n    workflow_registry,\n)\nfrom apps.patient_management.consents.workflows import (\n    PatientConsentCreationWorkflow,\n    PatientConsentDeletionWorkflow,\n    PatientConsentGrantWorkflow,\n    PatientConsentRestoreWorkflow,\n    PatientConsentRevokeWorkflow,\n    PatientConsentUpdateWorkflow,\n)\n\n\ndef register_workflows() -> None:\n    """\n    Register all Patient Consent workflows.\n    """\n    registrations = {\n        "consent.create": PatientConsentCreationWorkflow,\n        "consent.update": PatientConsentUpdateWorkflow,\n        "consent.delete": PatientConsentDeletionWorkflow,\n        "consent.restore": PatientConsentRestoreWorkflow,\n        "consent.grant": PatientConsentGrantWorkflow,\n        "consent.revoke": PatientConsentRevokeWorkflow,\n    }\n\n    for name, workflow in registrations.items():\n        if not workflow_registry.is_registered(\n            name,\n        ):\n            workflow_registry.register(\n                name=name,\n                workflow=workflow,\n            )\n\n\n__all__ = (\n    "register_workflows",\n)\n',
    "admin.py": '"""\nDjango admin configuration for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom django.contrib import admin\n\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\n\n\n@admin.register(PatientConsent)\nclass PatientConsentAdmin(admin.ModelAdmin):\n    """\n    Admin configuration for Patient Consent records.\n    """\n\n    list_display = (\n        "id",\n        "patient",\n        "organization",\n        "purpose",\n        "status",\n        "granted_at",\n        "expires_at",\n    )\n    list_filter = (\n        "purpose",\n        "status",\n        "is_active",\n        "is_deleted",\n    )\n    search_fields = (\n        "id",\n        "patient__id",\n        "evidence_reference",\n    )\n    ordering = (\n        "-created_at",\n    )\n\n\n__all__ = (\n    "PatientConsentAdmin",\n)\n',
    "validators.py": '"""\nValidation helpers for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom django.core.exceptions import ValidationError\nfrom django.utils import timezone\n\n\ndef validate_consent_dates(\n    *,\n    expires_at=None,\n    granted_at=None,\n) -> None:\n    """\n    Validate chronological Patient Consent timestamps.\n    """\n    if expires_at is not None and granted_at is not None:\n        if expires_at <= granted_at:\n            raise ValidationError(\n                "Consent expiration must occur after consent grant time.",\n            )\n\n    if expires_at is not None and expires_at <= timezone.now():\n        raise ValidationError(\n            "Consent expiration must be in the future.",\n        )\n\n\ndef validate_consent_notes(\n    value: str,\n) -> str:\n    """\n    Normalize consent notes and reject excessively large values.\n    """\n    normalized = str(\n        value or "",\n    ).strip()\n\n    if len(normalized) > 10000:\n        raise ValidationError(\n            "Consent notes cannot exceed 10,000 characters.",\n        )\n\n    return normalized\n\n\n__all__ = (\n    "validate_consent_dates",\n    "validate_consent_notes",\n)\n',
    "api/__init__.py": '"""\nPatient Consent API package.\n"""\n\nfrom __future__ import annotations\n\n__all__ = ()\n',
    "api/filters.py": '"""\nFilters for Patient Consent list endpoints.\n"""\n\nfrom __future__ import annotations\n\nimport django_filters\n\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\n\n\nclass PatientConsentFilter(\n    django_filters.FilterSet,\n):\n    """\n    Filter Patient Consent records by common domain fields.\n    """\n\n    class Meta:\n        """\n        Configure supported consent filters.\n        """\n\n        model = PatientConsent\n        fields = (\n            "patient",\n            "organization",\n            "purpose",\n            "status",\n        )\n\n\n__all__ = (\n    "PatientConsentFilter",\n)\n',
    "api/serializers/__init__.py": '"""\nPatient Consent serializer exports.\n"""\n\nfrom __future__ import annotations\n\nfrom .create import (\n    PatientConsentCreateSerializer,\n)\nfrom .detail import (\n    PatientConsentDetailSerializer,\n)\nfrom .list import (\n    PatientConsentListSerializer,\n)\nfrom .update import (\n    PatientConsentUpdateSerializer,\n)\n\n__all__ = (\n    "PatientConsentCreateSerializer",\n    "PatientConsentDetailSerializer",\n    "PatientConsentListSerializer",\n    "PatientConsentUpdateSerializer",\n)\n',
    "api/serializers/create.py": '"""\nPatient Consent creation serializer.\n\nValidation and payload preparation only.\n\nPatient Consent creation is performed by PatientConsentCreationWorkflow.\n"""\n\nfrom __future__ import annotations\n\nfrom rest_framework import serializers\n\nfrom apps.patient_management.consents.api.serializers.base import (\n    PatientConsentBaseSerializer,\n)\nfrom apps.patient_management.consents.constants import (\n    ConsentPurpose,\n)\nfrom apps.patient_management.consents.validators import (\n    validate_consent_dates,\n    validate_consent_notes,\n)\n\n\nclass PatientConsentCreateSerializer(\n    PatientConsentBaseSerializer,\n):\n    """\n    Validate Patient Consent creation input.\n    """\n\n    class Meta(PatientConsentBaseSerializer.Meta):\n        """\n        Configure creation serializer fields.\n        """\n\n        fields = (\n            "organization",\n            "patient",\n            "purpose",\n            "expires_at",\n            "notes",\n            "version",\n            "evidence_reference",\n        )\n        extra_kwargs = {\n            "organization": {\n                "required": True,\n            },\n            "patient": {\n                "required": True,\n            },\n            "purpose": {\n                "required": True,\n            },\n        }\n\n    def validate_purpose(\n        self,\n        value,\n    ):\n        """\n        Validate the requested consent purpose.\n        """\n        if value not in ConsentPurpose.values:\n            raise serializers.ValidationError(\n                "Unsupported consent purpose.",\n            )\n        return value\n\n    def validate_notes(\n        self,\n        value,\n    ):\n        """\n        Validate and normalize consent notes.\n        """\n        return validate_consent_notes(\n            value,\n        )\n\n    def validate(\n        self,\n        attrs,\n    ):\n        """\n        Validate consent date relationships.\n        """\n        validate_consent_dates(\n            expires_at=attrs.get(\n                "expires_at",\n            ),\n        )\n        return attrs\n\n\n__all__ = (\n    "PatientConsentCreateSerializer",\n)\n',
    "api/serializers/update.py": '"""\nPatient Consent update serializer.\n\nLifecycle fields remain workflow-controlled.\n"""\n\nfrom __future__ import annotations\n\nfrom rest_framework import serializers\n\nfrom apps.patient_management.consents.api.serializers.base import (\n    PatientConsentBaseSerializer,\n)\nfrom apps.patient_management.consents.validators import (\n    validate_consent_dates,\n    validate_consent_notes,\n)\n\n\nclass PatientConsentUpdateSerializer(\n    PatientConsentBaseSerializer,\n):\n    """\n    Validate mutable Patient Consent fields.\n    """\n\n    class Meta(PatientConsentBaseSerializer.Meta):\n        """\n        Configure update serializer fields.\n        """\n\n        fields = (\n            "purpose",\n            "expires_at",\n            "notes",\n            "version",\n            "evidence_reference",\n        )\n\n    def validate_notes(\n        self,\n        value,\n    ):\n        """\n        Validate and normalize consent notes.\n        """\n        return validate_consent_notes(\n            value,\n        )\n\n    def validate(\n        self,\n        attrs,\n    ):\n        """\n        Validate update-side consent dates.\n        """\n        validate_consent_dates(\n            expires_at=attrs.get(\n                "expires_at",\n            ),\n        )\n        return attrs\n\n\n__all__ = (\n    "PatientConsentUpdateSerializer",\n)\n',
    "api/serializers/detail.py": '"""\nPatient Consent detail serializer.\n"""\n\nfrom __future__ import annotations\n\nfrom apps.patient_management.consents.api.serializers.base import (\n    PatientConsentBaseSerializer,\n)\n\n\nclass PatientConsentDetailSerializer(\n    PatientConsentBaseSerializer,\n):\n    """\n    Serialize a complete Patient Consent representation.\n    """\n\n    class Meta(PatientConsentBaseSerializer.Meta):\n        """\n        Configure detail serializer fields.\n        """\n\n        fields = PatientConsentBaseSerializer.Meta.fields\n\n\n__all__ = (\n    "PatientConsentDetailSerializer",\n)\n',
    "api/serializers/list.py": '"""\nPatient Consent list serializer.\n"""\n\nfrom __future__ import annotations\n\nfrom apps.patient_management.consents.api.serializers.base import (\n    PatientConsentBaseSerializer,\n)\n\n\nclass PatientConsentListSerializer(\n    PatientConsentBaseSerializer,\n):\n    """\n    Serialize Patient Consent records for collection endpoints.\n    """\n\n    class Meta(PatientConsentBaseSerializer.Meta):\n        """\n        Configure list serializer fields.\n        """\n\n        fields = (\n            "id",\n            "patient",\n            "purpose",\n            "status",\n            "granted_at",\n            "revoked_at",\n            "expires_at",\n            "version",\n            "created_at",\n        )\n\n\n__all__ = (\n    "PatientConsentListSerializer",\n)\n',
    "api/views/__init__.py": '"""\nPatient Consent API view exports.\n"""\n\nfrom __future__ import annotations\n\nfrom .list_create import (\n    PatientConsentListCreateView,\n)\nfrom .retrieve_update_destroy import (\n    PatientConsentRetrieveUpdateDestroyView,\n)\nfrom .lifecycle import (\n    PatientConsentGrantView,\n    PatientConsentRevokeView,\n    PatientConsentRestoreView,\n)\n\n__all__ = (\n    "PatientConsentGrantView",\n    "PatientConsentListCreateView",\n    "PatientConsentRetrieveUpdateDestroyView",\n    "PatientConsentRestoreView",\n    "PatientConsentRevokeView",\n)\n',
    "api/views/list_create.py": '"""\nPatient Consent list/create API view.\n"""\n\nfrom __future__ import annotations\n\nfrom rest_framework import generics\nfrom rest_framework.exceptions import APIException\nfrom rest_framework.permissions import IsAuthenticated\n\nfrom apps.patient_management.consents.api.filters import (\n    PatientConsentFilter,\n)\nfrom apps.patient_management.consents.api.serializers import (\n    PatientConsentCreateSerializer,\n    PatientConsentListSerializer,\n)\nfrom apps.patient_management.consents.selectors import (\n    list_organization_consents,\n)\nfrom apps.patient_management.consents.workflows import (\n    PatientConsentCreationRequest,\n    PatientConsentCreationWorkflow,\n)\n\n\nclass PatientConsentListCreateView(\n    generics.ListCreateAPIView,\n):\n    """\n    Provide list and create operations for Patient Consents.\n    """\n\n    permission_classes = (\n        IsAuthenticated,\n    )\n    filterset_class = PatientConsentFilter\n\n    def get_serializer_class(\n        self,\n    ):\n        """\n        Select the serializer appropriate to the HTTP operation.\n        """\n        if self.request.method == "POST":\n            return PatientConsentCreateSerializer\n\n        return PatientConsentListSerializer\n\n    def get_queryset(\n        self,\n    ):\n        """\n        Return organization-scoped consent records.\n        """\n        organization = self.request.user.organization_roles.select_related(\n            "organization",\n        ).first().organization\n\n        tenant_id = organization.tenant_id\n\n        return list_organization_consents(\n            tenant_id=tenant_id,\n            organization_id=organization.pk,\n        )\n\n    def perform_create(\n        self,\n        serializer,\n    ) -> None:\n        """\n        Create a Patient Consent through the workflow layer.\n        """\n        data = serializer.validated_data\n        organization = data["organization"]\n\n        workflow = PatientConsentCreationWorkflow(\n            request=PatientConsentCreationRequest(\n                organization_id=organization.pk,\n                patient_id=data["patient"].pk,\n                data=data,\n            ),\n        )\n\n        try:\n            workflow.run(\n                actor_id=self.request.user.pk,\n                tenant_id=organization.tenant_id,\n            )\n        except (PermissionError, ValueError) as exc:\n            raise APIException(\n                str(exc),\n            ) from exc\n\n\n__all__ = (\n    "PatientConsentListCreateView",\n)\n',
    "api/views/retrieve_update_destroy.py": '"""\nPatient Consent retrieve/update/delete API view.\n"""\n\nfrom __future__ import annotations\n\nfrom uuid import UUID\n\nfrom rest_framework import generics\nfrom rest_framework.permissions import IsAuthenticated\n\nfrom apps.patient_management.consents.api.serializers import (\n    PatientConsentDetailSerializer,\n    PatientConsentUpdateSerializer,\n)\nfrom apps.patient_management.consents.models import (\n    PatientConsent,\n)\nfrom apps.patient_management.consents.selectors import (\n    get_consent,\n)\nfrom apps.patient_management.consents.workflows import (\n    PatientConsentDeletionRequest,\n    PatientConsentDeletionWorkflow,\n    PatientConsentUpdateRequest,\n    PatientConsentUpdateWorkflow,\n)\n\n\nclass PatientConsentRetrieveUpdateDestroyView(\n    generics.RetrieveUpdateDestroyAPIView,\n):\n    """\n    Provide retrieve, update, and delete operations for Patient Consents.\n    """\n\n    permission_classes = (\n        IsAuthenticated,\n    )\n\n    def get_serializer_class(\n        self,\n    ):\n        """\n        Select detail or update serialization.\n        """\n        if self.request.method in {\n            "PUT",\n            "PATCH",\n        }:\n            return PatientConsentUpdateSerializer\n\n        return PatientConsentDetailSerializer\n\n    def get_object(\n        self,\n    ) -> PatientConsent:\n        """\n        Resolve a consent through the tenant-scoped selector.\n        """\n        return get_consent(\n            tenant_id=self.request.user.tenant_id,\n            consent_id=UUID(\n                str(self.kwargs["pk"]),\n            ),\n        )\n\n    def perform_update(\n        self,\n        serializer,\n    ) -> None:\n        """\n        Update the consent through its workflow.\n        """\n        workflow = PatientConsentUpdateWorkflow(\n            request=PatientConsentUpdateRequest(\n                consent_id=self.get_object().pk,\n                data=serializer.validated_data,\n            ),\n        )\n        workflow.run(\n            actor_id=self.request.user.pk,\n            tenant_id=self.get_object().organization.tenant_id,\n        )\n\n    def perform_destroy(\n        self,\n        instance,\n    ) -> None:\n        """\n        Delete the consent through its workflow.\n        """\n        workflow = PatientConsentDeletionWorkflow(\n            request=PatientConsentDeletionRequest(\n                consent_id=instance.pk,\n            ),\n        )\n        workflow.run(\n            actor_id=self.request.user.pk,\n            tenant_id=instance.organization.tenant_id,\n        )\n\n\n__all__ = (\n    "PatientConsentRetrieveUpdateDestroyView",\n)\n',
    "api/views/lifecycle.py": '"""\nPatient Consent lifecycle API views.\n"""\n\nfrom __future__ import annotations\n\nfrom uuid import UUID\n\nfrom rest_framework import status\nfrom rest_framework.permissions import IsAuthenticated\nfrom rest_framework.response import Response\nfrom rest_framework.views import APIView\n\nfrom apps.patient_management.consents.selectors import (\n    get_consent,\n)\nfrom apps.patient_management.consents.workflows import (\n    PatientConsentGrantWorkflow,\n    PatientConsentLifecycleRequest,\n    PatientConsentRestoreWorkflow,\n    PatientConsentRevokeWorkflow,\n)\n\n\nclass PatientConsentGrantView(\n    APIView,\n):\n    """\n    Grant a Patient Consent through its workflow.\n    """\n\n    permission_classes = (\n        IsAuthenticated,\n    )\n\n    def post(\n        self,\n        request,\n        pk,\n    ):\n        """\n        Execute the grant workflow.\n        """\n        consent = get_consent(\n            tenant_id=request.user.tenant_id,\n            consent_id=UUID(\n                str(pk),\n            ),\n        )\n        result = PatientConsentGrantWorkflow(\n            request=PatientConsentLifecycleRequest(\n                consent_id=consent.pk,\n            ),\n        ).run(\n            actor_id=request.user.pk,\n            tenant_id=consent.organization.tenant_id,\n        )\n        return Response(\n            result.data,\n            status=status.HTTP_200_OK,\n        )\n\n\nclass PatientConsentRevokeView(\n    APIView,\n):\n    """\n    Revoke a Patient Consent through its workflow.\n    """\n\n    permission_classes = (\n        IsAuthenticated,\n    )\n\n    def post(\n        self,\n        request,\n        pk,\n    ):\n        """\n        Execute the revoke workflow.\n        """\n        consent = get_consent(\n            tenant_id=request.user.tenant_id,\n            consent_id=UUID(\n                str(pk),\n            ),\n        )\n        result = PatientConsentRevokeWorkflow(\n            request=PatientConsentLifecycleRequest(\n                consent_id=consent.pk,\n            ),\n        ).run(\n            actor_id=request.user.pk,\n            tenant_id=consent.organization.tenant_id,\n        )\n        return Response(\n            result.data,\n            status=status.HTTP_200_OK,\n        )\n\n\nclass PatientConsentRestoreView(\n    APIView,\n):\n    """\n    Restore a deleted Patient Consent through its workflow.\n    """\n\n    permission_classes = (\n        IsAuthenticated,\n    )\n\n    def post(\n        self,\n        request,\n        pk,\n    ):\n        """\n        Execute the restore workflow.\n        """\n        consent = get_consent(\n            tenant_id=request.user.tenant_id,\n            consent_id=UUID(\n                str(pk),\n            ),\n        )\n        result = PatientConsentRestoreWorkflow(\n            request=PatientConsentLifecycleRequest(\n                consent_id=consent.pk,\n            ),\n        ).run(\n            actor_id=request.user.pk,\n            tenant_id=consent.organization.tenant_id,\n        )\n        return Response(\n            result.data,\n            status=status.HTTP_200_OK,\n        )\n\n\n__all__ = (\n    "PatientConsentGrantView",\n    "PatientConsentRestoreView",\n    "PatientConsentRevokeView",\n)\n',
    "api/urls/__init__.py": '"""\nPatient Consent API URL package.\n"""\n\nfrom __future__ import annotations\n\n__all__ = ()\n',
    "api/urls/consent.py": '"""\nPatient Consent endpoint routes.\n"""\n\nfrom __future__ import annotations\n\nfrom django.urls import path\n\nfrom apps.patient_management.consents.api.views import (\n    PatientConsentGrantView,\n    PatientConsentListCreateView,\n    PatientConsentRetrieveUpdateDestroyView,\n    PatientConsentRestoreView,\n    PatientConsentRevokeView,\n)\n\nurlpatterns = [\n    path(\n        "",\n        PatientConsentListCreateView.as_view(),\n        name="consent-list-create",\n    ),\n    path(\n        "<uuid:pk>/",\n        PatientConsentRetrieveUpdateDestroyView.as_view(),\n        name="consent-detail",\n    ),\n    path(\n        "<uuid:pk>/grant/",\n        PatientConsentGrantView.as_view(),\n        name="consent-grant",\n    ),\n    path(\n        "<uuid:pk>/revoke/",\n        PatientConsentRevokeView.as_view(),\n        name="consent-revoke",\n    ),\n    path(\n        "<uuid:pk>/restore/",\n        PatientConsentRestoreView.as_view(),\n        name="consent-restore",\n    ),\n]\n\n__all__ = (\n    "urlpatterns",\n)\n',
    "urls.py": '"""\nTop-level URL configuration for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\nfrom django.urls import include\nfrom django.urls import path\n\nurlpatterns = [\n    path(\n        "",\n        include(\n            "apps.patient_management.consents.api.urls",\n        ),\n    ),\n]\n\n__all__ = (\n    "urlpatterns",\n)\n',
    "tests/__init__.py": '"""\nPatient Consent test package.\n"""\n\nfrom __future__ import annotations\n\n__all__ = ()\n',
    "migrations/__init__.py": '"""\nMigration package for Patient Consents.\n\nNo migration is generated by the module installer.\n"""\n\nfrom __future__ import annotations\n\n__all__ = ()\n',
    "permissions/consent.py": '"""\nRBAC permission identifiers for Patient Consents.\n"""\n\nfrom __future__ import annotations\n\n\nclass PatientConsentPermission:\n    """\n    Stable RBAC permission codes for Patient Consents.\n    """\n\n    MODULE = "patient_management.consents"\n\n    VIEW = f"{MODULE}.view"\n    LIST = f"{MODULE}.list"\n    CREATE = f"{MODULE}.create"\n    UPDATE = f"{MODULE}.update"\n    DELETE = f"{MODULE}.delete"\n    RESTORE = f"{MODULE}.restore"\n    GRANT = f"{MODULE}.grant"\n    REVOKE = f"{MODULE}.revoke"\n\n    ALL = (\n        VIEW,\n        LIST,\n        CREATE,\n        UPDATE,\n        DELETE,\n        RESTORE,\n        GRANT,\n        REVOKE,\n    )\n\n\n__all__ = (\n    "PatientConsentPermission",\n)\n',
    "exceptions.py": '"""\nPatient Consent domain exceptions.\n\nDomain-specific exceptions for consent validation and lifecycle handling.\n"""\n\nfrom __future__ import annotations\n\n\nclass PatientConsentError(Exception):\n    """\n    Base exception for Patient Consent domain errors.\n    """\n\n\nclass PatientConsentValidationError(PatientConsentError):\n    """\n    Raised when Patient Consent data fails domain validation.\n    """\n\n\nclass PatientConsentNotFoundError(PatientConsentError):\n    """\n    Raised when a requested Patient Consent cannot be found.\n    """\n\n\n__all__ = (\n    "PatientConsentError",\n    "PatientConsentValidationError",\n    "PatientConsentNotFoundError",\n)\n',
    "permissions/__init__.py": '"""\nPatient Consent permission package.\n"""\n\nfrom __future__ import annotations\n\nfrom apps.patient_management.consents.permissions.consent import (\n    PatientConsentPermission,\n)\n\n__all__ = (\n    "PatientConsentPermission",\n)\n',
    "api/urls.py": '"""\nPatient Consent API URL entry point.\n\nThe detailed consent routes are maintained in the api.urls package.\n"""\n\nfrom __future__ import annotations\n\nfrom apps.patient_management.consents.api.urls.consent import (\n    urlpatterns,\n)\n\n__all__ = (\n    "urlpatterns",\n)\n',
    ".installer_manifest.json": '{\n  "architecture": "API -> RBAC -> Workflow -> Policy -> Service -> Model -> Domain Event",\n  "backup_generated": false,\n  "canonical_patient": "apps.patient_management.patients.models.Patient",\n  "delete_existing_module_before_install": true,\n  "fresh_install": true,\n  "installer": "DatavionOS Patient Consents Production Installer",\n  "migrations_generated": false,\n  "module": "apps.patient_management.consents",\n  "pycache_generated": false,\n  "version": "2.0.1"\n}\n',
}


EXPECTED_STRUCTURE = [
    ".installer_manifest.json",
    "admin.py",
    "apps.py",
    "constants.py",
    "exceptions.py",
    "managers.py",
    "urls.py",
    "validators.py",
    "workflow_registry.py",
    "__init__.py",
    "api/filters.py",
    "api/urls.py",
    "api/__init__.py",
    "api/serializers/create.py",
    "api/serializers/detail.py",
    "api/serializers/list.py",
    "api/serializers/update.py",
    "api/serializers/__init__.py",
    "api/urls/consent.py",
    "api/urls/__init__.py",
    "api/views/lifecycle.py",
    "api/views/list_create.py",
    "api/views/retrieve_update_destroy.py",
    "api/views/__init__.py",
    "events/created.py",
    "events/deleted.py",
    "events/status_changed.py",
    "events/updated.py",
    "events/__init__.py",
    "migrations/__init__.py",
    "models/consent.py",
    "models/__init__.py",
    "permissions/consent.py",
    "permissions/__init__.py",
    "policies/consent.py",
    "policies/__init__.py",
    "selectors/consent.py",
    "selectors/__init__.py",
    "services/consent.py",
    "services/__init__.py",
    "tests/__init__.py",
    "workflows/creation.py",
    "workflows/deletion.py",
    "workflows/lifecycle.py",
    "workflows/update.py",
    "workflows/__init__.py",
]


WORKFLOW_NAMES = (
    "consent.create",
    "consent.update",
    "consent.delete",
    "consent.restore",
    "consent.grant",
    "consent.revoke",
)


def parse_source(
    *,
    relative_path: str,
    source: str,
) -> ast.Module:
    """
    Parse generated Python source.
    """
    try:
        return ast.parse(
            source,
            filename=relative_path,
        )
    except SyntaxError as exc:
        raise RuntimeError(
            f"Syntax error in {relative_path}: {exc}",
        ) from exc


def validate_structure() -> None:
    """
    Validate the exact Medical History-style source structure.
    """
    actual = set(FILES)
    expected = set(EXPECTED_STRUCTURE)

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    if missing:
        raise RuntimeError(
            "Required structure entries missing:\n  " + "\n  ".join(missing),
        )

    if extra:
        raise RuntimeError(
            "Unexpected structure entries present:\n  " + "\n  ".join(extra),
        )

    print("STRUCTURE: PASS")


def validate_source_style() -> None:
    """
    Validate DatavionOS source documentation and export conventions.
    """
    count = 0

    for relative_path, source in FILES.items():
        if not relative_path.endswith(".py"):
            continue

        tree = parse_source(
            relative_path=relative_path,
            source=source,
        )

        if not ast.get_docstring(
            tree,
            clean=False,
        ):
            raise RuntimeError(
                f"Module docstring missing: {relative_path}",
            )

        if not any(
            isinstance(node, ast.ImportFrom)
            and node.module == "__future__"
            and any(alias.name == "annotations" for alias in node.names)
            for node in tree.body
        ):
            raise RuntimeError(
                f"from __future__ import annotations missing: {relative_path}",
            )

        if not any(
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            )
            for node in tree.body
        ):
            raise RuntimeError(
                f"__all__ declaration missing: {relative_path}",
            )

        for node in ast.walk(tree):
            if isinstance(
                node,
                (
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ) and not ast.get_docstring(
                node,
                clean=False,
            ):
                raise RuntimeError(
                    f"Definition docstring missing: {relative_path}:{node.name}",
                )

        count += 1

    print(
        f"STYLE: PASS ({count} Python files)",
    )


def validate_architecture() -> None:
    """
    Validate the canonical Patient Management dependency chain.
    """
    required_layers = (
        "models/consent.py",
        "permissions/consent.py",
        "policies/consent.py",
        "selectors/consent.py",
        "services/consent.py",
        "events/created.py",
        "events/updated.py",
        "events/deleted.py",
        "events/status_changed.py",
        "workflows/creation.py",
        "workflows/update.py",
        "workflows/deletion.py",
        "workflows/lifecycle.py",
        "api/serializers/create.py",
        "api/serializers/detail.py",
        "api/serializers/list.py",
        "api/serializers/update.py",
        "api/views/list_create.py",
        "api/views/retrieve_update_destroy.py",
        "api/views/lifecycle.py",
    )

    for relative_path in required_layers:
        if relative_path not in FILES:
            raise RuntimeError(
                f"Architecture file missing: {relative_path}",
            )

    model_source = FILES["models/consent.py"]

    if (
        "apps.patient_management.patients.models" not in model_source
        or "Patient" not in model_source
    ):
        raise RuntimeError(
            "Canonical Patient reference missing from models/consent.py.",
        )

    registry_source = FILES["workflow_registry.py"]

    for workflow_name in WORKFLOW_NAMES:
        if workflow_name not in registry_source:
            raise RuntimeError(
                f"Workflow registry entry missing: {workflow_name}",
            )

    print("ARCHITECTURE: PASS")


def validate_compile() -> None:
    """
    Compile all embedded Python files before touching the target directory.
    """
    count = 0

    for relative_path, source in FILES.items():
        if not relative_path.endswith(".py"):
            continue

        compile(
            source,
            relative_path,
            "exec",
        )
        count += 1

    print(
        f"PY_COMPILE: PASS ({count} files)",
    )


def validate_manifest() -> None:
    """
    Validate the fresh-install manifest.
    """
    manifest = json.loads(
        FILES[".installer_manifest.json"],
    )

    expected_values = {
        "module": "apps.patient_management.consents",
        "canonical_patient": ("apps.patient_management.patients.models.Patient"),
        "fresh_install": True,
        "delete_existing_module_before_install": True,
        "migrations_generated": False,
        "backup_generated": False,
        "pycache_generated": False,
    }

    for key, expected_value in expected_values.items():
        if manifest.get(key) != expected_value:
            raise RuntimeError(
                f"Invalid manifest value: {key}",
            )

    print("MANIFEST: PASS")


def delete_existing_module() -> None:
    """
    Delete the complete existing Consents directory.
    """
    if TARGET.exists():
        shutil.rmtree(TARGET)

    print("OLD CONSENTS DIRECTORY: DELETED")


def install_fresh_module() -> None:
    """
    Create the complete fresh Consents module.
    """
    TARGET.mkdir(
        parents=True,
        exist_ok=True,
    )

    for relative_path, source in FILES.items():
        destination = TARGET / relative_path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            source,
            encoding="utf-8",
            newline="\n",
        )

    print("FRESH CONSENTS DIRECTORY: CREATED")
    print("VERIFY: PASS")
    print("INSTALLATION COMPLETE")
    print(
        "Workflow chain: "
        "API -> RBAC -> Workflow -> Policy -> Service -> Model -> Domain Event",
    )
    print(
        "Canonical Patient: apps.patient_management.patients.models.Patient",
    )
    print("No migration generated.")
    print("No backup generated.")
    print("No __pycache__ generated by installer.")


def main() -> None:
    """
    Validate everything, then delete and recreate Consents.
    """
    print(
        "DatavionOS Patient Consents Fresh Installer v2.1.0",
    )
    print(f"Target: {TARGET}")

    # All validation occurs before deletion so a failed validation never
    # destroys the current module.
    validate_structure()
    validate_manifest()
    validate_source_style()
    validate_architecture()
    validate_compile()

    delete_existing_module()
    install_fresh_module()


if __name__ == "__main__":
    main()
