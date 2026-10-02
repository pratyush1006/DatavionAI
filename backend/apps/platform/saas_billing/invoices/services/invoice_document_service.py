"""
Canonical SaaS invoice document service.

This service bridges canonical billing data and the invoice
presentation layer.

It does not create invoices and does not calculate billing.
Those responsibilities remain with the existing SaaS billing
domain.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.platform.saas_billing.invoices.rendering.context import (
    build_invoice_context,
)
from apps.platform.saas_billing.invoices.rendering.invoice_renderer import (
    render_invoice_html,
    render_invoice_pdf,
)
from apps.platform.saas_billing.invoices.rendering.seller_profile import (
    get_seller_profile,
)


class InvoiceDocumentService:
    """
    Generate invoice documents from canonical invoice data.
    """

    @staticmethod
    def build_context(
        invoice: Any,
        *,
        customer: Mapping[str, Any] | None = None,
        branding: Mapping[str, Any] | None = None,
        seller: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        seller_profile = dict(seller or get_seller_profile())

        return build_invoice_context(
            invoice,
            seller=seller_profile,
            customer=customer,
            branding=branding,
        )

    @classmethod
    def render_html(
        cls,
        invoice: Any,
        *,
        customer: Mapping[str, Any] | None = None,
        branding: Mapping[str, Any] | None = None,
        seller: Mapping[str, Any] | None = None,
    ) -> str:
        context = cls.build_context(
            invoice,
            customer=customer,
            branding=branding,
            seller=seller,
        )

        return render_invoice_html(
            context,
        )

    @classmethod
    def render_pdf(
        cls,
        invoice: Any,
        *,
        customer: Mapping[str, Any] | None = None,
        branding: Mapping[str, Any] | None = None,
        seller: Mapping[str, Any] | None = None,
    ) -> bytes:
        context = cls.build_context(
            invoice,
            customer=customer,
            branding=branding,
            seller=seller,
        )

        return render_invoice_pdf(
            context,
        )


__all__ = ("InvoiceDocumentService",)
