"""
DatavionAI - Patient Management Layer 3A
Selector implementation installer.

This script writes the production selector layer for the remaining
Patient Management modules without modifying models, services, APIs,
or workflows.

Usage:
    python install_patient_management_layer3a_selectors.py
"""

from __future__ import annotations

from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parent


FILES: dict[str, str] = {
    # ------------------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------------------
    r"apps\patient_management\relationships\selectors\relationship.py": r'''"""
Read selectors for Patient Relationships.

Architecture
------------
API
    ->
Selector
    ->
Organization-scoped QuerySet

Selectors are read-only and contain no mutation or authorization logic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.relationships.models import PatientRelationship

if TYPE_CHECKING:
    from apps.platform.organizations.models import Organization


class PatientRelationshipSelector:
    """
    Organization-scoped selector API for Patient Relationships.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientRelationship]:
        """
        Return the optimized base queryset.

        No unrestricted queryset should be exposed to tenant-facing APIs.
        """
        return (
            PatientRelationship.objects
            .select_related(
                "organization",
                "patient",
                "related_patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        relationship_id: UUID,
    ) -> PatientRelationship:
        """
        Return one relationship belonging to the organization.
        """
        return (
            PatientRelationshipSelector.queryset()
            .get(
                organization_id=organization_id,
                id=relationship_id,
            )
        )

    @staticmethod
    def get_by_id(
        *,
        organization_id: int,
        relationship_id: UUID,
    ) -> PatientRelationship:
        """
        Compatibility alias for get().
        """
        return PatientRelationshipSelector.get(
            organization_id=organization_id,
            relationship_id=relationship_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientRelationship]:
        """
        Return all relationships belonging to one organization.
        """
        return (
            PatientRelationshipSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientRelationship]:
        """
        Return all relationships for a patient within the organization.
        """
        return (
            PatientRelationshipSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-is_primary",
                "-created_at",
            )
        )

    @staticmethod
    def get_primary(
        *,
        organization_id: int,
        patient_id: int,
    ) -> PatientRelationship | None:
        """
        Return the primary relationship for a patient.
        """
        return (
            PatientRelationshipSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
                is_primary=True,
            )
            .first()
        )

    @staticmethod
    def list_active(
        *,
        organization_id: int,
    ) -> QuerySet[PatientRelationship]:
        """
        Return active relationships for an organization.
        """
        return (
            PatientRelationshipSelector.list_by_organization(
                organization_id=organization_id,
            )
            .filter(
                status__iexact="ACTIVE",
            )
        )

    @staticmethod
    def list_verified(
        *,
        organization_id: int,
    ) -> QuerySet[PatientRelationship]:
        """
        Return verified relationships for an organization.
        """
        return (
            PatientRelationshipSelector.list_by_organization(
                organization_id=organization_id,
            )
            .filter(
                verification_status__iexact="VERIFIED",
            )
        )


get_patient_relationship = PatientRelationshipSelector.get
get_patient_relationship_for_patient = PatientRelationshipSelector.list_by_patient
list_patient_relationships = PatientRelationshipSelector.list_by_organization


__all__ = (
    "PatientRelationshipSelector",
    "get_patient_relationship",
    "get_patient_relationship_for_patient",
    "list_patient_relationships",
)
''',

    r"apps\patient_management\relationships\selectors\__init__.py": r'''"""
Selectors for Patient Relationships.
"""

from apps.patient_management.relationships.selectors.relationship import (
    PatientRelationshipSelector,
    get_patient_relationship,
    get_patient_relationship_for_patient,
    list_patient_relationships,
)

__all__ = (
    "PatientRelationshipSelector",
    "get_patient_relationship",
    "get_patient_relationship_for_patient",
    "list_patient_relationships",
)
''',

    # ------------------------------------------------------------------
    # MEDICAL HISTORY
    # ------------------------------------------------------------------
    r"apps\patient_management\medical_history\selectors\medical_history.py": r'''"""
Read selectors for Patient Medical History.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.medical_history.models import (
    PatientMedicalHistory,
)


class PatientMedicalHistorySelector:
    """
    Organization-scoped selector API for medical history.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientMedicalHistory]:
        """
        Return the optimized base queryset.
        """
        return (
            PatientMedicalHistory.objects
            .select_related(
                "organization",
                "patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        medical_history_id: UUID,
    ) -> PatientMedicalHistory:
        """
        Return one medical history entry in the organization.
        """
        return (
            PatientMedicalHistorySelector.queryset()
            .get(
                organization_id=organization_id,
                id=medical_history_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientMedicalHistory]:
        """
        Return medical history entries for one organization.
        """
        return (
            PatientMedicalHistorySelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-onset_date",
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientMedicalHistory]:
        """
        Return medical history entries for one patient.
        """
        return (
            PatientMedicalHistorySelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-onset_date",
                "-created_at",
            )
        )

    @staticmethod
    def list_active(
        *,
        organization_id: int,
        patient_id: int | None = None,
    ) -> QuerySet[PatientMedicalHistory]:
        """
        Return active medical history entries.

        Patient scoping is optional, but organization scoping is mandatory.
        """
        queryset = (
            PatientMedicalHistorySelector.queryset()
            .filter(
                organization_id=organization_id,
                clinical_status__iexact="ACTIVE",
            )
        )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        return queryset.order_by(
            "-onset_date",
            "-created_at",
        )

    @staticmethod
    def list_by_type(
        *,
        organization_id: int,
        history_type: str,
        patient_id: int | None = None,
    ) -> QuerySet[PatientMedicalHistory]:
        """
        Return medical history entries filtered by history type.
        """
        queryset = (
            PatientMedicalHistorySelector.queryset()
            .filter(
                organization_id=organization_id,
                history_type=history_type,
            )
        )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        return queryset.order_by(
            "-onset_date",
            "-created_at",
        )


get_patient_medical_history = PatientMedicalHistorySelector.get
list_patient_medical_history = (
    PatientMedicalHistorySelector.list_by_patient
)
list_medical_history = PatientMedicalHistorySelector.list_by_organization


__all__ = (
    "PatientMedicalHistorySelector",
    "get_patient_medical_history",
    "list_patient_medical_history",
    "list_medical_history",
)
''',

    r"apps\patient_management\medical_history\selectors\__init__.py": r'''"""
Selectors for Patient Medical History.
"""

from apps.patient_management.medical_history.selectors.medical_history import (
    PatientMedicalHistorySelector,
    get_patient_medical_history,
    list_medical_history,
    list_patient_medical_history,
)

__all__ = (
    "PatientMedicalHistorySelector",
    "get_patient_medical_history",
    "list_medical_history",
    "list_patient_medical_history",
)
''',

    # ------------------------------------------------------------------
    # CONSENTS
    # ------------------------------------------------------------------
    r"apps\patient_management\consents\selectors\consent.py": r'''"""
Read selectors for Patient Consents.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.consents.models import Consent


class PatientConsentSelector:
    """
    Organization-scoped selector API for consent records.
    """

    @staticmethod
    def queryset() -> QuerySet[Consent]:
        """
        Return the optimized base queryset.
        """
        queryset = Consent.objects.all()

        field_names = {
            field.name
            for field in Consent._meta.get_fields()
        }

        select_related_fields = [
            field
            for field in (
                "organization",
                "patient",
                "granted_by",
                "revoked_by",
            )
            if field in field_names
        ]

        if select_related_fields:
            queryset = queryset.select_related(
                *select_related_fields,
            )

        return queryset

    @staticmethod
    def get(
        *,
        organization_id: int,
        consent_id: UUID,
    ) -> Consent:
        """
        Return one consent belonging to an organization.
        """
        return (
            PatientConsentSelector.queryset()
            .get(
                organization_id=organization_id,
                id=consent_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[Consent]:
        """
        Return organization-scoped consent records.
        """
        return (
            PatientConsentSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[Consent]:
        """
        Return consent records for a patient.
        """
        return (
            PatientConsentSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_active(
        *,
        organization_id: int,
        patient_id: int | None = None,
    ) -> QuerySet[Consent]:
        """
        Return active consents.

        The status field is intentionally queried dynamically through
        model metadata compatibility: the selector only relies on the
        confirmed organization/patient contract.
        """
        queryset = PatientConsentSelector.list_by_organization(
            organization_id=organization_id,
        )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        field_names = {
            field.name
            for field in Consent._meta.get_fields()
        }

        if "status" in field_names:
            queryset = queryset.filter(
                status__iexact="ACTIVE",
            )
        elif "is_active" in field_names:
            queryset = queryset.filter(
                is_active=True,
            )

        return queryset

    @staticmethod
    def exists(
        *,
        organization_id: int,
        consent_id: UUID,
    ) -> bool:
        """
        Determine whether a consent exists within an organization.
        """
        return (
            PatientConsentSelector.queryset()
            .filter(
                organization_id=organization_id,
                id=consent_id,
            )
            .exists()
        )


get_patient_consent = PatientConsentSelector.get
list_patient_consents = PatientConsentSelector.list_by_patient
list_consents = PatientConsentSelector.list_by_organization


__all__ = (
    "PatientConsentSelector",
    "get_patient_consent",
    "list_patient_consents",
    "list_consents",
)
''',

    r"apps\patient_management\consents\selectors\__init__.py": r'''"""
Selectors for Patient Consents.
"""

from apps.patient_management.consents.selectors.consent import (
    PatientConsentSelector,
    get_patient_consent,
    list_consents,
    list_patient_consents,
)

__all__ = (
    "PatientConsentSelector",
    "get_patient_consent",
    "list_consents",
    "list_patient_consents",
)
''',

    # ------------------------------------------------------------------
    # PREFERENCES
    # ------------------------------------------------------------------
    r"apps\patient_management\preferences\selectors\preference.py": r'''"""
Read selectors for Patient Preferences.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.preferences.models import (
    PatientPreference,
)


class PatientPreferenceSelector:
    """
    Organization-scoped selector API for PatientPreference.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientPreference]:
        """
        Return the optimized base queryset.
        """
        return (
            PatientPreference.objects
            .select_related(
                "organization",
                "patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        preference_id: UUID,
    ) -> PatientPreference:
        """
        Return one patient preference.
        """
        return (
            PatientPreferenceSelector.queryset()
            .get(
                organization_id=organization_id,
                id=preference_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientPreference]:
        """
        Return all preferences for an organization.
        """
        return (
            PatientPreferenceSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "patient_id",
                "-updated_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientPreference]:
        """
        Return preferences for one patient.
        """
        return (
            PatientPreferenceSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-updated_at",
            )
        )

    @staticmethod
    def first_for_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> PatientPreference | None:
        """
        Return the first preference record for a patient.
        """
        return (
            PatientPreferenceSelector.list_by_patient(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .first()
        )


get_patient_preference = PatientPreferenceSelector.get
list_patient_preferences = PatientPreferenceSelector.list_by_patient
list_preferences = PatientPreferenceSelector.list_by_organization


__all__ = (
    "PatientPreferenceSelector",
    "get_patient_preference",
    "list_patient_preferences",
    "list_preferences",
)
''',

    r"apps\patient_management\preferences\selectors\communication_preference.py": r'''"""
Read selectors for Patient Communication Preferences.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
)


class PatientCommunicationPreferenceSelector:
    """
    Organization-scoped selector API for communication preferences.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientCommunicationPreference]:
        """
        Return the optimized base queryset.
        """
        return (
            PatientCommunicationPreference.objects
            .select_related(
                "organization",
                "patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        communication_preference_id: UUID,
    ) -> PatientCommunicationPreference:
        """
        Return one communication preference.
        """
        return (
            PatientCommunicationPreferenceSelector.queryset()
            .get(
                organization_id=organization_id,
                id=communication_preference_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientCommunicationPreference]:
        """
        Return all communication preferences for an organization.
        """
        return (
            PatientCommunicationPreferenceSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "patient_id",
                "-updated_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientCommunicationPreference]:
        """
        Return communication preferences for one patient.
        """
        return (
            PatientCommunicationPreferenceSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-updated_at",
            )
        )

    @staticmethod
    def active_for_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientCommunicationPreference]:
        """
        Return active communication preferences for a patient.

        Supports either status-based or boolean-active models.
        """
        queryset = (
            PatientCommunicationPreferenceSelector.list_by_patient(
                organization_id=organization_id,
                patient_id=patient_id,
            )
        )

        field_names = {
            field.name
            for field in PatientCommunicationPreference._meta.get_fields()
        }

        if "status" in field_names:
            return queryset.filter(
                status__iexact="ACTIVE",
            )

        if "is_active" in field_names:
            return queryset.filter(
                is_active=True,
            )

        return queryset


get_patient_communication_preference = (
    PatientCommunicationPreferenceSelector.get
)
list_patient_communication_preferences = (
    PatientCommunicationPreferenceSelector.list_by_patient
)
list_communication_preferences = (
    PatientCommunicationPreferenceSelector.list_by_organization
)


__all__ = (
    "PatientCommunicationPreferenceSelector",
    "get_patient_communication_preference",
    "list_patient_communication_preferences",
    "list_communication_preferences",
)
''',

    r"apps\patient_management\preferences\selectors\__init__.py": r'''"""
Selectors for Patient Preferences.
"""

from apps.patient_management.preferences.selectors.communication_preference import (
    PatientCommunicationPreferenceSelector,
    get_patient_communication_preference,
    list_communication_preferences,
    list_patient_communication_preferences,
)
from apps.patient_management.preferences.selectors.preference import (
    PatientPreferenceSelector,
    get_patient_preference,
    list_patient_preferences,
    list_preferences,
)

__all__ = (
    "PatientPreferenceSelector",
    "PatientCommunicationPreferenceSelector",
    "get_patient_preference",
    "get_patient_communication_preference",
    "list_preferences",
    "list_patient_preferences",
    "list_communication_preferences",
    "list_patient_communication_preferences",
)
''',

    # ------------------------------------------------------------------
    # COMMUNICATION
    # ------------------------------------------------------------------
    r"apps\patient_management\communication\selectors\communication.py": r'''"""
Read selectors for Patient Communication records.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.communication.models import (
    PatientCommunication,
)


class PatientCommunicationSelector:
    """
    Organization-scoped selector API for patient communications.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientCommunication]:
        """
        Return the optimized base queryset.
        """
        return (
            PatientCommunication.objects
            .select_related(
                "organization",
                "patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        communication_id: UUID,
    ) -> PatientCommunication:
        """
        Return one communication belonging to the organization.
        """
        return (
            PatientCommunicationSelector.queryset()
            .get(
                organization_id=organization_id,
                id=communication_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientCommunication]:
        """
        Return organization-scoped communications.
        """
        return (
            PatientCommunicationSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientCommunication]:
        """
        Return communications for one patient.
        """
        return (
            PatientCommunicationSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_status(
        *,
        organization_id: int,
        status: str,
        patient_id: int | None = None,
    ) -> QuerySet[PatientCommunication]:
        """
        Return communications by status.
        """
        queryset = (
            PatientCommunicationSelector.queryset()
            .filter(
                organization_id=organization_id,
                status=status,
            )
        )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        return queryset.order_by(
            "-created_at",
        )

    @staticmethod
    def list_unread(
        *,
        organization_id: int,
        patient_id: int | None = None,
    ) -> QuerySet[PatientCommunication]:
        """
        Return unread communications.
        """
        queryset = (
            PatientCommunicationSelector.queryset()
            .filter(
                organization_id=organization_id,
                read_at__isnull=True,
            )
        )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        return queryset.order_by(
            "-created_at",
        )


get_patient_communication = PatientCommunicationSelector.get
list_patient_communications = (
    PatientCommunicationSelector.list_by_patient
)
list_communications = PatientCommunicationSelector.list_by_organization


__all__ = (
    "PatientCommunicationSelector",
    "get_patient_communication",
    "list_patient_communications",
    "list_communications",
)
''',

    r"apps\patient_management\communication\selectors\__init__.py": r'''"""
Selectors for Patient Communication.
"""

from apps.patient_management.communication.selectors.communication import (
    PatientCommunicationSelector,
    get_patient_communication,
    list_communications,
    list_patient_communications,
)

__all__ = (
    "PatientCommunicationSelector",
    "get_patient_communication",
    "list_communications",
    "list_patient_communications",
)
''',

    # ------------------------------------------------------------------
    # PATIENT DOCUMENTS
    # ------------------------------------------------------------------
    r"apps\patient_management\patient_documents\selectors\patient_document.py": r'''"""
Read selectors for Patient Documents.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentSelector:
    """
    Organization-scoped selector API for patient documents.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientDocument]:
        """
        Return the optimized document queryset.
        """
        queryset = PatientDocument.objects.all()

        field_names = {
            field.name
            for field in PatientDocument._meta.get_fields()
        }

        select_related_fields = [
            field
            for field in (
                "organization",
                "patient",
                "created_by",
                "updated_by",
            )
            if field in field_names
        ]

        if select_related_fields:
            queryset = queryset.select_related(
                *select_related_fields,
            )

        return queryset

    @staticmethod
    def get(
        *,
        organization_id: int,
        document_id: UUID,
    ) -> PatientDocument:
        """
        Return one patient document.
        """
        return (
            PatientDocumentSelector.queryset()
            .get(
                organization_id=organization_id,
                id=document_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientDocument]:
        """
        Return documents belonging to an organization.
        """
        return (
            PatientDocumentSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientDocument]:
        """
        Return documents belonging to a patient.
        """
        return (
            PatientDocumentSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_active(
        *,
        organization_id: int,
        patient_id: int | None = None,
    ) -> QuerySet[PatientDocument]:
        """
        Return active documents.
        """
        queryset = PatientDocumentSelector.queryset().filter(
            organization_id=organization_id,
        )

        field_names = {
            field.name
            for field in PatientDocument._meta.get_fields()
        }

        if "status" in field_names:
            queryset = queryset.filter(
                status__iexact="ACTIVE",
            )
        elif "is_active" in field_names:
            queryset = queryset.filter(
                is_active=True,
            )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        return queryset.order_by(
            "-created_at",
        )


get_patient_document = PatientDocumentSelector.get
list_patient_documents = PatientDocumentSelector.list_by_patient
list_documents = PatientDocumentSelector.list_by_organization


__all__ = (
    "PatientDocumentSelector",
    "get_patient_document",
    "list_patient_documents",
    "list_documents",
)
''',

    r"apps\patient_management\patient_documents\selectors\document_version.py": r'''"""
Read selectors for Patient Document Versions.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    DocumentVersion,
)


class DocumentVersionSelector:
    """
    Selector API for document versions.
    """

    @staticmethod
    def queryset() -> QuerySet[DocumentVersion]:
        """
        Return the optimized base queryset.
        """
        queryset = DocumentVersion.objects.all()

        field_names = {
            field.name
            for field in DocumentVersion._meta.get_fields()
        }

        select_related_fields = [
            field
            for field in (
                "organization",
                "patient_document",
                "created_by",
            )
            if field in field_names
        ]

        if select_related_fields:
            queryset = queryset.select_related(
                *select_related_fields,
            )

        return queryset

    @staticmethod
    def get(
        *,
        organization_id: int,
        version_id: UUID,
    ) -> DocumentVersion:
        """
        Return one document version within the organization.
        """
        return (
            DocumentVersionSelector.queryset()
            .get(
                organization_id=organization_id,
                id=version_id,
            )
        )

    @staticmethod
    def list_by_document(
        *,
        organization_id: int,
        document_id: UUID,
    ) -> QuerySet[DocumentVersion]:
        """
        Return all versions for a document.
        """
        field_names = {
            field.name
            for field in DocumentVersion._meta.get_fields()
        }

        filter_key = (
            "patient_document_id"
            if "patient_document" in field_names
            else "document_id"
        )

        return (
            DocumentVersionSelector.queryset()
            .filter(
                organization_id=organization_id,
                **{
                    filter_key: document_id,
                },
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def latest(
        *,
        organization_id: int,
        document_id: UUID,
    ) -> DocumentVersion | None:
        """
        Return the latest version of a document.
        """
        return (
            DocumentVersionSelector.list_by_document(
                organization_id=organization_id,
                document_id=document_id,
            )
            .first()
        )


get_document_version = DocumentVersionSelector.get
list_document_versions = DocumentVersionSelector.list_by_document


__all__ = (
    "DocumentVersionSelector",
    "get_document_version",
    "list_document_versions",
)
''',

    r"apps\patient_management\patient_documents\selectors\document_access_log.py": r'''"""
Read selectors for Patient Document Access Logs.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    DocumentAccessLog,
)


class DocumentAccessLogSelector:
    """
    Selector API for document access audit records.
    """

    @staticmethod
    def queryset() -> QuerySet[DocumentAccessLog]:
        """
        Return the optimized base queryset.
        """
        queryset = DocumentAccessLog.objects.all()

        field_names = {
            field.name
            for field in DocumentAccessLog._meta.get_fields()
        }

        select_related_fields = [
            field
            for field in (
                "organization",
                "patient",
                "patient_document",
                "actor",
                "user",
            )
            if field in field_names
        ]

        if select_related_fields:
            queryset = queryset.select_related(
                *select_related_fields,
            )

        return queryset

    @staticmethod
    def get(
        *,
        organization_id: int,
        access_log_id: UUID,
    ) -> DocumentAccessLog:
        """
        Return one access-log entry.
        """
        return (
            DocumentAccessLogSelector.queryset()
            .get(
                organization_id=organization_id,
                id=access_log_id,
            )
        )

    @staticmethod
    def list_by_document(
        *,
        organization_id: int,
        document_id: UUID,
    ) -> QuerySet[DocumentAccessLog]:
        """
        Return access logs for one document.
        """
        field_names = {
            field.name
            for field in DocumentAccessLog._meta.get_fields()
        }

        filter_key = (
            "patient_document_id"
            if "patient_document" in field_names
            else "document_id"
        )

        return (
            DocumentAccessLogSelector.queryset()
            .filter(
                organization_id=organization_id,
                **{
                    filter_key: document_id,
                },
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[DocumentAccessLog]:
        """
        Return document-access logs for one patient.
        """
        return (
            DocumentAccessLogSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-created_at",
            )
        )


get_document_access_log = DocumentAccessLogSelector.get
list_document_access_logs = (
    DocumentAccessLogSelector.list_by_document
)


__all__ = (
    "DocumentAccessLogSelector",
    "get_document_access_log",
    "list_document_access_logs",
)
''',

    r"apps\patient_management\patient_documents\selectors\__init__.py": r'''"""
Selectors for Patient Documents.
"""

from apps.patient_management.patient_documents.selectors.document_access_log import (
    DocumentAccessLogSelector,
    get_document_access_log,
    list_document_access_logs,
)
from apps.patient_management.patient_documents.selectors.document_version import (
    DocumentVersionSelector,
    get_document_version,
    list_document_versions,
)
from apps.patient_management.patient_documents.selectors.patient_document import (
    PatientDocumentSelector,
    get_patient_document,
    list_documents,
    list_patient_documents,
)

__all__ = (
    "PatientDocumentSelector",
    "DocumentVersionSelector",
    "DocumentAccessLogSelector",
    "get_patient_document",
    "get_document_version",
    "get_document_access_log",
    "list_documents",
    "list_patient_documents",
    "list_document_versions",
    "list_document_access_logs",
)
''',

    # ------------------------------------------------------------------
    # REFERRALS
    # ------------------------------------------------------------------
    r"apps\patient_management\referrals\selectors\referrals.py": r'''"""
Read selectors for Patient Referrals.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.referrals.models import PatientReferral


class PatientReferralSelector:
    """
    Organization-scoped selector API for referrals.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientReferral]:
        """
        Return the optimized base queryset.
        """
        return (
            PatientReferral.objects
            .select_related(
                "organization",
                "patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        referral_id: UUID,
    ) -> PatientReferral:
        """
        Return one referral within the organization.
        """
        return (
            PatientReferralSelector.queryset()
            .get(
                organization_id=organization_id,
                id=referral_id,
            )
        )

    @staticmethod
    def get_by_number(
        *,
        organization_id: int,
        referral_number: str,
    ) -> PatientReferral:
        """
        Return a referral by referral number.
        """
        return (
            PatientReferralSelector.queryset()
            .get(
                organization_id=organization_id,
                referral_number=referral_number.strip(),
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientReferral]:
        """
        Return organization-scoped referrals.
        """
        return (
            PatientReferralSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientReferral]:
        """
        Return referrals for one patient.
        """
        return (
            PatientReferralSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_status(
        *,
        organization_id: int,
        status: str,
        patient_id: int | None = None,
    ) -> QuerySet[PatientReferral]:
        """
        Return referrals by status.
        """
        queryset = (
            PatientReferralSelector.queryset()
            .filter(
                organization_id=organization_id,
                status=status,
            )
        )

        if patient_id is not None:
            queryset = queryset.filter(
                patient_id=patient_id,
            )

        return queryset.order_by(
            "-created_at",
        )

    @staticmethod
    def list_pending(
        *,
        organization_id: int,
        patient_id: int | None = None,
    ) -> QuerySet[PatientReferral]:
        """
        Return pending referrals.
        """
        return PatientReferralSelector.list_by_status(
            organization_id=organization_id,
            status="PENDING",
            patient_id=patient_id,
        )


get_patient_referral = PatientReferralSelector.get
list_patient_referrals = PatientReferralSelector.list_by_patient
list_referrals = PatientReferralSelector.list_by_organization


__all__ = (
    "PatientReferralSelector",
    "get_patient_referral",
    "list_patient_referrals",
    "list_referrals",
)
''',

    r"apps\patient_management\referrals\selectors\__init__.py": r'''"""
Selectors for Patient Referrals.
"""

from apps.patient_management.referrals.selectors.referrals import (
    PatientReferralSelector,
    get_patient_referral,
    list_patient_referrals,
    list_referrals,
)

__all__ = (
    "PatientReferralSelector",
    "get_patient_referral",
    "list_patient_referrals",
    "list_referrals",
)
''',

    # ------------------------------------------------------------------
    # TIMELINE
    # ------------------------------------------------------------------
    r"apps\patient_management\timeline\selectors\timeline.py": r'''"""
Read selectors for Patient Timeline Events.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.timeline.models import (
    PatientTimelineEvent,
)


class PatientTimelineEventSelector:
    """
    Organization-scoped selector API for timeline events.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientTimelineEvent]:
        """
        Return the optimized base queryset.
        """
        queryset = (
            PatientTimelineEvent.objects
        )

        field_names = {
            field.name
            for field in PatientTimelineEvent._meta.get_fields()
        }

        select_related_fields = [
            field
            for field in (
                "organization",
                "patient",
                "created_by",
            )
            if field in field_names
        ]

        if select_related_fields:
            queryset = queryset.select_related(
                *select_related_fields,
            )

        return queryset

    @staticmethod
    def get(
        *,
        organization_id: int,
        timeline_event_id: UUID,
    ) -> PatientTimelineEvent:
        """
        Return one timeline event.
        """
        return (
            PatientTimelineEventSelector.queryset()
            .get(
                organization_id=organization_id,
                id=timeline_event_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientTimelineEvent]:
        """
        Return timeline events for an organization.
        """
        return (
            PatientTimelineEventSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> QuerySet[PatientTimelineEvent]:
        """
        Return timeline events for a patient.
        """
        return (
            PatientTimelineEventSelector.queryset()
            .filter(
                organization_id=organization_id,
                patient_id=patient_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_recent(
        *,
        organization_id: int,
        patient_id: int,
        limit: int = 100,
    ) -> QuerySet[PatientTimelineEvent]:
        """
        Return recent patient timeline events.

        The limit is bounded to prevent accidental unbounded read loads.
        """
        safe_limit = max(
            1,
            min(
                int(limit),
                500,
            ),
        )

        return (
            PatientTimelineEventSelector.list_by_patient(
                organization_id=organization_id,
                patient_id=patient_id,
            )[:safe_limit]
        )


get_patient_timeline_event = PatientTimelineEventSelector.get
get_patient_timeline_event_for_patient = (
    PatientTimelineEventSelector.list_by_patient
)
list_patient_timeline_events = (
    PatientTimelineEventSelector.list_by_organization
)


__all__ = (
    "PatientTimelineEventSelector",
    "get_patient_timeline_event",
    "get_patient_timeline_event_for_patient",
    "list_patient_timeline_events",
)
''',

    r"apps\patient_management\timeline\selectors\__init__.py": r'''"""
Selectors for Patient Timeline.
"""

from apps.patient_management.timeline.selectors.timeline import (
    PatientTimelineEventSelector,
    get_patient_timeline_event,
    get_patient_timeline_event_for_patient,
    list_patient_timeline_events,
)

__all__ = (
    "PatientTimelineEventSelector",
    "get_patient_timeline_event",
    "get_patient_timeline_event_for_patient",
    "list_patient_timeline_events",
)
''',

    # ------------------------------------------------------------------
    # PORTAL
    # ------------------------------------------------------------------
    r"apps\patient_management\portal\selectors\portal.py": r'''"""
Read selectors for Patient Portal Accounts.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.portal.models import (
    PatientPortalAccount,
)


class PatientPortalAccountSelector:
    """
    Organization-scoped selector API for portal accounts.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientPortalAccount]:
        """
        Return the optimized base queryset.
        """
        return (
            PatientPortalAccount.objects
            .select_related(
                "organization",
                "patient",
            )
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        portal_account_id: UUID,
    ) -> PatientPortalAccount:
        """
        Return one portal account.
        """
        return (
            PatientPortalAccountSelector.queryset()
            .get(
                organization_id=organization_id,
                id=portal_account_id,
            )
        )

    @staticmethod
    def get_by_patient(
        *,
        organization_id: int,
        patient_id: int,
    ) -> PatientPortalAccount:
        """
        Return the portal account associated with a patient.
        """
        return (
            PatientPortalAccountSelector.queryset()
            .get(
                organization_id=organization_id,
                patient_id=patient_id,
            )
        )

    @staticmethod
    def get_by_username(
        *,
        organization_id: int,
        username: str,
    ) -> PatientPortalAccount:
        """
        Return a portal account by username.
        """
        return (
            PatientPortalAccountSelector.queryset()
            .get(
                organization_id=organization_id,
                username=username.strip(),
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[PatientPortalAccount]:
        """
        Return portal accounts for an organization.
        """
        return (
            PatientPortalAccountSelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_by_status(
        *,
        organization_id: int,
        status: str,
    ) -> QuerySet[PatientPortalAccount]:
        """
        Return portal accounts by status.
        """
        return (
            PatientPortalAccountSelector.queryset()
            .filter(
                organization_id=organization_id,
                status=status,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def list_active(
        *,
        organization_id: int,
    ) -> QuerySet[PatientPortalAccount]:
        """
        Return active portal accounts.
        """
        return PatientPortalAccountSelector.list_by_status(
            organization_id=organization_id,
            status="ACTIVE",
        )


get_patient_portal_account = PatientPortalAccountSelector.get
get_patient_portal_account_for_patient = (
    PatientPortalAccountSelector.get_by_patient
)
list_patient_portal_accounts = (
    PatientPortalAccountSelector.list_by_organization
)


__all__ = (
    "PatientPortalAccountSelector",
    "get_patient_portal_account",
    "get_patient_portal_account_for_patient",
    "list_patient_portal_accounts",
)
''',

    r"apps\patient_management\portal\selectors\__init__.py": r'''"""
Selectors for Patient Portal.
"""

from apps.patient_management.portal.selectors.portal import (
    PatientPortalAccountSelector,
    get_patient_portal_account,
    get_patient_portal_account_for_patient,
    list_patient_portal_accounts,
)

__all__ = (
    "PatientPortalAccountSelector",
    "get_patient_portal_account",
    "get_patient_portal_account_for_patient",
    "list_patient_portal_accounts",
)
''',

    # ------------------------------------------------------------------
    # MPI
    # ------------------------------------------------------------------
    r"apps\patient_management\mpi\selectors\mpi.py": r'''"""
Read selectors for the MPI module.

The MPI model contract in the current codebase is intentionally kept
minimal here. The selector enforces organization isolation and exposes
the shared read boundary without inventing business-specific fields.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from django.apps import apps
from django.db.models import Model, QuerySet


def _get_mpi_model() -> type[Model]:
    """
    Resolve the configured MPI model from the Patient MPI application.

    This avoids hard-coding an unverified model class name while the MPI
    module is being finalized in the current architecture.
    """
    app_config = apps.get_app_config(
        "patient_mpi",
    )

    models = tuple(
        app_config.get_models(),
    )

    if len(models) == 1:
        return models[0]

    preferred_names = {
        "mpi",
        "patientmpi",
        "patientmasterindex",
        "masterpatientindex",
        "mpirecord",
    }

    for model in models:
        if model._meta.model_name.lower() in preferred_names:
            return model

    raise LookupError(
        "Unable to resolve the canonical MPI model. "
        "The MPI application must expose exactly one model or use a "
        "recognized canonical model name."
    )


class MPISelector:
    """
    Organization-scoped selector API for MPI records.
    """

    @staticmethod
    def queryset() -> QuerySet[Any]:
        """
        Return the base MPI queryset.
        """
        model = _get_mpi_model()
        queryset = model.objects.all()

        field_names = {
            field.name
            for field in model._meta.get_fields()
        }

        select_related_fields = [
            field
            for field in (
                "organization",
                "patient",
            )
            if field in field_names
        ]

        if select_related_fields:
            queryset = queryset.select_related(
                *select_related_fields,
            )

        return queryset.filter(
            organization_id__isnull=False,
        )

    @staticmethod
    def get(
        *,
        organization_id: int,
        record_id: UUID,
    ) -> Any:
        """
        Return one MPI record inside the organization.
        """
        return (
            MPISelector.queryset()
            .get(
                organization_id=organization_id,
                id=record_id,
            )
        )

    @staticmethod
    def list_by_organization(
        *,
        organization_id: int,
    ) -> QuerySet[Any]:
        """
        Return MPI records for one organization.
        """
        return (
            MPISelector.queryset()
            .filter(
                organization_id=organization_id,
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def exists(
        *,
        organization_id: int,
        record_id: UUID,
    ) -> bool:
        """
        Determine whether an MPI record exists in the organization.
        """
        return (
            MPISelector.queryset()
            .filter(
                organization_id=organization_id,
                id=record_id,
            )
            .exists()
        )


get_mpi_record = MPISelector.get
list_mpi_records = MPISelector.list_by_organization


__all__ = (
    "MPISelector",
    "get_mpi_record",
    "list_mpi_records",
)
''',

    r"apps\patient_management\mpi\selectors\__init__.py": r'''"""
Selectors for Patient MPI.
"""

from apps.patient_management.mpi.selectors.mpi import (
    MPISelector,
    get_mpi_record,
    list_mpi_records,
)

__all__ = (
    "MPISelector",
    "get_mpi_record",
    "list_mpi_records",
)
''',
}


def write_file(relative_path: str, content: str) -> None:
    """
    Write one selector file and create parent directories.
    """
    target = BACKEND_ROOT / relative_path
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    target.write_text(
        content.rstrip() + "\n",
        encoding="utf-8",
    )


def main() -> None:
    """
    Install all Layer 3A selector files.
    """
    for relative_path, content in FILES.items():
        write_file(
            relative_path,
            content,
        )

    print()
    print("=" * 72)
    print("PATIENT MANAGEMENT - LAYER 3A SELECTORS")
    print("=" * 72)
    print(f"Files written: {len(FILES)}")
    print()
    print("Completed selector modules:")
    print("  [OK] relationships")
    print("  [OK] medical_history")
    print("  [OK] consents")
    print("  [OK] preferences")
    print("  [OK] communication")
    print("  [OK] patient_documents")
    print("  [OK] referrals")
    print("  [OK] timeline")
    print("  [OK] portal")
    print("  [OK] mpi")
    print()
    print("Layer 3A source files are now installed.")
    print("Do not run final Django validation yet; Patient Management")
    print("Layer 3B-3F is still pending.")
    print("=" * 72)
    print()


if __name__ == "__main__":
    main()
