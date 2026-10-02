from django.contrib import admin

from apps.pharmacy.models import (
    ControlledSubstanceControl,
    DispensingLine,
    DispensingOrder,
    InventoryQuarantine,
    MedicationBatch,
    Pharmacy,
    PharmacyBillingRecord,
    PharmacyIdempotencyKey,
    PharmacyProduct,
    PharmacyReturn,
    PharmacyReturnLine,
    ProcurementApproval,
    ProductRecall,
    PurchaseOrder,
    PurchaseOrderLine,
    RecallBatch,
    StockMovement,
    Supplier,
)

for model in (
    Pharmacy,
    Supplier,
    PharmacyProduct,
    MedicationBatch,
    StockMovement,
    PurchaseOrder,
    PurchaseOrderLine,
    DispensingOrder,
    DispensingLine,
    PharmacyReturn,
    PharmacyReturnLine,
    ControlledSubstanceControl,
    InventoryQuarantine,
    ProductRecall,
    RecallBatch,
    ProcurementApproval,
    PharmacyIdempotencyKey,
    PharmacyBillingRecord,
):
    admin.site.register(model)
