"""
Financial Management-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class ReportType(models.TextChoices):
    BALANCE_SHEET = "balance_sheet", "Balance Sheet"
    PROFIT_LOSS = "profit_loss", "Profit and Loss"
    CASH_FLOW = "cash_flow", "Cash Flow"
    TRIAL_BALANCE = "trial_balance", "Trial Balance"


class ReportStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


DEFAULT_REPORT_STATUS: Final[str] = ReportStatus.DRAFT


__all__ = [
    "ReportStatus",
    "ReportType",
]
