"""Django application configuration for Revenue Cycle claim scrubbing."""

from __future__ import annotations

from django.apps import AppConfig


class ClaimScrubbingConfig(AppConfig):
    """Configure the claim scrubbing application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle.claim_scrubbing"
    verbose_name = "Revenue Cycle Claim Scrubbing"


__all__ = ("ClaimScrubbingConfig",)
