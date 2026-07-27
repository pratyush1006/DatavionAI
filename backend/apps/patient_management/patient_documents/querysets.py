"""
Custom QuerySet implementations for the Patient Documents module.
"""

from __future__ import annotations

from django.db import models
from django.db.models import Q

from apps.patient_management.patient_documents.constants import (
    DocumentCategory,
    DocumentStatus,
    DocumentVisibility,
)


class PatientDocumentQuerySet(models.QuerySet):
    """
    Custom QuerySet for PatientDocument.
    """

    def active(self) -> PatientDocumentQuerySet:
        """
        Return active documents.
        """

        return self.filter(
            status=DocumentStatus.ACTIVE,
            is_active=True,
            is_deleted=False,
        )

    def draft(self) -> PatientDocumentQuerySet:
        """
        Return draft documents.
        """

        return self.filter(
            status=DocumentStatus.DRAFT,
            is_deleted=False,
        )

    def pending_review(self) -> PatientDocumentQuerySet:
        """
        Return documents awaiting verification.
        """

        return self.filter(
            status=DocumentStatus.PENDING_REVIEW,
            is_deleted=False,
        )

    def verified(self) -> PatientDocumentQuerySet:
        """
        Return verified documents.
        """

        return self.filter(
            status=DocumentStatus.VERIFIED,
            is_deleted=False,
        )

    def archived(self) -> PatientDocumentQuerySet:
        """
        Return archived documents.
        """

        return self.filter(
            status=DocumentStatus.ARCHIVED,
        )

    def expired(self) -> PatientDocumentQuerySet:
        """
        Return expired documents.
        """

        return self.filter(
            status=DocumentStatus.EXPIRED,
        )

    def deleted(self) -> PatientDocumentQuerySet:
        """
        Return soft deleted documents.
        """

        return self.filter(
            is_deleted=True,
        )

    def visible(self) -> PatientDocumentQuerySet:
        """
        Return documents visible to internal users.
        """

        return self.exclude(
            visibility=DocumentVisibility.PRIVATE,
        )

    def private(self) -> PatientDocumentQuerySet:
        """
        Return private documents.
        """

        return self.filter(
            visibility=DocumentVisibility.PRIVATE,
        )

    def shared(self) -> PatientDocumentQuerySet:
        """
        Return shared documents.
        """

        return self.filter(
            visibility=DocumentVisibility.SHARED,
        )

    def by_patient(
        self,
        patient,
    ) -> PatientDocumentQuerySet:
        """
        Filter by patient.
        """

        return self.filter(
            patient=patient,
        )

    def by_organization(
        self,
        organization,
    ) -> PatientDocumentQuerySet:
        """
        Filter by organization.
        """

        return self.filter(
            organization=organization,
        )

    def by_category(
        self,
        category: DocumentCategory | str,
    ) -> PatientDocumentQuerySet:
        """
        Filter by document category.
        """

        return self.filter(
            category=category,
        )

    def latest_version(self) -> PatientDocumentQuerySet:
        """
        Return only the latest version of documents.
        """

        return self.filter(
            is_latest_version=True,
        )

    def search(
        self,
        query: str,
    ) -> PatientDocumentQuerySet:
        """
        Search across common document fields.
        """

        if not query:
            return self

        return self.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(file_name__icontains=query)
            | Q(tags__icontains=query)
        )


__all__ = ("PatientDocumentQuerySet",)
