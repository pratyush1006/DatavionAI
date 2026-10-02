from apps.billing.finance import services

from .base import FinanceWorkflow

WORKFLOW_SPECS = {
    "finance.accounts_payable.create_vendor": (
        "create_vendor",
        "finance.vendor.created",
        False,
    ),
    "finance.accounts_payable.update_vendor": (
        "update_vendor",
        "finance.vendor.updated",
        True,
    ),
    "finance.accounts_payable.create_vendor_invoice": (
        "create_vendor_invoice",
        "finance.vendor_invoice.created",
        False,
    ),
    "finance.accounts_payable.update_vendor_invoice": (
        "update_vendor_invoice",
        "finance.vendor_invoice.updated",
        True,
    ),
    "finance.cash_management.create_bank_account": (
        "create_bank_account",
        "finance.bank_account.created",
        False,
    ),
    "finance.cash_management.update_bank_account": (
        "update_bank_account",
        "finance.bank_account.updated",
        True,
    ),
    "finance.cash_management.create_cash_transaction": (
        "create_cash_transaction",
        "finance.cash_transaction.created",
        False,
    ),
    "finance.cash_management.update_cash_transaction": (
        "update_cash_transaction",
        "finance.cash_transaction.rejected",
        True,
    ),
    "finance.financial_management.create_budget": (
        "create_budget",
        "finance.budget.created",
        False,
    ),
    "finance.financial_management.update_budget": (
        "update_budget",
        "finance.budget.updated",
        True,
    ),
    "finance.financial_management.create_financial_report": (
        "create_financial_report",
        "finance.financial_report.created",
        False,
    ),
    "finance.financial_management.update_financial_report": (
        "update_financial_report",
        "finance.financial_report.updated",
        True,
    ),
    "finance.general_ledger.create_account": (
        "create_ledger_account",
        "finance.ledger_account.created",
        False,
    ),
    "finance.general_ledger.update_account": (
        "update_ledger_account",
        "finance.ledger_account.updated",
        True,
    ),
    "finance.general_ledger.open_period": (
        "open_fiscal_period",
        "finance.fiscal_period.opened",
        False,
    ),
    "finance.general_ledger.lock_period": (
        "lock_fiscal_period",
        "finance.fiscal_period.locked",
        True,
    ),
    "finance.general_ledger.create_journal_entry": (
        "create_journal_entry",
        "finance.journal_entry.created",
        False,
    ),
    "finance.general_ledger.post_journal_entry": (
        "post_journal_entry",
        "finance.journal_entry.posted",
        True,
    ),
    "finance.general_ledger.reverse_journal_entry": (
        "reverse_journal_entry",
        "finance.journal_entry.reversed",
        True,
    ),
    "finance.tax_gst.create_tax_rate": (
        "create_tax_rate",
        "finance.tax_rate.created",
        False,
    ),
    "finance.tax_gst.update_tax_rate": (
        "update_tax_rate",
        "finance.tax_rate.updated",
        True,
    ),
    "finance.tax_gst.create_tax_filing": (
        "create_tax_filing",
        "finance.tax_filing.created",
        False,
    ),
    "finance.tax_gst.submit_tax_filing": (
        "submit_tax_filing",
        "finance.tax_filing.submitted",
        True,
    ),
}


def get_workflow(name):
    fn_name, event_type, instance_required = WORKFLOW_SPECS[name]
    fn = getattr(services, fn_name)

    def handler(*, organization, data, instance_id):
        if instance_required:
            return fn(organization=organization, instance_id=instance_id, data=data)
        return fn(organization=organization, data=data)

    return type(
        name.split(".")[-1].title() + "Workflow",
        (FinanceWorkflow,),
        {"name": name, "handler": staticmethod(handler), "event_type": event_type},
    )


def validate_workflows():
    errors = []
    for name in WORKFLOW_SPECS:
        try:
            get_workflow(name)
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    return errors
