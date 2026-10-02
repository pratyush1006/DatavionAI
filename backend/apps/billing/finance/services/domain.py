from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.billing.finance.models import (
    BankAccount,
    Budget,
    CashTransaction,
    FinancialReport,
    FiscalPeriod,
    JournalEntry,
    JournalLine,
    LedgerAccount,
    TaxFiling,
    TaxRate,
    Vendor,
    VendorInvoice,
)


def _payload(data, excluded=()):
    return {k: v for k, v in data.items() if k not in set(excluded)}


def _get(model, organization, instance_id):
    return model.objects.select_for_update().get(
        id=instance_id, organization=organization
    )


@transaction.atomic
def create_vendor(*, organization, data):
    return Vendor.objects.create(
        organization=organization, **_payload(data, ("organization",))
    )


@transaction.atomic
def update_vendor(*, organization, instance_id, data):
    obj = _get(Vendor, organization, instance_id)
    for k, v in _payload(data, ("organization", "id")).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def create_vendor_invoice(*, organization, data):
    vendor = Vendor.objects.get(id=data["vendor_id"], organization=organization)
    return VendorInvoice.objects.create(
        organization=organization,
        vendor=vendor,
        **_payload(data, ("organization", "vendor_id")),
    )


@transaction.atomic
def update_vendor_invoice(*, organization, instance_id, data):
    obj = _get(VendorInvoice, organization, instance_id)
    if "vendor_id" in data:
        obj.vendor = Vendor.objects.get(id=data["vendor_id"], organization=organization)
    for k, v in _payload(data, ("organization", "vendor_id", "id")).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def create_bank_account(*, organization, data):
    opening = Decimal(str(data.get("opening_balance", "0")))
    payload = _payload(data, ("organization", "current_balance"))
    payload["current_balance"] = opening
    return BankAccount.objects.create(organization=organization, **payload)


@transaction.atomic
def update_bank_account(*, organization, instance_id, data):
    obj = _get(BankAccount, organization, instance_id)
    for k, v in _payload(
        data, ("organization", "current_balance", "opening_balance", "id")
    ).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def create_cash_transaction(*, organization, data):
    bank = BankAccount.objects.select_for_update().get(
        id=data["bank_account_id"], organization=organization
    )
    if bank.status != "active":
        raise ValidationError("Bank account is not active.")
    amount = Decimal(str(data["amount"]))
    if amount <= 0:
        raise ValidationError("Amount must be positive.")
    if data["transaction_type"] not in {"credit", "debit"}:
        raise ValidationError("Invalid transaction type.")
    bank.current_balance = F("current_balance") + (
        amount if data["transaction_type"] == "credit" else -amount
    )
    bank.save(update_fields=("current_balance", "updated_at"))
    return CashTransaction.objects.create(
        organization=organization,
        bank_account=bank,
        **_payload(data, ("organization", "bank_account_id")),
    )


@transaction.atomic
def update_cash_transaction(*, organization, instance_id, data):
    raise ValidationError(
        "Cash transactions are immutable; create a compensating transaction."
    )


@transaction.atomic
def create_budget(*, organization, data):
    return Budget.objects.create(
        organization=organization, **_payload(data, ("organization",))
    )


@transaction.atomic
def update_budget(*, organization, instance_id, data):
    obj = _get(Budget, organization, instance_id)
    if obj.status == "closed":
        raise ValidationError("Closed budgets cannot be modified.")
    for k, v in _payload(data, ("organization", "id")).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def create_financial_report(*, organization, data):
    return FinancialReport.objects.create(
        organization=organization, **_payload(data, ("organization",))
    )


@transaction.atomic
def update_financial_report(*, organization, instance_id, data):
    obj = _get(FinancialReport, organization, instance_id)
    if obj.status == "generated":
        raise ValidationError("Generated reports are immutable.")
    for k, v in _payload(data, ("organization", "id")).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def create_ledger_account(*, organization, data):
    parent = None
    if data.get("parent_id"):
        parent = LedgerAccount.objects.get(
            id=data["parent_id"], organization=organization
        )
    return LedgerAccount.objects.create(
        organization=organization,
        parent=parent,
        **_payload(data, ("organization", "parent_id")),
    )


@transaction.atomic
def update_ledger_account(*, organization, instance_id, data):
    obj = _get(LedgerAccount, organization, instance_id)
    if "parent_id" in data:
        obj.parent = (
            None
            if data["parent_id"] is None
            else LedgerAccount.objects.get(
                id=data["parent_id"], organization=organization
            )
        )
    for k, v in _payload(data, ("organization", "parent_id", "id")).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def open_fiscal_period(*, organization, data):
    return FiscalPeriod.objects.create(
        organization=organization, **_payload(data, ("organization",))
    )


@transaction.atomic
def lock_fiscal_period(*, organization, instance_id, data=None):
    obj = _get(FiscalPeriod, organization, instance_id)
    obj.status = "locked"
    obj.save(update_fields=("status", "updated_at"))
    return obj


@transaction.atomic
def create_journal_entry(*, organization, data):
    period = FiscalPeriod.objects.get(
        id=data["fiscal_period_id"], organization=organization
    )
    if period.status != "open":
        raise ValidationError("Fiscal period is locked.")
    lines = data.get("lines") or []
    if len(lines) < 2:
        raise ValidationError("Journal entry requires at least two lines.")
    entry = JournalEntry.objects.create(
        organization=organization,
        fiscal_period=period,
        reference=data["reference"],
        description=data.get("description", ""),
        entry_date=data["entry_date"],
    )
    debit = Decimal("0")
    credit = Decimal("0")
    for raw in lines:
        account = LedgerAccount.objects.get(
            id=raw["account_id"], organization=organization, status="active"
        )
        line = JournalLine(
            entry=entry,
            account=account,
            description=raw.get("description", ""),
            debit=Decimal(str(raw.get("debit", "0"))),
            credit=Decimal(str(raw.get("credit", "0"))),
        )
        line.full_clean()
        line.save()
        debit += line.debit
        credit += line.credit
    if debit <= 0 or debit != credit:
        raise ValidationError("Journal entry is not balanced.")
    entry.total_debit = debit
    entry.total_credit = credit
    entry.full_clean()
    entry.save(update_fields=("total_debit", "total_credit", "updated_at"))
    return entry


@transaction.atomic
def post_journal_entry(*, organization, instance_id, data=None):
    entry = (
        JournalEntry.objects.select_for_update()
        .prefetch_related("lines")
        .get(id=instance_id, organization=organization)
    )
    if entry.status != "draft":
        raise ValidationError("Only draft journal entries can be posted.")
    if entry.total_debit <= 0 or entry.total_debit != entry.total_credit:
        raise ValidationError("Journal entry must be balanced.")
    if entry.fiscal_period.status != "open":
        raise ValidationError("Fiscal period is locked.")
    entry.status = "posted"
    entry.posted_at = timezone.now()
    entry.save(update_fields=("status", "posted_at", "updated_at"))
    return entry


@transaction.atomic
def reverse_journal_entry(*, organization, instance_id, data=None):
    original = (
        JournalEntry.objects.select_for_update()
        .prefetch_related("lines")
        .get(id=instance_id, organization=organization)
    )
    if original.status != "posted":
        raise ValidationError("Only posted journal entries can be reversed.")
    if JournalEntry.objects.filter(reversal_of=original).exists():
        raise ValidationError("Journal entry is already reversed.")
    if original.fiscal_period.status != "open":
        raise ValidationError("Fiscal period is locked.")
    reversal = JournalEntry.objects.create(
        organization=organization,
        fiscal_period=original.fiscal_period,
        reference=f"REV-{original.reference}",
        description=f"Reversal of {original.reference}",
        entry_date=timezone.localdate(),
        status="posted",
        total_debit=original.total_credit,
        total_credit=original.total_debit,
        posted_at=timezone.now(),
        reversal_of=original,
    )
    for line in original.lines.all():
        JournalLine.objects.create(
            entry=reversal,
            account=line.account,
            description=f"Reversal of {line.description}",
            debit=line.credit,
            credit=line.debit,
        )
    original.status = "reversed"
    original.save(update_fields=("status", "updated_at"))
    return reversal


@transaction.atomic
def create_tax_rate(*, organization, data):
    return TaxRate.objects.create(
        organization=organization, **_payload(data, ("organization",))
    )


@transaction.atomic
def update_tax_rate(*, organization, instance_id, data):
    obj = _get(TaxRate, organization, instance_id)
    for k, v in _payload(data, ("organization", "id")).items():
        setattr(obj, k, v)
    obj.full_clean()
    obj.save()
    return obj


@transaction.atomic
def create_tax_filing(*, organization, data):
    rate = TaxRate.objects.get(id=data["tax_rate_id"], organization=organization)
    return TaxFiling.objects.create(
        organization=organization,
        tax_rate=rate,
        **_payload(data, ("organization", "tax_rate_id")),
    )


@transaction.atomic
def submit_tax_filing(*, organization, instance_id, data=None):
    obj = _get(TaxFiling, organization, instance_id)
    if obj.status not in {"draft", "ready"}:
        raise ValidationError("Tax filing is not submittable.")
    obj.status = "submitted"
    obj.save(update_fields=("status", "updated_at"))
    return obj
