from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


FILES: dict[str, str] = {
    r"apps\patient_management\relationships\models\relationship.py": '''"""
Patient Relationship domain model.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import (
    AllObjectsManager,
    BaseModel,
    DeletedObjectsManager,
)
from apps.patient_management.patients.models import Patient
from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    RelationshipType,
    VerificationStatus,
)
from apps.patient_management.relationships.managers import (
    PatientRelationshipManager,
)
from apps.platform.organizations.models import Organization


class PatientRelationship(BaseModel):
    """
    Relationship between a patient and another patient or an
    external individual/entity.

    Domain invariants:
    - patient and organization must belong to the same organization;
    - internal relationships cannot target the same patient;
    - external relationships require relationship_name;
    - effective_to cannot precede effective_from;
    - only one active primary relationship may exist per patient;
    - only one active identical internal/external relationship may exist.
    """

    objects = PatientRelationshipManager()
    all_objects = AllObjectsManager()
    deleted_objects = DeletedObjectsManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_relationships",
        help_text=_("Organization that owns the relationship."),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_relationships",
        help_text=_("Primary patient."),
    )

    related_patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="related_patient_relationships",
        help_text=_("Related patient, when the relationship is internal."),
    )

    relationship_type = models.CharField(
        max_length=30,
        choices=RelationshipType.choices,
        help_text=_("Type of relationship."),
    )

    relationship_name = models.CharField(
        max_length=150,
        blank=True,
        help_text=_(
            "External person's or entity's relationship name "
            "when related_patient is not supplied."
        ),
    )

    is_primary = models.BooleanField(
        default=False,
        help_text=_("Whether this is the patient's primary relationship."),
    )

    status = models.CharField(
        max_length=20,
        choices=RelationshipStatus.choices,
        default=RelationshipStatus.ACTIVE,
        db_index=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )

    effective_from = models.DateField(
        null=True,
        blank=True,
    )

    effective_to = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "patient_relationships"

        verbose_name = _("Patient Relationship")
        verbose_name_plural = _("Patient Relationships")

        ordering = (
            "-is_primary",
            "relationship_type",
            "created_at",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                    "related_patient",
                    "relationship_type",
                ),
                condition=models.Q(
                    related_patient__isnull=False,
                    is_active=True,
                ),
                name="uq_patient_relationship_internal",
            ),
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                    "relationship_name",
                    "relationship_type",
                ),
                condition=models.Q(
                    related_patient__isnull=True,
                    is_active=True,
                ),
                name="uq_patient_relationship_external",
            ),
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "patient",
                ),
                condition=models.Q(
                    is_primary=True,
                    is_active=True,
                ),
                name="uq_patient_primary_relationship",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "organization",
                    "patient",
                    "status",
                ),
                name="rel_org_pat_status_idx",
            ),
            models.Index(
                fields=(
                    "organization",
                    "related_patient",
                ),
                name="rel_org_related_idx",
            ),
            models.Index(
                fields=(
                    "patient",
                    "relationship_type",
                ),
                name="rel_patient_type_idx",
            ),
            models.Index(
                fields=(
                    "verification_status",
                ),
                name="rel_verification_idx",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if self.organization_id is None:
            raise ValidationError(
                {
                    "organization": _(
                        "Organization is required."
                    )
                }
            )

        if self.patient_id is None:
            raise ValidationError(
                {
                    "patient": _(
                        "Patient is required."
                    )
                }
            )

        patient_organization_id = getattr(
            self.patient,
            "organization_id",
            None,
        )

        if (
            patient_organization_id is not None
            and patient_organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "organization": _(
                        "Relationship organization must match "
                        "the patient organization."
                    )
                }
            )

        if self.related_patient_id:
            related_patient_organization_id = getattr(
                self.related_patient,
                "organization_id",
                None,
            )

            if (
                related_patient_organization_id is not None
                and related_patient_organization_id != self.organization_id
            ):
                raise ValidationError(
                    {
                        "related_patient": _(
                            "Related patient must belong to the "
                            "same organization."
                        )
                    }
                )

        if (
            self.related_patient_id
            and self.patient_id
            and self.related_patient_id == self.patient_id
        ):
            raise ValidationError(
                {
                    "related_patient": _(
                        "A patient cannot have a relationship "
                        "with themselves."
                    )
                }
            )

        if (
            not self.related_patient_id
            and not self.relationship_name.strip()
        ):
            raise ValidationError(
                {
                    "relationship_name": _(
                        "Relationship name is required for "
                        "an external relationship."
                    )
                }
            )

        if self.effective_from and self.effective_to:
            if self.effective_to < self.effective_from:
                raise ValidationError(
                    {
                        "effective_to": _(
                            "Effective end date cannot be "
                            "before the start date."
                        )
                    }
                )

        if (
            self.status == RelationshipStatus.TERMINATED
            and self.is_active
        ):
            raise ValidationError(
                {
                    "is_active": _(
                        "A terminated relationship cannot be active."
                    )
                }
            )

    @property
    def is_external(self) -> bool:
        return self.related_patient_id is None

    @property
    def is_verified(self) -> bool:
        return (
            self.verification_status
            == VerificationStatus.VERIFIED
        )

    def __str__(self) -> str:
        target = (
            str(self.related_patient)
            if self.related_patient_id
            else self.relationship_name
        )

        return (
            f"{self.patient} → {target} "
            f"({self.get_relationship_type_display()})"
        )


__all__ = (
    "PatientRelationship",
)
''',
    r"apps\patient_management\relationships\selectors\relationship.py": '''"""
Organization-scoped read selectors for Patient Relationships.
"""

from __future__ import annotations

from typing import TypeAlias
from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.relationships.models import (
    PatientRelationship,
)
from apps.platform.organizations.models import Organization


OrganizationReference: TypeAlias = Organization | UUID | str


class PatientRelationshipSelector:
    """
    Read-only selector API for Patient Relationships.

    Every public selector requires an organization boundary.
    """

    @staticmethod
    def _organization_id(
        organization: OrganizationReference,
    ) -> UUID | str:
        if isinstance(organization, Organization):
            return organization.pk

        return organization

    @classmethod
    def queryset(
        cls,
    ) -> QuerySet[PatientRelationship]:
        return (
            PatientRelationship.objects
            .select_related(
                "organization",
                "patient",
                "related_patient",
            )
        )

    @classmethod
    def deleted_queryset(
        cls,
    ) -> QuerySet[PatientRelationship]:
        return (
            PatientRelationship.deleted_objects
            .select_related(
                "organization",
                "patient",
                "related_patient",
            )
        )

    @classmethod
    def get(
        cls,
        *,
        organization: OrganizationReference,
        relationship_id: UUID,
    ) -> PatientRelationship:
        return cls.queryset().get(
            organization_id=cls._organization_id(
                organization
            ),
            pk=relationship_id,
        )

    @classmethod
    def get_deleted(
        cls,
        *,
        organization: OrganizationReference,
        relationship_id: UUID,
    ) -> PatientRelationship:
        return cls.deleted_queryset().get(
            organization_id=cls._organization_id(
                organization
            ),
            pk=relationship_id,
        )

    @classmethod
    def list(
        cls,
        *,
        organization: OrganizationReference,
    ) -> QuerySet[PatientRelationship]:
        return (
            cls.queryset()
            .filter(
                organization_id=cls._organization_id(
                    organization
                ),
            )
            .order_by(
                "-is_primary",
                "-created_at",
            )
        )

    @classmethod
    def for_patient(
        cls,
        *,
        organization: OrganizationReference,
        patient_id: UUID,
    ) -> QuerySet[PatientRelationship]:
        return (
            cls.list(
                organization=organization,
            )
            .filter(
                patient_id=patient_id,
            )
        )

    @classmethod
    def get_primary(
        cls,
        *,
        organization: OrganizationReference,
        patient_id: UUID,
    ) -> PatientRelationship | None:
        return (
            cls.for_patient(
                organization=organization,
                patient_id=patient_id,
            )
            .filter(
                is_primary=True,
                is_active=True,
            )
            .first()
        )

    @classmethod
    def list_active(
        cls,
        *,
        organization: OrganizationReference,
    ) -> QuerySet[PatientRelationship]:
        return cls.list(
            organization=organization,
        ).filter(
            is_active=True,
            status="active",
        )

    @classmethod
    def list_verified(
        cls,
        *,
        organization: OrganizationReference,
    ) -> QuerySet[PatientRelationship]:
        return cls.list(
            organization=organization,
        ).filter(
            verification_status="verified",
        )

    @classmethod
    def list_terminated(
        cls,
        *,
        organization: OrganizationReference,
    ) -> QuerySet[PatientRelationship]:
        return cls.list(
            organization=organization,
        ).filter(
            status="terminated",
        )

    # Compatibility aliases used by existing API code.

    @classmethod
    def get_by_id(
        cls,
        *,
        organization: OrganizationReference,
        relationship_id: UUID,
    ) -> PatientRelationship:
        return cls.get(
            organization=organization,
            relationship_id=relationship_id,
        )


get_patient_relationship = (
    PatientRelationshipSelector.get
)

get_patient_relationship_for_patient = (
    PatientRelationshipSelector.for_patient
)

list_patient_relationships = (
    PatientRelationshipSelector.list
)


__all__ = (
    "PatientRelationshipSelector",
    "get_patient_relationship",
    "get_patient_relationship_for_patient",
    "list_patient_relationships",
)
''',
    r"apps\patient_management\relationships\services\relationship.py": '''"""
Domain services for Patient Relationships.

Responsibilities
----------------
Services own:

- domain validation;
- normalization;
- persistence;
- aggregate invariants;
- lifecycle mutation.

Services do not own:

- HTTP/API concerns;
- RBAC authorization;
- workflow orchestration;
- event publication;
- background task dispatch.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.patient_management.patients.models import Patient
from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    VerificationStatus,
)
from apps.patient_management.relationships.models import (
    PatientRelationship,
)
from apps.platform.accounts.models import User


class PatientRelationshipService:
    """
    Domain service for Patient Relationship mutations.
    """

    _PROTECTED_FIELDS = frozenset(
        {
            "id",
            "organization",
            "organization_id",
            "patient",
            "patient_id",
            "created_at",
            "created_by",
            "created_by_id",
            "updated_at",
            "updated_by",
            "updated_by_id",
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "deleted_by_id",
        }
    )

    @classmethod
    def _validate_mutable_fields(
        cls,
        data: Mapping[str, Any],
    ) -> None:
        protected = cls._PROTECTED_FIELDS.intersection(
            data.keys()
        )

        if protected:
            raise ValidationError(
                {
                    field: (
                        "This field cannot be changed through "
                        "the domain service."
                    )
                    for field in sorted(protected)
                }
            )

    @staticmethod
    def _normalize_data(
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        normalized = dict(data)

        for field in (
            "relationship_name",
            "notes",
        ):
            if (
                field in normalized
                and normalized[field] is not None
            ):
                normalized[field] = str(
                    normalized[field]
                ).strip()

        return normalized

    @staticmethod
    def _ensure_patient_organization(
        *,
        instance: PatientRelationship,
    ) -> None:
        organization_id = instance.organization_id
        patient = instance.patient

        if organization_id is None or patient is None:
            raise ValidationError(
                {
                    "organization": (
                        "Organization and patient are required."
                    )
                }
            )

        if patient.organization_id != organization_id:
            raise ValidationError(
                {
                    "organization": (
                        "Relationship organization must match "
                        "the patient organization."
                    )
                }
            )

        related_patient = instance.related_patient

        if (
            related_patient is not None
            and related_patient.organization_id != organization_id
        ):
            raise ValidationError(
                {
                    "related_patient": (
                        "Related patient must belong to "
                        "the same organization."
                    )
                }
            )

    @staticmethod
    def _ensure_not_deleted(
        instance: PatientRelationship,
    ) -> None:
        if instance.is_deleted:
            raise ValidationError(
                {
                    "is_deleted": (
                        "Deleted relationships cannot be modified. "
                        "Restore the relationship first."
                    )
                }
            )

    @staticmethod
    def _ensure_not_terminated(
        instance: PatientRelationship,
    ) -> None:
        if (
            instance.status
            == RelationshipStatus.TERMINATED
        ):
            raise ValidationError(
                {
                    "status": (
                        "A terminated relationship cannot be "
                        "reactivated."
                    )
                }
            )

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> PatientRelationship:
        data = dict(validated_data)

        cls._validate_mutable_fields(data)
        data = cls._normalize_data(data)

        instance = PatientRelationship(
            **data,
        )

        cls._ensure_patient_organization(
            instance=instance,
        )

        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: PatientRelationship,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> PatientRelationship:
        cls._ensure_not_deleted(
            instance,
        )

        cls._ensure_not_terminated(
            instance,
        )

        data = dict(validated_data)

        if not data:
            return instance

        cls._validate_mutable_fields(data)
        data = cls._normalize_data(data)

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        cls._ensure_patient_organization(
            instance=instance,
        )

        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        if instance.is_deleted:
            return instance

        instance.is_active = False
        instance.is_primary = False
        instance.is_deleted = True
        instance.deleted_at = timezone.now()

        if hasattr(instance, "deleted_by_id"):
            instance.deleted_by_id = (
                performed_by.pk
                if performed_by is not None
                else None
            )

        update_fields = [
            "is_active",
            "is_primary",
            "is_deleted",
            "deleted_at",
            "updated_at",
        ]

        if hasattr(instance, "deleted_by_id"):
            update_fields.append(
                "deleted_by_id"
            )

        instance.save(
            update_fields=update_fields,
        )

        return instance

    @classmethod
    @transaction.atomic
    def restore(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        if not instance.is_deleted:
            return instance

        instance.is_deleted = False
        instance.is_active = True
        instance.status = RelationshipStatus.ACTIVE
        instance.deleted_at = None

        if hasattr(instance, "deleted_by_id"):
            instance.deleted_by_id = None

        cls._ensure_patient_organization(
            instance=instance,
        )

        instance.full_clean()

        update_fields = [
            "is_deleted",
            "is_active",
            "status",
            "deleted_at",
            "updated_at",
        ]

        if hasattr(instance, "deleted_by_id"):
            update_fields.append(
                "deleted_by_id"
            )

        instance.save(
            update_fields=update_fields,
        )

        return instance

    @classmethod
    @transaction.atomic
    def activate(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        cls._ensure_not_deleted(
            instance,
        )

        cls._ensure_not_terminated(
            instance,
        )

        if (
            instance.is_active
            and instance.status
            == RelationshipStatus.ACTIVE
        ):
            return instance

        instance.is_active = True
        instance.status = RelationshipStatus.ACTIVE

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_active",
                "status",
                "updated_at",
            ],
        )

        return instance

    @classmethod
    @transaction.atomic
    def deactivate(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        cls._ensure_not_deleted(
            instance,
        )

        if (
            not instance.is_active
            and instance.status
            == RelationshipStatus.INACTIVE
        ):
            return instance

        if (
            instance.status
            == RelationshipStatus.TERMINATED
        ):
            return instance

        instance.is_active = False
        instance.is_primary = False
        instance.status = RelationshipStatus.INACTIVE

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_active",
                "is_primary",
                "status",
                "updated_at",
            ],
        )

        return instance

    @classmethod
    @transaction.atomic
    def verify(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        cls._ensure_not_deleted(
            instance,
        )

        if (
            instance.status
            == RelationshipStatus.TERMINATED
        ):
            raise ValidationError(
                {
                    "status": (
                        "A terminated relationship cannot "
                        "be verified."
                    )
                }
            )

        if (
            instance.verification_status
            == VerificationStatus.VERIFIED
        ):
            return instance

        instance.verification_status = (
            VerificationStatus.VERIFIED
        )

        instance.full_clean()

        instance.save(
            update_fields=[
                "verification_status",
                "updated_at",
            ],
        )

        return instance

    @classmethod
    @transaction.atomic
    def terminate(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        cls._ensure_not_deleted(
            instance,
        )

        if (
            instance.status
            == RelationshipStatus.TERMINATED
            and not instance.is_active
        ):
            return instance

        instance.status = RelationshipStatus.TERMINATED
        instance.is_active = False
        instance.is_primary = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_active",
                "is_primary",
                "updated_at",
            ],
        )

        return instance

    @classmethod
    @transaction.atomic
    def set_primary(
        cls,
        *,
        instance: PatientRelationship,
        performed_by: User | None = None,
    ) -> PatientRelationship:
        cls._ensure_not_deleted(
            instance,
        )

        cls._ensure_not_terminated(
            instance,
        )

        if not instance.is_active:
            raise ValidationError(
                {
                    "is_active": (
                        "Only an active relationship can "
                        "be marked as primary."
                    )
                }
            )

        if (
            instance.status
            != RelationshipStatus.ACTIVE
        ):
            raise ValidationError(
                {
                    "status": (
                        "Only an active relationship can "
                        "be marked as primary."
                    )
                }
            )

        related_relationships = (
            PatientRelationship.all_objects
            .select_for_update()
            .filter(
                organization_id=instance.organization_id,
                patient_id=instance.patient_id,
                is_deleted=False,
                is_active=True,
            )
        )

        related_relationships.exclude(
            pk=instance.pk,
        ).update(
            is_primary=False,
        )

        instance.is_primary = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "is_primary",
                "updated_at",
            ],
        )

        return instance


def create_patient_relationship(
    *,
    validated_data: Mapping[str, Any],
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.create(
        validated_data=validated_data,
        performed_by=performed_by,
    )


def update_patient_relationship(
    *,
    instance: PatientRelationship,
    validated_data: Mapping[str, Any],
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.update(
        instance=instance,
        validated_data=validated_data,
        performed_by=performed_by,
    )


def delete_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.delete(
        instance=instance,
        performed_by=performed_by,
    )


def restore_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.restore(
        instance=instance,
        performed_by=performed_by,
    )


def activate_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.activate(
        instance=instance,
        performed_by=performed_by,
    )


def deactivate_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.deactivate(
        instance=instance,
        performed_by=performed_by,
    )


def verify_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.verify(
        instance=instance,
        performed_by=performed_by,
    )


def terminate_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.terminate(
        instance=instance,
        performed_by=performed_by,
    )


def set_primary_patient_relationship(
    *,
    instance: PatientRelationship,
    performed_by: User | None = None,
) -> PatientRelationship:
    return PatientRelationshipService.set_primary(
        instance=instance,
        performed_by=performed_by,
    )


__all__ = (
    "PatientRelationshipService",
    "activate_patient_relationship",
    "create_patient_relationship",
    "deactivate_patient_relationship",
    "delete_patient_relationship",
    "restore_patient_relationship",
    "set_primary_patient_relationship",
    "terminate_patient_relationship",
    "update_patient_relationship",
    "verify_patient_relationship",
)
''',
    r"apps\patient_management\relationships\api\filters.py": '''"""
API filters for Patient Relationships.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.relationships.constants import (
    RelationshipStatus,
    RelationshipType,
    VerificationStatus,
)
from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class PatientRelationshipFilter(
    django_filters.FilterSet,
):
    patient = django_filters.UUIDFilter(
        field_name="patient_id",
    )

    related_patient = django_filters.UUIDFilter(
        field_name="related_patient_id",
    )

    relationship_type = django_filters.ChoiceFilter(
        choices=RelationshipType.choices,
    )

    status = django_filters.ChoiceFilter(
        choices=RelationshipStatus.choices,
    )

    verification_status = django_filters.ChoiceFilter(
        choices=VerificationStatus.choices,
    )

    is_primary = django_filters.BooleanFilter()

    is_active = django_filters.BooleanFilter()

    effective_from = django_filters.DateFilter(
        lookup_expr="exact",
    )

    effective_from_gte = django_filters.DateFilter(
        field_name="effective_from",
        lookup_expr="gte",
    )

    effective_from_lte = django_filters.DateFilter(
        field_name="effective_from",
        lookup_expr="lte",
    )

    effective_to = django_filters.DateFilter(
        lookup_expr="exact",
    )

    class Meta:
        model = PatientRelationship
        fields = (
            "patient",
            "related_patient",
            "relationship_type",
            "status",
            "verification_status",
            "is_primary",
            "is_active",
            "effective_from",
            "effective_to",
        )


__all__ = (
    "PatientRelationshipFilter",
)
''',
    r"apps\patient_management\relationships\workflows\relationship_lifecycle.py": '''"""
Lifecycle workflows for Patient Relationships.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.relationships.events import (
    PatientRelationshipStatusChangedEvent,
    PatientRelationshipUpdatedEvent,
)
from apps.patient_management.relationships.selectors import (
    PatientRelationshipSelector,
)
from apps.patient_management.relationships.services import (
    activate_patient_relationship,
    deactivate_patient_relationship,
    restore_patient_relationship,
    set_primary_patient_relationship,
    terminate_patient_relationship,
    verify_patient_relationship,
)
from apps.patient_management.relationships.policies import (
    PatientRelationshipPolicy,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipLifecycleRequest:
    relationship_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipLifecycleData:
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str
    restored: bool
    activated: bool
    deactivated: bool
    event_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipVerificationData:
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    verification_status: str
    changed: bool
    event_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipTerminationData:
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str
    terminated: bool
    event_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipPrimaryData:
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    changed: bool
    event_id: UUID


def _get_actor(
    context: WorkflowContext,
) -> User:
    try:
        return User.objects.get(
            pk=context.actor_id,
        )
    except User.DoesNotExist as exc:
        raise ValueError(
            "The authenticated actor was not found."
        ) from exc


def _get_relationship(
    *,
    context: WorkflowContext,
    relationship_id: UUID,
):
    try:
        return PatientRelationshipSelector.get(
            organization=OrganizationResolver.resolve(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
            ),
            relationship_id=relationship_id,
        )
    except ObjectDoesNotExist as exc:
        raise ValueError(
            "Patient relationship was not found."
        ) from exc


class OrganizationResolver:
    """
    Small workflow-local organization resolver.

    The relationship APIs already establish the organization context,
    but lifecycle workflows must independently enforce tenant scope.
    """

    @staticmethod
    def resolve(
        *,
        tenant_id: UUID,
        actor_id: UUID,
    ):
        from apps.platform.organizations.models import Organization

        organization = (
            Organization.objects
            .filter(
                tenant_id=tenant_id,
                organization_roles__user_id=actor_id,
            )
            .select_related()
            .first()
        )

        if organization is None:
            raise ValueError(
                "Organization context could not be resolved."
            )

        return organization


class PatientRelationshipRestoreWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData],
):
    workflow_name = "relationship.restore"

    def __init__(
        self,
        *,
        request: PatientRelationshipLifecycleRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipLifecycleData]:
        actor = _get_actor(context)

        organization = OrganizationResolver.resolve(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        try:
            relationship = (
                PatientRelationshipSelector.get_deleted(
                    organization=organization,
                    relationship_id=self._request.relationship_id,
                )
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Deleted patient relationship was not found."
            ) from exc

        if not self._policy.can_restore(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to restore "
                "this patient relationship."
            )

        previous_status = relationship.status

        relationship = restore_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                restored=True,
                activated=False,
                deactivated=False,
                event_id=event.event_id,
            ),
            message="Patient relationship restored successfully.",
            code="relationship_restored",
        )


class PatientRelationshipActivationWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData],
):
    workflow_name = "relationship.activate"

    def __init__(
        self,
        *,
        request: PatientRelationshipLifecycleRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipLifecycleData]:
        actor = _get_actor(context)

        organization = OrganizationResolver.resolve(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        try:
            relationship = PatientRelationshipSelector.get(
                organization=organization,
                relationship_id=self._request.relationship_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found."
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to activate "
                "this patient relationship."
            )

        previous_status = relationship.status

        relationship = activate_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                restored=False,
                activated=True,
                deactivated=False,
                event_id=event.event_id,
            ),
            message="Patient relationship activated successfully.",
            code="relationship_activated",
        )


class PatientRelationshipDeactivationWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData],
):
    workflow_name = "relationship.deactivate"

    def __init__(
        self,
        *,
        request: PatientRelationshipLifecycleRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipLifecycleData]:
        actor = _get_actor(context)

        organization = OrganizationResolver.resolve(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        try:
            relationship = PatientRelationshipSelector.get(
                organization=organization,
                relationship_id=self._request.relationship_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found."
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to deactivate "
                "this patient relationship."
            )

        previous_status = relationship.status

        relationship = deactivate_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                restored=False,
                activated=False,
                deactivated=True,
                event_id=event.event_id,
            ),
            message="Patient relationship deactivated successfully.",
            code="relationship_deactivated",
        )


class PatientRelationshipVerificationWorkflow(
    BaseWorkflow[PatientRelationshipVerificationData],
):
    workflow_name = "relationship.verify"

    def __init__(
        self,
        *,
        request: PatientRelationshipLifecycleRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipVerificationData]:
        actor = _get_actor(context)

        organization = OrganizationResolver.resolve(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        try:
            relationship = PatientRelationshipSelector.get(
                organization=organization,
                relationship_id=self._request.relationship_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found."
            ) from exc

        if not self._policy.can_verify(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to verify "
                "this patient relationship."
            )

        previous_status = relationship.verification_status

        relationship = verify_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        changed = (
            previous_status
            != relationship.verification_status
        )

        event = PatientRelationshipUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            changes={
                "verification_status": {
                    "old": previous_status,
                    "new": relationship.verification_status,
                },
            },
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipVerificationData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                verification_status=(
                    relationship.verification_status
                ),
                changed=changed,
                event_id=event.event_id,
            ),
            message="Patient relationship verified successfully.",
            code="relationship_verified",
        )


class PatientRelationshipTerminationWorkflow(
    BaseWorkflow[PatientRelationshipTerminationData],
):
    workflow_name = "relationship.terminate"

    def __init__(
        self,
        *,
        request: PatientRelationshipLifecycleRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipTerminationData]:
        actor = _get_actor(context)

        organization = OrganizationResolver.resolve(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        try:
            relationship = PatientRelationshipSelector.get(
                organization=organization,
                relationship_id=self._request.relationship_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found."
            ) from exc

        if not self._policy.can_terminate(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to terminate "
                "this patient relationship."
            )

        previous_status = relationship.status

        relationship = terminate_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipTerminationData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                terminated=True,
                event_id=event.event_id,
            ),
            message="Patient relationship terminated successfully.",
            code="relationship_terminated",
        )


class PatientRelationshipSetPrimaryWorkflow(
    BaseWorkflow[PatientRelationshipPrimaryData],
):
    workflow_name = "relationship.set_primary"

    def __init__(
        self,
        *,
        request: PatientRelationshipLifecycleRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipPrimaryData]:
        actor = _get_actor(context)

        organization = OrganizationResolver.resolve(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        try:
            relationship = PatientRelationshipSelector.get(
                organization=organization,
                relationship_id=self._request.relationship_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found."
            ) from exc

        if not self._policy.can_set_primary(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to set "
                "this patient relationship as primary."
            )

        changed = not relationship.is_primary

        relationship = set_primary_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            changes={
                "is_primary": {
                    "old": not changed,
                    "new": True,
                },
            },
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipPrimaryData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                changed=changed,
                event_id=event.event_id,
            ),
            message="Patient relationship set as primary successfully.",
            code="relationship_primary",
        )


__all__ = (
    "PatientRelationshipActivationWorkflow",
    "PatientRelationshipDeactivationWorkflow",
    "PatientRelationshipLifecycleData",
    "PatientRelationshipLifecycleRequest",
    "PatientRelationshipPrimaryData",
    "PatientRelationshipRestoreWorkflow",
    "PatientRelationshipSetPrimaryWorkflow",
    "PatientRelationshipTerminationData",
    "PatientRelationshipTerminationWorkflow",
    "PatientRelationshipVerificationData",
    "PatientRelationshipVerificationWorkflow",
)
''',
    r"apps\patient_management\relationships\workflow_registry.py": '''"""
Central workflow registry for Patient Relationships.
"""

from __future__ import annotations

from apps.core.workflows.registry import workflow_registry
from apps.patient_management.relationships.workflows import (
    PatientRelationshipActivationWorkflow,
    PatientRelationshipCreationWorkflow,
    PatientRelationshipDeactivationWorkflow,
    PatientRelationshipDeletionWorkflow,
    PatientRelationshipRestoreWorkflow,
    PatientRelationshipSetPrimaryWorkflow,
    PatientRelationshipTerminationWorkflow,
    PatientRelationshipUpdateWorkflow,
    PatientRelationshipVerificationWorkflow,
)


def register_patient_relationship_workflows() -> None:
    """
    Register all supported Patient Relationship workflows.

    Registration is idempotent.
    """

    workflows = (
        (
            "relationship.create",
            PatientRelationshipCreationWorkflow,
        ),
        (
            "relationship.update",
            PatientRelationshipUpdateWorkflow,
        ),
        (
            "relationship.delete",
            PatientRelationshipDeletionWorkflow,
        ),
        (
            "relationship.restore",
            PatientRelationshipRestoreWorkflow,
        ),
        (
            "relationship.activate",
            PatientRelationshipActivationWorkflow,
        ),
        (
            "relationship.deactivate",
            PatientRelationshipDeactivationWorkflow,
        ),
        (
            "relationship.verify",
            PatientRelationshipVerificationWorkflow,
        ),
        (
            "relationship.terminate",
            PatientRelationshipTerminationWorkflow,
        ),
        (
            "relationship.set_primary",
            PatientRelationshipSetPrimaryWorkflow,
        ),
    )

    for name, workflow in workflows:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_patient_relationship_workflows()


__all__ = (
    "register_patient_relationship_workflows",
)
''',
    r"apps\patient_management\relationships\workflows\__init__.py": '''"""
Workflow exports for Patient Relationships.
"""

from .relationship_creation import (
    PatientRelationshipCreationData,
    PatientRelationshipCreationRequest,
    PatientRelationshipCreationWorkflow,
)
from .relationship_deletion import (
    PatientRelationshipDeletionData,
    PatientRelationshipDeletionRequest,
    PatientRelationshipDeletionWorkflow,
)
from .relationship_lifecycle import (
    PatientRelationshipActivationWorkflow,
    PatientRelationshipDeactivationWorkflow,
    PatientRelationshipLifecycleData,
    PatientRelationshipLifecycleRequest,
    PatientRelationshipPrimaryData,
    PatientRelationshipRestoreWorkflow,
    PatientRelationshipSetPrimaryWorkflow,
    PatientRelationshipTerminationData,
    PatientRelationshipTerminationWorkflow,
    PatientRelationshipVerificationData,
    PatientRelationshipVerificationWorkflow,
)
from .relationship_update import (
    PatientRelationshipUpdateData,
    PatientRelationshipUpdateRequest,
    PatientRelationshipUpdateWorkflow,
)


__all__ = (
    "PatientRelationshipActivationWorkflow",
    "PatientRelationshipCreationData",
    "PatientRelationshipCreationRequest",
    "PatientRelationshipCreationWorkflow",
    "PatientRelationshipDeactivationWorkflow",
    "PatientRelationshipDeletionData",
    "PatientRelationshipDeletionRequest",
    "PatientRelationshipDeletionWorkflow",
    "PatientRelationshipLifecycleData",
    "PatientRelationshipLifecycleRequest",
    "PatientRelationshipPrimaryData",
    "PatientRelationshipRestoreWorkflow",
    "PatientRelationshipSetPrimaryWorkflow",
    "PatientRelationshipTerminationData",
    "PatientRelationshipTerminationWorkflow",
    "PatientRelationshipUpdateData",
    "PatientRelationshipUpdateRequest",
    "PatientRelationshipUpdateWorkflow",
    "PatientRelationshipVerificationData",
    "PatientRelationshipVerificationWorkflow",
)
''',
    r"apps\patient_management\relationships\api\views\lifecycle.py": '''"""
Lifecycle API views for Patient Relationships.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseGenericAPIView
from apps.patient_management.relationships.workflows import (
    PatientRelationshipActivationWorkflow,
    PatientRelationshipDeactivationWorkflow,
    PatientRelationshipLifecycleRequest,
    PatientRelationshipRestoreWorkflow,
    PatientRelationshipSetPrimaryWorkflow,
    PatientRelationshipTerminationWorkflow,
    PatientRelationshipVerificationWorkflow,
)


RELATIONSHIP_TAG: Final[tuple[str, ...]] = (
    "Patient Relationships",
)


class PatientRelationshipLifecycleAPIView(
    BaseGenericAPIView,
):
    """
    Common adapter for relationship lifecycle workflows.
    """

    permission_classes = (
        IsAuthenticated,
    )

    def build_request(
        self,
    ) -> PatientRelationshipLifecycleRequest:
        relationship_id = self.kwargs.get(
            "relationship_id",
        )

        if relationship_id is None:
            raise ValueError(
                "Relationship identifier is required."
            )

        return PatientRelationshipLifecycleRequest(
            relationship_id=relationship_id,
        )

    def execute_relationship_workflow(
        self,
        *,
        workflow,
        workflow_name: str,
    ):
        context = self.build_workflow_context(
            workflow_name=workflow_name,
        )

        result = workflow(
            request=self.build_request(),
        ).execute(
            context=context,
        )

        return self.handle_workflow_result(
            result,
        )


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipActivateAPIView(
    PatientRelationshipLifecycleAPIView,
):
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipActivationWorkflow,
            workflow_name="relationship.activate",
        )


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipDeactivateAPIView(
    PatientRelationshipLifecycleAPIView,
):
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipDeactivationWorkflow,
            workflow_name="relationship.deactivate",
        )


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipRestoreAPIView(
    PatientRelationshipLifecycleAPIView,
):
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipRestoreWorkflow,
            workflow_name="relationship.restore",
        )


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipVerifyAPIView(
    PatientRelationshipLifecycleAPIView,
):
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipVerificationWorkflow,
            workflow_name="relationship.verify",
        )


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipTerminateAPIView(
    PatientRelationshipLifecycleAPIView,
):
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipTerminationWorkflow,
            workflow_name="relationship.terminate",
        )


@extend_schema(
    tags=RELATIONSHIP_TAG,
)
class PatientRelationshipSetPrimaryAPIView(
    PatientRelationshipLifecycleAPIView,
):
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        return self.execute_relationship_workflow(
            workflow=PatientRelationshipSetPrimaryWorkflow,
            workflow_name="relationship.set_primary",
        )


__all__ = (
    "PatientRelationshipActivateAPIView",
    "PatientRelationshipDeactivateAPIView",
    "PatientRelationshipRestoreAPIView",
    "PatientRelationshipSetPrimaryAPIView",
    "PatientRelationshipTerminateAPIView",
    "PatientRelationshipVerifyAPIView",
)
''',
    r"apps\patient_management\relationships\api\views\__init__.py": '''"""
Patient Relationship API views.
"""

from .lifecycle import (
    PatientRelationshipActivateAPIView,
    PatientRelationshipDeactivateAPIView,
    PatientRelationshipRestoreAPIView,
    PatientRelationshipSetPrimaryAPIView,
    PatientRelationshipTerminateAPIView,
    PatientRelationshipVerifyAPIView,
)
from .list_create import (
    PatientRelationshipListCreateAPIView,
)
from .retrieve_update_destroy import (
    PatientRelationshipRetrieveUpdateDestroyAPIView,
)


__all__ = (
    "PatientRelationshipActivateAPIView",
    "PatientRelationshipDeactivateAPIView",
    "PatientRelationshipListCreateAPIView",
    "PatientRelationshipRestoreAPIView",
    "PatientRelationshipRetrieveUpdateDestroyAPIView",
    "PatientRelationshipSetPrimaryAPIView",
    "PatientRelationshipTerminateAPIView",
    "PatientRelationshipVerifyAPIView",
)
''',
    r"apps\patient_management\relationships\api\urls\relationship.py": '''"""
URL patterns for Patient Relationships.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.relationships.api.views import (
    PatientRelationshipActivateAPIView,
    PatientRelationshipDeactivateAPIView,
    PatientRelationshipListCreateAPIView,
    PatientRelationshipRestoreAPIView,
    PatientRelationshipRetrieveUpdateDestroyAPIView,
    PatientRelationshipSetPrimaryAPIView,
    PatientRelationshipTerminateAPIView,
    PatientRelationshipVerifyAPIView,
)


app_name = "patient-relationships"


urlpatterns = (
    path(
        "",
        PatientRelationshipListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:relationship_id>/",
        PatientRelationshipRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "<uuid:relationship_id>/activate/",
        PatientRelationshipActivateAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:relationship_id>/deactivate/",
        PatientRelationshipDeactivateAPIView.as_view(),
        name="deactivate",
    ),
    path(
        "<uuid:relationship_id>/restore/",
        PatientRelationshipRestoreAPIView.as_view(),
        name="restore",
    ),
    path(
        "<uuid:relationship_id>/verify/",
        PatientRelationshipVerifyAPIView.as_view(),
        name="verify",
    ),
    path(
        "<uuid:relationship_id>/terminate/",
        PatientRelationshipTerminateAPIView.as_view(),
        name="terminate",
    ),
    path(
        "<uuid:relationship_id>/set-primary/",
        PatientRelationshipSetPrimaryAPIView.as_view(),
        name="set-primary",
    ),
)


__all__ = (
    "app_name",
    "urlpatterns",
)
''',
    r"apps\patient_management\relationships\api\urls\__init__.py": '''"""
Patient Relationship API URL exports.
"""

from .relationship import (
    app_name,
    urlpatterns,
)


__all__ = (
    "app_name",
    "urlpatterns",
)
''',
    r"apps\patient_management\relationships\urls.py": '''"""
Application URL exports for Patient Relationships.
"""

from apps.patient_management.relationships.api.urls import (
    urlpatterns,
)


__all__ = (
    "urlpatterns",
)
''',
    r"apps\patient_management\relationships\apps.py": '''"""
Django application configuration for Patient Relationships.
"""

from __future__ import annotations

from django.apps import AppConfig


class RelationshipsConfig(AppConfig):
    """
    Patient Relationships application configuration.
    """

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "apps.patient_management.relationships"
    label = "patient_relationships"
    verbose_name = "Patient Relationships"

    def ready(self) -> None:
        """
        Register workflow and signal integrations.
        """

        from apps.patient_management.relationships import (
            workflow_registry,
        )

        workflow_registry.register_patient_relationship_workflows()

        try:
            from apps.patient_management.relationships import signals  # noqa: F401
        except ImportError:
            pass


__all__ = (
    "RelationshipsConfig",
)
''',
}


def write_files() -> None:
    for relative_path, content in FILES.items():
        path = BASE_DIR / relative_path
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        path.write_text(
            content,
            encoding="utf-8",
            newline="\n",
        )
        print(f"UPDATED: {relative_path}")


if __name__ == "__main__":
    write_files()
    print()
    print("Relationships module production implementation has been written.")
