"""
Prior Authorization models.

The RCM prior authorization module tracks the revenue-cycle workflow around
prior authorizations. It references the insurance app's ``Authorization``
record, which owns the payer-facing authorization data.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.insurance.models import Authorization
from apps.platform.organizations.models import Organization


class PriorAuthorizationRequest(BaseModel):
    """
    RCM tracking record for a prior authorization request.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="prior_authorization_requests",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="prior_authorization_requests",
    )

    authorization = models.OneToOneField(
        Authorization,
        on_delete=models.CASCADE,
        related_name="rcm_request",
        help_text="Linked insurance authorization record.",
    )

    requested_by = models.CharField(
        max_length=150,
        blank=True,
    )

    submitted_to_payer_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    decision_received_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    payer_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    clinical_notes = models.TextField(
        blank=True,
    )

    follow_up_date = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "prior_authorization_requests"

        verbose_name = "Prior Authorization Request"

        verbose_name_plural = "Prior Authorization Requests"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
                name="pa_org_pat_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"PA Request {self.authorization}"


__all__ = [
    "PriorAuthorizationRequest",
]
