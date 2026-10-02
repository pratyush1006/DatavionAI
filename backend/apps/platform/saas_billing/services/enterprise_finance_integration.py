"""
Canonical SaaS Invoice -> Enterprise Finance integration.

This module is owned by SaaS billing because SaaS billing owns the
source invoice lifecycle.

Enterprise Finance is the accounting destination.

Healthcare billing is intentionally isolated and is never imported
or modified by this integration.

Canonical ownership:

    SaaS Billing
        apps/platform/saas_billing

    Enterprise Finance
        apps/billing/finance

    Healthcare Billing
        apps/revenue_cycle/billing
"""

from __future__ import annotations

import os
from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.billing.finance.models import (
    FiscalPeriod,
    LedgerAccount,
)
from apps.billing.finance.services import (
    create_journal_entry,
    post_journal_entry,
    record_audit,
)
from apps.billing.finance.services.idempotency import (
    execute_idempotent,
)

WORKFLOW = "saas_invoice.enterprise_finance_settlement"

SOURCE_DOMAIN = "apps.platform.saas_billing"
SOURCE_DOCUMENT_TYPE = "saas_invoice"


def _configured_account_code(
    name: str,
) -> str:
    """
    Read a configurable Enterprise Finance ledger account code.

    Secrets and accounting configuration are never hard-coded into
    source code.
    """

    value = os.environ.get(
        name,
        "",
    ).strip()

    if not value:
        raise ValidationError(f"Missing enterprise finance configuration: {name}")

    return value


def _account(
    *,
    organization: Any,
    code: str,
) -> LedgerAccount:
    """
    Resolve an active organization-specific ledger account.
    """

    return LedgerAccount.objects.get(
        organization=organization,
        code=code,
        status="active",
    )


def _invoice_date(
    invoice: Any,
):
    """
    Resolve accounting date for the SaaS invoice.
    """

    issued_at = getattr(
        invoice,
        "issued_at",
        None,
    )

    if issued_at:
        return issued_at.date()

    return timezone.localdate()


def _period(
    *,
    organization: Any,
    entry_date,
) -> FiscalPeriod:
    """
    Resolve the open fiscal period covering the invoice date.
    """

    period = (
        FiscalPeriod.objects.filter(
            organization=organization,
            period_start__lte=entry_date,
            period_end__gte=entry_date,
            status="open",
        )
        .order_by("period_start")
        .first()
    )

    if period is None:
        raise ValidationError(
            f"No open enterprise finance fiscal period covers {entry_date}."
        )

    return period


def _invoice_metadata(
    invoice: Any,
) -> dict[str, Any]:
    """
    Resolve invoice metadata without assuming one specific Invoice
    implementation.
    """

    metadata = getattr(
        invoice,
        "metadata",
        None,
    )

    if isinstance(
        metadata,
        dict,
    ):
        return metadata

    invoice_data = getattr(
        invoice,
        "invoice_data",
        None,
    )

    if isinstance(
        invoice_data,
        dict,
    ):
        return invoice_data

    return {}


def build_finance_payload(
    *,
    invoice: Any,
) -> dict[str, Any]:
    """
    Build the canonical finance payload from the SaaS invoice.

    This is a projection only. SaaS billing remains the source of truth.
    """

    organization = invoice.organization

    subtotal = Decimal(
        str(
            getattr(
                invoice,
                "subtotal",
                "0",
            )
            or "0"
        )
    )

    tax_amount = Decimal(
        str(
            getattr(
                invoice,
                "tax_amount",
                "0",
            )
            or "0"
        )
    )

    total_amount = Decimal(
        str(
            getattr(
                invoice,
                "total_amount",
                "0",
            )
            or "0"
        )
    )

    payment_reference = (
        getattr(
            invoice,
            "payment_reference",
            "",
        )
        or ""
    )

    metadata = _invoice_metadata(
        invoice,
    )

    subscription = getattr(
        invoice,
        "subscription",
        None,
    )

    return {
        "invoice_id": str(
            invoice.pk,
        ),
        "organization_id": str(
            organization.pk,
        ),
        "subscription_id": (str(subscription.pk) if subscription is not None else ""),
        "invoice_number": invoice.invoice_number,
        "invoice_date": _invoice_date(
            invoice,
        ).isoformat(),
        "due_date": (
            invoice.due_at.date().isoformat()
            if getattr(
                invoice,
                "due_at",
                None,
            )
            else None
        ),
        "currency": invoice.currency,
        "subtotal": str(
            subtotal,
        ),
        "tax_amount": str(
            tax_amount,
        ),
        "total_amount": str(
            total_amount,
        ),
        "paid_amount": str(
            getattr(
                invoice,
                "paid_amount",
                "0",
            )
            or "0"
        ),
        "payment_status": invoice.status,
        "payment_method": getattr(
            invoice,
            "payment_provider",
            "",
        ),
        "payment_reference": payment_reference,
        "razorpay_order_id": metadata.get(
            "razorpay_order_id",
        ),
        "razorpay_payment_id": metadata.get(
            "razorpay_payment_id",
        ),
        "razorpay_signature_verified": metadata.get(
            "razorpay_signature_verified",
        ),
        "source_domain": SOURCE_DOMAIN,
        "source_document_type": SOURCE_DOCUMENT_TYPE,
    }


def _settle_invoice(
    *,
    invoice: Any,
):
    """
    Create and post the Enterprise Finance journal entry.

    Accounting:

        Debit  -> Payment / Razorpay account
        Credit -> SaaS Revenue account
    """

    organization = invoice.organization

    entry_date = _invoice_date(
        invoice,
    )

    period = _period(
        organization=organization,
        entry_date=entry_date,
    )

    revenue_code = _configured_account_code(
        "DATAVIONOS_FINANCE_SAAS_REVENUE_ACCOUNT_CODE",
    )

    payment_code = _configured_account_code(
        "DATAVIONOS_FINANCE_RAZORPAY_ACCOUNT_CODE",
    )

    revenue_account = _account(
        organization=organization,
        code=revenue_code,
    )

    payment_account = _account(
        organization=organization,
        code=payment_code,
    )

    total_amount = Decimal(
        str(
            getattr(
                invoice,
                "total_amount",
                "0",
            )
            or "0"
        )
    )

    if total_amount <= Decimal("0"):
        raise ValidationError(
            "Enterprise Finance settlement requires a positive SaaS invoice total."
        )

    reference = (f"SAAS-INV-{invoice.invoice_number}")[:160]

    entry = create_journal_entry(
        organization=organization,
        data={
            "fiscal_period_id": period.pk,
            "reference": reference,
            "description": (
                f"SaaS subscription invoice settlement {invoice.invoice_number}"
            ),
            "entry_date": entry_date,
            "lines": [
                {
                    "account_id": payment_account.pk,
                    "description": ("SaaS subscription payment"),
                    "debit": str(
                        total_amount,
                    ),
                    "credit": "0",
                },
                {
                    "account_id": revenue_account.pk,
                    "description": ("SaaS subscription revenue"),
                    "debit": "0",
                    "credit": str(
                        total_amount,
                    ),
                },
            ],
        },
    )

    posted = post_journal_entry(
        organization=organization,
        instance_id=entry.pk,
    )

    payload = build_finance_payload(
        invoice=invoice,
    )

    record_audit(
        organization=organization,
        workflow=WORKFLOW,
        entity_type="SaaSInvoice",
        entity_id=invoice.pk,
        payload={
            "finance_journal_entry_id": str(
                posted.pk,
            ),
            "invoice": payload,
        },
    )

    return posted


@transaction.atomic
def settle_saas_invoice_in_finance(
    *,
    invoice: Any,
):
    """
    Idempotently settle a paid SaaS invoice in Enterprise Finance.

    SaaS billing remains the source of truth.

    Finance receives a journal representation only after the SaaS
    invoice has reached the PAID or SETTLED state.

    Repeated calls for the same invoice are protected by the canonical
    Enterprise Finance idempotency mechanism.
    """

    status = str(
        getattr(
            invoice,
            "status",
            "",
        )
        or "",
    ).lower()

    if status not in {
        "paid",
        "settled",
    }:
        raise ValidationError(
            "Only paid or settled SaaS invoices can be posted to enterprise finance."
        )

    total_amount = Decimal(
        str(
            getattr(
                invoice,
                "total_amount",
                "0",
            )
            or "0"
        )
    )

    if total_amount <= Decimal("0"):
        return {
            "journal_entry": None,
            "already_settled": False,
            "skipped": True,
            "reason": "zero_value_invoice",
            "invoice_id": str(
                invoice.pk,
            ),
            "workflow": WORKFLOW,
        }

    key = f"saas-invoice:{invoice.pk}"

    result, existed = execute_idempotent(
        organization=invoice.organization,
        workflow=WORKFLOW,
        key=key,
        execute=lambda: _settle_invoice(
            invoice=invoice,
        ),
    )

    return {
        "journal_entry": result,
        "already_settled": existed,
        "skipped": False,
        "invoice_id": str(
            invoice.pk,
        ),
        "workflow": WORKFLOW,
    }


__all__ = (
    "build_finance_payload",
    "settle_saas_invoice_in_finance",
)
