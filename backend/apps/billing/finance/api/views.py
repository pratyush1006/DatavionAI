from django.apps import apps
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.finance.models import (
    BankAccount,
    Budget,
    CashTransaction,
    FinanceOutboxEvent,
    FinancialReport,
    FiscalPeriod,
    JournalEntry,
    LedgerAccount,
    TaxFiling,
    TaxRate,
    Vendor,
    VendorInvoice,
)
from apps.billing.finance.workflows.base import FinanceWorkflowRequest
from apps.billing.finance.workflows.registry import get_workflow

RESOURCE_MODELS = {
    "vendors": Vendor,
    "vendor-invoices": VendorInvoice,
    "bank-accounts": BankAccount,
    "cash-transactions": CashTransaction,
    "budgets": Budget,
    "reports": FinancialReport,
    "periods": FiscalPeriod,
    "ledger-accounts": LedgerAccount,
    "journal-entries": JournalEntry,
    "tax-rates": TaxRate,
    "tax-filings": TaxFiling,
}
RESOURCE_CREATE = {
    "vendors": "finance.accounts_payable.create_vendor",
    "vendor-invoices": "finance.accounts_payable.create_vendor_invoice",
    "bank-accounts": "finance.cash_management.create_bank_account",
    "cash-transactions": "finance.cash_management.create_cash_transaction",
    "budgets": "finance.financial_management.create_budget",
    "reports": "finance.financial_management.create_financial_report",
    "periods": "finance.general_ledger.open_period",
    "ledger-accounts": "finance.general_ledger.create_account",
    "journal-entries": "finance.general_ledger.create_journal_entry",
    "tax-rates": "finance.tax_gst.create_tax_rate",
    "tax-filings": "finance.tax_gst.create_tax_filing",
}
RESOURCE_UPDATE = {
    "vendors": "finance.accounts_payable.update_vendor",
    "vendor-invoices": "finance.accounts_payable.update_vendor_invoice",
    "bank-accounts": "finance.cash_management.update_bank_account",
    "cash-transactions": "finance.cash_management.update_cash_transaction",
    "budgets": "finance.financial_management.update_budget",
    "reports": "finance.financial_management.update_financial_report",
    "ledger-accounts": "finance.general_ledger.update_account",
    "tax-rates": "finance.tax_gst.update_tax_rate",
}


def organization_from(request):
    raw = (
        request.headers.get("X-Organization-ID")
        or request.data.get("organization_id")
        or request.query_params.get("organization_id")
    )
    if not raw:
        raise ValueError("organization_id is required")
    Organization = apps.get_model("organizations", "Organization")
    return Organization.objects.get(id=raw)


def serialize(obj):
    if isinstance(obj, dict):
        return obj
    data = model_to_dict(obj)
    data["id"] = str(obj.pk)
    return data


class FinanceHealthAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        org = organization_from(request)
        qs = FinanceOutboxEvent.objects.filter(organization=org)
        return Response(
            {
                "status": "ok",
                "outbox": {
                    "pending": qs.filter(status="pending").count(),
                    "processing": qs.filter(status="processing").count(),
                    "published": qs.filter(status="published").count(),
                },
            }
        )


class FinanceCollectionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, resource):
        model = RESOURCE_MODELS.get(resource)
        if not model:
            return Response({"detail": "Unknown resource"}, status=404)
        org = organization_from(request)
        qs = model.objects.filter(organization=org)
        return Response([serialize(x) for x in qs[:200]])

    def post(self, request, resource):
        workflow_name = RESOURCE_CREATE.get(resource)
        if not workflow_name:
            return Response({"detail": "Unknown create workflow"}, status=404)
        org = organization_from(request)
        result = get_workflow(workflow_name)().execute(
            None,
            FinanceWorkflowRequest(
                organization=org,
                payload=dict(request.data),
                actor_id=getattr(request.user, "id", None),
                idempotency_key=request.headers.get("Idempotency-Key"),
            ),
        )
        return Response(serialize(result.data), status=status.HTTP_201_CREATED)


class FinanceWorkflowAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, resource, object_id):
        model = RESOURCE_MODELS.get(resource)
        if not model:
            return Response({"detail": "Unknown resource"}, status=404)
        obj = model.objects.filter(
            id=object_id, organization=organization_from(request)
        ).first()
        if not obj:
            return Response({"detail": "Not found"}, status=404)
        return Response(serialize(obj))

    def patch(self, request, resource, object_id):
        workflow_name = RESOURCE_UPDATE.get(resource)
        if not workflow_name:
            return Response({"detail": "Unsupported update"}, status=400)
        org = organization_from(request)
        result = get_workflow(workflow_name)().execute(
            None,
            FinanceWorkflowRequest(
                organization=org,
                payload=dict(request.data),
                actor_id=getattr(request.user, "id", None),
                instance_id=object_id,
                idempotency_key=request.headers.get("Idempotency-Key"),
            ),
        )
        return Response(serialize(result.data))

    def post(self, request, resource, object_id):
        actions = {
            ("journal-entries", "post"): "finance.general_ledger.post_journal_entry",
            (
                "journal-entries",
                "reverse",
            ): "finance.general_ledger.reverse_journal_entry",
            ("periods", "lock"): "finance.general_ledger.lock_period",
            ("tax-filings", "submit"): "finance.tax_gst.submit_tax_filing",
        }
        action = request.query_params.get("action")
        workflow_name = actions.get((resource, action))
        if not workflow_name:
            return Response({"detail": "Unsupported action"}, status=400)
        org = organization_from(request)
        result = get_workflow(workflow_name)().execute(
            None,
            FinanceWorkflowRequest(
                organization=org,
                payload=dict(request.data),
                actor_id=getattr(request.user, "id", None),
                instance_id=object_id,
                idempotency_key=request.headers.get("Idempotency-Key"),
            ),
        )
        return Response(serialize(result.data))
