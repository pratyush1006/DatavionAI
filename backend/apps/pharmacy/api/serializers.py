from rest_framework import serializers

from apps.pharmacy.models import (
    DispensingLine,
    DispensingOrder,
    MedicationBatch,
    Pharmacy,
    PharmacyProduct,
    PharmacyReturn,
    PurchaseOrder,
    StockMovement,
    StockTransferLine,
    StockTransferOrder,
    Supplier,
)


class DispensingLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispensingLine
        fields = ("id", "product", "batch", "quantity_prescribed", "quantity_dispensed")
        read_only_fields = fields


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = (
            "id",
            "organization",
            "code",
            "name",
            "address",
            "phone",
            "email",
            "status",
        )
        read_only_fields = ("id", "status")


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            "id",
            "organization",
            "code",
            "name",
            "contact_name",
            "phone",
            "email",
            "tax_id",
            "address",
        )
        read_only_fields = ("id",)


class PharmacyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyProduct
        fields = (
            "id",
            "organization",
            "pharmacy",
            "medication",
            "sku",
            "barcode",
            "reorder_level",
            "reorder_quantity",
            "unit_cost",
            "selling_price",
            "tax_rate",
        )
        read_only_fields = ("id",)


class MedicationBatchSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    medication_name = serializers.CharField(
        source="product.medication.display_name", read_only=True
    )

    class Meta:
        model = MedicationBatch
        fields = (
            "id",
            "product",
            "product_sku",
            "medication_name",
            "batch_number",
            "manufacture_date",
            "expiry_date",
            "quantity_received",
            "quantity_available",
            "quantity_reserved",
            "purchase_price",
            "selling_price",
        )
        read_only_fields = (
            "id",
            "quantity_received",
            "quantity_available",
            "quantity_reserved",
        )


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    pharmacy_name = serializers.CharField(source="pharmacy.name", read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            "id",
            "organization",
            "pharmacy",
            "supplier",
            "supplier_name",
            "pharmacy_name",
            "order_number",
            "status",
            "ordered_at",
            "received_at",
            "notes",
        )
        read_only_fields = ("id", "status", "ordered_at", "received_at")


class DispensingOrderSerializer(serializers.ModelSerializer):
    prescription_number = serializers.CharField(
        source="prescription.prescription_number", read_only=True
    )
    patient_name = serializers.CharField(
        source="prescription.patient.display_name", read_only=True
    )
    pharmacy_name = serializers.CharField(source="pharmacy.name", read_only=True)
    lines = DispensingLineSerializer(
        source="dispensing_lines", many=True, read_only=True
    )

    class Meta:
        model = DispensingOrder
        fields = (
            "id",
            "organization",
            "pharmacy",
            "prescription",
            "prescription_number",
            "patient_name",
            "pharmacy_name",
            "lines",
            "dispense_number",
            "status",
            "pharmacist_id",
            "dispensed_at",
        )
        read_only_fields = ("id", "status", "dispensed_at")


class PharmacyReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyReturn
        fields = (
            "id",
            "return_type",
            "dispensing_order",
            "purchase_order",
            "return_number",
            "reason",
            "processed_by_id",
        )
        read_only_fields = ("id", "processed_by_id")


class StockMovementSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source="batch.product.sku", read_only=True)
    medication_name = serializers.CharField(
        source="batch.product.medication.display_name", read_only=True
    )
    batch_number = serializers.CharField(source="batch.batch_number", read_only=True)

    class Meta:
        model = StockMovement
        fields = "__all__"
        read_only_fields = (
            "id",
            "organization",
            "actor_id",
            "created_at",
            "updated_at",
        )


class StockTransferLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransferLine
        fields = "__all__"
        read_only_fields = ("id", "transfer_order", "destination_batch")


class StockTransferOrderSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="source_pharmacy.name", read_only=True)
    destination_name = serializers.CharField(
        source="destination_pharmacy.name", read_only=True
    )
    lines = StockTransferLineSerializer(many=True, read_only=True)

    class Meta:
        model = StockTransferOrder
        fields = "__all__"
        read_only_fields = (
            "id",
            "organization",
            "status",
            "approved_by_id",
            "completed_at",
            "created_at",
            "updated_at",
        )
