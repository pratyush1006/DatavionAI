"""
Tax and GST-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class TaxType(models.TextChoices):
    GST = "gst", "GST"
    CGST = "cgst", "CGST"
    SGST = "sgst", "SGST"
    IGST = "igst", "IGST"
    TDS = "tds", "TDS"
    TCS = "tcs", "TCS"


class FilingStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    FILED = "filed", "Filed"
    PAID = "paid", "Paid"
    PENDING = "pending", "Pending"


DEFAULT_TAX_TYPE: Final[str] = TaxType.GST


__all__ = [
    "FilingStatus",
    "TaxType",
]
