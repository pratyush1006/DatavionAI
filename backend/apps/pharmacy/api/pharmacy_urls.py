from django.urls import path

from apps.pharmacy.api.health import PharmacyHealthAPIView
from apps.pharmacy.api.views import (
    BatchListAPIView,
    CompleteStockTransferAPIView,
    DispenseOrderAPIView,
    DispensingBillAPIView,
    DispensingOrderListCreateAPIView,
    PharmacyInventoryAPIView,
    PharmacyListCreateAPIView,
    PharmacyOperationalSummaryAPIView,
    PharmacyReturnListCreateAPIView,
    ProductListCreateAPIView,
    PurchaseApprovalDecisionAPIView,
    PurchaseApprovalRequestAPIView,
    PurchaseOrderListCreateAPIView,
    ReceiveStockAPIView,
    StockMovementListAPIView,
    StockTransferListCreateAPIView,
    SupplierListCreateAPIView,
)

urlpatterns = [
    path("health/", PharmacyHealthAPIView.as_view(), name="pharmacy-health"),
    path(
        "pharmacies/", PharmacyListCreateAPIView.as_view(), name="pharmacy-list-create"
    ),
    path(
        "suppliers/", SupplierListCreateAPIView.as_view(), name="supplier-list-create"
    ),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("batches/", BatchListAPIView.as_view(), name="batch-list"),
    path(
        "purchase-orders/",
        PurchaseOrderListCreateAPIView.as_view(),
        name="purchase-order-list-create",
    ),
    path(
        "purchase-orders/<uuid:order_id>/request-approval/",
        PurchaseApprovalRequestAPIView.as_view(),
        name="purchase-order-request-approval",
    ),
    path(
        "purchase-approvals/<uuid:approval_id>/decide/",
        PurchaseApprovalDecisionAPIView.as_view(),
        name="purchase-approval-decide",
    ),
    path(
        "dispensing-orders/",
        DispensingOrderListCreateAPIView.as_view(),
        name="dispensing-order-list-create",
    ),
    path(
        "dispensing-orders/<uuid:order_id>/dispense/",
        DispenseOrderAPIView.as_view(),
        name="dispensing-order-dispense",
    ),
    path(
        "dispensing-orders/<uuid:order_id>/bill/",
        DispensingBillAPIView.as_view(),
        name="dispensing-order-bill",
    ),
    path(
        "returns/", PharmacyReturnListCreateAPIView.as_view(), name="return-list-create"
    ),
    path("inventory/", PharmacyInventoryAPIView.as_view(), name="pharmacy-inventory"),
    path(
        "inventory/receive/",
        ReceiveStockAPIView.as_view(),
        name="pharmacy-inventory-receive",
    ),
    path(
        "summary/",
        PharmacyOperationalSummaryAPIView.as_view(),
        name="pharmacy-operational-summary",
    ),
    path(
        "stock-movements/",
        StockMovementListAPIView.as_view(),
        name="stock-movement-list",
    ),
    path(
        "stock-transfers/",
        StockTransferListCreateAPIView.as_view(),
        name="stock-transfer-list-create",
    ),
    path(
        "stock-transfers/<uuid:transfer_id>/complete/",
        CompleteStockTransferAPIView.as_view(),
        name="stock-transfer-complete",
    ),
]
