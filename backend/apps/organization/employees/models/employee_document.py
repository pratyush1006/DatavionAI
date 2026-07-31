"""
Employee document model.

Stores employee document metadata and links to the
central Document Management bounded context.

Responsibilities
----------------
- Employee document association
- Document classification
- Verification lifecycle
- Expiry tracking
- Document ownership reference

Non-responsibilities
--------------------
- File storage
- Upload handling
- File versioning
- Virus scanning
- Storage lifecycle
- Document access policies

Those responsibilities belong to the Document Management
bounded context.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.organization.employees.constants import (
    DocumentType,
    VerificationStatus,
)


class EmployeeDocument(
    BaseModel,
):
    """
    Document metadata associated with an employee.

    Actual file storage is handled by the Document Management
    service.
    """

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Employee"),
        help_text=_(
            "Employee who owns this document.",
        ),
    )

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.PROTECT,
        related_name="employee_documents",
        verbose_name=_("Document"),
        help_text=_(
            "Reference to the managed document entity.",
        ),
    )

    document_type = models.CharField(
        _("Document Type"),
        max_length=50,
        choices=DocumentType.choices,
        db_index=True,
        help_text=_(
            "Classification of the employee document.",
        ),
    )

    title = models.CharField(
        _("Title"),
        max_length=255,
    )

    document_number = models.CharField(
        _("Document Number"),
        max_length=150,
        blank=True,
        help_text=_(
            "Reference number or identifier.",
        ),
    )

    issuing_authority = models.CharField(
        _("Issuing Authority"),
        max_length=200,
        blank=True,
    )

    issue_date = models.DateField(
        _("Issue Date"),
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        _("Expiry Date"),
        null=True,
        blank=True,
    )

    verification_status = models.CharField(
        _("Verification Status"),
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )

    verified_at = models.DateTimeField(
        _("Verified At"),
        null=True,
        blank=True,
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_employee_documents",
        verbose_name=_("Verified By"),
    )

    remarks = models.TextField(
        _("Remarks"),
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_employee_documents"

        verbose_name = _(
            "Employee Document",
        )

        verbose_name_plural = _(
            "Employee Documents",
        )

        ordering = (
            "employee",
            "document_type",
            "title",
        )

        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(
                        expiry_date__isnull=True,
                    )
                    | Q(
                        issue_date__isnull=True,
                    )
                    | Q(
                        expiry_date__gte=F(
                            "issue_date",
                        ),
                    )
                ),
                name=("ck_employee_document_dates"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("employee",),
                name=("idx_emp_document_employee"),
            ),
            models.Index(
                fields=("document_type",),
                name=("idx_emp_document_type"),
            ),
            models.Index(
                fields=("expiry_date",),
                name=("idx_emp_document_expiry"),
            ),
            models.Index(
                fields=("verification_status",),
                name=("idx_emp_document_verification"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable representation.
        """

        return f"{self.employee.employee_code} - {self.title}"


__all__: tuple[str, ...] = ("EmployeeDocument",)
