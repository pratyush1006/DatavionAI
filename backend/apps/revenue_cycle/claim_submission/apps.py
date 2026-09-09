"""Django application configuration for claim submission."""

from __future__ import annotations

from django.apps import AppConfig


class ClaimSubmissionConfig(AppConfig):
    """Configure the claim submission application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.claim_submission"
    label = "revenue_cycle_claim_submission"
    verbose_name = "Revenue Cycle Claim Submission"


__all__ = ("ClaimSubmissionConfig",)
