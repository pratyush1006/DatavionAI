"""
Selectors for Patient Family Members.

Selectors own read-only querying, organization/tenant scoping,
related-object loading, and visibility boundaries.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.family_members.models import FamilyMember
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class FamilyMemberSelector:
    """Read-only, organization-scoped Family Member queries."""

    @staticmethod
    def queryset(
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        queryset = FamilyMember.objects.select_related(
            "organization",
            "patient",
        ).filter(
            organization=organization,
        )

        if tenant_id is not None:
            queryset = queryset.filter(
                organization__tenant_id=tenant_id,
            )

        return queryset

    @staticmethod
    def empty_queryset() -> QuerySet[FamilyMember]:
        return FamilyMember.objects.none()

    @classmethod
    def list(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.queryset(
            organization=organization,
            tenant_id=tenant_id,
        ).order_by(
            "first_name",
            "last_name",
        )

    @classmethod
    def list_by_organization(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.list(
            organization=organization,
            tenant_id=tenant_id,
        )

    @classmethod
    def list_by_patient(
        cls,
        *,
        organization: Organization,
        patient: Patient | None = None,
        patient_id: UUID | None = None,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        queryset = cls.list(
            organization=organization,
            tenant_id=tenant_id,
        )

        if patient is not None:
            patient_id = patient.id

        if patient_id is None:
            return cls.empty_queryset()

        return queryset.filter(
            patient_id=patient_id,
            patient__organization=organization,
        ).order_by(
            "relationship",
            "first_name",
            "last_name",
        )

    @classmethod
    def get(
        cls,
        *,
        organization: Organization,
        family_member_id: UUID,
        tenant_id: UUID | None = None,
    ) -> FamilyMember:
        return get_object_or_404(
            cls.queryset(
                organization=organization,
                tenant_id=tenant_id,
            ),
            pk=family_member_id,
        )

    @staticmethod
    def get_deleted(
        *,
        organization: Organization,
        family_member_id: UUID,
        tenant_id: UUID | None = None,
    ) -> FamilyMember:
        queryset = FamilyMember.deleted_objects.select_related(
            "organization",
            "patient",
        ).filter(
            organization=organization,
        )

        if tenant_id is not None:
            queryset = queryset.filter(
                organization__tenant_id=tenant_id,
            )

        return get_object_or_404(
            queryset,
            pk=family_member_id,
        )

    @staticmethod
    def list_deleted(
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        queryset = FamilyMember.deleted_objects.select_related(
            "organization",
            "patient",
        ).filter(
            organization=organization,
        )

        if tenant_id is not None:
            queryset = queryset.filter(
                organization__tenant_id=tenant_id,
            )

        return queryset.order_by(
            "-deleted_at",
            "first_name",
            "last_name",
        )

    @classmethod
    def get_next_of_kin(
        cls,
        *,
        organization: Organization,
        patient_id: UUID,
        tenant_id: UUID | None = None,
    ) -> FamilyMember | None:
        return (
            cls.list_by_patient(
                organization=organization,
                patient_id=patient_id,
                tenant_id=tenant_id,
            )
            .filter(
                is_next_of_kin=True,
            )
            .first()
        )

    @classmethod
    def list_emergency_contacts(
        cls,
        *,
        organization: Organization,
        patient_id: UUID,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.list_by_patient(
            organization=organization,
            patient_id=patient_id,
            tenant_id=tenant_id,
        ).filter(
            is_emergency_contact=True,
        )

    @classmethod
    def list_living(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.list(
            organization=organization,
            tenant_id=tenant_id,
        ).filter(
            is_living=True,
        )

    @classmethod
    def list_deceased(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.list(
            organization=organization,
            tenant_id=tenant_id,
        ).filter(
            is_living=False,
        )

    @classmethod
    def list_active(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.list(
            organization=organization,
            tenant_id=tenant_id,
        ).filter(
            is_active=True,
        )

    @classmethod
    def list_inactive(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        return cls.list(
            organization=organization,
            tenant_id=tenant_id,
        ).filter(
            is_active=False,
        )

    @classmethod
    def search(
        cls,
        *,
        organization: Organization,
        query: str,
        tenant_id: UUID | None = None,
    ) -> QuerySet[FamilyMember]:
        queryset = cls.list(
            organization=organization,
            tenant_id=tenant_id,
        )

        query = (query or "").strip()

        if not query:
            return queryset

        return queryset.filter(
            Q(family_member_number__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(mobile_number__icontains=query)
            | Q(relationship__icontains=query)
        ).order_by(
            "first_name",
            "last_name",
        )

    @classmethod
    def count_by_patient(
        cls,
        *,
        organization: Organization,
        patient_id: UUID,
        tenant_id: UUID | None = None,
    ) -> int:
        return cls.list_by_patient(
            organization=organization,
            patient_id=patient_id,
            tenant_id=tenant_id,
        ).count()

    @classmethod
    def count_by_organization(
        cls,
        *,
        organization: Organization,
        tenant_id: UUID | None = None,
    ) -> int:
        return cls.list(
            organization=organization,
            tenant_id=tenant_id,
        ).count()


__all__ = ("FamilyMemberSelector",)
