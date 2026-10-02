"""
Dynamic SaaS invoice renderer.

The renderer is presentation-only.

Business calculations must be performed by the canonical
SaaS billing domain before rendering.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from django.template import Context, Engine

TEMPLATE_PATH = (
    Path(__file__).resolve().parent.parent / "templates" / "default_invoice.html"
)


class InvoiceRenderError(RuntimeError):
    """Invoice rendering failure."""


def render_invoice_html(
    context: Mapping[str, Any],
) -> str:
    """
    Render the canonical invoice HTML template.
    """

    if not TEMPLATE_PATH.exists():
        raise InvoiceRenderError(f"Invoice template not found: {TEMPLATE_PATH}")

    template_source = TEMPLATE_PATH.read_text(
        encoding="utf-8",
    )

    engine = Engine(
        autoescape=True,
    )

    template = engine.from_string(
        template_source,
    )

    return template.render(
        Context(
            dict(context),
        )
    )


def render_invoice_pdf(
    context: Mapping[str, Any],
) -> bytes:
    """
    Render PDF when an already-installed PDF engine exists.

    No dependency is installed by this module.

    Supported existing renderer:
      WeasyPrint
    """

    html = render_invoice_html(
        context,
    )

    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise InvoiceRenderError(
            "PDF rendering requires an already-installed "
            "WeasyPrint package. HTML rendering remains "
            "available without it."
        ) from exc

    return HTML(
        string=html,
    ).write_pdf()


__all__ = (
    "InvoiceRenderError",
    "render_invoice_html",
    "render_invoice_pdf",
)
