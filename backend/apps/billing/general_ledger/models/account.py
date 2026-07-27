"""
General Ledger account model.
"""

from __future__ import annotations

from django.db import models

from apps.billing.general_ledger.constants import (
    DEFAULT_ACCOUNT_STATUS,
    AccountStatus,
    AccountType,
)
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class GeneralLedgerAccount(BaseModel):
    """
    Represents a chart-of-accounts entry within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="general_ledger_accounts",
        help_text="Organization that owns the ledger account.",
    )

    code = models.CharField(
        max_length=30,
        help_text="Account code.",
    )

    name = models.CharField(
        max_length=150,
        help_text="Account name.",
    )

    description = models.TextField(
        blank=True,
        help_text="Account description.",
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        help_text="General ledger account type.",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text="Parent account for hierarchical ledgers.",
    )

    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=DEFAULT_ACCOUNT_STATUS,
        db_index=True,
        help_text="Account lifecycle status.",
    )

    class Meta:
        db_table = "general_ledger_accounts"

        verbose_name = "General Ledger Account"

        verbose_name_plural = "General Ledger Accounts"

        ordering = (
            "code",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="gl_acct_org_status_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "account_type",
                ],
                name="gl_acct_org_type_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="unique_gl_account_code_per_organization",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.code} - {self.name}"


__all__ = [
    "GeneralLedgerAccount",
]
