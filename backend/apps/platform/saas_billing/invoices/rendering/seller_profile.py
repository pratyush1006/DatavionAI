"""
Dynamic DatavionOS seller/company billing profile.

No legal/company information is hard-coded here.

Values are read from Django settings first and environment
variables second.
"""

from __future__ import annotations

import os
from typing import Any


def _setting(
    settings: Any,
    name: str,
    default: str = "",
) -> str:
    value = getattr(
        settings,
        name,
        None,
    )

    if value is None:
        value = os.getenv(
            name,
            default,
        )

    return str(value or "")


def get_seller_profile() -> dict[str, str]:
    """
    Return the legal seller profile used by invoices.

    Configure these values in the deployment environment.

    Supported fields:
      INVOICE_SELLER_LEGAL_NAME
      INVOICE_SELLER_DISPLAY_NAME
      INVOICE_SELLER_ADDRESS_LINE1
      INVOICE_SELLER_ADDRESS_LINE2
      INVOICE_SELLER_CITY
      INVOICE_SELLER_STATE
      INVOICE_SELLER_COUNTRY
      INVOICE_SELLER_POSTAL_CODE
      INVOICE_SELLER_PHONE
      INVOICE_SELLER_EMAIL
      INVOICE_SELLER_BILLING_EMAIL
      INVOICE_SELLER_WEBSITE
      INVOICE_SELLER_GSTIN
      INVOICE_SELLER_PAN
      INVOICE_SELLER_CIN
      INVOICE_SELLER_LLPIN
      INVOICE_SELLER_LOGO_URL
      INVOICE_SELLER_INVOICE_PREFIX
    """

    try:
        from django.conf import settings
    except ImportError:
        settings = None

    names = (
        "LEGAL_NAME",
        "DISPLAY_NAME",
        "ADDRESS_LINE1",
        "ADDRESS_LINE2",
        "CITY",
        "STATE",
        "COUNTRY",
        "POSTAL_CODE",
        "PHONE",
        "EMAIL",
        "BILLING_EMAIL",
        "WEBSITE",
        "GSTIN",
        "PAN",
        "CIN",
        "LLPIN",
        "LOGO_URL",
        "INVOICE_PREFIX",
    )

    profile: dict[str, str] = {}

    for suffix in names:
        key = f"INVOICE_SELLER_{suffix}"

        profile[suffix.lower()] = _setting(
            settings,
            key,
        )

    return profile


__all__ = ("get_seller_profile",)
